# AGENTS.md — 项目规范

> 本文件定义项目的编码规范、技术偏好和协作约定。
> 所有 Agent 在执行任务时必须遵守本规范。

## 项目信息

- **项目名称**：Multi-Agent Dev Assistant
- **项目类型**：通用开发辅助系统
- **技术栈**：Python 3.10+, LangGraph, LangChain, FastAPI
- **目标用户**：开发者

## 核心定位

**通用开发辅助系统**，不是特定业务系统。

- ✅ 任何项目都能用
- ✅ 任何技术栈都能用
- ✅ 换公司也能带走
- ❌ 不绑定特定业务
- ❌ 不绑定特定技术栈

## 编码规范

### Python 代码风格

- **缩进**：4 空格
- **行宽**：88 字符（Black 默认）
- **命名**：
  - 类名：PascalCase
  - 函数名：snake_case
  - 常量：UPPER_SNAKE_CASE
  - 私有成员：_leading_underscore
- **类型注解**：所有函数必须有类型注解
- **文档字符串**：所有公共函数必须有 docstring

### 代码组织

- **模块导入顺序**：
  1. 标准库
  2. 第三方库
  3. 项目内部模块
- **文件结构**：
  - 模块级文档字符串
  - 导入语句
  - 常量定义
  - 类定义
  - 函数定义
- **最大文件行数**：500 行（超过则拆分）

### 命名约定

```python
# 好的命名
class DebateEngine:
    async def run_debate(self, topic: str) -> DebateResult:
        pass

# 不好的命名
class DE:
    async def run(self, t):
        pass
```

## 技术偏好

### Agent 编排

- **框架**：LangGraph
- **理由**：专为 Agent 设计，支持复杂工作流，图结构匹配辩论流程

### Agent 框架

- **框架**：LangChain
- **理由**：生态完善，工具链丰富，社区活跃

### API 框架

- **框架**：FastAPI
- **理由**：高性能，自动文档生成，类型安全

### 数据验证

- **框架**：Pydantic
- **理由**：类型安全，序列化方便，与 FastAPI 集成好

### 数据库

- **开发环境**：SQLite（简单，无需配置）
- **生产环境**：MySQL（稳定，功能丰富）
- **ORM**：SQLAlchemy

## 协作约定

### 辩论规则

1. **发言顺序**：按团队优先级发言
2. **发言时长**：每轮最多 500 token
3. **辩论轮数**：最多 3 轮
4. **共识机制**：多数投票 + 决策者裁决

### 代码审查

1. **审查者**：决策者（用户）
2. **审查标准**：符合本规范
3. **审查流程**：提交 → 审查 → 修改 → 合并

### 提交规范

- **提交信息格式**：`<type>(<scope>): <subject>`
- **类型**：
  - feat: 新功能
  - fix: 修复
  - docs: 文档
  - style: 格式
  - refactor: 重构
  - test: 测试
  - chore: 构建/工具

```bash
# 示例
git commit -m "feat(debate): add adversarial debate mode"
git commit -m "fix(agent): fix consensus algorithm bug"
git commit -m "docs(readme): update installation guide"
```

## 错误处理

### 异常处理

- **原则**：捕获具体异常，不捕获 Exception
- **日志**：所有异常必须记录日志
- **恢复**：提供降级方案

```python
# 好的异常处理
try:
    result = await debate_engine.run_debate(topic)
except DebateTimeoutError:
    logger.warning("Debate timeout, using default decision")
    result = default_decision
except DebateError as e:
    logger.error(f"Debate failed: {e}")
    raise

# 不好的异常处理
try:
    result = await debate_engine.run_debate(topic)
except:
    pass
```

### 降级策略

1. **辩论降级**：多团队辩论 → 单团队分析
2. **决策降级**：自动决策 → 人工审核
3. **超时降级**：长时间辩论 → 快速决策

## 测试规范

### 测试类型

- **单元测试**：pytest
- **集成测试**：pytest + testcontainers
- **端到端测试**：pytest + httpx

### 测试覆盖率

- **目标**：80% 以上
- **关键模块**：90% 以上
- **工具**：pytest-cov

### 测试命名

```python
# 好的命名
def test_debate_engine_returns_result():
    pass

def test_debate_engine_handles_timeout():
    pass

# 不好的命名
def test_debate():
    pass
```

## 性能要求

### 响应时间

- **问题解析**：< 1 秒
- **单轮辩论**：< 30 秒
- **完整工作流**：< 5 分钟

### 并发处理

- **最大并发数**：10
- **队列机制**：asyncio
- **超时设置**：30 秒（单轮），5 分钟（完整流程）

## 安全要求

### 数据安全

- **本地存储**：决策日志本地存储
- **不上传代码**：敏感代码不上传
- **数据保留**：可配置保留策略

### 操作安全

- **硬约束**：Harness Engine 拦截
- **审计日志**：所有操作记录
- **敏感操作**：二次确认

## 文档要求

### 代码文档

- **模块文档**：每个模块必须有文档字符串
- **函数文档**：所有公共函数必须有 docstring
- **类文档**：所有类必须有 docstring

### 用户文档

- **README**：项目说明、安装、使用
- **API 文档**：Swagger UI 自动生成
- **架构文档**：ARCHITECTURE.md
- **任务计划**：TASK_PLAN.md

## 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-21 | 1.0.0 | 初始版本 |
| 2026-05-21 | 1.0.1 | 修正定位为通用开发辅助系统 |
