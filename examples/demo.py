"""
Multi-Agent Document Processing System — Demo

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

class OCRSpecialist:
    """OCR 技术专家"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        return AgentResponse(
            agent_id="ocr_specialist",
            decision="使用 PaddleOCR-VL",
            reasoning="PaddleOCR-VL 对中文表格识别准确率高，支持版面分析",
            confidence=0.9
        )


class DocClassifier:
    """文档分类专家"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        return AgentResponse(
            agent_id="doc_classifier",
            decision="租赁合同",
            reasoning="包含'租赁'、'承租方'、'出租方'等关键词，置信度 95%",
            confidence=0.95
        )


class RuleValidator:
    """规则验证专家"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        return AgentResponse(
            agent_id="rule_validator",
            decision="验证通过",
            reasoning="文档包含必要的签名字段和日期字段",
            confidence=0.85
        )


class CostAnalyst:
    """成本分析师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        return AgentResponse(
            agent_id="cost_analyst",
            decision="预计成本 $0.05",
            reasoning="单页文档，PaddleOCR-VL API 调用费用约 $0.05",
            confidence=0.8
        )


class RiskAssessor:
    """风险评估师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        return AgentResponse(
            agent_id="risk_assessor",
            decision="低风险",
            reasoning="标准文档类型，无特殊风险",
            confidence=0.85
        )


class PerformanceEngineer:
    """性能工程师"""
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        return AgentResponse(
            agent_id="performance_engineer",
            decision="预计耗时 3 秒",
            reasoning="单页文档，OCR 识别 + 分类约 3 秒",
            confidence=0.9
        )


# ============================================================
# 辩论引擎
# ============================================================

class DebateEngine:
    """辩论引擎"""
    
    def __init__(self):
        self.agents = [
            OCRSpecialist(),
            DocClassifier(),
            RuleValidator(),
            CostAnalyst(),
            RiskAssessor(),
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
    
    def __init__(self):
        self.budget_threshold = 10.0  # 预算阈值（美元）
        self.risk_threshold = "高"     # 风险阈值
    
    async def evaluate(self, responses: List[AgentResponse]) -> Dict[str, Any]:
        """评估辩论结果"""
        print(f"\n{'='*60}")
        print("决策者评估")
        print(f"{'='*60}")
        
        # 提取各维度评估
        ocr_decision = next(r for r in responses if r.agent_id == "ocr_specialist")
        classifier_decision = next(r for r in responses if r.agent_id == "doc_classifier")
        cost_decision = next(r for r in responses if r.agent_id == "cost_analyst")
        risk_decision = next(r for r in responses if r.agent_id == "risk_assessor")
        
        # 成本检查
        cost_value = float(cost_decision.decision.split("$")[1])
        if cost_value > self.budget_threshold:
            print(f"❌ 成本超预算: ${cost_value} > ${self.budget_threshold}")
            return {"approved": False, "reason": "成本超预算"}
        
        # 风险检查
        if risk_decision.decision == self.risk_threshold:
            print(f"❌ 风险过高: {risk_decision.decision}")
            return {"approved": False, "reason": "风险过高"}
        
        # 置信度检查
        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        if avg_confidence < 0.8:
            print(f"❌ 平均置信度过低: {avg_confidence:.2f} < 0.80")
            return {"approved": False, "reason": "置信度过低"}
        
        # 审批通过
        print(f"✅ 审批通过")
        print(f"   OCR 引擎: {ocr_decision.decision}")
        print(f"   文档类型: {classifier_decision.decision}")
        print(f"   预计成本: {cost_decision.decision}")
        print(f"   风险等级: {risk_decision.decision}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        
        return {
            "approved": True,
            "ocr_engine": ocr_decision.decision,
            "document_type": classifier_decision.decision,
            "cost": cost_decision.decision,
            "risk": risk_decision.decision,
            "confidence": avg_confidence,
        }


# ============================================================
# 主流程
# ============================================================

async def main():
    """主流程演示"""
    print("=" * 60)
    print("Multi-Agent Document Processing System — Demo")
    print("=" * 60)
    
    # 模拟文档输入
    document = {
        "filename": "租赁合同.pdf",
        "pages": 1,
        "content": "租赁合同内容...",
    }
    
    print(f"\n输入文档: {document['filename']}")
    print(f"页数: {document['pages']}")
    
    # 初始化组件
    debate_engine = DebateEngine()
    decision_maker = DecisionMaker()
    
    # 阶段1：方向辩论
    print("\n" + "=" * 60)
    print("阶段1：方向辩论")
    print("=" * 60)
    
    responses = await debate_engine.run_debate(
        topic="文档处理方案选择",
        context={"document": document}
    )
    
    # 阶段2：决策评估
    print("\n" + "=" * 60)
    print("阶段2：决策评估")
    print("=" * 60)
    
    decision = await decision_maker.evaluate(responses)
    
    # 阶段3：执行（如果审批通过）
    if decision["approved"]:
        print(f"\n{'='*60}")
        print("阶段3：执行")
        print(f"{'='*60}")
        print(f"\n开始处理文档...")
        print(f"  - OCR 引擎: {decision['ocr_engine']}")
        print(f"  - 文档类型: {decision['document_type']}")
        print(f"  - 预计成本: {decision['cost']}")
        print(f"  - 预计耗时: 3 秒")
        print(f"\n✅ 文档处理完成!")
    else:
        print(f"\n❌ 审批未通过: {decision['reason']}")
    
    # 输出决策日志
    print(f"\n{'='*60}")
    print("决策日志")
    print(f"{'='*60}")
    print(f"文档: {document['filename']}")
    print(f"审批: {'通过' if decision['approved'] else '未通过'}")
    if decision['approved']:
        print(f"结果:")
        print(f"  - OCR 引擎: {decision['ocr_engine']}")
        print(f"  - 文档类型: {decision['document_type']}")
        print(f"  - 预计成本: {decision['cost']}")
        print(f"  - 风险等级: {decision['risk']}")
        print(f"  - 置信度: {decision['confidence']:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
