"""
基础测试

测试 Agent 基类、辩论团队、辩论引擎的基本功能。
"""

import pytest
import asyncio
from typing import List

from agents.base import BaseAgent, SimpleAgent, AgentMessage, AgentResponse, DebateContext
from agents.teams import (
    DebateTeam,
    TechExpert,
    Architect,
    CostAnalyst,
    RiskAssessor,
    QualityEngineer,
    PerformanceEngineer,
    create_full_team,
    create_tech_team,
    create_review_team
)
from core.debate_engine import DebateEngine, AdversarialDebate, JuryPanel
from core.decision_maker import DecisionMaker


# ============================================================
# Agent 基类测试
# ============================================================

class TestAgentBase:
    """Agent 基类测试"""
    
    def test_agent_message_creation(self):
        """测试创建 Agent 消息"""
        message = AgentMessage(
            agent_id="test_agent",
            role="测试角色",
            content="测试内容",
            confidence=0.8
        )
        
        assert message.agent_id == "test_agent"
        assert message.role == "测试角色"
        assert message.content == "测试内容"
        assert message.confidence == 0.8
        assert message.message_id is not None
        assert message.timestamp is not None
    
    def test_agent_response_creation(self):
        """测试创建 Agent 响应"""
        response = AgentResponse(
            agent_id="test_agent",
            decision="测试决策",
            reasoning="测试理由",
            confidence=0.9,
            alternatives=["方案A", "方案B"],
            risks=["风险1", "风险2"],
            suggestions=["建议1", "建议2"]
        )
        
        assert response.agent_id == "test_agent"
        assert response.decision == "测试决策"
        assert response.reasoning == "测试理由"
        assert response.confidence == 0.9
        assert len(response.alternatives) == 2
        assert len(response.risks) == 2
        assert len(response.suggestions) == 2
    
    def test_debate_context_creation(self):
        """测试创建辩论上下文"""
        context = DebateContext(
            topic="测试主题",
            description="测试描述",
            constraints=["约束1", "约束2"],
            requirements=["需求1", "需求2"],
            background={"key": "value"}
        )
        
        assert context.topic == "测试主题"
        assert context.description == "测试描述"
        assert len(context.constraints) == 2
        assert len(context.requirements) == 2
        assert context.background == {"key": "value"}
    
    def test_simple_agent_creation(self):
        """测试创建简单 Agent"""
        agent = SimpleAgent(
            agent_id="test_agent",
            role="测试角色",
            description="测试描述",
            expertise=["技能1", "技能2"]
        )
        
        assert agent.agent_id == "test_agent"
        assert agent.role == "测试角色"
        assert agent.description == "测试描述"
        assert len(agent.expertise) == 2
    
    @pytest.mark.asyncio
    async def test_simple_agent_analyze(self):
        """测试简单 Agent 分析"""
        agent = SimpleAgent(
            agent_id="test_agent",
            role="测试角色"
        )
        
        context = DebateContext(
            topic="测试主题",
            description="测试描述"
        )
        
        response = await agent.analyze(context)
        
        assert response.agent_id == "test_agent"
        assert response.decision == "需要更多信息"
        assert response.confidence == 0.5
    
    @pytest.mark.asyncio
    async def test_simple_agent_vote(self):
        """测试简单 Agent 投票"""
        agent = SimpleAgent(
            agent_id="test_agent",
            role="测试角色"
        )
        
        context = DebateContext(
            topic="测试主题",
            description="测试描述"
        )
        
        proposals = [
            AgentResponse(
                agent_id="agent1",
                decision="方案A",
                reasoning="理由A",
                confidence=0.8
            ),
            AgentResponse(
                agent_id="agent2",
                decision="方案B",
                reasoning="理由B",
                confidence=0.9
            )
        ]
        
        vote = await agent.vote(context, proposals)
        
        assert vote.agent_id == "test_agent"
        assert "方案B" in vote.content  # 应该选择置信度最高的


# ============================================================
# 辩论团队测试
# ============================================================

