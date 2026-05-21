# 架构设计文档

> Multi-Agent Document Processing System 技术架构

## 1. 系统架构概述

### 1.1 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    决策层（Decision Layer）                   │
│  用户 / Hermes-Agent                                         │
│  职责：审核辩论结果，评估预算/风险，批准执行                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    编排层（Orchestration Layer）              │
│  Orchestrator                                                │
│  职责：调度辩论团队，管理六阶工作流，处理并发                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    辩论层（Debate Layer）                     │
│  6 个专业团队 × 8 种辩论模式                                 │
│  职责：从不同视角对抗推演，产出最优方案                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    执行层（Execution Layer）                  │
│  OCR 引擎 / 分类器 / 规则引擎                                │
│  职责：具体执行任务，产出结果                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    约束层（Constraint Layer）                 │
│  Harness Engine + AGENTS.md + SOUL.md                        │
│  职责：硬约束拦截 + 项目规范 + 人格约束                      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 数据流

```
用户输入文档
    ↓
文档预处理（格式转换、大小检查）
    ↓
Orchestrator 调度
    ↓
┌─────────────────────────────────────────┐
│           辩论流程                       │
│                                          │
│  方向辩论 → 方案辩论 → 投票/裁决         │
│      ↓           ↓           ↓           │
│  OCR专家    分类专家    规则专家          │
│  成本专家   风险专家    性能专家          │
└─────────────────────────────────────────┘
    ↓
决策层审核（预算/风险/可行性）
    ↓
执行层处理（OCR + 分类 + 规则验证）
    ↓
结果输出 + 决策日志
```

---

## 2. 核心模块设计

### 2.1 Agent 基类

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class AgentMessage(BaseModel):
    """Agent 消息"""
    agent_id: str
    role: str
    content: str
    confidence: float
    metadata: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    """Agent 响应"""
    agent_id: str
    decision: str
    reasoning: str
    confidence: float
    alternatives: List[str] = []
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    """Agent 基类"""
    
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
    
    @abstractmethod
    async def analyze(self, context: Dict[str, Any]) -> AgentResponse:
        """分析任务"""
        pass
    
    @abstractmethod
    async def debate(self, messages: List[AgentMessage]) -> AgentResponse:
        """参与辩论"""
        pass
    
    @abstractmethod
    async def vote(self, proposals: List[AgentResponse]) -> AgentMessage:
        """投票"""
        pass
```

### 2.2 辩论团队

```python
class DebateTeam:
    """辩论团队"""
    
    def __init__(self, team_id: str, agents: List[BaseAgent]):
        self.team_id = team_id
        self.agents = agents
    
    async def discuss(self, topic: str, context: Dict[str, Any]) -> List[AgentResponse]:
        """团队讨论"""
        responses = []
        for agent in self.agents:
            response = await agent.analyze(context)
            responses.append(response)
        return responses
    
    async def consensus(self, responses: List[AgentResponse]) -> AgentResponse:
        """达成共识"""
        # 实现共识算法
        pass

# 6 个专业团队
class OCRTeam(DebateTeam):
    """OCR 技术团队"""
    pass

class ClassifierTeam(DebateTeam):
    """文档分类团队"""
    pass

class RuleValidatorTeam(DebateTeam):
    """规则验证团队"""
    pass

class CostAnalystTeam(DebateTeam):
    """成本分析团队"""
    pass

class RiskAssessorTeam(DebateTeam):
    """风险评估团队"""
    pass

class PerformanceTeam(DebateTeam):
    """性能工程团队"""
    pass
```

### 2.3 辩论引擎

```python
class DebateEngine:
    """辩论引擎"""
    
    def __init__(self):
        self.teams: Dict[str, DebateTeam] = {}
        self.modes: Dict[str, DebateMode] = {}
    
    def register_team(self, team: DebateTeam):
        """注册辩论团队"""
        self.teams[team.team_id] = team
    
    def register_mode(self, mode: 'DebateMode'):
        """注册辩论模式"""
        self.modes[mode.mode_id] = mode
    
    async def run_debate(
        self,
        topic: str,
        mode: str,
        teams: List[str],
        context: Dict[str, Any]
    ) -> 'DebateResult':
        """运行辩论"""
        debate_mode = self.modes[mode]
        debate_teams = [self.teams[t] for t in teams]
        return await debate_mode.execute(topic, debate_teams, context)

