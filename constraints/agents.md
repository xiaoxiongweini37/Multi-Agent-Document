# AGENTS.md — 项目规范

> 本文件定义项目的编码规范、技术偏好和协作约定。
> 所有 Agent 在执行任务时必须遵守本规范。

## 项目信息

- **项目名称**：Multi-Agent Document Processing System
- **项目类型**：AI 文档处理系统
- **技术栈**：Python 3.10+, LangGraph, PaddleOCR-VL, Qwen2.5-VL
- **目标用户**：香港公司文档处理

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
class DocumentProcessor:
    def process_document(self, doc: Document) -> ProcessedDocument:
        pass

# 不好的命名
class DocProc:
    def proc(self, d):
        pass
```

## 技术偏好

### OCR 引擎

- **首选**：PaddleOCR-VL（中文识别准确率高）
- **备选**：MinerU（本地部署，无 API 费用）
- **策略**：PaddleOCR-VL 优先，失败时 fallback 到 MinerU

### LLM 模型

- **决策层**：强推理模型（GPT-4, Claude 等）
- **执行层**：便宜模型（MiniMax, Qwen 等）
- **原则**：辩论在便宜模型跑，决策者只拍板

### 数据库

- **主数据库**：MySQL（决策日志）
- **缓存**：Redis（辩论结果缓存）
- **ORM**：SQLAlchemy

### API 框架

- **框架**：FastAPI
- **文档**：Swagger UI 自动生成
- **版本控制**：URL 路径版本（/api/v1/...）

## 协作约定

### 辩论规则

1. **发言顺序**：按团队优先级发言
2. **发言时长**：每轮最多 500 token
3. **辩论轮数**：最多 3 轮
4. **共识机制**：多数投票 + 决策者裁决

### 代码审查

1. **审查者**：决策者（用户/Hermes）
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
git commit -m "feat(ocr): add PaddleOCR-VL integration"
git commit -m "fix(debate): fix consensus algorithm bug"
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
    result = ocr_engine.process(image)
except OCRTimeoutError:
    logger.warning("OCR timeout, falling back to MinerU")
    result = mineru_engine.process(image)
except OCRError as e:
    logger.error(f"OCR failed: {e}")
    raise

# 不好的异常处理
try:
    result = ocr_engine.process(image)
except:
    pass
```

### 降级策略

1. **OCR 引擎降级**：PaddleOCR-VL → MinerU
2. **辩论降级**：多团队辩论 → 单团队分析
3. **决策降级**：自动决策 → 人工审核

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
def test_document_upload_success():
    pass

def test_document_upload_invalid_format():
    pass

# 不好的命名
def test_upload():
    pass
```

## 性能要求

### 响应时间

- **文档上传**：< 1 秒
- **OCR 识别**：< 10 秒（单页）
- **辩论流程**：< 5 分钟（单轮）
- **工作流执行**：< 1 小时（完整流程）

### 并发处理

- **最大并发数**：10
- **队列机制**：Celery + Redis
- **超时设置**：30 秒（API），5 分钟（任务）

## 安全要求

### 数据安全

- **存储加密**：AES-256
- **传输加密**：HTTPS
- **访问控制**：RBAC

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
