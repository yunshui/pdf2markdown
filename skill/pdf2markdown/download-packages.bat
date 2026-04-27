@echo off
REM 下载离线安装包脚本 - Windows

setlocal enabledelayedexpansion

echo ==================================
echo PDF to Markdown - 下载离线包
echo ==================================
echo.

REM 创建packages目录
if not exist packages-windows mkdir packages-windows

echo 正在下载 Windows 依赖包到 packages-windows\ 目录...
echo.

REM 下载所有包（包含wheel和源码）
pip download -r requirements.txt -d packages-windows --only-binary :all:

if %errorlevel% neq 0 (
    echo [错误] 下载失败
    pause
    exit /b 1
)

echo.
echo ==================================
echo [成功] 下载完成!
echo ==================================
echo.
echo packages-windows\ 目录内容:
dir /B packages-windows
echo.

echo ==================================
echo 使用方法
echo ==================================
echo.
echo 在线环境（本机）:
echo   1. 已完成下载
echo   2. 将以下目录复制到离线环境:
echo      - pdf2markdown\ (整个文件夹)
echo      - packages-windows\ (依赖包文件夹)
echo.
echo 离线环境（目标机器）:
echo   1. 将 pdf2markdown\ 文件夹复制到目标机器
echo   2. 运行离线安装:
echo      pip install --no-index --find-links=packages-windows -r requirements.txt
echo.
echo 或者使用离线安装脚本:
echo   install-offline.bat
echo.
pause