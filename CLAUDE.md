# PDF转Markdown工具 - Claude项目文档

一个使用大语言模型（默认Qwen3.5-Plus）将PDF内容转换为Markdown格式的Python工具。

## 📋 项目概览

| 属性 | 信息 |
|------|------|
| 项目名称 | PDF to Markdown Converter |
| 版本 | 1.0.0 |
| 状态 | ✅ 生产就绪 |
| 最后更新 | 2026-04-29 |
| 许可证 | MIT |

## 🎯 核心功能

- 📄 单页/多页PDF支持
- 🔄 智能重试机制
- 📝 完整日志记录
- ⚙️ 灵活配置管理
- 🎯 格式保持
- 🔍 页面摘要生成
- 💾 断点续传
- 🚀 Windows离线安装支持
- 🔧 OpenClaw技能集成

## 📚 文档导航

### 用户文档

- [中文README](README.md) - 项目介绍和快速开始
- [英文README](README_EN.md) - English documentation

### 详细文档

| 文档 | 描述 | 章节数 |
|------|------|--------|
| [需求文档](docs/requirements.md) | 功能需求、非功能需求、接口需求、验收标准 | 9 |
| [技术文档](docs/technical.md) | 技术栈、系统架构、数据流、API参考 | 10 |
| [设计文档](docs/design.md) | 设计原则、系统设计、接口设计 | 13 |
| [流程文档](docs/workflow.md) | 详细的工作流程说明 | 10 |
| [工作规则](docs/workflow-rules.md) | 项目工作流程和决策规则 | 7 |
| [经验教训](docs/lessons-learned.md) | 开发经验和改进建议 | 13 |
| [项目进度](docs/progress.md) | 实施进度和测试结果 | 9 |

## 🏗️ 项目结构

```
pdf2markdown/
├── conf/                       # 配置文件
│   └── setting.json            # 配置文件
├── docs/                       # 详细文档目录
│   ├── requirements.md         # 需求文档
│   ├── technical.md            # 技术文档
│   ├── design.md               # 设计文档
│   ├── workflow.md             # 流程文档
│   ├── lessons-learned.md      # 经验教训
│   └── progress.md             # 项目进度
├── skills/                     # OpenClaw技能目录
│   └── pdf2markdown/           # PDF转Markdown技能
│       ├── conf/               # 技能配置
│       ├── packages-windows/   # Windows离线依赖包
│       ├── pdf2md.py           # 技能入口
│       ├── src/                # 技能源代码
│       └── install-offline.bat # Windows离线安装脚本
├── logs/                       # 日志目录（按天）
├── output/                     # 输出目录
├── src/                        # 源代码
│   ├── __init__.py
│   ├── main.py                 # CLI入口
│   ├── config.py               # 配置管理
│   ├── logger.py               # 日志系统
│   ├── pdf_processor.py        # PDF处理
│   ├── model_client.py         # 模型客户端
│   ├── converter.py            # 转换逻辑
│   └── state_manager.py        # 状态管理
├── tests/                      # 测试代码
├── CLAUDE.md                   # 本文档
├── pdf2md.py                   # 主入口脚本
├── requirements.txt            # Python依赖
├── README.md                   # 中文说明
└── README_EN.md                # 英文说明
```

## 🔧 技术栈

- **Python 3.10+** - 主要编程语言
- **PyMuPDF** - PDF处理和渲染
- **Pillow** - 图片处理
- **requests** - HTTP请求
- **tqdm** - 进度显示（预留）

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 单页转换时间 | ~24秒 |
| 多页转换时间 | ~33秒/页 |
| 内存占用 | < 200MB |
| 图片分辨率 | 1654x2339 (200 DPI) |
| API成功率 | 100% (测试期间) |

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd pdf2markdown

# 安装依赖
pip install -r requirements.txt
```

### 配置

编辑 `conf/setting.json` 配置API信息。

### 使用

```bash
# 基本用法
python3 pdf2md.py document.pdf

# 验证API
python3 pdf2md.py document.pdf --validate-api

# 更多选项
python3 pdf2md.py document.pdf --max-retries 5 --output-dir ./output
```

## 📖 核心模块说明

### src/config.py
配置加载和管理，支持JSON文件和命令行参数覆盖。

### src/logger.py
日志系统，按天记录，包含执行上下文。

### src/pdf_processor.py
PDF处理，使用PyMuPDF将页面转换为图片。

### src/model_client.py
LLM API客户端，支持重试和超时控制。

### src/converter.py
转换主逻辑，处理单页和多页PDF。

### src/main.py
命令行接口，参数解析和用户交互。

## ⚙️ 配置说明

### model 模型配置
- `name`: 模型名称
- `api_url`: API端点URL
- `api_key`: API密钥
- `timeout`: 超时时间（秒）

### conversion 转换配置
- `max_retries`: 重试次数
- `single_page_prompt`: 单页提示词
- `multi_page_summary_prompt`: 多页摘要提示词

### paths 路径配置
- `output_dir`: 输出目录
- `logs_dir`: 日志目录

## 🎨 输出格式

### 单页PDF
```
output/
└── document.md
```

### 多页PDF
```
output/
└── document_md/
    ├── document.md          # 主索引文件
    └── pages/
        ├── page_1.md
        ├── page_2.md
        └── ...
