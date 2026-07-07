# AI 简历解析 CLI Demo

在招聘流程中，快速理解候选人简历并判断其与岗位的匹配程度，是一项常见但耗时的工作。本项目实现了一个命令行 CLI 工具，支持读取 PDF 简历、调用 AI 模型提取关键信息，并根据岗位描述进行匹配评分。

## 技术选型

| 领域 | 技术 | 说明 |
|------|------|------|
| 语言 | Python 3.10+ | 主开发语言 |
| CLI 框架 | Typer | 自动生成 `--help`，终端输出友好 |
| PDF 解析 | pypdf | 纯 Python 实现，轻量可靠 |
| AI 模型 | DeepSeek API | 兼容 OpenAI SDK，成本低 |
| JSON 校验 | Pydantic v2 | 声明式 schema 校验 |
| 配置管理 | python-dotenv | 从 `.env` 加载环境变量 |
| 测试 | pytest | 单元测试 + CLI 集成测试 |

## 环境变量配置

复制 `.env.example` 为 `.env` 并填写 API Key：

```bash
cp .env.example .env
```

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `DEEPSEEK_API_KEY` | 是（非 mock 模式） | — | DeepSeek API 密钥 |
| `DEEPSEEK_BASE_URL` | 否 | `https://api.deepseek.com` | API 基础地址 |
| `DEEPSEEK_MODEL` | 否 | `deepseek-chat` | 模型名称 |
| `LOG_LEVEL` | 否 | `WARNING` | 日志级别（DEBUG/INFO/WARNING） |

> 无 API Key 时可使用 `--mock` 模式完整演示所有功能。

## 安装方式

### 方式一：pip 安装（推荐）

```bash
pip install -e ".[dev]"
```

### 方式二：Makefile

```bash
make install
```

### 方式三：Docker

```bash
docker build -t resume-cli .
docker run --rm -e DEEPSEEK_API_KEY=sk-xxx resume-cli --help
```

### 生成示例 PDF

```bash
python scripts/generate_sample_pdf.py
```

## CLI 命令说明

### 全局选项

| 选项 | 说明 |
|------|------|
| `--mock` | 使用预设 mock 响应，无需 API Key |
| `--output`, `-o` | 将结果保存到指定文件 |
| `--help` | 显示帮助信息 |

### 1. parse — 简历文本解析

```bash
resume-cli parse <pdf_path> [--output result.txt]
```

读取本地 PDF 简历并提取文本内容。

### 2. extract — AI 结构化信息提取

```bash
resume-cli extract <pdf_path> [--mock] [--output result.json]
```

从简历中提取姓名、联系方式、教育背景、技能等结构化信息。

### 3. score — JD 匹配评分

```bash
resume-cli score <pdf_path> --jd <jd_path> [--mock] [--output result.json]
```

根据岗位描述文件对简历进行匹配评分。

## 示例输入和输出

### parse 示例

```bash
resume-cli parse samples/resume.pdf
```

```
Zhang San
Phone: 13800138000
Email: zhangsan@example.com
...
```

### extract 示例

```bash
resume-cli extract samples/resume.pdf --mock
```

```json
{
  "name": "张三",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "city": "北京",
  "education": [
    {
      "school": "清华大学",
      "major": "计算机科学与技术",
      "degree": "本科",
      "graduation_time": "2020-06"
    }
  ],
  "skills": ["Python", "JavaScript", "React", "FastAPI", "MySQL"]
}
```

### score 示例

```bash
resume-cli score samples/resume.pdf --jd samples/sample_jd.txt --mock
```

```json
{
  "overall_score": 82,
  "skill_score": 88,
  "experience_score": 80,
  "education_score": 75,
  "comment": "候选人具备较好的全栈开发基础，技能与岗位要求较匹配，但缺少明确的大模型应用经验。",
  "interview_questions": [
    "请介绍一个你主导过的全栈项目。",
    "你是否有调用大模型 API 的实际经验？"
  ]
}
```

## 已实现功能

### 核心功能
- [x] `parse` — PDF 文本提取，含文件不存在/非 PDF/无法读取/文本为空等错误处理
- [x] `extract` — AI 结构化信息提取，JSON 校验
- [x] `score` — JD 匹配评分（0-100），含面试问题生成
- [x] 三个命令均支持 `--help`

### 加分项
- [x] `--output` 保存结果到文件
- [x] `--mock` 模式，无 API Key 可演示
- [x] AI 返回 JSON 自动修复（markdown 包裹、尾逗号等）
- [x] 日志输出（`LOG_LEVEL` 环境变量控制）
- [x] Dockerfile + Makefile

### 测试
- [x] PDF 解析边界测试
- [x] JSON 修复与 schema 校验测试
- [x] CLI mock 模式端到端测试

```bash
make test
# 或
pytest -v
```

## 已知问题

- **扫描件 PDF**：图片型或扫描件 PDF 无法提取文本，会提示"PDF 文本为空"
- **AI 响应稳定性**：偶发格式异常已通过 `json_repair` 模块缓解，极端情况仍可能校验失败
- **复杂排版**：多栏、表格等复杂排版的 PDF 文本提取顺序可能不准确

## 项目结构

```
CLI Demo/
├── resume_cli/          # 主包
│   ├── cli.py           # CLI 入口
│   ├── pdf_parser.py    # PDF 文本提取
│   ├── ai/              # AI 调用、提示词、mock、JSON 修复
│   ├── schemas/         # Pydantic 数据模型
│   └── services/        # extract / score 业务逻辑
├── tests/               # 测试
├── samples/             # 示例文件
├── scripts/             # 工具脚本
├── Dockerfile
├── Makefile
└── README.md
```
