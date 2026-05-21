"""
Multi-Agent Dev Assistant — Agents 模块

包含所有辩论团队的定义。
"""

from .base import BaseAgent, SimpleAgent, AgentMessage, AgentResponse, DebateContext
from .teams import (
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

__all__ = [
    # 基类
    "BaseAgent",
    "SimpleAgent",
    "AgentMessage",
    "AgentResponse",
    "DebateContext",
    
    # 团队
    "DebateTeam",
    "TechExpert",
    "Architect",
    "CostAnalyst",
    "RiskAssessor",
    "QualityEngineer",
    "PerformanceEngineer",
    
    # 工厂函数
    "create_full_team",
    "create_tech_team",
    "create_review_team",
]
