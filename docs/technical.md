# 技术文档 (Technical Documentation)

## 1. 技术栈

### 1.1 编程语言
- **Python 3.10+**
  - 选择理由：生态丰富，易于维护，支持异步处理

### 1.2 核心依赖库

| 库名 | 版本 | 用途 | 说明 |
|------|------|------|------|
| PyMuPDF | 1.23.26 | PDF处理 | 高性能PDF解析和渲染 |
| Pillow | 10.3.0 | 图片处理 | 图像格式转换和处理 |
| requests | 2.31.0 | HTTP请求 | 简洁的HTTP客户端 |
| tqdm | 4.66.4 | 进度条 | 进度显示（已预留） |
| fpdf2 | 2.8.7 | PDF生成 | 测试用，非生产依赖 |

### 1.3 开发环境
- **操作系统**: macOS / Linux / Windows
- **Python版本**: 3.10+
- **包管理器**: pip

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                      命令行接口 (CLI)                     │
│                      src/main.py                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    配置管理层                              │
│                   src/config.py                          │
│  - 加载配置文件                                           │
│  - 命令行参数覆盖                                         │
│  - 配置验证                                              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   转换器核心层                             │
│                 src/converter.py                         │
│  - 单页/多页判断                                         │
│  - 转换流程控制                                           │
│  - 结果生成                                              │
└──────────┬──────────────────────┬────────────────────────┘
           │                      │
┌──────────▼──────────┐  ┌────────▼────────────────────────┐
│   PDF处理层          │  │     模型客户端层                  │
│  pdf_processor.py    │  │    model_client.py              │
│  - PDF验证          │  │  - API调用                     │
│  - 页面截图         │  │  - 重试机制                     │
│  - 图片处理         │  │  - 超时控制                     │
└─────────────────────┘  └────────────┬───────────────────┘
                                    │
                         ┌──────────▼─────────────────────┐
                         │        LLM API                  │
                         │  - OpenAI兼容接口               │
                         │  - 图片输入支持                  │
                         └─────────────────────────────────┘
```

### 2.2 模块职责

#### src/config.py
- **职责**: 配置加载、解析、验证、管理
- **输入**: 配置文件路径、命令行参数
- **输出**: Config对象
- **关键方法**:
  - `load_config()`: 加载配置文件
  - `update()`: 更新配置项
  - `get()`: 获取配置值

#### src/logger.py
- **职责**: 日志记录和管理
- **输入**: 日志消息、日志级别
- **输出**: 日志文件、控制台输出
- **关键方法**:
  - `info()`: 记录信息日志
  - `error()`: 记录错误日志
  - `log_page_progress()`: 记录页面进度

#### src/pdf_processor.py
- **职责**: PDF文件处理和图片转换
- **输入**: PDF文件路径
- **输出**: PIL Image对象列表
- **关键方法**:
  - `validate_pdf()`: 验证PDF文件
  - `get_page_count()`: 获取页数
  - `pdf_to_images()`: 转换为图片

#### src/model_client.py
- **职责**: LLM API调用和响应处理
- **输入**: prompt、图片列表
- **输出**: Markdown文本
- **关键方法**:
  - `call()`: 调用模型API
  - `validate_api()`: 验证API连接
  - `_prepare_request()`: 准备请求

#### src/converter.py
- **职责**: 转换流程控制
- **输入**: PDF文件路径、配置
- **输出**: Markdown文件
- **关键方法**:
  - `convert()`: 主转换入口
  - `_convert_single_page()`: 单页转换
  - `_convert_multi_page()`: 多页转换

#### src/main.py
- **职责**: 命令行接口
- **输入**: 命令行参数
- **输出**: 转换结果
- **关键方法**:
  - `parse_args()`: 解析命令行参数
  - `main()`: 主函数

---

## 3. 数据流

### 3.1 单页PDF转换流程

```
PDF文件
  ↓
PDFProcessor.validate_pdf()
  ↓ (验证通过)
PDFProcessor.pdf_to_images()
  ↓ (图片列表)
ModelClient.call()
  ↓ (Markdown内容)
Converter.save_markdown()
  ↓
输出文件: output/your_file.md
```

### 3.2 多页PDF转换流程

```
PDF文件
  ↓
PDFProcessor.validate_pdf()
  ↓ (获取页数N)
PDFProcessor.pdf_to_images()
  ↓ (N张图片)
循环处理每页:
  ├─ ModelClient.call() (完整转换)
  ├─ 保存到 pages/page_X.md
  ├─ ModelClient.call() (摘要生成)
  └─ 保存摘要信息
  ↓
创建索引文件 (包含所有页面链接和摘要)
  ↓
输出目录结构:
  output/your_file_md/
  ├── your_file.md (索引)
  └── pages/
      ├── page_1.md
      ├── page_2.md
      └── ...
```

---

## 4. 关键技术实现

### 4.1 PDF转图片

**技术方案**: 使用PyMuPDF (fitz)

```python
# 核心实现
zoom = dpi / 72.0  # DPI转换为缩放因子
mat = fitz.Matrix(zoom, zoom)  # 变换矩阵
pix = page.get_pixmap(matrix=mat)  # 渲染页面
img_bytes = pix.tobytes("png")  # 转换为PNG
img = Image.open(BytesIO(img_bytes))  # PIL Image对象
```

**优势**:
- 高性能渲染
- 支持多种PDF特性
- 可控制输出质量（DPI）

### 4.2 API调用

**技术方案**: 使用requests + OpenAI兼容接口

```python
# 请求格式
payload = {
    "model": model_name,
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }}
        ]
    }],
    "temperature": 0.7,
    "max_tokens": 4096
}
```

**特点**:
- 支持图片输入
- 兼容OpenAI格式
- 灵活的参数配置

### 4.3 重试机制

**技术方案**: 递归重试 + 指数退避

```python
def call(self, prompt, images, retry_count=0):
    try:
        # 执行请求
        response = self._make_request(payload)
        return self._extract_response_content(response)
    except Exception as e:
        if retry_count < self.max_retries:
            time.sleep(5)  # 固定5秒延迟
            return self.call(prompt, images, retry_count + 1)
        else:
            raise ValueError(f"Failed after {self.max_retries} retries")
