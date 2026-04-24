# 设计文档 (Design Document)

## 1. 设计原则

### 1.1 核心原则
1. **单一职责**: 每个模块只负责一个明确的功能
2. **开闭原则**: 对扩展开放，对修改关闭
3. **依赖倒置**: 依赖抽象而非具体实现
4. **接口隔离**: 接口精简，职责明确

### 1.2 设计目标
- 代码可读性优先
- 模块化程度高
- 易于测试和维护
- 支持功能扩展

---

## 2. 系统设计

### 2.1 分层架构

```
┌─────────────────────────────────────────────┐
│           表现层 (Presentation)               │
│              CLI Interface                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│           业务逻辑层 (Business)                │
│              Converter                        │
└────┬──────────────────────────────┬───────────┘
     │                              │
┌────▼──────┐              ┌────────▼────────┐
│  数据处理层 │              │  服务层 (Service)│
│  PDFProc   │              │  ModelClient    │
└────────────┘              └─────────────────┘
```

### 2.2 模块设计

#### 配置模块 (config.py)
```
Config
├── DEFAULT_CONFIG: Dict[str, Any]
├── __init__(config_path: str)
├── _load_config() -> Dict
├── _save_config(config: Dict) -> None
├── _deep_merge(base, override) -> Dict
├── update(**kwargs) -> None
├── get(key: str, default: Any) -> Any
└── save() -> None
```

**设计要点**:
- 深度合并支持嵌套配置
- 默认配置保证最小可用性
- 运行时可修改和保存

#### 日志模块 (logger.py)
```
Logger
├── _loggers: Dict[str, Logger]
├── __new__(name: str, logs_dir: str) -> Logger
├── _setup_logger(name: str, logs_dir: str) -> Logger
├── _get_caller_info() -> Tuple[str, int]
├── debug(message: str, **kwargs) -> None
├── info(message: str, **kwargs) -> None
├── warning(message: str, **kwargs) -> None
├── error(message: str, exception: Exception, **kwargs) -> None
├── critical(message: str, exception: Exception, **kwargs) -> None
└── log_page_progress(current_page: int, total_pages: int, action: str) -> None
```

**设计要点**:
- 单例模式管理logger实例
- 自动获取调用上下文
- 专用方法记录页面进度

#### PDF处理模块 (pdf_processor.py)
```
PDFProcessor
├── __init__(logger_name: str)
├── validate_pdf(pdf_path: str) -> bool
├── get_page_count(pdf_path: str) -> int
├── pdf_to_images(pdf_path: str, dpi: int) -> List[Image]
└── pdf_page_to_image(pdf_path: str, page_num: int, dpi: int) -> Image
```

**设计要点**:
- 无状态设计，每次调用独立
- 支持单页和多页处理
- 统一的错误处理

#### 模型客户端模块 (model_client.py)
```
ModelClient
├── __init__(model_name, api_url, api_key, timeout, max_retries)
├── _image_to_base64(image: Image) -> str
├── _prepare_request(prompt: str, images: List[Image]) -> Dict
├── _make_request(payload: Dict) -> Response
├── _extract_response_content(response: Response) -> str
├── call(prompt: str, images: List[Image], retry_count: int) -> str
└── validate_api() -> Tuple[bool, str]
```

**设计要点**:
- 封装所有API交互细节
- 自动重试机制
- 支持多种错误类型

#### 转换器模块 (converter.py)
```
PDFToMarkdownConverter
├── __init__(config: Config)
├── convert(pdf_path: str) -> Tuple[bool, str]
├── _convert_single_page(pdf_path: str) -> Tuple[bool, str]
├── _convert_multi_page(pdf_path: str, page_count: int) -> Tuple[bool, str]
├── _create_multi_page_index(base_name: str, summaries: List) -> str
├── _get_single_page_output_path(pdf_path: str) -> str
└── _save_markdown(file_path: str, content: str) -> None
```

**设计要点**:
- 策略模式处理单页/多页
- 统一的输出接口
- 分离文件生成逻辑

---

## 3. 数据模型设计

### 3.1 配置数据结构

```json
{
  "model": {
    "name": "string",           // 模型名称
    "api_url": "string",        // API端点
    "api_key": "string",        // API密钥
    "timeout": "int"            // 超时时间(秒)
  },
  "conversion": {
    "max_retries": "int",       // 最大重试次数
    "single_page_prompt": "string",   // 单页提示词
    "multi_page_summary_prompt": "string"  // 多页摘要提示词
  },
  "paths": {
    "output_dir": "string",     // 输出目录
    "logs_dir": "string"        // 日志目录
  }
}
```

### 3.2 API请求数据结构

```json
{
  "model": "string",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "string"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
      ]
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### 3.3 输出数据结构

#### 单页输出
```
output/
└── document.md
```

#### 多页输出
```
output/
└── document_md/
    ├── document.md          # 索引文件
    └── pages/
        ├── page_1.md
        ├── page_2.md
        └── ...