class DebateMode(ABC):
    """辩论模式基类"""
    
    @abstractmethod
    async def execute(
        self,
        topic: str,
        teams: List[DebateTeam],
        context: Dict[str, Any]
    ) -> 'DebateResult':
        pass

class AdversarialDebate(DebateMode):
    """对抗辩论模式"""
    pass

class JuryPanel(DebateMode):
    """陪审团模式"""
    pass

class RiskPriorityMatrix(DebateMode):
    """风险优先级矩阵模式"""
    pass
```

### 2.4 约束系统

```python
class ConstraintSystem:
    """约束系统"""
    
    def __init__(self):
        self.harness = HarnessEngine()
        self.agents_spec = AgentsSpec()
        self.soul = SoulSpec()
    
    async def validate(self, action: Dict[str, Any]) -> bool:
        """验证操作是否符合约束"""
        # 1. 硬约束检查
        if not self.harness.check(action):
            return False
        
        # 2. 项目规范检查
        self.agents_spec.apply(action)
        
        # 3. 人格约束检查
        self.soul.apply(action)
        
        return True

class HarnessEngine:
    """硬约束引擎"""
    
    def __init__(self):
        self.rules: List[Callable] = []
    
    def add_rule(self, rule: Callable):
        """添加硬约束规则"""
        self.rules.append(rule)
    
    def check(self, action: Dict[str, Any]) -> bool:
        """检查是否违反硬约束"""
        for rule in self.rules:
            if not rule(action):
                return False
        return True

class AgentsSpec:
    """项目规范"""
    pass

class SoulSpec:
    """人格约束"""
    pass
```

### 2.5 工作流编排

```python
class Orchestrator:
    """六阶工作流编排器"""
    
    def __init__(self, debate_engine: DebateEngine, constraint_system: ConstraintSystem):
        self.debate_engine = debate_engine
        self.constraint_system = constraint_system
    
    async def execute_workflow(self, task: Dict[str, Any]) -> 'WorkflowResult':
        """执行六阶工作流"""
        
        # 任务1：方向辩论
        direction = await self.phase1_direction(task)
        
        # 任务2：方案辩论
        plan = await self.phase2_plan(task, direction)
        
        # 任务3：具体执行
        execution = await self.phase3_execute(task, plan)
        
        # 任务4：改进
        improvement = await self.phase4_improve(task, execution)
        
        # 任务5：全局评估
        evaluation = await self.phase5_evaluate(task, improvement)
        
        # 任务6：最终改进
        final = await self.phase6_finalize(task, evaluation)
        
        return final
    
    async def phase1_direction(self, task: Dict[str, Any]) -> 'DirectionResult':
        """阶段1：方向辩论"""
        pass
    
    async def phase2_plan(self, task: Dict[str, Any], direction: 'DirectionResult') -> 'PlanResult':
        """阶段2：方案辩论"""
        pass
    
    async def phase3_execute(self, task: Dict[str, Any], plan: 'PlanResult') -> 'ExecutionResult':
        """阶段3：具体执行"""
        pass
    
    async def phase4_improve(self, task: Dict[str, Any], execution: 'ExecutionResult') -> 'ImprovementResult':
        """阶段4：改进"""
        pass
    
    async def phase5_evaluate(self, task: Dict[str, Any], improvement: 'ImprovementResult') -> 'EvaluationResult':
        """阶段5：全局评估"""
        pass
    
    async def phase6_finalize(self, task: Dict[str, Any], evaluation: 'EvaluationResult') -> 'WorkflowResult':
        """阶段6：最终改进"""
        pass
```

---

## 3. 数据模型

### 3.1 文档模型

```python
class Document(BaseModel):
    """文档模型"""
    id: str
    filename: str
    content: bytes
    mime_type: str
    pages: int
    created_at: datetime
    metadata: Dict[str, Any] = {}

class DocumentType(BaseModel):
    """文档类型"""
    id: str
    name: str
    description: str
    keywords: List[str]
    rules: List[str]

class ClassificationResult(BaseModel):
    """分类结果"""
    document_id: str
    document_type: str
    confidence: float
    features: Dict[str, Any]
    timestamp: datetime
```

### 3.2 辩论模型

```python
class DebateTopic(BaseModel):
    """辩论主题"""
    id: str
    title: str
    description: str
    context: Dict[str, Any]
    created_at: datetime

class DebateRound(BaseModel):
    """辩论轮次"""
    id: str
    topic_id: str
    round_number: int
    responses: List[AgentResponse]
    timestamp: datetime

