#!/bin/bash
echo "🎤 Echo Garden - 安装音频依赖"
echo "================================"

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到 macOS 系统"
    echo "正在安装 PyAudio..."
    
    # 检查是否有 Homebrew
    if command -v brew &> /dev/null; then
        echo "使用 Homebrew 安装 PortAudio..."
        brew install portaudio
    else
        echo "请先安装 Homebrew: https://brew.sh/"
        exit 1
    fi
    
    # 安装 PyAudio
    pip3 install pyaudio
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到 Linux 系统"
    echo "正在安装依赖..."
    
    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-pyaudio portaudio19-dev python3-dev
        pip3 install pyaudio
    # CentOS/RHEL
    elif command -v yum &> /dev/null; then
        sudo yum install -y portaudio-devel python3-devel
        pip3 install pyaudio
    else
        echo "请手动安装 PortAudio 开发库"
        exit 1
    fi
    
else
    echo "Windows 系统请运行 install_audio_windows.bat"
fi

echo ""
echo "✅ 安装完成！现在可以使用实时音频功能了"
echo "运行: python3 echo_garden_realtime.py"
