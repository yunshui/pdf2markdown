# packages-windows 目录说明

此目录包含 PDF to Markdown Converter Skill 的 Windows 依赖包，用于 Windows 离线安装。

## 下载的包（Windows AMD64）

| 包文件 | 大小 | 说明 |
|--------|------|------|
| pymupdf-*.whl | ~18MB | PDF处理库（C扩展） |
| pillow-*.whl | ~2.4MB | 图片处理库（C扩展） |
| requests-*.whl | ~63KB | HTTP请求库（纯Python） |
| tqdm-*.whl | ~77KB | 进度条库（纯Python） |
| certifi-*.whl | ~133KB | SSL证书库 |
| charset_normalizer-*.whl | ~155KB | 字符编码库 |
| idna-*.whl | ~67KB | IDNA编码库 |
| urllib3-*.whl | ~129KB | URL处理库 |

**总大小**: ~21MB

## 使用方式

### 离线安装

```cmd
pip install --no-index --find-links=packages-windows -r requirements.txt
```

或使用离线安装脚本：
```cmd
install-offline.bat
```

## 注意事项

1. **平台**: Windows x86_64 (AMD64)
2. **Python 版本**: 需要 Python 3.10+
3. **兼容性**: 这些包在 Windows 10/11 上兼容

## 安装脚本

使用 `install-offline.bat` 脚本会自动使用此目录的包进行离线安装。