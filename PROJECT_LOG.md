# Multi-Agent Dev Assistant 项目记录

> 项目启动日期：2026-05-21
> 项目目标：构建基于多 Agent 辩论机制的智能开发辅助系统
> GitHub：https://github.com/xiaoxiongweini37/Multi-Agent-Document

---

## 项目定位

**通用开发辅助系统**，不是特定业务系统。

- ✅ 任何项目都能用
- ✅ 任何技术栈都能用
- ✅ 换公司也能带走
- ❌ 不绑定 OCR
- ❌ 不绑定特定业务

**核心价值**：帮你想清楚怎么写代码，而不是替你写代码。

---

## 2026-05-21（项目启动）

### 今日完成

1. **项目初始化**
   - 创建本地工程目录：D:\Multi-agent-document
   - 链接远程 GitHub 仓库
   - 创建项目目录结构（agents/、debate/、constraints/、workflow/、core/、api/、tests/、examples/）

2. **文档编写**
   - README.md：项目说明、特性介绍、架构设计、技术栈
   - TASK_PLAN.md：8 阶段开发计划，预计 20 周完成
   - ARCHITECTURE.md：详细技术架构设计（分层架构、核心模块、数据模型、接口设计）
   - AGENTS.md：项目规范（编码规范、技术偏好、协作约定）
   - SOUL.md：人格约束（决策偏好、行为准则、禁止行为）
   - PROJECT_LOG.md：项目记录（本文档）

3. **基础代码**
   - requirements.txt：依赖管理
   - .gitignore：Git 忽略规则
   - examples/demo.py：基础演示代码
   - 各模块 __init__.py 文件

4. **推送到 GitHub**
   - 仓库地址：https://github.com/xiaoxiongweini37/Multi-Agent-Document

5. **定位修正**
   - 从"OCR 处理系统"修正为"开发辅助系统"
   - 确保通用性和可移植性
   - 不绑定特定业务，换公司也能用

### 技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| Agent 编排框架 | LangGraph | 用户熟悉，专为 Agent 设计，图结构匹配辩论流程 |
| Agent 框架 | LangChain | 生态完善，工具链丰富 |
| API 框架 | FastAPI | 高性能，自动文档生成 |
| 数据验证 | Pydantic | 类型安全，序列化方便 |
| 数据库 | SQLite/MySQL | 决策日志存储 |

### 架构设计要点

```
分层架构：
┌─────────────────────────────────────────┐
│  决策层（用户）                          │
│  审核辩论结果，评估可行性/成本/风险      │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  编排层（Orchestrator）                  │
│  调度辩论团队，管理工作流               │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  辩论层（6 个团队 × 8 种模式）           │
│  多视角对抗推演，产出最优方案           │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  约束层（Harness + AGENTS + SOUL）       │
│  硬约束 + 规范 + 风格                   │
└─────────────────────────────────────────┘
```

### 辩论团队设计

| 团队 | 视角 | 职责 |
|------|------|------|
| Tech Expert | 技术 | 技术选型，可行性评估 |
| Architect | 架构 | 系统设计，模块划分 |
| Cost Analyst | 成本 | 开发成本，维护成本 |
| Risk Assessor | 风险 | 技术债，安全风险 |
| Quality Engineer | 质量 | 代码规范，测试覆盖 |
| Performance Engineer | 性能 | 性能优化，扩展性 |

### 应用场景

| 场景 | 说明 |
|------|------|
| 技术选型 | A vs B，多视角对比 |
| 方案评估 | 可行性、成本、风险 |
| 代码审查 | 质量、规范、安全 |
| 架构设计 | 系统设计、模块划分 |
| 问题排查 | 根因分析、优化建议 |

### 开发计划

| 阶段 | 目标 | 预计时间 |
|------|------|----------|
| 第一阶段 | 基础框架搭建 | 1-2 周 |
| 第二阶段 | 辩论团队实现 | 2-3 周 |
| 第三阶段 | 辩论模式实现 | 2-3 周 |
| 第四阶段 | 约束系统实现 | 1-2 周 |
| 第五阶段 | 工作流编排 | 2-3 周 |
| 第六阶段 | 应用场景实现 | 2-3 周 |
| 第七阶段 | API 和 CLI | 2 周 |
| 第八阶段 | 测试和优化 | 2 周 |

### 面试亮点

1. **多 Agent 辩论架构** — 展示 AI 系统设计能力
2. **分层决策机制** — 展示工程架构思维
3. **三层约束系统** — 展示质量保障意识
4. **意图驱动设计** — 展示产品思维
5. **通用适用** — 展示抽象能力
6. **成本优化** — 展示商业意识

### 下一步计划

- [ ] 开始第一阶段：基础框架搭建
- [ ] 实现 Agent 基类
- [ ] 实现辩论引擎核心
- [ ] 实现单轮辩论流程

---

## 项目笔记

### 灵感来源

参考文章：https://zhuanlan.zhihu.com/p/2038294109237073828

核心思想：
- 多 Agent 辩论 + 分层架构
- 16 支辩论团队 × 8 种辩论模式
- 六阶工作流：从方向到交付的完整闭环
- 三层约束：Harness Engine + AGENTS.md + SOUL.md
- 意图驱动：只说"要什么"，不说"怎么做"
- 成本优化：辩论在便宜模型跑，决策者只拍板

