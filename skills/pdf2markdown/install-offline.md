# Windows 离线安装指南

## 方案概述

Windows 离线安装需要三个步骤：

1. **在有网络的机器上**：下载依赖包（Windows、macOS 或 Linux 机器均可）
2. **传输文件**：将依赖包和技能文件复制到目标机器
3. **在离线环境中**：运行离线安装脚本

---

## 第一步：在有网络的机器上下载依赖包

### 1.1 在 Windows 机器上下载（推荐）

打开命令提示符（CMD），按 `Win + R`，输入 `cmd`，回车

```cmd
cd path\to\pdf2markdown
download-packages.bat
```

### 1.2 在 macOS 或 Linux 机器上下载

如果只有 macOS 或 Linux 机器，也可以下载 Windows 的依赖包：

```bash
cd path/to/pdf2markdown
pip download -r requirements.txt -d packages-windows --platform win_amd64 --only-binary :all:
```

### 1.3 验证下载

检查 `packages-windows\` 目录是否包含以下文件：
- PyMuPDF-*.whl
- Pillow-*.whl
- requests-*.whl
- tqdm-*.whl

---

## 第二步：传输文件到离线环境

### 2.1 需要传输的内容

将以下内容打包传输到离线机器：

```
pdf2markdown\
├── main.py
├── requirements.txt
├── install-offline.bat
├── packages-windows\         ← Windows 依赖包
│   ├── PyMuPDF-*.whl
│   ├── Pillow-*.whl
│   ├── requests-*.whl
│   └── tqdm-*.whl
└── src\                      ← 所有源代码文件
```

### 2.2 传输方式

- U盘/移动硬盘
- 局域网共享
- 文件传输工具（如飞秋、局域网传输助手）

---

## 第三步：在离线环境中安装

### 3.1 解压/复制文件

将传输的文件放置到目标目录，例如：`C:\pdf2markdown\`

### 3.2 打开命令提示符

按 `Win + R`，输入 `cmd`，回车

### 3.3 进入技能目录

```cmd
cd C:\pdf2markdown
```

### 3.4 运行离线安装脚本

```cmd
install-offline.bat
```

脚本会自动检测 `packages-windows` 目录并使用其中的包进行安装。

### 3.5 验证安装

```cmd
python test.py
```

如果测试通过，说明安装成功。

---

## 使用技能

### 4.1 设置 API 密钥

```cmd
set PDF2MD_API_KEY=your-api-key-here
```

### 4.2 运行转换

```cmd
python main.py document.pdf
```

或者直接使用命令行参数：

```cmd
python main.py document.pdf --api-key your-api-key
```

---

## 常见问题

### 问题1：下载脚本失败

**原因**：网络连接问题或 pip 未配置

**解决**：
```cmd
# 手动升级 pip
python -m pip install --upgrade pip

# 再次运行下载脚本
download-packages.bat
```

### 问题2：离线安装失败

**原因**：缺少某些依赖包

**解决**：
```cmd
# 尝试混合安装（部分在线）
pip install --find-links=packages -r requirements.txt
```

### 问题3：某些包无法离线安装

**原因**：部分 C 扩展包需要编译环境

**解决**：
```cmd
# 在线安装失败的包
pip install package-name

# 或者安装编译工具
# 1. 安装 Visual C++ Build Tools
# 2. 或使用预编译 wheel 文件
```

### 问题4：找不到 Python

**原因**：Python 未安装或未添加到 PATH

**解决**：
1. 安装 Python 3.10+: https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 重启命令提示符

---

## 完整示例

### 在线机器（下载）

```cmd
C:\Users\User> cd Desktop\skill\pdf2markdown

C:\Users\User\Desktop\skill\pdf2markdown> download-packages.bat

==================================
PDF to Markdown - 下载离线包
==================================

检测系统平台...
✓ 平台: win_amd64

下载依赖包到 packages\ 目录...
...
[成功] 下载完成!
```

### 离线机器（安装）

```cmd
C:\> cd pdf2markdown

C:\pdf2markdown> install-offline.bat

==================================
PDF to Markdown - 离线安装
==================================

检查 Python...
[OK] Python 版本: 3.10.0
[OK] 找到 packages 目录

正在离线安装依赖...
...
[OK] 依赖安装成功

==================================
[成功] 离线安装完成!
==================================
```

### 运行转换

```cmd
C:\pdf2markdown> set PDF2MD_API_KEY=sk-xxxxx

C:\pdf2markdown> python main.py document.pdf

✓ Conversion successful!
  Output: output\document_md
```

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `install.bat` | 在线安装脚本 |
| `download-packages.bat` | 下载依赖包脚本 |
| `install-offline.bat` | 离线安装脚本 |
| `packages\` | 依赖包目录（下载后生成） |
| `requirements.txt` | 依赖清单 |

---

## 注意事项

1. **Python 版本**：确保安装 Python 3.10 或更高版本
2. **网络环境**：下载脚本需要网络连接
3. **磁盘空间**：确保有足够空间存储依赖包（约 50MB）
4. **权限**：可能需要管理员权限安装包
5. **路径**：避免使用包含中文或空格的路径