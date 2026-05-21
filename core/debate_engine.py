"""
辩论引擎

核心模块，负责管理辩论流程、模式选择、结果汇总。
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from agents.base import AgentResponse, AgentMessage, DebateContext
from agents.teams import DebateTeam


class DebateRound(BaseModel):
    """辩论轮次"""
    
    round_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    round_number: int
    team_responses: Dict[str, List[AgentResponse]] = {}  # team_id -> responses
    messages: List[AgentMessage] = []
    timestamp: datetime = Field(default_factory=datetime.now)


class DebateResult(BaseModel):
    """辩论结果"""
    
    debate_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    mode: str
    teams: List[str]  # team_ids
    rounds: List[DebateRound] = []
    consensus: Optional[AgentResponse] = None
    votes: List[AgentMessage] = []
    confidence: float = 0.0
    summary: str = ""
    recommendations: List[str] = []
    risks: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DebateMode:
    """
    辩论模式基类
    
    定义不同的辩论机制，如对抗辩论、陪审团、风险矩阵等。
    """
    
    def __init__(self, mode_id: str, name: str, description: str = ""):
        self.mode_id = mode_id
        self.name = name
        self.description = description
    
    async def execute(
        self,
        context: DebateContext,
        teams: List[DebateTeam],
        max_rounds: int = 3
    ) -> DebateResult:
        """
        执行辩论
        
        Args:
            context: 辩论上下文
            teams: 参与辩论的团队
            max_rounds: 最大辩论轮数
            
        Returns:
            DebateResult: 辩论结果
        """
        raise NotImplementedError


class AdversarialDebate(DebateMode):
    """
    对抗辩论模式
    
    两个团队正反方辩论，通过多轮对抗达成共识。
    """
    
    def __init__(self):
        super().__init__(
            mode_id="adversarial_debate",
            name="对抗辩论",
            description="两个团队正反方辩论，通过多轮对抗达成共识"
        )
    
    async def execute(
        self,
        context: DebateContext,
        teams: List[DebateTeam],
        max_rounds: int = 3
    ) -> DebateResult:
        """执行对抗辩论"""
        if len(teams) < 2:
            raise ValueError("对抗辩论需要至少 2 个团队")
        
        rounds = []
        all_messages = []
        
        # 第一轮：各团队独立分析
        round1 = DebateRound(round_number=1)
        for team in teams:
            responses = await team.discuss(context)
            round1.team_responses[team.team_id] = responses
            
            # 转换为消息
            for response in responses:
                message = AgentMessage(
                    agent_id=response.agent_id,
                    role=team.name,
                    content=f"{response.decision}: {response.reasoning}",
                    confidence=response.confidence
                )
                round1.messages.append(message)
                all_messages.append(message)
        
        rounds.append(round1)
        
        # 后续轮次：辩论
        for round_num in range(2, max_rounds + 1):
            debate_round = DebateRound(round_number=round_num)
            
            for team in teams:
                responses = await team.debate(context, all_messages)
                debate_round.team_responses[team.team_id] = responses
                
                for response in responses:
                    message = AgentMessage(
                        agent_id=response.agent_id,
                        role=team.name,
                        content=f"{response.decision}: {response.reasoning}",
                        confidence=response.confidence
                    )
                    debate_round.messages.append(message)
                    all_messages.append(message)
            
            rounds.append(debate_round)
        
        # 投票
        all_proposals = []
        for round_data in rounds:
            for team_id, responses in round_data.team_responses.items():
                all_proposals.extend(responses)
        
        votes = []
        for team in teams:
            team_votes = await team.vote(context, all_proposals)
            votes.extend(team_votes)
        
        # 计算共识
        consensus = self._calculate_consensus(all_proposals, votes)
        
        return DebateResult(
            topic=context.topic,
            mode=self.mode_id,
            teams=[t.team_id for t in teams],
            rounds=rounds,
            consensus=consensus,
            votes=votes,
            confidence=consensus.confidence if consensus else 0.0,
            summary=self._generate_summary(rounds, consensus),
            recommendations=self._extract_recommendations(all_proposals),
            risks=self._extract_risks(all_proposals)
        )
    
    def _calculate_consensus(
        self,
        proposals: List[AgentResponse],
        votes: List[AgentMessage]
    ) -> Optional[AgentResponse]:
        """计算共识"""
        if not proposals:
            return None
        
        # 统计投票
        vote_counts: Dict[str, float] = {}
        for vote in votes:
            # 从投票内容中提取决策
            content = vote.content
            for proposal in proposals:
                if proposal.decision in content:
                    if proposal.decision not in vote_counts:
                        vote_counts[proposal.decision] = 0.0
                    vote_counts[proposal.decision] += vote.confidence
        
        # 找出票数最高的决策
        if not vote_counts:
            # 如果没有投票，选择置信度最高的提案
            return max(proposals, key=lambda p: p.confidence)
        
        best_decision = max(vote_counts, key=vote_counts.get)
        
        # 找到对应的提案
        for proposal in proposals:
            if proposal.decision == best_decision:
                return proposal
        
        return proposals[0]
    
    def _generate_summary(
        self,
        rounds: List[DebateRound],
        consensus: Optional[AgentResponse]
    ) -> str:
        """生成摘要"""
        if not consensus:
            return "未能达成共识"
        
        return f"经过 {len(rounds)} 轮辩论，达成共识：{consensus.decision}"
    
    def _extract_recommendations(self, proposals: List[AgentResponse]) -> List[str]:
        """提取建议"""
        recommendations = []
        for proposal in proposals:
            recommendations.extend(proposal.suggestions)
        return list(set(recommendations))
    
    def _extract_risks(self, proposals: List[AgentResponse]) -> List[str]:
        """提取风险"""
        risks = []
        for proposal in proposals:
            risks.extend(proposal.risks)
        return list(set(risks))


class JuryPanel(DebateMode):
    """
    陪审团模式
    
    多个团队投票裁决，多数票决定结果。
    """
    
    def __init__(self):
        super().__init__(
            mode_id="jury_panel",
            name="陪审团",
            description="多个团队投票裁决，多数票决定结果"
        )
    
    async def execute(
        self,
        context: DebateContext,
        teams: List[DebateTeam],
        max_rounds: int = 1
    ) -> DebateResult:
        """执行陪审团裁决"""
        rounds = []
        all_proposals = []
        
        # 各团队分析
        round1 = DebateRound(round_number=1)
        for team in teams:
            responses = await team.discuss(context)
            round1.team_responses[team.team_id] = responses
            all_proposals.extend(responses)
            
            for response in responses:
                message = AgentMessage(
                    agent_id=response.agent_id,
                    role=team.name,
                    content=f"{response.decision}: {response.reasoning}",
                    confidence=response.confidence
                )
                round1.messages.append(message)
        
        rounds.append(round1)
        
        # 投票
        votes = []
        for team in teams:
            team_votes = await team.vote(context, all_proposals)
            votes.extend(team_votes)
        
        # 计算共识
        consensus = self._calculate_consensus(all_proposals, votes)
        
        return DebateResult(
            topic=context.topic,
            mode=self.mode_id,
            teams=[t.team_id for t in teams],
            rounds=rounds,
            consensus=consensus,
            votes=votes,
            confidence=consensus.confidence if consensus else 0.0,
            summary=self._generate_summary(consensus),
            recommendations=self._extract_recommendations(all_proposals),
            risks=self._extract_risks(all_proposals)
        )
    
    def _calculate_consensus(
        self,
        proposals: List[AgentResponse],
        votes: List[AgentMessage]
    ) -> Optional[AgentResponse]:
        """计算共识"""
        if not proposals:
            return None
        
        # 统计投票
        vote_counts: Dict[str, float] = {}
        for vote in votes:
            content = vote.content
            for proposal in proposals:
                if proposal.decision in content:
                    if proposal.decision not in vote_counts:
                        vote_counts[proposal.decision] = 0.0
                    vote_counts[proposal.decision] += vote.confidence
        
        if not vote_counts:
            return max(proposals, key=lambda p: p.confidence)
        
        best_decision = max(vote_counts, key=vote_counts.get)
        
        for proposal in proposals:
            if proposal.decision == best_decision:
                return proposal
        
        return proposals[0]
    
    def _generate_summary(self, consensus: Optional[AgentResponse]) -> str:
        """生成摘要"""
        if not consensus:
            return "未能达成共识"
        return f"陪审团裁决：{consensus.decision}"
    
    def _extract_recommendations(self, proposals: List[AgentResponse]) -> List[str]:
        """提取建议"""
        recommendations = []
        for proposal in proposals:
            recommendations.extend(proposal.suggestions)
        return list(set(recommendations))
    
    def _extract_risks(self, proposals: List[AgentResponse]) -> List[str]:
        """提取风险"""
        risks = []
        for proposal in proposals:
            risks.extend(proposal.risks)
        return list(set(risks))


class DebateEngine:
    """
    辩论引擎
    
    管理辩论模式、团队，执行辩论流程。
    """
    
    def __init__(self):
        self.modes: Dict[str, DebateMode] = {}
        self.teams: Dict[str, DebateTeam] = {}
        
        # 注册默认模式
        self.register_mode(AdversarialDebate())
        self.register_mode(JuryPanel())
    
    def register_mode(self, mode: DebateMode):
        """注册辩论模式"""
        self.modes[mode.mode_id] = mode
    
    def register_team(self, team: DebateTeam):
        """注册辩论团队"""
        self.teams[team.team_id] = team
    
    def get_mode(self, mode_id: str) -> Optional[DebateMode]:
        """获取辩论模式"""
        return self.modes.get(mode_id)
    
    def get_team(self, team_id: str) -> Optional[DebateTeam]:
        """获取辩论团队"""
        return self.teams.get(team_id)
    
    def list_modes(self) -> List[Dict[str, str]]:
        """列出所有辩论模式"""
        return [
            {
                "mode_id": mode.mode_id,
                "name": mode.name,
                "description": mode.description
            }
            for mode in self.modes.values()
        ]
    
    def list_teams(self) -> List[Dict[str, Any]]:
        """列出所有辩论团队"""
        return [team.get_team_summary() for team in self.teams.values()]
    
    async def run_debate(
        self,
        context: DebateContext,
        mode_id: str,
        team_ids: List[str],
        max_rounds: int = 3
    ) -> DebateResult:
        """
        运行辩论
        
        Args:
            context: 辩论上下文
            mode_id: 辩论模式 ID
            team_ids: 参与辩论的团队 ID 列表
            max_rounds: 最大辩论轮数
            
        Returns:
            DebateResult: 辩论结果
        """
        # 获取辩论模式
        mode = self.get_mode(mode_id)
        if not mode:
            raise ValueError(f"未找到辩论模式: {mode_id}")
        
        # 获取辩论团队
        teams = []
        for team_id in team_ids:
            team = self.get_team(team_id)
            if not team:
                raise ValueError(f"未找到辩论团队: {team_id}")
            teams.append(team)
        
        # 执行辩论
        result = await mode.execute(context, teams, max_rounds)
        
        return result
