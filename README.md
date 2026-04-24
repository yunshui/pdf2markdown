# PDF转Markdown工具

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

一个使用大语言模型（默认Qwen3.5-Plus）将PDF文档转换为Markdown格式的Python工具。

## ✨ 特性

- 📄 **单页/多页支持** - 自动识别并处理单页或多页PDF
- 🔄 **智能重试** - 网络错误自动重试，确保转换成功
- 📝 **完整日志** - 按天记录详细日志，包含执行上下文
- ⚙️ **灵活配置** - 支持JSON配置文件和命令行参数
- 🎯 **格式保持** - 尽量保持原PDF的格式和结构
- 🔍 **页面摘要** - 多页PDF自动生成中文页面摘要
- 🚀 **简单易用** - 一条命令完成转换

## 📦 安装

### 前置要求

- Python 3.10+
- pip

### 安装步骤

```bash
# 克隆仓库
git clone <repository-url>
cd pdf2markdown

# 安装依赖
pip install -r requirements.txt
```

## 🚀 快速开始

### 1. 配置API

编辑 `conf/setting.json`，配置你的API信息：

```json
{
  "model": {
    "name": "qwen3.5-plus",
    "api_url": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
    "api_key": "your-api-key-here",
    "timeout": 60
  },
  "conversion": {
    "max_retries": 3,
    "single_page_prompt": "请将这张图片中的内容转换为Markdown格式，保持原有的格式和结构。",
    "multi_page_summary_prompt": "请总结这张图片中的关键信息，用简短的中文描述。"
  },
  "paths": {
    "output_dir": "output",
    "logs_dir": "logs"
  }
}
```

### 2. 转换PDF

```bash
# 基本用法
python3 pdf2md.py document.pdf

# 验证API连接
python3 pdf2md.py document.pdf --validate-api

# 自定义重试次数
python3 pdf2md.py document.pdf --max-retries 5

# 指定输出目录
python3 pdf2md.py document.pdf --output-dir ./markdown_output
```

## 📖 使用说明

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `pdf_path` | PDF文件路径（必填） | - |
| `--config, -c` | 配置文件路径 | conf/setting.json |
| `--model` | 模型名称 | 配置文件中的值 |
| `--api-url` | API端点URL | 配置文件中的值 |
| `--api-key` | API密钥 | 配置文件中的值 |
| `--timeout` | 请求超时时间（秒） | 120 |
| `--max-retries` | 最大重试次数 | 3 |
| `--single-page-prompt` | 单页转换提示词 | 配置文件中的值 |
| `--multi-page-summary-prompt` | 多页摘要提示词 | 配置文件中的值 |
| `--output-dir` | 输出目录 | output |
| `--logs-dir` | 日志目录 | logs |
| `--validate-api` | 验证API连接 | false |
| `--resume` | 从上次中断处恢复 | false |
| `--reset-state` | 重置状态重新开始 | false |
| `--show-progress` | 显示当前进度（不执行转换） | false |
| `-v, --verbose` | 详细输出 | false |
| `--version` | 显示版本信息 | - |
| `--help` | 显示帮助信息 | - |

### 新增功能

#### 进度显示
- 实时控制台进度条显示
- 每页处理时间统计
- 剩余时间预估
- 平均每页耗时显示

#### 断点续传
- 支持中断后恢复（Ctrl+C）
- 自动保存处理状态
- 跳过已完成的页面
- 重新处理失败的页面

#### 容错机制
- 单页失败不影响整体转换
- 生成失败页面占位符
- 失败页面错误记录
- 转换完成后生成失败报告

### 输出格式

#### 单页PDF
```
output/
└── document.md    # 包含完整的Markdown内容
```

#### 多页PDF
```
output/
└── document_md/
    ├── document.md          # 主索引文件（含导航链接和中文摘要）
    └── pages/
        ├── page_1.md        # 第1页完整内容
        ├── page_2.md        # 第2页完整内容
        └── ...
```

### 配置说明

#### model 模型配置
- `name`: 模型名称（如 qwen3.5-plus、gpt-4-vision-preview）
- `api_url`: API端点URL（支持完整路径或基础URL）
- `api_key`: API密钥
- `timeout`: 请求超时时间（秒）

#### conversion 转换配置
- `max_retries`: 失败重试次数
- `single_page_prompt`: 单页转换提示词
- `multi_page_summary_prompt`: 多页摘要提示词

#### paths 路径配置
- `output_dir`: Markdown输出目录
- `logs_dir`: 日志文件目录

### 使用示例

#### 基本用法
```bash
# 转换PDF（会显示进度条）
python3 pdf2md.py document.pdf
```

#### 断点续传
```bash
# 转换被中断后，恢复继续
python3 pdf2md.py document.pdf --resume

# 查看当前进度（不执行转换）
python3 pdf2md.py document.pdf --show-progress

# 重置状态重新开始
python3 pdf2md.py document.pdf --reset-state
```