```

---

## 4. 接口设计

### 4.1 公共接口

#### 命令行接口
```bash
pdf2md.py <input_pdf> [options]

Options:
  --config PATH        配置文件路径
  --model NAME         模型名称
  --api-url URL        API端点
  --api-key KEY        API密钥
  --timeout SECONDS    超时时间
  --max-retries NUM    重试次数
  --output-dir DIR     输出目录
  --validate-api       验证API
  -v, --verbose        详细输出
```

#### 编程接口
```python
from src.converter import PDFToMarkdownConverter
from src.config import Config

# 创建转换器
config = Config("path/to/config.json")
converter = PDFToMarkdownConverter(config)

# 执行转换
success, output_path = converter.convert("document.pdf")
```

### 4.2 内部接口

#### PDFProcessor
```python
# 验证PDF
is_valid: bool = processor.validate_pdf(pdf_path)

# 获取页数
count: int = processor.get_page_count(pdf_path)

# 转换图片
images: List[Image] = processor.pdf_to_images(pdf_path, dpi=200)
```

#### ModelClient
```python
# 调用模型
result: str = client.call(prompt, images)

# 验证API
is_valid: bool, message: str = client.validate_api()
```

---

## 5. 错误处理设计

### 5.1 错误层次结构

```
Exception
├── ValueError (配置错误)
├── FileNotFoundError (文件不存在)
├── requests.RequestException (网络错误)
│   ├── Timeout (超时)
│   ├── ConnectionError (连接错误)
│   └── HTTPError (HTTP错误)
└── Exception (其他错误)
```

### 5.2 错误处理策略

| 错误类型 | 处理策略 | 重试 | 日志级别 |
|---------|---------|------|---------|
| 文件不存在 | 立即失败 | ❌ | ERROR |
| PDF无效 | 立即失败 | ❌ | ERROR |
| 配置错误 | 使用默认值 | ❌ | WARNING |
| 网络超时 | 重试N次 | ✅ | WARNING |
| 连接错误 | 重试N次 | ✅ | WARNING |
| HTTP 4xx | 不重试 | ❌ | ERROR |
| HTTP 5xx | 重试N次 | ✅ | WARNING |
| 其他错误 | 重试N次 | ✅ | ERROR |

### 5.3 错误信息格式

```
[时间戳] - [类名] - [文件名:行号] - [级别] - [消息] | 参数: {...}
```

---

## 6. 日志设计

### 6.1 日志级别

| 级别 | 用途 | 示例 |
|------|------|------|
| DEBUG | 调试信息 | API请求详情、图片尺寸 |
| INFO | 正常流程 | 转换开始、页面处理 |
| WARNING | 警告信息 | 重试、配置使用默认值 |
| ERROR | 错误信息 | API调用失败、文件读取失败 |
| CRITICAL | 严重错误 | 系统级错误 |

### 6.2 日志文件组织

```
logs/
├── 2026-04-24.log
├── 2026-04-25.log
└── ...
```

**命名规则**: `YYYY-MM-DD.log`

**滚动策略**: 按天创建，不自动删除（需手动清理）

### 6.3 日志内容

#### 标准格式
```
2026-04-24 16:47:31 - PDFProcessor - [logger.py:103] - INFO - [PDFToMarkdownConverter:28] PDFProcessor initialized
```

#### 页面进度日志
```
2026-04-24 16:47:32 - PDFProcessor - [logger.py:103] - INFO - [PDFProcessor:93] Rendering PDF page 1/1 | Params: {'current_page': 1, 'total_pages': 1}
```

#### 错误日志
```
2026-04-24 16:47:34 - ModelClient - [logger.py:121] - ERROR - [PDFToMarkdownConverter:87] API returned status code 404 | Params: {'response_text': '...'}
```

---

## 7. 性能设计

### 7.1 性能指标

| 指标 | 目标值 | 实测值 |
|------|--------|--------|
| 单页转换时间 | < 60秒 | ~24秒 |
| 内存占用 | < 500MB | < 200MB |
| 日志写入延迟 | < 100ms | < 10ms |
| API重试次数 | ≤ 3次 | - |

### 7.2 性能优化点

1. **图片处理优化**
   - 使用BytesIO避免磁盘I/O
   - 合理的DPI设置（200 DPI）

2. **API调用优化**
   - 批量请求
   - 连接复用（requests Session）

3. **日志优化**
   - 异步写入
   - 按天滚动

4. **并发优化（预留）**
   - 多页并行处理
   - 线程池管理

---

## 8. 安全设计

### 8.1 敏感信息保护

1. **API密钥**
   - 存储在配置文件
   - 不记录到日志
   - 支持环境变量

2. **输入验证**
   - 文件路径验证
   - PDF格式验证
   - 参数类型检查

3. **网络安全**
   - 强制HTTPS
   - SSL证书验证
   - 合理超时设置

### 8.2 权限控制

```python
# 文件操作权限
os.makedirs(output_dir, exist_ok=True)  # 仅创建目录
with open(file_path, 'w', encoding='utf-8') as f:  # 仅写入
```

---

## 9. 扩展性设计

### 9.1 预留扩展点

1. **多模型支持**
   ```python
   # 配置中可切换不同模型
   "model": {
       "name": "qwen3.5-plus",  # 可切换为其他模型
       ...
   }
   ```

2. **自定义Prompt**
   ```python
   "conversion": {
       "single_page_prompt": "...",  # 可自定义
       "multi_page_summary_prompt": "..."
   }
   ```

3. **输出格式扩展**
   ```python
   # 预留输出格式选择
   def _save_output(self, content, format='markdown'):
       if format == 'markdown':
           ...
       elif format == 'html':
           ...
   ```

4. **并行处理**
   ```python
   # 预留并发接口
   def _convert_pages_parallel(self, images, max_workers=4):
       with ThreadPoolExecutor(max_workers) as executor:
           futures = [executor.submit(...)]
   ```

### 9.2 插件机制（设计构想）

```python
class ConverterPlugin:
    def pre_process(self, pdf_path):
        """预处理钩子"""
        pass

    def post_process(self, markdown, pdf_path):
        """后处理钩子"""
        pass

