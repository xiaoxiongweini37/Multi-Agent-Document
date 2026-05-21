"""
Multi-Agent Dev Assistant — Demo

运行方式：
    python examples/demo.py
"""

import asyncio
from typing import Dict, Any, List

# 导入项目模块
from agents.base import DebateContext
from agents.teams import create_full_team, create_tech_team, create_review_team
from core.debate_engine import DebateEngine, AdversarialDebate, JuryPanel
from core.decision_maker import DecisionMaker


async def demo_tech_selection():
    """演示：技术选型"""
    print("\n" + "=" * 60)
    print("场景1：技术选型 — MongoDB vs PostgreSQL")
    print("=" * 60)
    
    # 创建辩论引擎
    engine = DebateEngine()
    
    # 注册团队（创建两个视角的团队）
    from agents.teams import DebateTeam, TechExpert, Architect, CostAnalyst, RiskAssessor
    
    # 技术团队：关注技术实现
    tech_team = DebateTeam(
        team_id="tech_team",
        name="技术实现团队",
        description="关注技术实现和可行性",
        agents=[TechExpert(), Architect()]
    )
    
    # 业务团队：关注成本和风险
    business_team = DebateTeam(
        team_id="business_team",
        name="业务评估团队",
        description="关注成本和风险",
        agents=[CostAnalyst(), RiskAssessor()]
    )
    
    engine.register_team(tech_team)
    engine.register_team(business_team)
    
    # 创建辩论上下文
    context = DebateContext(
        topic="MongoDB vs PostgreSQL",
        description="选择数据库技术栈",
        constraints=["成本 < $100/月", "必须支持 ACID"],
        requirements=["文档型数据", "复杂查询", "中等规模"],
        background={
            "data_type": "文档型 + 关系型",
            "query_pattern": "复杂查询为主",
            "scale": "中等",
            "budget": "$100/月"
        }
    )
    
    # 运行辩论
    result = await engine.run_debate(
        context=context,
        mode_id="adversarial_debate",
        team_ids=["tech_team", "business_team"],
        max_rounds=2
    )
    
    # 输出辩论结果
    print(f"\n辩论结果:")
    print(f"  主题: {result.topic}")
    print(f"  模式: {result.mode}")
    print(f"  轮数: {len(result.rounds)}")
    print(f"  共识: {result.consensus.decision if result.consensus else '无'}")
    print(f"  置信度: {result.confidence:.2f}")
    
    # 决策评估
    decision_maker = DecisionMaker()
    decision = await decision_maker.evaluate(result)
    
    print(f"\n决策结果:")
    print(f"  决策: {decision.decision}")
    print(f"  批准: {'是' if decision.approved else '否'}")
    print(f"  理由: {decision.reasoning}")
    
    if decision.recommendations:
        print(f"\n建议:")
        for rec in decision.recommendations:
            print(f"  - {rec}")
    
    if decision.risks:
        print(f"\n风险:")
        for risk in decision.risks:
            print(f"  - {risk}")


async def demo_code_review():
    """演示：代码审查"""
    print("\n" + "=" * 60)
    print("场景2：代码审查")
    print("=" * 60)
    
    # 创建辩论引擎
    engine = DebateEngine()
    
    # 注册团队
    review_team = create_review_team()
    engine.register_team(review_team)
    
    # 创建辩论上下文
    context = DebateContext(
        topic="代码审查: 用户认证模块",
        description="审查用户认证模块的代码质量",
        constraints=["符合 PEP 8", "测试覆盖 > 80%"],
        requirements=["安全性", "可维护性", "性能"],
        background={
            "code": "def login(username, password):\n    user = db.query(username)\n    if user.password == password:\n        return token\n    return None",
            "language": "python",
            "purpose": "用户认证"
        }
    )
    
    # 运行辩论
    result = await engine.run_debate(
        context=context,
        mode_id="jury_panel",
        team_ids=["review_team"],
        max_rounds=1
    )
    
    # 输出辩论结果
    print(f"\n审查结果:")
    print(f"  主题: {result.topic}")
    print(f"  共识: {result.consensus.decision if result.consensus else '无'}")
    print(f"  置信度: {result.confidence:.2f}")
    
    # 决策评估
    decision_maker = DecisionMaker()
    decision = await decision_maker.evaluate(result)
    
    print(f"\n决策:")
    print(f"  {decision.decision}")
    print(f"  理由: {decision.reasoning}")


async def demo_architecture():
    """演示：架构设计"""
    print("\n" + "=" * 60)
    print("场景3：架构设计")
    print("=" * 60)
    
    # 创建辩论引擎
    engine = DebateEngine()
    
    # 注册团队（创建两个视角的团队）
    from agents.teams import DebateTeam, TechExpert, Architect, CostAnalyst, RiskAssessor, QualityEngineer, PerformanceEngineer
    
    # 技术团队：关注技术实现和架构
    tech_team = DebateTeam(
        team_id="arch_tech_team",
        name="技术架构团队",
        description="关注技术实现和架构设计",
        agents=[TechExpert(), Architect(), PerformanceEngineer()]
    )
    
    # 业务团队：关注成本、风险和质量
    business_team = DebateTeam(
        team_id="arch_business_team",
        name="业务评估团队",
        description="关注成本、风险和质量",
        agents=[CostAnalyst(), RiskAssessor(), QualityEngineer()]
    )
    
    engine.register_team(tech_team)
    engine.register_team(business_team)
    
    # 创建辩论上下文
    context = DebateContext(
        topic="聊天系统架构设计",
        description="设计一个实时聊天系统",
        constraints=["使用 Python", "部署在 AWS", "开发时间 < 3 个月"],
        requirements=["高并发", "可扩展", "低成本"],
        background={
            "users": 10000,
            "concurrent": 1000,
            "features": ["文字", "图片", "文件", "群聊"],
            "team_size": 3
        }
    )
    
    # 运行辩论
    result = await engine.run_debate(
        context=context,
        mode_id="adversarial_debate",
        team_ids=["arch_tech_team", "arch_business_team"],
        max_rounds=2
    )
    
    # 输出辩论结果
    print(f"\n架构设计结果:")
    print(f"  主题: {result.topic}")
    print(f"  共识: {result.consensus.decision if result.consensus else '无'}")
    print(f"  置信度: {result.confidence:.2f}")
    
    # 决策评估
    decision_maker = DecisionMaker()
    decision = await decision_maker.evaluate(result)
    
    print(f"\n决策:")
    print(f"  {decision.decision}")
    print(f"  理由: {decision.reasoning}")
    
    if decision.recommendations:
        print(f"\n建议:")
        for rec in decision.recommendations:
            print(f"  - {rec}")


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
