#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden Beautiful UI - 简洁美观版
A simplified but beautiful version of Echo Garden with modern interface

Features:
- Clean modern interface design
- Beautiful color themes
- Smooth animations
- Enhanced user experience
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import math
import time
import threading
from collections import deque

# 尝试导入音频库
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  PyAudio not installed, using simulated audio mode")


class BeautifulTheme:
    """美观主题类"""
    
    AURORA = {
        'name': '极光梦境',
        'bg': '#0f1419',
        'canvas_bg': '#1e2328', 
        'panel_bg': '#252a31',
        'accent': '#3e4651',
        'highlight': '#7c4dff',
        'text': '#e8eaed',
        'secondary_text': '#9aa0a6',
        'trunk': ['#4a5568', '#2d3748', '#1a202c'],
        'leaves': ['#7c4dff', '#651fff', '#3f51b5', '#2196f3', '#00bcd4', '#4caf50', '#8bc34a', '#cddc39']
    }
    
    FOREST = {
        'name': '翡翠森林',
        'bg': '#0d1b0f',
        'canvas_bg': '#1a2c1e',
        'panel_bg': '#243329',
        'accent': '#2e5233',
        'highlight': '#4caf50',
        'text': '#e8f5e8',
        'secondary_text': '#81c784',
        'trunk': ['#3e2723', '#5d4037', '#795548'],
        'leaves': ['#4caf50', '#66bb6a', '#81c784', '#a5d6a7', '#2e7d32', '#388e3c']
    }
    
    SUNSET = {
        'name': '暖阳晚霞',
        'bg': '#2c1810',
        'canvas_bg': '#3d2317',
        'panel_bg': '#4a2c1a',
        'accent': '#68401f',
        'highlight': '#ff6b35',
        'text': '#fff8f3',
        'secondary_text': '#ffcc8a',
        'trunk': ['#5d4037', '#8d6e63', '#a1887f'],
        'leaves': ['#ff6b35', '#ff8a65', '#ffab91', '#ffcc8a', '#ff5722', '#f4511e']
    }
    
    OCEAN = {
        'name': '深海蓝调',
        'bg': '#0c1821',
        'canvas_bg': '#1b2631',
        'panel_bg': '#2a3441',
        'accent': '#34495e',
        'highlight': '#3498db',
        'text': '#ecf0f1',
        'secondary_text': '#85c1e9',
        'trunk': ['#2c3e50', '#34495e', '#5d6d7e'],
        'leaves': ['#3498db', '#5dade2', '#85c1e9', '#aed6f1', '#2980b9', '#1f618d']
    }


class ModernFrame(tk.Frame):
    """现代化框架组件"""
    
    def __init__(self, parent, bg_color='#1e2328', **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)


