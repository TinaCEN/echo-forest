@echo off
echo 🎤 Echo Garden - 安装音频依赖 (Windows)
echo ==========================================

echo 正在安装 PyAudio...
pip install pyaudio

if %errorlevel% equ 0 (
    echo.
    echo ✅ 安装成功！
    echo 现在可以使用实时音频功能了
    echo 运行: python echo_garden_realtime.py
) else (
    echo.
    echo ❌ 安装失败，尝试备用方法...
    echo 下载预编译的 PyAudio wheel...
    
    echo 请访问以下网址手动下载适合您系统的 PyAudio：
    echo https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    echo.
    echo 下载后运行：pip install 下载的文件名.whl
)

pause
