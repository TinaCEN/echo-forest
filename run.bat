@echo off
echo 🌳 启动 Echo Garden - 交互式生成艺术 🌳
echo.
python echo_garden.py
if %errorlevel% neq 0 (
    echo.
    echo 运行出错，请检查Python是否正确安装
    pause
)