class SimpleWaveform(tk.Canvas):
    """简化波形显示"""
    
    def __init__(self, parent, width=200, height=350, theme=None, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=theme['canvas_bg'] if theme else '#1e2328',
                        highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.theme = theme
        
    def update_display(self, waveform_data, features):
        """更新显示"""
        self.delete("all")
        
        # 绘制边框
        self.create_rectangle(2, 2, self.width-2, self.height-2,
                            outline=self.theme['accent'], width=2, fill='')
        
        # 绘制中心线
        center_y = self.height // 2
        self.create_line(10, center_y, self.width-10, center_y,
                        fill=self.theme['accent'], width=1)
        
        # 绘制波形
        if waveform_data and len(waveform_data) > 1:
            points = []
            for i, value in enumerate(waveform_data[:80]):
                x = 10 + i * ((self.width - 20) / 80)
                y = center_y - (value * (self.height - 60) * 0.4)
                points.extend([x, y])
            
            if len(points) >= 4:
                self.create_line(points, fill=self.theme['highlight'], 
                               width=2, smooth=True)
        
        # 显示音频信息
        if features:
            volume = features.get('volume', 0)
            pitch = features.get('pitch', 0)
            energy = features.get('energy', 0)
            
            y_start = self.height - 80
            
            # 音量条
            vol_width = volume * (self.width - 40)
            self.create_rectangle(20, y_start, 20 + vol_width, y_start + 15,
                                fill=self.theme['highlight'], outline='')
            self.create_text(self.width//2, y_start + 7, text=f'音量: {volume:.2f}',
                           fill=self.theme['text'], font=('Arial', 9))
            
            # 音调条
            pitch_width = pitch * (self.width - 40)
            self.create_rectangle(20, y_start + 25, 20 + pitch_width, y_start + 40,
                                fill=self.theme['leaves'][2], outline='')
            self.create_text(self.width//2, y_start + 32, text=f'音调: {pitch:.2f}',
                           fill=self.theme['text'], font=('Arial', 9))
            
            # 能量条
            energy_width = energy * (self.width - 40)
            self.create_rectangle(20, y_start + 50, 20 + energy_width, y_start + 65,
                                fill=self.theme['leaves'][4], outline='')
            self.create_text(self.width//2, y_start + 57, text=f'能量: {energy:.2f}',
                           fill=self.theme['text'], font=('Arial', 9))


class BeautifulTree:
    """美观树木类"""
    
    STYLES = ['classic', 'weeping', 'bushy', 'tall', 'spiral']
    
    def __init__(self, x, y, theme, audio_features=None, style=None):
        self.x = x
        self.y = y
        self.theme = theme
        self.audio_features = audio_features or self._random_features()
        self.style = style or random.choice(self.STYLES)
        
        # 根据音频特征设置属性
        self.height = 60 + self.audio_features['volume'] * 120
        self.trunk_width = 6 + self.audio_features['volume'] * 10
        self.branches = int(3 + self.audio_features['energy'] * 6)
        self.sway_speed = 0.5 + self.audio_features['pitch'] * 2
        
        self.growth = 0.0
        self.is_growing = True
        self.sway_phase = random.random() * math.pi * 2
        
    def _random_features(self):
        return {
            'volume': random.uniform(0.3, 0.8),
            'pitch': random.uniform(0.2, 0.8),
            'energy': random.uniform(0.3, 0.7)
        }
    
    def update(self, dt):
        """更新树木状态"""
        if self.is_growing:
            self.growth = min(1.0, self.growth + 0.02 * dt * 60)
            if self.growth >= 1.0:
                self.is_growing = False
        
        self.sway_phase += self.sway_speed * dt
    
    def draw(self, canvas):
        """绘制树木"""
        if self.growth <= 0:
            return
        
        # 计算摇摆
        sway_x = math.sin(self.sway_phase) * 8 * self.audio_features['volume']
        
        # 绘制树干
        trunk_height = self.height * 0.4 * self.growth
        trunk_color = random.choice(self.theme['trunk'])
        
        canvas.create_line(
            self.x, self.y,
            self.x + sway_x, self.y - trunk_height,
            width=int(self.trunk_width * self.growth),
            fill=trunk_color,
            capstyle=tk.ROUND
        )
        
        # 绘制树枝
        if self.growth > 0.3:
            self._draw_branches(canvas, self.x + sway_x, self.y - trunk_height)
    
    def _draw_branches(self, canvas, start_x, start_y):
        """绘制树枝系统"""
        branch_height = self.height * 0.6 * (self.growth - 0.3) / 0.7
        
        for i in range(self.branches):
            angle = -120 + (240 / max(1, self.branches - 1)) * i
            length = branch_height * random.uniform(0.6, 1.0)
            
            self._draw_single_branch(canvas, start_x, start_y, angle, length, 0)
    
    def _draw_single_branch(self, canvas, x, y, angle, length, depth):
        """递归绘制单个分支"""
        if depth > 3 or length < 12:
            # 绘制叶子
            self._draw_leaves(canvas, x, y)
            return
        
        # 计算分支端点
        rad = math.radians(angle)
        end_x = x + length * math.cos(rad)
        end_y = y + length * math.sin(rad)
        
        # 绘制分支
        branch_color = random.choice(self.theme['trunk'])
        width = max(1, 5 - depth)
        
        canvas.create_line(x, y, end_x, end_y, 
                         width=width, fill=branch_color, capstyle=tk.ROUND)
        
        # 递归绘制子分支
        if depth < 3:
            for i in range(2):
                new_angle = angle + random.uniform(-35, 35)
                new_length = length * random.uniform(0.6, 0.8)
                self._draw_single_branch(canvas, end_x, end_y, new_angle, new_length, depth + 1)
    
    def _draw_leaves(self, canvas, x, y):
        """绘制叶子"""
        leaf_count = random.randint(4, 10)
        
        for _ in range(leaf_count):
            offset_x = random.uniform(-15, 15)
            offset_y = random.uniform(-15, 15)
            
            leaf_x = x + offset_x
            leaf_y = y + offset_y
            size = random.uniform(3, 7)
            
            color = random.choice(self.theme['leaves'])
            
            # 不同的叶子形状
            shape = random.choice(['oval', 'triangle'])
            
            if shape == 'oval':
                canvas.create_oval(leaf_x - size, leaf_y - size,
                                 leaf_x + size, leaf_y + size,
                                 fill=color, outline='')
            else:  # triangle
                points = [
                    leaf_x, leaf_y - size,
                    leaf_x - size, leaf_y + size,
                    leaf_x + size, leaf_y + size
                ]
                canvas.create_polygon(points, fill=color, outline='')


class SimpleAudioProcessor:
    """简化音频处理器"""
    
    def __init__(self):
        self.sim_time = 0
        self.is_recording = False
        
    def get_current_features(self):
        self.sim_time += 0.1
        return {
            'volume': 0.5 + 0.3 * math.sin(self.sim_time),
            'pitch': 0.4 + 0.4 * math.sin(self.sim_time * 0.7),
            'energy': 0.3 + 0.4 * math.sin(self.sim_time * 1.3)
        }
    
    def get_waveform_data(self):
        return [math.sin(i * 0.2 + self.sim_time) * (0.5 + 0.5 * math.sin(self.sim_time * 0.3)) 
               for i in range(100)]
    
    def start_recording(self):
        self.is_recording = True
        return True
    
    def stop_recording(self):
        self.is_recording = False


class EchoGardenBeautiful:
    """Echo Garden 美观版主程序"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echo Garden Beautiful - 美观交互艺术")
        self.root.geometry("1300x800")
        
        # 主题系统
        self.themes = [BeautifulTheme.AURORA, BeautifulTheme.FOREST, 
                      BeautifulTheme.SUNSET, BeautifulTheme.OCEAN]
        self.current_theme_index = 0
        self.current_theme = self.themes[self.current_theme_index]
        
        # 设置根窗口背景
        self.root.configure(bg=self.current_theme['bg'])
        
        # 音频处理器
        self.audio_processor = SimpleAudioProcessor()
        
        # 树木列表
        self.trees = []
        
        # 音频状态
        self.is_live_mode = False
        self.last_audio_features = None
        
        # 创建界面
        self.create_beautiful_ui()
        self.bind_events()
        
        # 动画循环
        self.last_time = time.time()
        self.animate()
        
        # 显示欢迎信息
        self.show_welcome()
    
    def create_beautiful_ui(self):
        """创建美观界面"""
        # 顶部标题栏
        self.create_header()
        
        # 主内容区域
        main_frame = ModernFrame(self.root, self.current_theme['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧控制面板
        left_panel = self.create_control_panel(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # 右侧画布区域
        canvas_frame = ModernFrame(main_frame, self.current_theme['panel_bg'])
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 主画布
        self.canvas = tk.Canvas(
            canvas_frame,
            bg=self.current_theme['canvas_bg'],
            width=900,
            height=550,
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # 底部状态栏
        self.create_status_bar()
    
    def create_header(self):
        """创建标题栏"""
        header = ModernFrame(self.root, self.current_theme['bg'])
        header.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # 主标题
        title_label = tk.Label(
            header,
            text="🌳 Echo Garden Beautiful",
            font=('Arial', 28, 'bold'),
            fg=self.current_theme['text'],
            bg=self.current_theme['bg']
        )
        title_label.pack(side=tk.LEFT, pady=10)
        
        # 主题信息
        self.theme_label = tk.Label(
            header,
            text=f"主题: {self.current_theme['name']}",
            font=('Arial', 14),
            fg=self.current_theme['secondary_text'],
            bg=self.current_theme['bg']
        )
        self.theme_label.pack(side=tk.RIGHT, pady=10)
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        panel = ModernFrame(parent, self.current_theme['panel_bg'])
        panel.configure(width=300)
        panel.pack_propagate(False)
        
        # 面板标题
        title = tk.Label(
            panel,
            text="🎵 音频控制",
            font=('Arial', 16, 'bold'),
            fg=self.current_theme['text'],
            bg=self.current_theme['panel_bg']
        )
        title.pack(pady=(20, 10))
        
        # 波形显示
        self.waveform = SimpleWaveform(panel, theme=self.current_theme)
        self.waveform.pack(pady=10)
        
        # 控制按钮区域
        button_frame = ModernFrame(panel, self.current_theme['panel_bg'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # 按钮样式
        button_style = {
            'font': ('Arial', 11, 'bold'),
            'fg': 'white',
            'bg': self.current_theme['highlight'],
            'activebackground': self.current_theme['accent'],
            'relief': tk.FLAT,
            'bd': 0,
            'pady': 8
        }
        
        # 控制按钮
        self.live_button = tk.Button(
            button_frame,
            text="🎤 开启实时模式",
            command=self.toggle_live_mode,
            **button_style
        )
        self.live_button.pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="🎵 声音种树",
            command=self.sound_plant,
            **button_style
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="🌱 随机种树",
            command=self.random_plant,
            **button_style
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="🎨 切换主题",
            command=self.switch_theme,
            bg=self.current_theme['accent'],
            activebackground=self.current_theme['highlight'],
            **{k: v for k, v in button_style.items() if k not in ['bg', 'activebackground']}
        ).pack(fill=tk.X, pady=5)
        
        return panel
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = ModernFrame(self.root, self.current_theme['bg'])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="状态: 就绪 - 点击画布种植树木",
            font=('Arial', 12),
            fg=self.current_theme['secondary_text'],
            bg=self.current_theme['bg']
        )
        self.status_label.pack(side=tk.LEFT, pady=5)
        
        # 操作提示
        help_label = tk.Label(
            status_frame,
            text="快捷键: 1-4切换主题 | C清空 | S保存 | Space声音种树",
            font=('Arial', 10),
            fg=self.current_theme['accent'],
            bg=self.current_theme['bg']
        )
        help_label.pack(side=tk.RIGHT, pady=5)
    
    def bind_events(self):
        """绑定事件"""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
    
    def on_canvas_click(self, event):
        """画布点击事件"""
        features = self.last_audio_features if self.is_live_mode else None
        self.plant_tree_at(event.x, event.y, features)
    
    def on_key_press(self, event):
        """键盘事件"""
        key = event.keysym.lower()
        
        if key in ['1', '2', '3', '4']:
            theme_index = int(key) - 1
            if theme_index < len(self.themes):
                self.current_theme_index = theme_index
                self.current_theme = self.themes[theme_index]
                self.update_theme()
        elif key == 'c':
            self.clear_garden()
        elif key == 's':
            self.save_artwork()
        elif key == 'space':
            self.sound_plant()
    
    def toggle_live_mode(self):
        """切换实时模式"""
        if self.is_live_mode:
            self.is_live_mode = False
            self.live_button.config(text="🎤 开启实时模式")
            self.status_label.config(text="状态: 实时模式已关闭")
        else:
            self.is_live_mode = True
            self.live_button.config(text="🔴 关闭实时模式")
            self.status_label.config(text="状态: 实时模式已开启")
    
    def plant_tree_at(self, x, y, audio_features=None):
        """在指定位置种植树木"""
        if y < 50:
            y = 50
        
        tree = BeautifulTree(x, y, self.current_theme, audio_features)
        self.trees.append(tree)
        
        self.status_label.config(text=f"状态: 新树已种植 ({len(self.trees)} 棵树)")
    
    def sound_plant(self):
        """声音种植"""
        sound_input = simpledialog.askstring(
            "声音描述",
            "请输入描述声音的文字:\n(例如: 高亢激昂、轻柔如水、节奏强劲等)",
            parent=self.root
        )
        
        if sound_input:
            features = self.analyze_sound_text(sound_input)
            x = random.randint(50, 850)
            y = random.randint(200, 500)
            self.plant_tree_at(x, y, features)
            
            self.status_label.config(text=f"状态: 声音树已种植 - '{sound_input}'")
    
    def analyze_sound_text(self, text):
        """分析声音文本"""
        text = text.lower()
        features = {'volume': 0.5, 'pitch': 0.5, 'energy': 0.5}
        
        # 音量关键词
        if any(word in text for word in ['大声', '响亮', '高亢', '激昂']):
            features['volume'] = random.uniform(0.7, 0.9)
        elif any(word in text for word in ['轻', '柔', '小', '微']):
            features['volume'] = random.uniform(0.2, 0.4)
        
        # 音调关键词
        if any(word in text for word in ['高', '尖', '细', '清脆']):
            features['pitch'] = random.uniform(0.7, 0.9)
        elif any(word in text for word in ['低', '沉', '厚', '浑厚']):
            features['pitch'] = random.uniform(0.1, 0.3)
        
        # 能量关键词
        if any(word in text for word in ['强劲', '有力', '活跃', '快']):
            features['energy'] = random.uniform(0.7, 0.9)
        elif any(word in text for word in ['平静', '慢', '稳', '如水']):
            features['energy'] = random.uniform(0.2, 0.4)
        
        return features
    
    def random_plant(self):
        """随机种植"""
        x = random.randint(50, 850)
        y = random.randint(200, 500)
        self.plant_tree_at(x, y)
    
    def switch_theme(self):
        """切换主题"""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme = self.themes[self.current_theme_index]
        self.update_theme()
    
    def update_theme(self):
        """更新主题"""
        # 更新窗口背景
        self.root.configure(bg=self.current_theme['bg'])
        self.canvas.configure(bg=self.current_theme['canvas_bg'])
        
        # 更新标签
        self.theme_label.config(text=f"主题: {self.current_theme['name']}")
        
        # 更新树木主题
        for tree in self.trees:
            tree.theme = self.current_theme
        
        self.status_label.config(text=f"状态: 已切换到 {self.current_theme['name']} 主题")
    
    def clear_garden(self):
        """清空花园"""
        self.trees.clear()
        self.canvas.delete("all")
        self.status_label.config(text="状态: 花园已清空")
    
    def save_artwork(self):
        """保存作品"""
        if not self.trees:
            messagebox.showwarning("提示", "没有树木可以保存！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("EPS files", "*.eps"), ("All files", "*.*")],
            title="保存 Echo Garden 作品"
        )
        
        if filename:
            try:
                self.canvas.postscript(file=filename)
                self.status_label.config(text=f"状态: 作品已保存到 {filename}")
                messagebox.showinfo("成功", f"作品已保存！\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def animate(self):
        """动画循环"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # 获取音频数据
        self.last_audio_features = self.audio_processor.get_current_features()
        waveform_data = self.audio_processor.get_waveform_data()
        
        # 更新波形显示
        self.waveform.update_display(waveform_data, self.last_audio_features)
        
        # 更新树木
        for tree in self.trees:
            tree.update(dt)
        
        # 重绘场景
        self.redraw()
        
        # 继续动画
        self.root.after(50, self.animate)
    
    def redraw(self):
        """重绘场景"""
        self.canvas.delete("all")
        
        # 绘制背景装饰
        self.draw_background_decoration()
        
        # 绘制所有树木
        for tree in self.trees:
            tree.draw(self.canvas)
    
    def draw_background_decoration(self):
        """绘制背景装饰"""
        canvas_width = max(900, self.canvas.winfo_width() or 900)
        canvas_height = max(550, self.canvas.winfo_height() or 550)
        
        # 确保尺寸有效
        if canvas_width < 50 or canvas_height < 50:
            return
        
        # 根据主题绘制不同装饰
        if self.current_theme['name'] == '极光梦境':
            # 绘制星星
            for _ in range(20):
                x = random.randint(20, canvas_width - 20)
                y = random.randint(20, canvas_height // 2)
                size = random.randint(1, 2)
                
                self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                      fill='white', outline='')
        
        elif self.current_theme['name'] == '深海蓝调':
            # 绘制波浪线
            for i in range(3):
                y = canvas_height - 80 - i * 30
                if y > 20:  # 确保y坐标有效
                    points = []
                    for x in range(0, canvas_width, 20):
                        wave_y = y + math.sin(x * 0.02 + time.time()) * 8
                        points.extend([x, wave_y])
                    
                    if len(points) >= 4:
                        self.canvas.create_line(points, fill=self.current_theme['accent'],
                                              width=2, smooth=True)
    
    def show_welcome(self):
        """显示欢迎信息"""
        welcome = f"""
🌟 欢迎使用 Echo Garden Beautiful！

✨ 本版本特色：
• 简洁优雅的现代界面设计  
• 4种精美主题配色方案
• 流畅的动画效果
• 直观的操作体验

🎮 快速上手：
1. 点击画布任意位置种植树木
2. 使用"声音种树"输入文字描述
3. 按数字键1-4切换主题
4. 按C键清空，S键保存作品

🎨 当前主题: {self.current_theme['name']}

开始创作属于您的美丽声音花园！🌳✨
        """
        
        messagebox.showinfo("欢迎", welcome)
    
    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序已退出")


def main():
    """主函数"""
    print("🌳 启动 Echo Garden Beautiful - 简洁美观版 🌳")
    print("✨ 现代化界面设计，简洁而不失美观")
    
    app = EchoGardenBeautiful()
    app.run()


if __name__ == "__main__":
    main()
