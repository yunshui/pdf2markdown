@echo off
REM 离线安装脚本 - Windows

setlocal enabledelayedexpansion

echo ==================================
echo PDF to Markdown - 离线安装
echo ==================================
echo.

REM 检查 Python
echo 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python 版本: %PYTHON_VERSION%

REM 检查 packages-windows 目录
if not exist packages-windows (
    echo [错误] 未找到 packages-windows 目录
    echo 请先运行 download-packages.bat 下载依赖包
    pause
    exit /b 1
)

echo [OK] 找到 packages-windows 目录（Windows 离线包）

REM 安装依赖
echo.
echo 正在离线安装依赖...
pip install --no-index --find-links=packages-windows -r requirements.txt

if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    echo.
    echo 尝试解决方案:
    echo 1. 检查 packages-windows 目录是否完整
    echo 2. 尝试运行: pip install --find-links=packages-windows -r requirements.txt
    echo 3. 某些包可能需要在线安装编译环境
    pause
    exit /b 1
)

echo [OK] 依赖安装成功

REM 验证安装
echo.
echo 验证安装...
python -c "import fitz, requests, PIL, tqdm" >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 某些依赖可能未正确安装，但程序仍可运行
) else (
    echo [OK] 所有依赖已验证
)

echo.
echo ==================================
echo [成功] 离线安装完成!
echo ==================================
echo.
echo 使用方法:
echo   python main.py document.pdf --api-key YOUR_API_KEY
echo.
echo 或设置环境变量:
echo   set PDF2MD_API_KEY=your-api-key
echo   python main.py document.pdf
echo.
pause