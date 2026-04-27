@echo off
REM PDF to Markdown Converter Skill - Windows 安装脚本

echo ==================================
echo PDF to Markdown Converter Skill
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

REM 检查 pip
echo 检查 pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 pip
    pause
    exit /b 1
)
echo [OK] pip 已安装

REM 安装依赖
echo.
echo 安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [OK] 依赖安装成功

REM 验证安装
echo.
echo 验证安装...
python -c "import fitz, requests, PIL, tqdm" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 某些依赖未正确安装
    pause
    exit /b 1
)

echo [OK] 所有依赖已验证

echo.
echo ==================================
echo [成功] 安装完成!
echo ==================================
echo.
echo 使用方法:
echo   python main.py document.pdf --api-key YOUR_API_KEY
echo.
echo 或设置环境变量:
echo   set PDF2MD_API_KEY=your-api-key
echo   python main.py document.pdf
echo.
echo 运行测试:
echo   python test.py
echo.
pause