```

## 📝 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `pdf_path` | PDF文件路径（必填） | - |
| `--config, -c` | 配置文件路径 | conf/setting.json |
| `--model` | 模型名称 | 配置值 |
| `--api-url` | API端点URL | 配置值 |
| `--api-key` | API密钥 | 配置值 |
| `--timeout` | 超时时间（秒） | 配置值 |
| `--max-retries` | 重试次数 | 配置值 |
| `--output-dir` | 输出目录 | output |
| `--logs-dir` | 日志目录 | logs |
| `--validate-api` | 验证API | false |
| `-v, --verbose` | 详细输出 | false |
| `--version` | 显示版本 | - |
| `--help` | 显示帮助 | - |

## 🧪 测试

### 功能测试

```bash
# 创建测试PDF
python3 -c "from fpdf import FPDF; pdf = FPDF(); pdf.add_page(); pdf.set_font('Arial', 'B', 16); pdf.cell(40, 10, 'Hello World'); pdf.output('test.pdf')"

# 运行转换
python3 pdf2md.py test.pdf
```

### 集成测试

```bash
# 验证所有组件
python3 << 'EOF'
from src.config import Config
from src.logger import get_logger
from src.pdf_processor import PDFProcessor
from src.model_client import ModelClient
from src.converter import PDFToMarkdownConverter

config = Config()
logger = get_logger("test")
processor = PDFProcessor()
client = ModelClient(...)
converter = PDFToMarkdownConverter(config)
EOF
```

## ⚠️ 注意事项

1. **API密钥安全** - 妥善保管，不要提交到版本控制
2. **网络要求** - 需要稳定的网络连接
3. **处理时间** - 大型PDF文件耗时较长
4. **API费用** - 注意使用量和费用
5. **日志管理** - 定期清理日志文件

## 🐛 故障排除

### 常见问题

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 404错误 | API URL错误 | 检查配置文件 |
| 超时 | 网络慢/文件大 | 增加timeout |
| 转换失败 | API密钥无效 | 更新api_key |
| 无限重试 | 配置错误 | 检查max_retries |

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 开发流程

1. Fork仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启Pull Request

### 代码规范

- 遵循PEP 8
- 添加注释和文档字符串
- 编写测试
- 更新文档

## 📄 许可证

MIT License

## 🙏 致谢

- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Qwen](https://help.aliyun.com/zh/dashscope/)
- [OpenAI API](https://platform.openai.com/docs/api-reference)

## 📞 联系方式

- Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Email: your-email@example.com

## 🔌 OpenClaw 技能

项目包含完整的 OpenClaw 技能，可在 Windows 环境中离线使用。

### 技能位置

```
skills/pdf2markdown/
├── pdf2md.py                   # 技能入口
├── conf/setting.json           # 配置文件
├── install-offline.bat         # Windows离线安装脚本
├── install-offline.md          # 离线安装文档
├── packages-windows/           # Windows依赖包
└── src/                        # 源代码
```

### 在线安装

```bash
# 进入技能目录
cd skills/pdf2markdown

# 设置API密钥
export PDF2MD_API_KEY="your-api-key"

# 运行转换
python pdf2md.py document.pdf
```

### Windows 离线安装

```cmd
# 进入技能目录
cd skills\pdf2markdown

# 运行离线安装
install-offline.bat

# 使用技能
python pdf2md.py document.pdf --api-key YOUR_API_KEY
```

详细信息请参考 `skills/pdf2markdown/install-offline.md`

## 📝 更新日志

### v1.0.0 (2026-04-24)
- ✨ 初始版本发布
- ✅ 单页/多页PDF转换
- ✅ 完善的日志系统
- ✅ 重试机制和超时控制
- ✅ 完整的文档体系

### v1.0.1 (2026-04-29)
- 🚀 添加 OpenClaw 技能支持
- 🔧 添加 Windows 离线安装功能
- 💾 添加断点续传功能
- 📦 包含 Windows 离线依赖包
- 📄 更新项目文档

---

**本文档由 [Claude Code](https://claude.com/claude-code) 维护**