class TestDebateTeam:
    """辩论团队测试"""
    
    def test_team_creation(self):
        """测试创建团队"""
        team = DebateTeam(
            team_id="test_team",
            name="测试团队",
            description="测试描述",
            agents=[TechExpert(), Architect()]
        )
        
        assert team.team_id == "test_team"
        assert team.name == "测试团队"
        assert len(team.agents) == 2
    
    def test_team_summary(self):
        """测试团队摘要"""
        team = create_tech_team()
        summary = team.get_team_summary()
        
        assert summary["team_id"] == "tech_team"
        assert summary["name"] == "技术选型团队"
        assert len(summary["agents"]) == 4
    
    @pytest.mark.asyncio
    async def test_team_discuss(self):
        """测试团队讨论"""
        team = create_tech_team()
        
        context = DebateContext(
            topic="测试主题",
            description="测试描述"
        )
        
        responses = await team.discuss(context)
        
        assert len(responses) == 4  # 4 个 Agent
        for response in responses:
            assert response.agent_id is not None
            assert response.decision is not None
            assert response.confidence >= 0.0 and response.confidence <= 1.0
    
    @pytest.mark.asyncio
    async def test_team_vote(self):
        """测试团队投票"""
        team = create_tech_team()
        
        context = DebateContext(
            topic="测试主题",
            description="测试描述"
        )
        
        proposals = [
            AgentResponse(
                agent_id="agent1",
                decision="方案A",
                reasoning="理由A",
                confidence=0.8
            )
        ]
        
        votes = await team.vote(context, proposals)
        
        assert len(votes) == 4  # 4 个 Agent 投票


# ============================================================
# 预定义团队测试
# ============================================================

class TestPredefinedTeams:
    """预定义团队测试"""
    
    def test_create_full_team(self):
        """测试创建完整团队"""
        team = create_full_team()
        
        assert team.team_id == "full_team"
        assert team.name == "完整辩论团队"
        assert len(team.agents) == 6
    
    def test_create_tech_team(self):
        """测试创建技术选型团队"""
        team = create_tech_team()
        
        assert team.team_id == "tech_team"
        assert team.name == "技术选型团队"
        assert len(team.agents) == 4
    
    def test_create_review_team(self):
        """测试创建代码审查团队"""
        team = create_review_team()
        
        assert team.team_id == "review_team"
        assert team.name == "代码审查团队"
        assert len(team.agents) == 4


# ============================================================
# 辩论引擎测试
# ============================================================

class TestDebateEngine:
    """辩论引擎测试"""
    
    def test_engine_creation(self):
        """测试创建辩论引擎"""
        engine = DebateEngine()
        
        assert len(engine.modes) == 2  # adversarial_debate, jury_panel
        assert len(engine.teams) == 0
    
    def test_register_mode(self):
        """测试注册辩论模式"""
        engine = DebateEngine()
        
        # 默认已经有 2 个模式
        modes = engine.list_modes()
        assert len(modes) == 2
        
        mode_ids = [m["mode_id"] for m in modes]
        assert "adversarial_debate" in mode_ids
        assert "jury_panel" in mode_ids
    
    def test_register_team(self):
        """测试注册辩论团队"""
        engine = DebateEngine()
        team = create_tech_team()
        
        engine.register_team(team)
        
        assert len(engine.teams) == 1
        assert engine.get_team("tech_team") is not None
    
    def test_list_modes(self):
        """测试列出辩论模式"""
        engine = DebateEngine()
        modes = engine.list_modes()
        
        assert len(modes) == 2
        for mode in modes:
            assert "mode_id" in mode
            assert "name" in mode
            assert "description" in mode
    
    def test_list_teams(self):
        """测试列出辩论团队"""
        engine = DebateEngine()
        team = create_tech_team()
        engine.register_team(team)
        
        teams = engine.list_teams()
        
        assert len(teams) == 1
        assert teams[0]["team_id"] == "tech_team"
    
    @pytest.mark.asyncio
    async def test_run_adversarial_debate(self):
        """测试运行对抗辩论"""
        engine = DebateEngine()
        team = create_tech_team()
        engine.register_team(team)
        
        context = DebateContext(
            topic="MongoDB vs PostgreSQL",
            description="选择数据库",
            constraints=["成本 < $100/月"],
            requirements=["文档型数据", "复杂查询"]
        )
        
        result = await engine.run_debate(
            context=context,
            mode_id="adversarial_debate",
            team_ids=["tech_team"],
            max_rounds=2
        )
        
        assert result.topic == "MongoDB vs PostgreSQL"
        assert result.mode == "adversarial_debate"
        assert len(result.rounds) == 2
        assert result.consensus is not None
        assert result.confidence >= 0.0 and result.confidence <= 1.0
    
    @pytest.mark.asyncio
    async def test_run_jury_panel(self):
        """测试运行陪审团"""
        engine = DebateEngine()
        team = create_tech_team()
        engine.register_team(team)
        
        context = DebateContext(
            topic="MongoDB vs PostgreSQL",
            description="选择数据库"
        )
        
        result = await engine.run_debate(
            context=context,
            mode_id="jury_panel",
            team_ids=["tech_team"],
            max_rounds=1
        )
        
        assert result.topic == "MongoDB vs PostgreSQL"
        assert result.mode == "jury_panel"
        assert len(result.rounds) == 1
        assert result.consensus is not None
    
    @pytest.mark.asyncio
    async def test_run_debate_invalid_mode(self):
        """测试运行辩论 - 无效模式"""
        engine = DebateEngine()
        team = create_tech_team()
        engine.register_team(team)
        
        context = DebateContext(
            topic="测试主题",
            description="测试描述"
        )
        
        with pytest.raises(ValueError, match="未找到辩论模式"):
            await engine.run_debate(
                context=context,
                mode_id="invalid_mode",
                team_ids=["tech_team"]
            )
    
    @pytest.mark.asyncio
    async def test_run_debate_invalid_team(self):
        """测试运行辩论 - 无效团队"""
        engine = DebateEngine()
        
        context = DebateContext(
            topic="测试主题",
            description="测试描述"
        )
        
        with pytest.raises(ValueError, match="未找到辩论团队"):
            await engine.run_debate(
                context=context,
                mode_id="adversarial_debate",
                team_ids=["invalid_team"]
            )