```

**支持的错误类型**:
- Timeout: 请求超时
- ConnectionError: 连接错误
- HTTPError: HTTP错误（4xx, 5xx）
- 通用异常

### 4.4 日志系统

**技术方案**: Python标准logging模块 + 自定义Logger类

```python
# 日志格式
'%(asctime)s - %(name)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s'
```

**特性**:
- 按天滚动日志文件
- 同时输出到文件和控制台
- 自动记录调用上下文（类名、行号）
- 支持参数记录

### 4.5 配置管理

**技术方案**: JSON + 命令行覆盖

```python
# 深度合并配置
def _deep_merge(base, override):
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
```

**特点**:
- 支持嵌套配置
- 命令行参数优先级高于配置文件
- 缺失配置时使用默认值

---

## 5. 错误处理

### 5.1 异常类型

| 异常类型 | 触发场景 | 处理方式 |
|---------|---------|---------|
| FileNotFoundError | PDF文件不存在 | 退出并提示错误 |
| ValueError | PDF格式无效 | 退出并提示错误 |
| requests.Timeout | API请求超时 | 重试 |
| requests.ConnectionError | 网络连接失败 | 重试 |
| requests.HTTPError | HTTP错误 | 重试 |
| Exception | 其他异常 | 重试后抛出 |

### 5.2 错误码

| 错误码 | 含义 | HTTP状态 |
|--------|------|----------|
| 0 | 成功 | 200 |
| 1 | 文件不存在 | - |
| 2 | PDF无效 | - |
| 3 | API调用失败 | 4xx/5xx |
| 4 | 超时 | - |
| 5 | 配置错误 | - |

---

## 6. 性能优化

### 6.1 当前优化

1. **图片处理**
   - 使用内存中的BytesIO避免磁盘I/O
   - PNG格式平衡质量和大小

2. **API调用**
   - 批量请求（单次请求包含所有图片）
   - 合理的timeout设置

3. **日志系统**
   - 异步写入（由logging库处理）
   - 按天滚动避免文件过大

### 6.2 可选优化

1. **并行处理**
   - 多页PDF可并行转换
   - 使用线程池或异步I/O

2. **缓存机制**
   - 缓存已转换页面
   - 支持断点续传

3. **进度显示**
   - 使用tqdm显示进度条
   - 实时更新进度

4. **资源管理**
   - 限制并发数
   - 及时释放内存

---

## 7. 安全考虑

### 7.1 API密钥管理
- API密钥存储在配置文件中
- 不记录到日志
- 支持环境变量（可扩展）

### 7.2 输入验证
- 验证PDF文件路径
- 检查文件扩展名
- 限制文件大小（可添加）

### 7.3 网络安全
- 使用HTTPS
- 验证SSL证书
- 合理的timeout设置

---

## 8. 部署

### 8.1 本地部署

```bash
# 克隆仓库
git clone <repository-url>
cd pdf2markdown

# 安装依赖
pip install -r requirements.txt

# 配置API
vim conf/setting.json

# 运行
python3 pdf2md.py document.pdf
```

### 8.2 Docker部署（可选）

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "pdf2md.py"]
```

---

## 9. 维护指南

### 9.1 日志分析

日志位置: `logs/YYYY-MM-DD.log`

关键信息:
- API调用时间
- 错误原因
- 处理进度

### 9.2 配置更新

修改 `conf/setting.json` 后无需重启，每次运行都会重新加载。

### 9.3 依赖更新

```bash
pip install --upgrade -r requirements.txt
```

### 9.4 常见问题

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 404错误 | API URL错误 | 检查配置文件中的api_url |
| 超时 | 网络慢/文件大 | 增加timeout或减少DPI |
| 转换失败 | API密钥无效 | 更新api_key |
| 内存不足 | 图片过大 | 降低DPI |

---

## 10. API参考

### 10.1 外部API

**DashScope API**
- 基础URL: `https://coding.dashscope.aliyuncs.com/v1/chat/completions`
- 方法: POST
- 认证: Bearer Token
- 文档: https://help.aliyun.com/zh/dashscope/

### 10.2 内部API

#### Config类
```python
class Config:
    def __init__(self, config_path: Optional[str] = None)
    def update(self, **kwargs) -> None
    def get(self, key: str, default: Any = None) -> Any
```

#### PDFProcessor类
```python
class PDFProcessor:
    def __init__(self, logger_name: str = "PDFProcessor")
    def validate_pdf(self, pdf_path: str) -> bool
    def get_page_count(self, pdf_path: str) -> int
    def pdf_to_images(self, pdf_path: str, dpi: int = 200) -> List[Image.Image]
```

#### ModelClient类
```python
class ModelClient:
    def __init__(self, model_name: str, api_url: str, api_key: str,
                 timeout: int = 60, max_retries: int = 3)
    def call(self, prompt: str, images: List[Image.Image]) -> str
    def validate_api(self) -> Tuple[bool, str]
```

#### PDFToMarkdownConverter类
```python
class PDFToMarkdownConverter:
    def __init__(self, config: Config)
    def convert(self, pdf_path: str) -> Tuple[bool, str]
```