class DebateResult(BaseModel):
    """辩论结果"""
    topic_id: str
    mode: str
    teams: List[str]
    rounds: List[DebateRound]
    consensus: AgentResponse
    confidence: float
    metadata: Dict[str, Any]
```

### 3.3 决策日志

```python
class DecisionLog(BaseModel):
    """决策日志"""
    id: str
    task_id: str
    phase: str
    debate_result: DebateResult
    decision: str
    reasoning: str
    approved_by: str
    timestamp: datetime
    metadata: Dict[str, Any]
```

---

## 4. 接口设计

### 4.1 API 接口

```python
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="Multi-Agent Document API")

@app.post("/documents/upload")
async def upload_document(file: UploadFile):
    """上传文档"""
    pass

@app.post("/debate/start")
async def start_debate(topic: str, mode: str, teams: List[str]):
    """开始辩论"""
    pass

@app.get("/debate/{debate_id}/result")
async def get_debate_result(debate_id: str):
    """获取辩论结果"""
    pass

@app.get("/decisions/logs")
async def get_decision_logs(task_id: str = None):
    """获取决策日志"""
    pass

@app.post("/workflow/execute")
async def execute_workflow(task: Dict[str, Any]):
    """执行工作流"""
    pass
```

---

## 5. 扩展性设计

### 5.1 插件机制

```python
class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
    
    def register(self, plugin: 'Plugin'):
        """注册插件"""
        self.plugins[plugin.name] = plugin
    
    def load_plugins(self, directory: str):
        """加载插件目录"""
        pass

class Plugin(ABC):
    """插件基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]):
        pass
```

### 5.2 自定义辩论团队

```python
# 用户可以自定义辩论团队
custom_team = DebateTeam(
    team_id="custom_team",
    agents=[
        CustomAgent("agent1", "技术专家"),
        CustomAgent("agent2", "业务专家"),
    ]
)

debate_engine.register_team(custom_team)
```

### 5.3 自定义辩论模式

```python
# 用户可以自定义辩论模式
class CustomDebateMode(DebateMode):
    async def execute(self, topic, teams, context):
        # 自定义辩论逻辑
        pass

debate_engine.register_mode(CustomDebateMode())
```

---

## 6. 部署架构

### 6.1 单机部署

```
┌─────────────────────────────────────────┐
│              应用服务器                   │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ FastAPI  │  │ 辩论引擎 │  │ 工作流   │ │
│  │ 接口     │  │         │  │ 编排器   │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ OCR引擎  │  │ 分类器  │  │ 规则引擎 │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                          │
│  ┌─────────┐                             │
│  │  MySQL  │                             │
│  └─────────┘                             │
└─────────────────────────────────────────┘
```

### 6.2 分布式部署

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  应用服务器1  │     │  应用服务器2  │     │  应用服务器3  │
│  (FastAPI)   │     │  (辩论引擎)  │     │  (工作流)    │
└──────────────┘     └──────────────┘     └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                      ┌──────────────┐
                      │   MySQL     │
                      │   集群      │
                      └──────────────┘
```

---

## 7. 性能优化

### 7.1 辩论并行化

- 同一轮辩论中，多个团队可以并行执行
- 使用 asyncio 实现并发
- 限制最大并发数，避免资源耗尽

### 7.2 上下文管理

- 每个辩论团队独立的上下文空间
- 避免上下文污染
- 定期清理过期上下文

### 7.3 缓存机制

- 缓存常见辩论结果
- 缓存 OCR 识别结果
- 缓存分类结果

---

## 8. 监控与日志

### 8.1 监控指标

- 辩论轮数
- 辩论时长
- Token 消耗
- 决策准确率
- 系统资源使用

### 8.2 日志系统

- 结构化日志
- 分级日志（DEBUG/INFO/WARNING/ERROR）
- 日志聚合与分析

---

## 9. 安全考虑

### 9.1 数据安全

- 文档加密存储
- 传输加密（HTTPS）
- 访问控制（RBAC）

### 9.2 操作安全

- Harness Engine 硬约束
- 操作审计日志
- 敏感操作二次确认

---

## 10. 未来扩展

### 10.1 功能扩展

- 支持更多文档类型
- 支持多语言
- 支持实时协作

### 10.2 性能扩展

- 分布式辩论引擎
- GPU 加速 OCR
- 流式处理大文档

### 10.3 生态扩展

- 插件市场
- 社区贡献
- 商业化版本