# ============================================================
# 决策者测试
# ============================================================

class TestDecisionMaker:
    """决策者测试"""
    
    def test_decision_maker_creation(self):
        """测试创建决策者"""
        maker = DecisionMaker(
            budget_threshold=10000.0,
            risk_threshold="高",
            confidence_threshold=0.7
        )
        
        assert maker.budget_threshold == 10000.0
        assert maker.risk_threshold == "高"
        assert maker.confidence_threshold == 0.7
        assert len(maker.decision_history) == 0
    
    @pytest.mark.asyncio
    async def test_evaluate_approved(self):
        """测试评估 - 批准"""
        maker = DecisionMaker()
        
        # 创建一个高置信度的辩论结果
        from core.debate_engine import DebateResult, DebateRound
        
        result = DebateResult(
            topic="测试主题",
            mode="adversarial_debate",
            teams=["test_team"],
            rounds=[DebateRound(round_number=1)],
            consensus=AgentResponse(
                agent_id="test_agent",
                decision="测试决策",
                reasoning="测试理由",
                confidence=0.9
            ),
            confidence=0.9,
            summary="测试摘要",
            recommendations=["建议1", "建议2"],
            risks=[]
        )
        
        decision = await maker.evaluate(result)
        
        assert decision.approved is True
        assert "批准" in decision.decision
        assert decision.confidence == 0.9
    
    @pytest.mark.asyncio
    async def test_evaluate_rejected_low_confidence(self):
        """测试评估 - 拒绝（置信度不足）"""
        maker = DecisionMaker(confidence_threshold=0.8)
        
        from core.debate_engine import DebateResult, DebateRound
        
        result = DebateResult(
            topic="测试主题",
            mode="adversarial_debate",
            teams=["test_team"],
            rounds=[DebateRound(round_number=1)],
            consensus=AgentResponse(
                agent_id="test_agent",
                decision="测试决策",
                reasoning="测试理由",
                confidence=0.5
            ),
            confidence=0.5,
            summary="测试摘要"
        )
        
        decision = await maker.evaluate(result)
        
        assert decision.approved is False
        assert "拒绝" in decision.decision
        assert "置信度不足" in decision.reasoning
    
    def test_decision_history(self):
        """测试决策历史"""
        maker = DecisionMaker()
        
        assert len(maker.get_decision_history()) == 0
        
        maker.clear_history()
        
        assert len(maker.get_decision_history()) == 0


# ============================================================
# 集成测试
# ============================================================

class TestIntegration:
    """集成测试"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """测试完整工作流"""
        # 创建辩论引擎
        engine = DebateEngine()
        
        # 注册团队
        tech_team = create_tech_team()
        engine.register_team(tech_team)
        
        # 创建辩论上下文
        context = DebateContext(
            topic="MongoDB vs PostgreSQL",
            description="选择数据库",
            constraints=["成本 < $100/月"],
            requirements=["文档型数据", "复杂查询"]
        )
        
        # 运行辩论
        debate_result = await engine.run_debate(
            context=context,
            mode_id="adversarial_debate",
            team_ids=["tech_team"],
            max_rounds=2
        )
        
        # 决策评估
        decision_maker = DecisionMaker()
        decision = await decision_maker.evaluate(debate_result)
        
        # 验证结果
        assert debate_result.topic == "MongoDB vs PostgreSQL"
        assert debate_result.consensus is not None
        assert decision.topic == "MongoDB vs PostgreSQL"
        assert decision.confidence >= 0.0 and decision.confidence <= 1.0
        
        # 验证决策历史
        assert len(decision_maker.get_decision_history()) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
