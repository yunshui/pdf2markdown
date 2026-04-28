---
name: pdf2markdown
description: "Convert PDF files to Markdown using LLM vision model. Supports single/multi-page, progress bar, resume, and error handling."
---

# PDF to Markdown 转换技能

将 PDF 文件转换为 Markdown 格式的 Python 工具，使用多模态 LLM（默认 Qwen3.5-Plus）识别页面内容。

## 何时使用

用户要求：
- 把 PDF 转成 Markdown
- 提取 PDF 中的文字/表格/公式
- PDF 内容转文本

## 前置检查

1. **依赖已安装**：确认 `PyMuPDF`、`Pillow`、`requests` 已安装
   ```bash
   python -c "import fitz, PIL, requests, tqdm"
   ```
2. **配置文件存在**：`~/.openclaw/skills/pdf2markdown/conf/setting.json`（包含 API key）
3. **入口脚本**：`~/.openclaw/skills/pdf2markdown/pdf2md.py`

如果配置文件不存在，从 `conf.example.json` 复制并让用户提供 API key。

## 使用方法

### 基本转换

```bash
cd ~/.openclaw/skills/pdf2markdown
python pdf2md.py <PDF文件路径>
```

### 常用参数

| 参数 | 说明 |
|------|------|
| `--validate-api` | 验证 API 连接 |
| `--max-retries N` | 最大重试次数（默认 3） |
| `--timeout N` | 请求超时秒数（默认 120） |
| `--output-dir DIR` | 自定义输出目录 |
| `--resume` | 从上次中断处恢复 |
| `--reset-state` | 重置状态重新开始 |
| `--show-progress` | 仅显示进度，不执行转换 |
| `--config FILE` | 自定义配置文件路径 |

### 示例

```bash
# 基本转换
python pdf2md.py /path/to/document.pdf

# 自定义输出目录 + 增加超时
python pdf2md.py /path/to/document.pdf --output-dir ~/Documents/markdown --timeout 180

# 验证 API 连接
python pdf2md.py test.pdf --validate-api
```

## 输出格式

**单页 PDF：**
```
output/
└── document.md
```

**多页 PDF：**
```
output/
└── document_md/
    ├── document.md          # 主索引文件（含导航链接+中文摘要）
    └── pages/
        ├── page_1.md
        ├── page_2.md
        └── ...
```

## 特性

- 📄 单页/多页自动识别
- 🔄 API 调用失败自动重试
- 📝 详细日志（`logs/` 目录，按天记录）
- 📊 实时进度条 + 剩余时间预估
- ⏸️ 支持中断恢复（Ctrl+C 后 `--resume`）
- ❌ 单页失败不影响整体转换，生成 error 占位符

## 配置说明

配置文件：`conf/setting.json`

```json
{
  "model": {
    "name": "qwen3.5-plus",
    "api_url": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
    "api_key": "your-api-key",
    "timeout": 120
  },
  "conversion": {
    "max_retries": 3,
    "single_page_prompt": "请将这张图片中的内容转换为Markdown格式...",
    "multi_page_summary_prompt": "请总结这张图片中的关键信息..."
  },
  "paths": {
    "output_dir": "output",
    "logs_dir": "logs"
  }
}
```

## 故障排查

| 问题 | 解决 |
|------|------|
| 404 错误 | 检查 `api_url` 配置 |
| 超时 | 增加 `--timeout` 或降低 DPI |
| 转换失败 | 检查 API key 是否有效 |
| 依赖缺失 | `pip install -r requirements.txt` |
