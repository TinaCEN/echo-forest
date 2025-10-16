#!/usr/bin/env python3
# Echo Garden 启动脚本

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from echo_garden import main
    main()
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保 echo_garden.py 文件在同一目录下")
except Exception as e:
    print(f"运行错误: {e}")
    input("按回车键退出...")
