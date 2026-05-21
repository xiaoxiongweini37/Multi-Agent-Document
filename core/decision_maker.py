"""
决策者模块

负责审核辩论结果，评估预算/风险，做出最终决策。
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from core.debate_engine import DebateResult
from agents.base import AgentResponse


class Decision(BaseModel):
    """决策模型"""
    
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    approved: bool
    decision: str
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    risks: List[str] = []
    recommendations: List[str] = []
    budget_check: Optional[Dict[str, Any]] = None
    risk_check: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DecisionMaker:
    """
    决策者
    
    审核辩论结果，评估预算/风险，做出最终决策。
    """
    
    def __init__(
        self,
        budget_threshold: float = 10000.0,
        risk_threshold: str = "高",
        confidence_threshold: float = 0.7
    ):
        """
        初始化决策者
        
        Args:
            budget_threshold: 预算阈值
            risk_threshold: 风险阈值（高/中/低）
            confidence_threshold: 置信度阈值
        """
        self.budget_threshold = budget_threshold
        self.risk_threshold = risk_threshold
        self.confidence_threshold = confidence_threshold
        self.decision_history: List[Decision] = []
    
    async def evaluate(self, debate_result: DebateResult) -> Decision:
        """
        评估辩论结果
        
        Args:
            debate_result: 辩论结果
            
        Returns:
            Decision: 决策结果
        """
        # 预算检查
        budget_check = self._check_budget(debate_result)
        
        # 风险检查
        risk_check = self._check_risks(debate_result)
        
        # 置信度检查
        confidence_check = self._check_confidence(debate_result)
        
        # 综合判断
        approved = (
            budget_check["passed"] and
            risk_check["passed"] and
            confidence_check["passed"]
        )
        
        # 生成决策
        if approved:
            decision = self._generate_approved_decision(debate_result)
            reasoning = self._generate_approved_reasoning(
                debate_result, budget_check, risk_check, confidence_check
            )
        else:
            decision = self._generate_rejected_decision(
                debate_result, budget_check, risk_check, confidence_check
            )
            reasoning = self._generate_rejected_reasoning(
                budget_check, risk_check, confidence_check
            )
        
        result = Decision(
            topic=debate_result.topic,
            approved=approved,
            decision=decision,
            reasoning=reasoning,
            confidence=debate_result.confidence,
            risks=debate_result.risks,
            recommendations=debate_result.recommendations,
            budget_check=budget_check,
            risk_check=risk_check,
            metadata={
                "debate_id": debate_result.debate_id,
                "mode": debate_result.mode,
                "teams": debate_result.teams,
                "rounds": len(debate_result.rounds)
            }
        )
        
        self.decision_history.append(result)
        return result
    
    def _check_budget(self, debate_result: DebateResult) -> Dict[str, Any]:
        """检查预算"""
        # 从辩论结果中提取成本信息
        # 这里简化处理，实际应该解析各团队的成本分析
        estimated_cost = 0.0
        
        for round_data in debate_result.rounds:
            for team_id, responses in round_data.team_responses.items():
                for response in responses:
                    # 尝试从 reasoning 中提取成本
                    if "成本" in response.reasoning or "$" in response.reasoning:
                        # 简单提取，实际应该更精确
                        estimated_cost += 1000.0  # 假设值
        
        passed = estimated_cost <= self.budget_threshold
        
        return {
            "passed": passed,
            "estimated_cost": estimated_cost,
            "threshold": self.budget_threshold,
            "message": f"预算{'通过' if passed else '超支'}: ${estimated_cost:.2f} / ${self.budget_threshold:.2f}"
        }
    
    def _check_risks(self, debate_result: DebateResult) -> Dict[str, Any]:
        """检查风险"""
        high_risks = []
        medium_risks = []
        low_risks = []
        
        for risk in debate_result.risks:
            if "高" in risk or "严重" in risk:
                high_risks.append(risk)
            elif "中" in risk:
                medium_risks.append(risk)
            else:
                low_risks.append(risk)
        
        # 根据风险阈值判断
        if self.risk_threshold == "高":
            passed = len(high_risks) == 0
        elif self.risk_threshold == "中":
            passed = len(high_risks) == 0 and len(medium_risks) <= 2
        else:
            passed = len(high_risks) == 0 and len(medium_risks) == 0
        
        return {
            "passed": passed,
            "high_risks": high_risks,
            "medium_risks": medium_risks,
            "low_risks": low_risks,
            "message": f"风险{'通过' if passed else '过高'}: 高风险 {len(high_risks)} 个, 中风险 {len(medium_risks)} 个"
        }
    
    def _check_confidence(self, debate_result: DebateResult) -> Dict[str, Any]:
        """检查置信度"""
        passed = debate_result.confidence >= self.confidence_threshold
        
        return {
            "passed": passed,
            "confidence": debate_result.confidence,
            "threshold": self.confidence_threshold,
            "message": f"置信度{'通过' if passed else '不足'}: {debate_result.confidence:.2f} / {self.confidence_threshold:.2f}"
        }
    
    def _generate_approved_decision(self, debate_result: DebateResult) -> str:
        """生成批准决策"""
        if debate_result.consensus:
            return f"批准: {debate_result.consensus.decision}"
        return "批准: 通过辩论达成的方案"
    
    def _generate_rejected_decision(
        self,
        debate_result: DebateResult,
        budget_check: Dict[str, Any],
        risk_check: Dict[str, Any],
        confidence_check: Dict[str, Any]
    ) -> str:
        """生成拒绝决策"""
        reasons = []
        
        if not budget_check["passed"]:
            reasons.append("预算超支")
        if not risk_check["passed"]:
            reasons.append("风险过高")
        if not confidence_check["passed"]:
            reasons.append("置信度不足")
        
        return f"拒绝: {', '.join(reasons)}"
    
    def _generate_approved_reasoning(
        self,
        debate_result: DebateResult,
        budget_check: Dict[str, Any],
        risk_check: Dict[str, Any],
        confidence_check: Dict[str, Any]
    ) -> str:
        """生成批准理由"""
        return (
            f"经过 {len(debate_result.rounds)} 轮辩论，{len(debate_result.teams)} 个团队参与讨论。"
            f"{budget_check['message']}。"
            f"{risk_check['message']}。"
            f"{confidence_check['message']}。"
            f"综合评估后批准执行。"
        )
    
    def _generate_rejected_reasoning(
        self,
        budget_check: Dict[str, Any],
        risk_check: Dict[str, Any],
        confidence_check: Dict[str, Any]
    ) -> str:
        """生成拒绝理由"""
        issues = []
        
        if not budget_check["passed"]:
            issues.append(budget_check["message"])
        if not risk_check["passed"]:
            issues.append(risk_check["message"])
        if not confidence_check["passed"]:
            issues.append(confidence_check["message"])
        
        return f"决策未通过，原因：{'; '.join(issues)}"
    
    def get_decision_history(self) -> List[Decision]:
        """获取决策历史"""
        return self.decision_history.copy()
    
    def clear_history(self):
        """清空决策历史"""
        self.decision_history.clear()
