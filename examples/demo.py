"""
Multi-Agent Dev Assistant — Demo

运行方式：
    python examples/demo.py
"""

import asyncio
from typing import Dict, Any, List


# ============================================================
# 模拟 Agent 基类（实际实现见 agents/ 目录）
# ============================================================

class AgentMessage:
    """Agent 消息"""
    def __init__(self, agent_id: str, role: str, content: str, confidence: float):
        self.agent_id = agent_id
        self.role = role
        self.content = content
        self.confidence = confidence


class AgentResponse:
    """Agent 响应"""
    def __init__(self, agent_id: str, decision: str, reasoning: str, confidence: float):
        self.agent_id = agent_id
        self.decision = decision
        self.reasoning = reasoning
        self.confidence = confidence


# ============================================================
# 模拟辩论团队
# ============================================================

class TechExpert:
    """技术专家"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        topic = context.get("topic", "")
        if "MongoDB" in topic and "PostgreSQL" in topic:
            return AgentResponse(
                agent_id="tech_expert",
                decision="PostgreSQL",
                reasoning="PostgreSQL 支持 JSONB，兼顾文档型和关系型查询，功能更全面",
                confidence=0.85
            )
        return AgentResponse(
            agent_id="tech_expert",
            decision="需要更多信息",
            reasoning="技术选型需要了解具体需求",
            confidence=0.5
        )


class Architect:
    """架构专家"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        topic = context.get("topic", "")
        if "MongoDB" in topic and "PostgreSQL" in topic:
            return AgentResponse(
                agent_id="architect",
                decision="PostgreSQL",
                reasoning="PostgreSQL 更成熟，生态更好，长期维护成本更低",
                confidence=0.80
            )
        return AgentResponse(
            agent_id="architect",
            decision="需要更多信息",
            reasoning="架构设计需要了解系统规模和团队能力",
            confidence=0.5
        )


class CostAnalyst:
    """成本分析师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        topic = context.get("topic", "")
        if "MongoDB" in topic and "PostgreSQL" in topic:
            return AgentResponse(
                agent_id="cost_analyst",
                decision="PostgreSQL",
                reasoning="PostgreSQL 开源免费，MongoDB Atlas 云服务成本较高",
                confidence=0.90
            )
        return AgentResponse(
            agent_id="cost_analyst",
            decision="需要更多信息",
            reasoning="成本分析需要了解使用规模和部署方式",
            confidence=0.5
        )


class RiskAssessor:
    """风险评估师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        topic = context.get("topic", "")
        if "MongoDB" in topic and "PostgreSQL" in topic:
            return AgentResponse(
                agent_id="risk_assessor",
                decision="PostgreSQL",
                reasoning="PostgreSQL 更成熟稳定，社区活跃，遇到问题容易找到解决方案",
                confidence=0.85
            )
        return AgentResponse(
            agent_id="risk_assessor",
            decision="需要更多信息",
            reasoning="风险评估需要了解业务场景和团队经验",
            confidence=0.5
        )


class QualityEngineer:
    """质量工程师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        topic = context.get("topic", "")
        if "MongoDB" in topic and "PostgreSQL" in topic:
            return AgentResponse(
                agent_id="quality_engineer",
                decision="PostgreSQL",
                reasoning="PostgreSQL 支持 ACID，数据一致性更强，适合关键业务",
                confidence=0.88
            )
        return AgentResponse(
            agent_id="quality_engineer",
            decision="需要更多信息",
            reasoning="质量评估需要了解数据重要性和一致性要求",
            confidence=0.5
        )


class PerformanceEngineer:
    """性能工程师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        topic = context.get("topic", "")
        if "MongoDB" in topic and "PostgreSQL" in topic:
            return AgentResponse(
                agent_id="performance_engineer",
                decision="两者相当",
                reasoning="简单查询 MongoDB 略快，复杂查询 PostgreSQL 更优，整体性能相当",
                confidence=0.75
            )
        return AgentResponse(
            agent_id="performance_engineer",
            decision="需要更多信息",
            reasoning="性能评估需要了解查询模式和数据规模",
            confidence=0.5
        )


# ============================================================
# 辩论引擎
# ============================================================

class DebateEngine:
    """辩论引擎"""
    
    def __init__(self):
        self.agents = [
            TechExpert(),
            Architect(),
            CostAnalyst(),
            RiskAssessor(),
            QualityEngineer(),
            PerformanceEngineer(),
        ]
    
    async def run_debate(self, topic: str, context: Dict[str, Any]) -> List[AgentResponse]:
        """运行辩论"""
        print(f"\n{'='*60}")
        print(f"辩论主题: {topic}")
        print(f"{'='*60}")
        
        responses = []
        for i, agent in enumerate(self.agents, 1):
            response = await agent.analyze(context)
            responses.append(response)
            print(f"\n[{i}] {response.agent_id}")
            print(f"    决策: {response.decision}")
            print(f"    理由: {response.reasoning}")
            print(f"    置信度: {response.confidence}")
        
        return responses


# ============================================================
# 决策者
# ============================================================

