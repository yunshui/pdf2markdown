# PDF to Markdown Converter Skill - 安装指南

## 在线安装（推荐）

适用于有网络连接的环境。

### 快速安装

```bash
cd skill/pdf2markdown
./install.sh
```

### 手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行测试（可选）
python test.py

# 3. 使用
python main.py document.pdf --api-key YOUR_API_KEY
```

## 不同平台安装

### macOS

```bash
# 确保使用 Python 3.10+
python3 --version

# 安装依赖
pip3 install -r requirements.txt
```

### Linux

```bash
# 安装系统依赖（如果需要）
sudo apt-get install python3-dev libjpeg-dev zlib1g-dev

# 安装 Python 依赖
pip3 install -r requirements.txt
```

### Windows

```powershell
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py document.pdf --api-key YOUR_API_KEY
```

## 环境变量配置

```bash
# 设置 API 密钥（可选，也可以用 --api-key 参数）
export PDF2MD_API_KEY="your-api-key-here"

# 设置自定义 API URL（可选）
export PDF2MD_API_URL="https://api.example.com/v1/chat/completions"
```

## 验证安装

```bash
# 运行测试
python test.py

# 查看帮助
python main.py --help
```

## 常见问题

### Python 版本不兼容
```
Error: Python 3.10+ required
```
**解决**: 使用 Python 3.10 或更高版本

### 缺少系统库（Linux）
```
error: command 'gcc' failed
```
**解决**:
```bash
sudo apt-get install python3-dev libjpeg-dev zlib1g-dev
```

### 权限问题
```
Permission denied
```
**解决**:
```bash
pip install --user -r requirements.txt
```

## 离线安装

如果需要在离线环境中安装，请提前下载依赖：

```bash
# 在有网络的机器上
pip download -r requirements.txt -d packages

# 传输 packages 目录到离线环境
# 在离线环境中
pip install --no-index --find-links=packages -r requirements.txt
```