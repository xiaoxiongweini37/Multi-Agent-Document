"""
Multi-Agent Dev Assistant — Core 模块

包含辩论引擎和决策者的核心实现。
"""

from .debate_engine import (
    DebateEngine,
    DebateMode,
    AdversarialDebate,
    JuryPanel,
    DebateRound,
    DebateResult
)
from .decision_maker import DecisionMaker, Decision

__all__ = [
    # 辩论引擎
    "DebateEngine",
    "DebateMode",
    "AdversarialDebate",
    "JuryPanel",
    "DebateRound",
    "DebateResult",
    
    # 决策者
    "DecisionMaker",
    "Decision",
]