class DecisionMaker:
    """决策者"""
    
    async def evaluate(self, responses: List[AgentResponse]) -> Dict[str, Any]:
        """评估辩论结果"""
        print(f"\n{'='*60}")
        print("决策者评估")
        print(f"{'='*60}")
        
        # 统计投票
        votes = {}
        for r in responses:
            decision = r.decision
            if decision not in votes:
                votes[decision] = []
            votes[decision].append(r)
        
        # 找出票数最多的决策
        max_votes = max(len(v) for v in votes.values())
        top_decisions = [d for d, v in votes.items() if len(v) == max_votes]
        
        # 计算平均置信度
        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        
        # 输出投票结果
        print(f"\n投票结果:")
        for decision, voters in votes.items():
            print(f"  {decision}: {len(votes)} 票")
        
        print(f"\n推荐决策: {top_decisions[0]}")
        print(f"平均置信度: {avg_confidence:.2f}")
        
        # 输出各团队意见
        print(f"\n各团队意见:")
        for r in responses:
            print(f"  {r.agent_id}: {r.decision}")
        
        return {
            "decision": top_decisions[0],
            "confidence": avg_confidence,
            "votes": votes,
            "reasoning": "基于多团队投票和置信度综合评估"
        }


# ============================================================
# 主流程
# ============================================================

async def demo_tech_selection():
    """演示：技术选型"""
    print("\n" + "=" * 60)
    print("场景1：技术选型")
    print("=" * 60)
    
    # 初始化组件
    debate_engine = DebateEngine()
    decision_maker = DecisionMaker()
    
    # 运行辩论
    topic = "MongoDB vs PostgreSQL"
    context = {
        "topic": topic,
        "data_type": "文档型 + 关系型",
        "query_pattern": "复杂查询为主",
        "scale": "中等",
        "budget": "$100/月",
    }
    
    responses = await debate_engine.run_debate(topic, context)
    
    # 决策评估
    decision = await decision_maker.evaluate(responses)
    
    # 输出最终结果
    print(f"\n{'='*60}")
    print("最终决策报告")
    print(f"{'='*60}")
    print(f"问题: {topic}")
    print(f"决策: {decision['decision']}")
    print(f"置信度: {decision['confidence']:.2f}")
    print(f"理由: {decision['reasoning']}")


async def demo_code_review():
    """演示：代码审查"""
    print("\n" + "=" * 60)
    print("场景2：代码审查")
    print("=" * 60)
    
    # 模拟代码审查结果
    print("\n代码审查结果:")
    print("┌─────────────────────────────────────────┐")
    print("│ 代码质量：7/10                          │")
    print("├─────────────────────────────────────────┤")
    print("│ 问题：                                  │")
    print("│ 1. 命名不规范（P1）                     │")
    print("│ 2. 缺少错误处理（P1）                   │")
    print("│ 3. N+1 查询（P2）                       │")
    print("│ 4. 缺少注释（P3）                       │")
    print("├─────────────────────────────────────────┤")
    print("│ 建议：                                  │")
    print("│ 1. 重构函数命名，使用描述性名称         │")
    print("│ 2. 添加 try-catch 和日志                │")
    print("│ 3. 使用 JOIN 替代循环查询               │")
    print("│ 4. 添加关键逻辑注释                     │")
    print("└─────────────────────────────────────────┘")


async def demo_architecture():
    """演示：架构设计"""
    print("\n" + "=" * 60)
    print("场景3：架构设计")
    print("=" * 60)
    
    print("\n架构设计建议:")
    print("┌─────────────────────────────────────────┐")
    print("│ 方案A：单体应用                         │")
    print("│ 优点：简单，开发快，部署方便            │")
    print("│ 缺点：扩展性差，耦合度高                │")
    print("│ 适用：初期，团队小                      │")
    print("├─────────────────────────────────────────┤")
    print("│ 方案B：微服务                           │")
    print("│ 优点：扩展性好，独立部署                │")
    print("│ 缺点：复杂度高，运维成本高              │")
    print("│ 适用：成熟期，团队大                    │")
    print("├─────────────────────────────────────────┤")
    print("│ 推荐：先单体，后续拆分                  │")
    print("│ 理由：当前团队小，快速验证需求更重要    │")
    print("│ 路径：单体 → 模块化 → 微服务            │")
    print("└─────────────────────────────────────────┘")


async def main():
    """主流程演示"""
    print("=" * 60)
    print("Multi-Agent Dev Assistant — Demo")
    print("=" * 60)
    print("\n这是一个通用开发辅助系统，帮你做技术决策、方案评估、代码审查等。")
    print("\n适用场景：")
    print("  1. 技术选型（A vs B）")
    print("  2. 方案评估（可行性、成本、风险）")
    print("  3. 代码审查（质量、规范、安全）")
    print("  4. 架构设计（系统设计、模块划分）")
    print("  5. 问题排查（根因分析、优化建议）")
    
    # 演示三个场景
    await demo_tech_selection()
    await demo_code_review()
    await demo_architecture()
    
    print("\n" + "=" * 60)
    print("演示结束")
    print("=" * 60)
    print("\n这个系统适用于任何项目，换公司也能带走。")
    print("详细文档请查看 README.md")


if __name__ == "__main__":
    asyncio.run(main())