# 插件注册
converter.register_plugin(CustomPlugin())
```

---

## 10. 测试设计

### 10.1 测试策略

| 测试类型 | 覆盖范围 | 工具 |
|---------|---------|------|
| 单元测试 | 各模块函数 | pytest |
| 集成测试 | 模块间交互 | pytest |
| 功能测试 | 端到端功能 | pytest + requests-mock |
| 性能测试 | 响应时间 | pytest-benchmark |

### 10.2 测试用例示例

#### PDFProcessor测试
```python
def test_validate_pdf():
    processor = PDFProcessor()
    assert processor.validate_pdf("test_single.pdf") == True
    assert processor.validate_pdf("nonexistent.pdf") == False

def test_pdf_to_images():
    processor = PDFProcessor()
    images = processor.pdf_to_images("test_single.pdf")
    assert len(images) == 1
    assert images[0].width > 0
    assert images[0].height > 0
```

#### ModelClient测试
```python
def test_retry_mechanism():
    client = ModelClient(..., max_retries=2)
    with requests_mock.Mocker() as m:
        m.post("...", status_code=500)
        assert m.call_count == 3  # 初始 + 2次重试
```

---

## 11. 部署设计

### 11.1 文件结构设计

```
pdf2markdown/
├── bin/                    # 可执行文件
│   └── pdf2md             # 启动脚本
├── conf/                   # 配置文件
│   └── setting.json
├── docs/                   # 文档
├── lib/                    # 核心库
│   └── src/
├── logs/                   # 日志
├── output/                 # 输出
├── tests/                  # 测试
└── README.md               # 说明文档
```

### 11.2 安装设计

```python
# setup.py
from setuptools import setup

setup(
    name='pdf2markdown',
    version='1.0.0',
    packages=['src'],
    install_requires=[
        'PyMuPDF>=1.23.0',
        'requests>=2.31.0',
        'Pillow>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'pdf2md=src.main:main',
        ],
    },
)
```

---

## 12. 版本设计

### 12.1 版本号规则

`MAJOR.MINOR.PATCH`

- **MAJOR**: 重大架构变更
- **MINOR**: 新功能添加
- **PATCH**: Bug修复

### 12.2 版本规划

| 版本 | 时间 | 主要内容 |
|------|------|---------|
| 1.0.0 | 2026-04-24 | 基础功能实现 |
| 1.1.0 | 计划中 | 并行处理、进度条 |
| 1.2.0 | 计划中 | 批处理、多格式输出 |
| 2.0.0 | 计划中 | Web界面、插件系统 |

---

## 13. 设计决策记录

### 13.1 使用PyMuPDF而非pdfplumber

**决策**: 使用PyMuPDF (fitz)

**理由**:
- 性能更好
- 图片渲染质量更高
- API更简洁
- 支持更多PDF特性

### 13.2 使用requests而非aiohttp

**决策**: 使用requests同步库

**理由**:
- 使用简单
- 代码更易读
- 当前规模下性能足够
- 后续可轻松迁移到异步

### 13.3 使用JSON而非YAML配置

**决策**: 使用JSON配置

**理由**:
- Python原生支持
- 更轻量
- 减少依赖
- 标准化格式

### 13.4 递归重试而非循环

**决策**: 使用递归实现重试

**理由**:
- 代码简洁
- 状态自然传递
- 重试次数有限，无栈溢出风险