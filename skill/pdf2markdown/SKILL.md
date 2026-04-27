# PDF to Markdown Converter Skill

独立的OpenClaw技能包，用于将PDF文件转换为Markdown格式。

## 📁 目录结构

```
skill/
├── __init__.py              # Skill包初始化
├── main.py                  # 主入口文件
├── manifest.yaml            # Skill元数据配置
├── requirements.txt         # Python依赖包
├── config.example.json      # 配置示例
├── README.md                # 使用文档
├── LICENSE                  # MIT许可证
├── install.sh               # 安装脚本
├── test.py                  # 测试脚本
├── .gitignore               # Git忽略规则
└── src/                     # 源代码目录
    ├── __init__.py
    ├── config.py            # 配置管理
    ├── converter.py         # 转换逻辑
    ├── logger.py            # 日志系统
    ├── main.py              # CLI接口
    ├── model_client.py      # LLM客户端
    ├── pdf_processor.py     # PDF处理
    └── state_manager.py     # 状态管理
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skill
bash install.sh
```

或手动安装：

```bash
pip install -r requirements.txt
```

### 2. 设置API密钥

```bash
export PDF2MD_API_KEY="your-api-key-here"
```

### 3. 运行转换

```bash
python main.py document.pdf
```

## 📋 依赖包

| 包名 | 版本 | 用途 |
|------|------|------|
| PyMuPDF | 1.23.0+ | PDF处理 |
| requests | 2.31.0+ | HTTP请求 |
| Pillow | 10.0.0+ | 图片处理 |
| tqdm | 4.66.0+ | 进度显示 |

## 🔧 配置

### 环境变量

- `PDF2MD_API_URL`: LLM API端点
- `PDF2MD_API_KEY`: LLM API密钥

### 命令行参数

```bash
python main.py document.pdf [选项]

选项:
  --config PATH           配置文件路径
  --model NAME            模型名称
  --api-url URL           API URL
  --api-key KEY           API密钥
  --timeout SECONDS       超时时间
  --max-retries NUM       最大重试次数
  --output-dir DIR        输出目录
  --resume                断点续传
  --show-progress         显示进度
  --verbose               详细输出
```

## 📊 输出格式

### 单页PDF

```
output/
└── document.md
```

### 多页PDF

```
output/
└── document_md/
    ├── document.md          # 索引文件
    ├── .state.json          # 状态文件
    └── pages/
        ├── page_1.md
        ├── page_1_summary.txt
        └── ...
```

## 🧪 测试

```bash
python test.py
```

## 📝 功能特性

- ✅ 单页/多页PDF转换
- ✅ 格式保持（表格、标题、列表）
- ✅ 断点续传
- ✅ 页面摘要生成
- ✅ 进度跟踪
- ✅ 时间预估
- ✅ 错误重试
- ✅ 完整日志

## 📄 许可证

MIT License