#### 控制台进度输出示例
```
[Processing page 5/87] Progress: 5.75% (5/87 done, 0 failed)
  Average: 45s/page | Estimated remaining: 1h 2m 15s
```

#### 处理失败的页面
如果某页转换失败，工具会：
1. 生成 `page_X_error.md` 占位符文件
2. 记录错误原因
3. 继续处理后续页面
4. 完成后生成失败报告

#### 日志时间预估
日志中会显示：
```
2026-04-24 18:00:00 - PDFToMarkdownConverter - INFO - Time estimation: Page 5/87
  | current_page: 5
  | total_pages: 87
  | average_time: 45.2
  | total_elapsed: 226.0
  | estimated_remaining: 3710.8
```

## 📚 文档

- [需求文档](docs/requirements.md) - 功能需求、非功能需求、验收标准
- [技术文档](docs/technical.md) - 技术栈、系统架构、API参考
- [设计文档](docs/design.md) - 设计原则、系统设计、接口设计
- [流程文档](docs/workflow.md) - 详细的工作流程说明
- [工作规则](docs/workflow-rules.md) - 项目工作流程和决策规则 ⭐
- [经验教训](docs/lessons-learned.md) - 开发过程中的经验和教训
- [项目进度](docs/progress.md) - 实施进度和测试结果

## 🏗️ 项目结构

```
pdf2markdown/
├── bin/                        # 可执行文件
│   └── pdf2md                  # 启动脚本
├── conf/                       # 配置文件
│   └── setting.json            # 配置文件
├── docs/                       # 文档目录
│   ├── requirements.md         # 需求文档
│   ├── technical.md            # 技术文档
│   ├── design.md               # 设计文档
│   ├── workflow.md             # 流程文档
│   ├── lessons-learned.md      # 经验教训
│   └── progress.md             # 项目进度
├── logs/                       # 日志目录（按天）
├── output/                     # 输出目录
├── src/                        # 源代码
│   ├── __init__.py
│   ├── main.py                 # CLI入口
│   ├── config.py               # 配置管理
│   ├── logger.py               # 日志系统
│   ├── pdf_processor.py        # PDF处理
│   ├── model_client.py         # 模型客户端
│   └── converter.py            # 转换逻辑
├── tests/                      # 测试代码
├── CLAUDE.md                   # Claude项目文档
├── pdf2md.py                   # 主入口脚本
├── requirements.txt            # Python依赖
├── README.md                   # 本文档
└── README_EN.md                # 英文文档
```

## 🔧 技术栈

- **Python 3.10+** - 主要编程语言
- **PyMuPDF** - PDF处理和渲染
- **Pillow** - 图片处理
- **requests** - HTTP请求
- **tqdm** - 进度显示（预留）

## 📊 性能

| 指标 | 数值 |
|------|------|
| 单页转换时间 | ~24秒 |
| 多页转换时间 | ~33秒/页 |
| 内存占用 | < 200MB |
| 图片分辨率 | 1654x2339 (200 DPI) |

## ⚠️ 注意事项

1. **API密钥安全** - 请妥善保管API密钥，不要提交到版本控制
2. **网络要求** - 需要稳定的网络连接访问API
3. **处理时间** - 大型PDF文件可能需要较长时间
4. **API费用** - API调用可能产生费用，请注意使用量
5. **日志管理** - 日志文件会持续增长，请定期清理

## 🐛 故障排除

### 问题：404错误
**原因**: API URL配置错误

**解决**:
```bash
# 检查配置文件中的api_url
cat conf/setting.json

# 验证API连接
python3 pdf2md.py test.pdf --validate-api
```

### 问题：超时
**原因**: 网络慢或文件过大

**解决**:
```bash
# 增加超时时间
python3 pdf2md.py document.pdf --timeout 120

# 降低DPI以减少图片大小（需要修改代码）
```

### 问题：转换失败
**原因**: API密钥无效或额度不足

**解决**:
```bash
# 检查API密钥配置
# 更新api_key后重试
python3 pdf2md.py document.pdf --api-key your-new-key
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 开发流程

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

### 代码规范

- 遵循PEP 8代码风格
- 添加必要的注释和文档字符串
- 编写测试用例
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF处理库
- [Qwen](https://help.aliyun.com/zh/dashscope/) - 通义千问大模型
- [OpenAI API](https://platform.openai.com/docs/api-reference) - API格式参考

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/your-repo/issues)
- 发送邮件至：your-email@example.com

## 📝 更新日志

### v1.0.0 (2026-04-24)
- ✨ 初始版本发布
- ✅ 单页PDF转换功能
- ✅ 多页PDF转换功能
- ✅ 完善的日志系统
- ✅ 灵活的配置管理
- ✅ 重试机制和超时控制

---

**Made with ❤️ by AI Assistant**