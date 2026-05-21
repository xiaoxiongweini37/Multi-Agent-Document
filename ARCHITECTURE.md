# 架构设计文档

> Multi-Agent Dev Assistant 技术架构

## 1. 系统架构概述

### 1.1 核心定位

**通用开发辅助系统**，不是特定业务系统。

- ✅ 任何项目都能用
- ✅ 任何技术栈都能用
- ✅ 换公司也能带走
- ❌ 不绑定 OCR
- ❌ 不绑定特定业务

### 1.2 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    决策层（Decision Layer）                   │
│  用户（你）                                                   │
│  职责：审核辩论结果，评估预算/风险，批准执行                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    编排层（Orchestration Layer）              │
│  Orchestrator                                                │
│  职责：调度辩论团队，管理工作流，处理并发                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    辩论层（Debate Layer）                     │
│  6 个专业团队 × 8 种辩论模式                                 │
│  职责：从不同视角对抗推演，产出最优方案                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    约束层（Constraint Layer）                 │
│  Harness Engine + AGENTS.md + SOUL.md                        │
│  职责：硬约束拦截 + 项目规范 + 人格约束                      │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 数据流

```
用户提出问题
    ↓
Orchestrator 解析意图
    ↓
┌─────────────────────────────────────────┐
│           辩论流程                       │
│                                          │
│  方向辩论 → 方案辩论 → 投票/裁决         │
│      ↓           ↓           ↓           │
│  技术专家  架构专家  成本专家            │
│  风险专家  质量专家  性能专家            │
└─────────────────────────────────────────┘
    ↓
决策层审核（可行性/成本/风险）
    ↓
输出：决策报告 + 理由 + 风险提示
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
        """分析问题"""
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
class TechExpertTeam(DebateTeam):
    """技术专家团队"""
    pass

class ArchitectTeam(DebateTeam):
    """架构专家团队"""
    pass

class CostAnalystTeam(DebateTeam):
    """成本分析团队"""
    pass

class RiskAssessorTeam(DebateTeam):
    """风险评估团队"""
    pass

class QualityEngineerTeam(DebateTeam):
    """质量工程团队"""
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
        
        # 任务3：具体建议
        suggestion = await self.phase3_suggest(task, plan)
        
        # 任务4：改进
        improvement = await self.phase4_improve(task, suggestion)
        
        # 任务5：全局评估
        evaluation = await self.phase5_evaluate(task, improvement)
        
        # 任务6：最终建议
        final = await self.phase6_finalize(task, evaluation)
        
        return final
```

---

## 3. 数据模型

### 3.1 问题模型

```python
class Question(BaseModel):
    """问题模型"""
    id: str
    type: str  # tech_selection, plan_review, code_review, architecture, debugging
    title: str
    description: str
    context: Dict[str, Any]
    constraints: List[str]
    created_at: datetime
```

### 3.2 辩论模型

```python
class DebateTopic(BaseModel):
    """辩论主题"""
    id: str
    question_id: str
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

### 3.3 决策模型

```python
class Decision(BaseModel):
    """决策模型"""
    id: str
    question_id: str
    debate_result: DebateResult
    decision: str
    reasoning: str
    risks: List[str]
    alternatives: List[str]
    confidence: float
    timestamp: datetime
```

### 3.4 决策日志

```python
class DecisionLog(BaseModel):
    """决策日志"""
    id: str
    question_id: str
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
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Multi-Agent Dev Assistant API")

@app.post("/questions/ask")
async def ask_question(question: Question):
    """提出问题"""
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
async def get_decision_logs(question_id: str = None):
    """获取决策日志"""
    pass

@app.post("/workflow/execute")
async def execute_workflow(question: Question):
    """执行工作流"""
    pass
```

### 4.2 CLI 接口

```bash
# 提出问题
dev-assistant ask "这个项目用 MongoDB 还是 PostgreSQL？"

# 开始辩论
dev-assistant debate --topic "数据库选型" --mode adversarial_debate --teams tech,cost,risk

# 获取结果
dev-assistant result <debate_id>