### 关键概念

1. **辩论不是花架子** — 是降本增效的核心手段
2. **长任务反而省 token** — 上下文切割、推理成本下放、自治执行
3. **三层约束像漏斗** — 从外到内层层收窄代理的自由度
4. **意图驱动不是说人话** — 是表达粒度的控制
5. **记忆持久化需要外部审计** — Agent 缺乏元认知能力

### 定位修正记录

**2026-05-21**：从"OCR 处理系统"修正为"开发辅助系统"

原因：
- 原设计绑定 OCR 业务，换公司不能用
- 用户真正需要的是开发辅助，不是业务系统
- 通用性更重要，任何项目都能用

修正内容：
- README.md：重新定位为开发辅助系统
- TASK_PLAN.md：调整开发计划，增加应用场景阶段
- ARCHITECTURE.md：重新设计，聚焦通用开发辅助
- PROJECT_LOG.md：记录定位修正

### 待解决问题

- [ ] 如何设计辩论轮数的动态调整机制
- [ ] 如何处理辩论过程中的死锁情况
- [ ] 如何量化辩论质量
- [ ] 如何优化 token 消耗
- [ ] 如何设计通用的问题描述格式

---

*记录持续更新中...*

---

## 2026-05-21（第一阶段：基础框架实现）

### 今日完成

1. **Agent 基类实现** (`agents/base.py`)
   - AgentMessage：消息模型（id, role, content, confidence）
   - AgentResponse：响应模型（decision, reasoning, confidence）
   - DebateContext：辩论上下文模型
   - BaseAgent：抽象基类，定义 analyze/debate/vote 接口
   - SimpleAgent：简单实现，用于测试

2. **辩论团队实现** (`agents/teams.py`)
   - DebateTeam：团队类，支持 discuss/debate/vote 方法
   - 6 个预定义 Agent：TechExpert, Architect, CostAnalyst, RiskAssessor, QualityEngineer, PerformanceEngineer
   - 3 个工厂函数：create_full_team, create_tech_team, create_review_team

3. **辩论引擎实现** (`core/debate_engine.py`)
   - DebateRound：辩论轮次模型
   - DebateResult：辩论结果模型
   - DebateMode：辩论模式基类
   - AdversarialDebate：对抗辩论模式
   - JuryPanel：陪审团模式
   - DebateEngine：主引擎，管理模式和团队

4. **决策者实现** (`core/decision_maker.py`)
   - Decision：决策模型
   - DecisionMaker：评估辩论结果，检查预算/风险/置信度

5. **测试实现** (`tests/test_basic.py`)
   - 25+ 测试用例
   - 覆盖所有核心组件
   - 包含集成测试

6. **Demo 更新** (`examples/demo.py`)
   - 技术选型场景
   - 代码审查场景
   - 架构设计场景

### 技术实现要点

```
Agent 架构：
- BaseAgent（抽象基类）
  ├── analyze()：分析问题
  ├── debate()：参与辩论
  └── vote()：投票
- SimpleAgent（简单实现）
  └── 用于测试和演示

团队架构：
- DebateTeam（团队类）
  ├── discuss()：团队讨论
  ├── debate()：团队辩论
  └── vote()：团队投票
- 预定义团队
  ├── create_full_team()：6 个成员
  ├── create_tech_team()：4 个成员
  └── create_review_team()：4 个成员

辩论引擎：
- DebateEngine（主引擎）
  ├── register_mode()：注册辩论模式
  ├── register_team()：注册辩论团队
  └── run_debate()：运行辩论
- 辩论模式
  ├── AdversarialDebate：对抗辩论
  └── JuryPanel：陪审团

决策者：
- DecisionMaker（决策者）
  ├── evaluate()：评估辩论结果
  ├── _check_budget()：检查预算
  ├── _check_risks()：检查风险
  └── _check_confidence()：检查置信度
```

### 测试结果

```
运行测试：pytest tests/test_basic.py -v

测试覆盖：
- Agent 基类：6 个测试
- 辩论团队：4 个测试
- 预定义团队：3 个测试
- 辩论引擎：7 个测试
- 决策者：4 个测试
- 集成测试：1 个测试

总计：25+ 测试用例
```

### 下一步计划

- [ ] 实现更多辩论模式（risk_priority_matrix, cost_benefit_analysis 等）
- [ ] 实现约束系统（Harness Engine, AGENTS.md, SOUL.md）
- [ ] 实现工作流编排（Orchestrator）
- [ ] 实现 API 接口（FastAPI）
- [ ] 实现 CLI 工具

### 面试要点

这个实现展示了以下能力：

1. **面向对象设计**：清晰的类层次结构，抽象基类 + 具体实现
2. **异步编程**：使用 asyncio 实现并发
3. **设计模式**：工厂模式、策略模式、模板方法模式
4. **测试驱动**：完整的单元测试和集成测试
5. **类型安全**：使用 Pydantic 做数据验证
6. **模块化设计**：各模块职责清晰，便于扩展

