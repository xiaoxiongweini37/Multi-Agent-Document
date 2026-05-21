"""
辩论团队定义

每个团队包含多个 Agent，从不同视角分析问题。
"""

from typing import List, Dict, Any
from .base import BaseAgent, SimpleAgent, AgentResponse, AgentMessage, DebateContext


class DebateTeam:
    """
    辩论团队
    
    包含多个 Agent，从不同视角分析问题。
    """
    
    def __init__(
        self,
        team_id: str,
        name: str,
        description: str = "",
        agents: List[BaseAgent] = []
    ):
        """
        初始化辩论团队
        
        Args:
            team_id: 团队唯一标识
            name: 团队名称
            description: 团队描述
            agents: 团队成员列表
        """
        self.team_id = team_id
        self.name = name
        self.description = description
        self.agents = agents
    
    async def discuss(self, context: DebateContext) -> List[AgentResponse]:
        """
        团队讨论
        
        所有 Agent 独立分析问题，返回各自的观点。
        
        Args:
            context: 辩论上下文
            
        Returns:
            List[AgentResponse]: 各 Agent 的分析结果
        """
        responses = []
        for agent in self.agents:
            response = await agent.analyze(context)
            responses.append(response)
        return responses
    
    async def debate(
        self,
        context: DebateContext,
        messages: List[AgentMessage]
    ) -> List[AgentResponse]:
        """
        团队辩论
        
        所有 Agent 参与辩论，考虑其他人的观点后给出自己的看法。
        
        Args:
            context: 辩论上下文
            messages: 其他团队的消息
            
        Returns:
            List[AgentResponse]: 各 Agent 的辩论结果
        """
        responses = []
        for agent in self.agents:
            response = await agent.debate(context, messages)
            responses.append(response)
        return responses
    
    async def vote(
        self,
        context: DebateContext,
        proposals: List[AgentResponse]
    ) -> List[AgentMessage]:
        """
        团队投票
        
        所有 Agent 投票选择最佳方案。
        
        Args:
            context: 辩论上下文
            proposals: 各团队的提案
            
        Returns:
            List[AgentMessage]: 各 Agent 的投票结果
        """
        votes = []
        for agent in self.agents:
            vote = await agent.vote(context, proposals)
            votes.append(vote)
        return votes
    
    def get_team_summary(self) -> Dict[str, Any]:
        """获取团队摘要"""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "description": self.description,
            "agents": [agent.to_dict() for agent in self.agents]
        }
    
    def add_agent(self, agent: BaseAgent):
        """添加团队成员"""
        self.agents.append(agent)
    
    def remove_agent(self, agent_id: str):
        """移除团队成员"""
        self.agents = [a for a in self.agents if a.agent_id != agent_id]
    
    def __repr__(self) -> str:
        return f"<DebateTeam(id={self.team_id}, name={self.name}, agents={len(self.agents)})>"


# ============================================================
# 预定义的辩论团队
# ============================================================

class TechExpert(SimpleAgent):
    """技术专家"""
    
    def __init__(self):
        super().__init__(
            agent_id="tech_expert",
            role="技术专家",
            description="负责评估技术方案的可行性、技术栈选择、实现难度",
            expertise=["技术选型", "可行性评估", "技术栈", "实现难度"]
        )


class Architect(SimpleAgent):
    """架构专家"""
    
    def __init__(self):
        super().__init__(
            agent_id="architect",
            role="架构专家",
            description="负责设计系统架构，考虑扩展性、可维护性、团队规模",
            expertise=["系统设计", "模块划分", "扩展性", "可维护性"]
        )


class CostAnalyst(SimpleAgent):
    """成本分析师"""
    
    def __init__(self):
        super().__init__(
            agent_id="cost_analyst",
            role="成本分析师",
            description="负责评估成本，包括开发时间、服务器费用、维护成本",
            expertise=["开发成本", "维护成本", "服务器费用", "人力成本"]
        )


class RiskAssessor(SimpleAgent):
    """风险评估师"""
    
    def __init__(self):
        super().__init__(
            agent_id="risk_assessor",
            role="风险评估师",
            description="负责评估风险，包括技术债、安全漏洞、依赖风险",
            expertise=["技术债", "安全风险", "依赖风险", "业务风险"]
        )


class QualityEngineer(SimpleAgent):
    """质量工程师"""
    
    def __init__(self):
        super().__init__(
            agent_id="quality_engineer",
            role="质量工程师",
            description="负责确保代码质量，包括规范、测试、文档",
            expertise=["代码规范", "测试覆盖", "文档质量", "可维护性"]
        )


class PerformanceEngineer(SimpleAgent):
    """性能工程师"""
    
    def __init__(self):
        super().__init__(
            agent_id="performance_engineer",
            role="性能工程师",
            description="负责评估性能，包括响应时间、并发能力、资源占用",
            expertise=["响应时间", "并发能力", "资源占用", "扩展性"]
        )


# ============================================================
# 预定义团队组合
# ============================================================

def create_full_team() -> DebateTeam:
    """创建完整的辩论团队（6 个成员）"""
    return DebateTeam(
        team_id="full_team",
        name="完整辩论团队",
        description="包含所有 6 个专业角色的完整辩论团队",
        agents=[
            TechExpert(),
            Architect(),
            CostAnalyst(),
            RiskAssessor(),
            QualityEngineer(),
            PerformanceEngineer(),
        ]
    )


def create_tech_team() -> DebateTeam:
    """创建技术选型团队"""
    return DebateTeam(
        team_id="tech_team",
        name="技术选型团队",
        description="专注于技术选型的团队",
        agents=[
            TechExpert(),
            Architect(),
            CostAnalyst(),
            RiskAssessor(),
        ]
    )


def create_review_team() -> DebateTeam:
    """创建代码审查团队"""
    return DebateTeam(
        team_id="review_team",
        name="代码审查团队",
        description="专注于代码审查的团队",
        agents=[
            TechExpert(),
            QualityEngineer(),
            PerformanceEngineer(),
            RiskAssessor(),
        ]
    )