# 执行完整工作流
dev-assistant workflow "帮我设计一个聊天系统"
```

---

## 5. 应用场景

### 5.1 技术选型

```python
question = Question(
    type="tech_selection",
    title="数据库选型",
    description="这个项目用 MongoDB 还是 PostgreSQL？",
    context={
        "data_type": "文档型",
        "query_pattern": "复杂查询",
        "scale": "中等",
    },
    constraints=["成本 < $100/月", "必须支持 ACID"]
)
```

### 5.2 方案评估

```python
question = Question(
    type="plan_review",
    title="实时聊天功能",
    description="我想做一个实时聊天功能",
    context={
        "users": 1000,
        "concurrent": 100,
        "features": ["文字", "图片", "文件"],
    },
    constraints=["开发时间 < 2 周", "成本 < $5000"]
)
```

### 5.3 代码审查

```python
question = Question(
    type="code_review",
    title="代码审查",
    description="帮我审查这段代码",
    context={
        "code": "...",
        "language": "python",
        "purpose": "数据处理",
    },
    constraints=["符合 PEP 8", "测试覆盖 > 80%"]
)
```

### 5.4 架构设计

```python
question = Question(
    type="architecture",
    title="系统架构设计",
    description="这个系统怎么设计？",
    context={
        "requirements": ["高并发", "可扩展", "低成本"],
        "team_size": 3,
        "timeline": "3 个月",
    },
    constraints=["使用 Python", "部署在 AWS"]
)
```

### 5.5 问题排查

```python
question = Question(
    type="debugging",
    title="接口响应慢",
    description="这个接口响应很慢，怎么优化？",
    context={
        "api": "/api/users",
        "response_time": "5 秒",
        "target": "< 1 秒",
        "database": "PostgreSQL",
    },
    constraints=["不能停机", "不能改数据库结构"]
)
```

---

## 6. 扩展性设计

### 6.1 插件机制

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

### 6.2 自定义辩论团队

```python
# 用户可以自定义辩论团队
custom_team = DebateTeam(
    team_id="custom_team",
    agents=[
        CustomAgent("agent1", "领域专家"),
        CustomAgent("agent2", "业务专家"),
    ]
)

debate_engine.register_team(custom_team)
```

### 6.3 自定义辩论模式

```python
# 用户可以自定义辩论模式
class CustomDebateMode(DebateMode):
    async def execute(self, topic, teams, context):
        # 自定义辩论逻辑
        pass

debate_engine.register_mode(CustomDebateMode())
```

### 6.4 自定义应用场景

```python
# 用户可以自定义应用场景
class CustomScenario:
    """自定义场景"""
    
    def __init__(self, name: str, teams: List[str], mode: str):
        self.name = name
        self.teams = teams
        self.mode = mode
    
    async def execute(self, question: Question) -> Decision:
        # 自定义执行逻辑
        pass
```

---

## 7. 部署架构

### 7.1 本地部署（推荐）

```
┌─────────────────────────────────────────┐
│              本地环境                     │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ CLI工具  │  │ API服务  │  │ 辩论引擎 │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                          │
│  ┌─────────┐                             │
│  │  SQLite │                             │
│  └─────────┘                             │
└─────────────────────────────────────────┘
```

### 7.2 服务器部署

```
┌──────────────┐     ┌──────────────┐
│  应用服务器   │     │   数据库     │
│  (FastAPI)   │     │   (MySQL)    │
└──────────────┘     └──────────────┘
```

---

## 8. 性能优化

### 8.1 辩论并行化

- 同一轮辩论中，多个团队可以并行执行
- 使用 asyncio 实现并发
- 限制最大并发数，避免资源耗尽

### 8.2 上下文管理

- 每个辩论团队独立的上下文空间
- 避免上下文污染
- 定期清理过期上下文

### 8.3 缓存机制

- 缓存常见辩论结果
- 缓存技术选型结论
- 缓存代码审查结果

---

## 9. 安全考虑

### 9.1 数据安全

- 决策日志本地存储
- 不上传敏感代码
- 可配置数据保留策略

### 9.2 操作安全

- Harness Engine 硬约束
- 操作审计日志
- 敏感操作二次确认

---

## 10. 未来扩展

### 10.1 功能扩展

- 支持更多应用场景
- 支持多语言
- 支持团队协作

### 10.2 性能扩展

- 分布式辩论引擎
- GPU 加速推理
- 流式处理大问题

### 10.3 生态扩展

- 插件市场
- 社区贡献
- 商业化版本
