#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden 启动器 - 选择不同版本运行
Launch different versions of Echo Garden
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class EchoGardenLauncher:
    """Echo Garden 启动器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echo Garden 启动器")
        self.root.geometry("500x400")
        self.root.configure(bg='#1e2328')
        self.root.resizable(False, False)
        
        self.create_ui()
    
    def create_ui(self):
        """创建启动器界面"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="🌳 Echo Garden 启动器",
            font=('Arial', 20, 'bold'),
            fg='#e8eaed',
            bg='#1e2328'
        )
        title_label.pack(pady=(30, 20))
        
        # 副标题
        subtitle_label = tk.Label(
            self.root,
            text="选择您想要运行的版本",
            font=('Arial', 12),
            fg='#9aa0a6',
            bg='#1e2328'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # 版本按钮
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'fg': 'white',
            'relief': tk.FLAT,
            'bd': 0,
            'pady': 12,
            'width': 32
        }
        
        # 高级版按钮 (新增)
        premium_btn = tk.Button(
            self.root,
            text="🎨 高级点阵艺术版 (最新)",
            command=self.launch_premium,
            bg='#ff6b9d',
            activebackground='#f8b500',
            **button_style
        )
        premium_btn.pack(pady=8)
        
        # 美观版按钮
        beautiful_btn = tk.Button(
            self.root,
            text="✨ 美观优化版 (推荐)",
            command=self.launch_beautiful,
            bg='#7c4dff',
            activebackground='#651fff',
            **button_style
        )
        beautiful_btn.pack(pady=8)
        
        # 原版按钮
        original_btn = tk.Button(
            self.root,
            text="📱 经典原版",
            command=self.launch_original,
            bg='#4caf50',
            activebackground='#388e3c',
            **button_style
        )
        original_btn.pack(pady=8)
        
        # 实时版按钮
        realtime_btn = tk.Button(
            self.root,
            text="🎤 实时音频版",
            command=self.launch_realtime,
            bg='#ff6b35',
            activebackground='#f4511e',
            **button_style
        )
        realtime_btn.pack(pady=8)
        
        # 说明文本
        info_text = """
版本说明:
🎨 高级点阵艺术版: 基于现代设计的点阵风格 (最新)
✨ 美观优化版: 现代界面，4种精美主题
📱 经典原版: 功能完整的标准版本
🎤 实时音频版: 支持麦克风实时输入(需PyAudio)
        """
        
        info_label = tk.Label(
            self.root,
            text=info_text,
            font=('Arial', 10),
            fg='#9aa0a6',
            bg='#1e2328',
            justify=tk.LEFT
        )
        info_label.pack(pady=(30, 20))
    
    def launch_premium(self):
        """启动高级版"""
        self.launch_version("echo_garden_premium.py", "高级点阵艺术版")
    
    def launch_beautiful(self):
        """启动美观版"""
        self.launch_version("echo_garden_beautiful.py", "美观优化版")
    
    def launch_original(self):
        """启动原版"""
        self.launch_version("echo_garden.py", "经典原版")
    
    def launch_realtime(self):
        """启动实时版"""
        self.launch_version("echo_garden_realtime.py", "实时音频版")
    
    def launch_version(self, filename, version_name):
        """启动指定版本"""
        try:
            # 检查文件是否存在
            if not os.path.exists(filename):
                messagebox.showerror("错误", f"找不到文件: {filename}")
                return
            
            # 隐藏启动器窗口
            self.root.withdraw()
            
            # 启动程序
            result = subprocess.run([sys.executable, filename], 
                                  capture_output=False, 
                                  cwd=os.getcwd())
            
            # 程序结束后显示启动器
            self.root.deiconify()
            
            if result.returncode != 0:
                messagebox.showwarning("提示", f"{version_name} 已结束运行")
            
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("错误", f"启动失败: {str(e)}")
    
    def run(self):
        """运行启动器"""
        self.root.mainloop()


def main():
    """主函数"""
    launcher = EchoGardenLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
