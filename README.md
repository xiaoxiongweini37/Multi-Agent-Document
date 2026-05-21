# Multi-Agent Document Processing System

> 基于多 Agent 辩论机制的智能文档处理系统

## 项目简介

Multi-Agent Document（DocDebate）是一个基于多 Agent 辩论机制的智能文档处理系统，专门用于香港公司文档的 OCR 识别与分类。

系统采用分层架构设计：
- **上层决策者**（用户/Hermes）：审核辩论结果，评估预算/风险，批准执行
- **下层执行层**（多个专业 Agent）：从不同视角辩论方案，产出最优解

## 核心特性

- **多 Agent 辩论**：6 个专业团队从不同视角对抗推演
- **8 种辩论模式**：adversarial_debate、jury_panel、risk_priority_matrix 等
- **六阶工作流**：从方向到交付的完整闭环
- **三层约束**：Harness Engine（硬拦截）+ AGENTS.md（规范）+ SOUL.md（风格）
- **意图驱动**：只说"要什么"，不说"怎么做"
- **成本优化**：辩论在便宜模型跑，决策者只拍板

## 架构设计

```
用户输入文档
    ↓
┌─────────────────────────────────────────┐
│           Agent 辩论层                   │
├──────────┬──────────┬──────────┬────────┤
│ OCR专家  │ 分类专家 │ 规则专家 │ 成本专家│
│          │          │          │        │
│ "用Paddle│ "这是     │ "需要检查│ "处理100│
│ OCR-VL"  │ 租赁合同" │ 签名字段"│ 页$0.5" │
└──────────┴──────────┴──────────┴────────┘
    ↓ 辩论讨论
┌─────────────────────────────────────────┐
│           决策层（用户/Hermes）           │
│  评估：技术可行性 + 成本 + 风险 + 准确率  │
│  决策：批准/驳回/修改方案                 │
└─────────────────────────────────────────┘
    ↓ 执行
输出结果 + 决策日志
```

## 辩论团队

| 团队 | 视角 | 职责 |
|------|------|------|
| OCR Specialist | 技术 | 选择最佳 OCR 引擎，评估准确率 |
| Doc Classifier | 业务 | 文档类型识别，分类策略 |
| Rule Validator | 合规 | 业务规则验证，香港法规合规 |
| Cost Analyst | 成本 | Token/API 费用估算 |
| Risk Assessor | 风险 | 失败率、数据安全、边界情况 |
| Performance Engineer | 性能 | 处理速度、并发、资源占用 |

## 辩论模式

| 模式 | 适用场景 |
|------|----------|
| adversarial_debate | 技术选型（PaddleOCR vs MinerU） |
| jury_panel | 方案评审（多团队投票） |
| risk_priority_matrix | 风险评估（高/中/低分级） |
| cost_benefit_analysis | 成本收益分析 |
| delphi_method | 专家意见收敛 |
| six_thinking_hat | 六顶思考帽 |
| swot_analysis | 优劣势分析 |
| red_team | 红队攻击测试 |

## 六阶工作流

```
任务1（方向辩论）→ 任务2（方案辩论）→ 任务3（具体执行）
    ↓                    ↓                    ↓
任务4（改进）    → 任务5（全局评估）→ 任务6（最终改进）
```

## 目录结构

```
Multi-Agent-Document/
├── agents/                    # Agent 定义
│   ├── debate_teams/          # 辩论团队
│   └── roles/                 # 角色定义
├── debate/                    # 辩论引擎
│   ├── modes/                 # 辩论模式
│   └── templates/             # 辩论模板
├── constraints/               # 约束系统
│   ├── harness.py             # 硬约束引擎
│   ├── agents.md              # 项目规范
│   └── soul.md                # 人格约束
├── workflow/                  # 工作流编排
│   ├── orchestrator.py        # 六阶工作流
│   └── pipeline.py            # 任务流水线
├── core/                      # 核心功能
│   ├── document.py            # 文档处理
│   └── ocr_engines/           # OCR 引擎
├── api/                       # API 接口
├── tests/                     # 测试
├── docs/                      # 文档
├── examples/                  # 示例
├── README.md                  # 项目说明
├── TASK_PLAN.md               # 任务计划书
├── ARCHITECTURE.md            # 架构设计
└── requirements.txt           # 依赖
```

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/xiaoxiongweini37/Multi-Agent-Document.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行示例
python examples/demo.py
```

## 技术栈

- **Python 3.10+**
- **LangGraph** — Agent 编排
- **PaddleOCR-VL** — OCR 识别
- **Qwen2.5-VL** — 文档分类
- **MySQL** — 决策日志
- **FastAPI** — API 接口

## 应用场景

- 香港公司文档 OCR 识别
- 文档类型自动分类
- 业务规则验证
- 合规性检查
- 批量文档处理

## 面试亮点

1. **多 Agent 辩论架构** — 展示 AI 系统设计能力
2. **分层决策机制** — 展示工程架构思维
3. **三层约束系统** — 展示质量保障意识
4. **意图驱动设计** — 展示产品思维
5. **实际业务场景** — 香港文档处理，有真实价值
6. **成本优化** — 展示商业意识

## License

MIT License

## 作者

xiaoxiongweini37
