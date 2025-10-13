#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden - 交互式生成艺术
通过实时麦克风输入生成树木艺术作品

功能:
- 鼠标点击：种下种子，生成随机树木
- 键盘 1/2/3：切换主题（暖色/冷色/单色）
- 键盘 C：清空画布
- 键盘 S：保存为 .eps 文件
- 实时音频：麦克风输入实时波形显示和树木生成
- 多样化树木：各种随机样式的树木生成
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import math
import time
import threading
from collections import deque
import struct
import sys

# 尝试导入音频库，如果失败则使用模拟音频
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  PyAudio未安装，将使用模拟音频模式")
    print("   要启用真实麦克风，请运行: pip install pyaudio")


class ColorTheme:
    """颜色主题类"""
    
    WARM = {
        'name': '暖色调',
        'trunk': ['#8B4513        # 控制按钮
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 实时音频按钮
        if AUDIO_AVAILABLE and self.audio_processor:
            self.live_button = tk.Button(
                control_frame, 
                text="🎤 开始实时", 
                command=self.toggle_live_mode,
                font=("Arial", 12),
                bg='lightgreen'
            )
            self.live_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🎵 声音种树", 
            command=self.record_and_plant,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)D', '#CD853F'],
        'leaves': ['#FF6B35', '#F7931E', '#FFD23F', '#FFA500', '#FF7F50'],
        'background': '#FFF8DC'
    }
    
    COOL = {
        'name': '冷色调',
        'trunk': ['#2F4F4F', '#708090', '#696969'],
        'leaves': ['#20B2AA', '#48D1CC', '#00CED1', '#87CEEB', '#4682B4'],
        'background': '#F0F8FF'
    }
    
    MONO = {
        'name': '单色调',
        'trunk': ['#2F2F2F', '#4F4F4F', '#6F6F6F'],
        'leaves': ['#808080', '#A0A0A0', '#C0C0C0', '#D3D3D3', '#E0E0E0'],
        'background': '#F5F5F5'
    }


class RealTimeAudioProcessor:
    """实时音频处理器"""
    
    def __init__(self):
        self.chunk = 1024
        self.format = None
        self.channels = 1
        self.rate = 44100
        self.audio = None
        self.stream = None
        self.is_recording = False
        self.audio_buffer = deque(maxlen=100)  # 保存最近100帧音频数据
        
        if AUDIO_AVAILABLE:
            try:
                self.audio = pyaudio.PyAudio()
                self.format = pyaudio.paInt16
                print("✅ 音频设备初始化成功")
            except Exception as e:
                print(f"❌ 音频初始化失败: {e}")
                self.audio = None
    
    def start_recording(self):
        """开始录音"""
        if not self.audio or self.is_recording:
            return False
        
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self._audio_callback
            )
            self.stream.start_stream()
            self.is_recording = True
            print("🎤 开始实时录音")
            return True
        except Exception as e:
            print(f"❌ 录音启动失败: {e}")
            return False
    
    def stop_recording(self):
        """停止录音"""
        if self.stream and self.is_recording:
            self.stream.stop_stream()
            self.stream.close()
            self.is_recording = False
            print("🔇 停止录音")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """音频回调函数"""
        if status:
            print(f"音频状态: {status}")
        
        # 处理音频数据
        audio_data = struct.unpack(f'{frame_count}h', in_data)
        self.audio_buffer.append(audio_data)
        
        return (in_data, pyaudio.paContinue)
    
    def get_current_features(self):
        """获取当前音频特征"""
        if not self.audio_buffer:
            return self._get_random_features()
        
        # 获取最新的音频数据
        latest_data = list(self.audio_buffer)[-1] if self.audio_buffer else []
        
        if not latest_data:
            return self._get_random_features()
        
        # 计算音量 (RMS)
        rms = math.sqrt(sum(x*x for x in latest_data) / len(latest_data))
        volume = min(rms / 3000.0, 1.0)
        
        # 计算音调特征 (简化的频率分析)
        # 使用过零率近似音调
        zero_crossings = sum(1 for i in range(1, len(latest_data)) 
                           if latest_data[i-1] * latest_data[i] < 0)
        pitch = min(zero_crossings / len(latest_data), 1.0)
        
        # 计算能量
        energy = min(sum(abs(x) for x in latest_data) / (len(latest_data) * 1000), 1.0)
        
        return {
            'volume': volume,
            'pitch': pitch, 
            'energy': energy,
            'raw_data': latest_data
        }
    
    def get_waveform_data(self):
        """获取波形显示数据"""
        if not self.audio_buffer:
            # 模拟波形数据
            return [math.sin(i * 0.1) * random.uniform(0.5, 1.0) 
                   for i in range(100)]
        
        # 返回最新音频数据的归一化版本
        latest_data = list(self.audio_buffer)[-1] if self.audio_buffer else []
        if not latest_data:
            return []
        
        # 归一化到 -1 到 1 范围
        max_val = max(abs(x) for x in latest_data) or 1
        return [x / max_val for x in latest_data]
    
    def _get_random_features(self):
        """模拟音频特征（当没有真实音频时）"""
        return {
            'volume': random.uniform(0.2, 0.8),
            'pitch': random.uniform(0.1, 0.9),
            'energy': random.uniform(0.3, 0.7),
            'raw_data': []
        }
    
    def __del__(self):
        """清理资源"""
        self.stop_recording()
        if self.audio:
            self.audio.terminate()


class SoundSimulator:
    """声音模拟器 - 用于没有麦克风时的模拟"""
    
    def __init__(self):
        self.sound_patterns = {
            '高音': {'volume': 0.8, 'pitch': 0.9, 'energy': 0.7},
            '低音': {'volume': 0.6, 'pitch': 0.2, 'energy': 0.5},
            '大声': {'volume': 0.9, 'pitch': 0.5, 'energy': 0.8},
            '轻柔': {'volume': 0.3, 'pitch': 0.4, 'energy': 0.3},
            '节奏': {'volume': 0.7, 'pitch': 0.6, 'energy': 0.9},
            '旋律': {'volume': 0.5, 'pitch': 0.8, 'energy': 0.6},
            '和谐': {'volume': 0.6, 'pitch': 0.7, 'energy': 0.5},
            '激烈': {'volume': 0.9, 'pitch': 0.8, 'energy': 0.9},
        }
    
    def analyze_text_input(self, text_input):
        """根据文本输入生成音频特征"""
        if not text_input:
            return self._get_random_features()
        
        text_input = text_input.lower()
        
        # 基于文本内容的特征
        volume = min(len(text_input) / 20.0, 1.0)
        
        # 分析文本中的特殊词汇
        features = {'volume': volume, 'pitch': 0.5, 'energy': 0.5}
        
        for keyword, pattern in self.sound_patterns.items():
            if keyword in text_input:
                features['volume'] = (features['volume'] + pattern['volume']) / 2
                features['pitch'] = (features['pitch'] + pattern['pitch']) / 2
                features['energy'] = (features['energy'] + pattern['energy']) / 2
        
        # 根据字符种类调整音调
        vowels = sum(1 for c in text_input if c in 'aeiou')
        consonants = sum(1 for c in text_input if c.isalpha() and c not in 'aeiou')
        
        if vowels + consonants > 0:
            features['pitch'] = vowels / (vowels + consonants)
        
        # 根据标点符号调整能量
        punctuation = sum(1 for c in text_input if not c.isalnum() and not c.isspace())
        features['energy'] = min(features['energy'] + punctuation / 10.0, 1.0)
        
        return features
    
    def _get_random_features(self):
        """返回随机音频特征"""
        return {
            'volume': random.uniform(0.2, 0.8),
            'pitch': random.uniform(0.1, 0.9),
            'energy': random.uniform(0.3, 0.7)
        }


class Tree:
    """多样化树木类"""
    
    # 树木样式枚举
    TREE_STYLES = ['classic', 'weeping', 'bushy', 'tall', 'wide', 'spiral', 'fractal']
    
    def __init__(self, x, y, theme, audio_features=None, style=None):
        self.x = x
        self.y = y
        self.theme = theme
        self.audio_features = audio_features or {
            'volume': random.uniform(0.3, 0.8),
            'pitch': random.uniform(0.2, 0.8),
            'energy': random.uniform(0.4, 0.7)
        }
        
        # 随机选择树木样式
        self.style = style or random.choice(self.TREE_STYLES)
        
        # 根据音频特征和样式决定树的属性
        self._init_tree_properties()
        
        self.growth = 0.0  # 成长进度 0-1
        self.is_growing = True
        self.swaying = 0.0  # 摇摆动画
    
    def _init_tree_properties(self):
        """根据音频特征和样式初始化树的属性"""
        volume = self.audio_features['volume']
        pitch = self.audio_features['pitch']
        energy = self.audio_features['energy']
        
        # 基础属性
        base_height = 80 + volume * 120
        base_branches = int(2 + energy * 8)
        base_angle = 25 + pitch * 50
        
        # 根据样式调整属性
        if self.style == 'classic':
            self.height = base_height
            self.branches = base_branches
            self.angle_variance = base_angle
            self.trunk_ratio = 0.3
            self.leaf_density = 1.0
            
        elif self.style == 'weeping':  # 垂柳样式
            self.height = base_height * 0.8
            self.branches = base_branches + 2
            self.angle_variance = base_angle * 0.5
            self.trunk_ratio = 0.4
            self.leaf_density = 1.5
            self.weeping_factor = 0.7
            
        elif self.style == 'bushy':  # 灌木样式
            self.height = base_height * 0.6
            self.branches = base_branches + 4
            self.angle_variance = base_angle * 1.5
            self.trunk_ratio = 0.2
            self.leaf_density = 2.0
            
        elif self.style == 'tall':  # 高瘦样式
            self.height = base_height * 1.4
            self.branches = max(2, base_branches - 2)
            self.angle_variance = base_angle * 0.7
            self.trunk_ratio = 0.5
            self.leaf_density = 0.7
            
        elif self.style == 'wide':  # 宽阔样式
            self.height = base_height * 0.9
            self.branches = base_branches + 3
            self.angle_variance = base_angle * 1.3
            self.trunk_ratio = 0.25
            self.leaf_density = 1.2
            
        elif self.style == 'spiral':  # 螺旋样式
            self.height = base_height * 1.1
            self.branches = base_branches
            self.angle_variance = base_angle
            self.trunk_ratio = 0.3
            self.leaf_density = 1.0
            self.spiral_factor = pitch * 360
            
        elif self.style == 'fractal':  # 分形样式
            self.height = base_height
            self.branches = max(2, int(base_branches * 0.7))
            self.angle_variance = base_angle * 0.8
            self.trunk_ratio = 0.35
            self.leaf_density = 0.8
            self.fractal_depth = int(4 + energy * 3)
        
        # 动画属性
        self.growth_speed = 0.015 + energy * 0.025
        self.sway_speed = 0.5 + pitch * 1.5
        self.sway_amplitude = volume * 5
    
    def update(self, dt, audio_features=None):
        """更新树的成长和动画"""
        # 成长动画
        if self.is_growing:
            self.growth += self.growth_speed * dt
            if self.growth >= 1.0:
                self.growth = 1.0
                self.is_growing = False
        
        # 摇摆动画
        self.swaying += self.sway_speed * dt
        
        # 如果有实时音频数据，添加响应动画
        if audio_features and not self.is_growing:
            volume = audio_features.get('volume', 0)
            self.sway_amplitude = volume * 8  # 根据音量调整摇摆幅度
    
    def draw(self, canvas):
        """绘制多样化树木"""
        if self.growth <= 0:
            return
        
        # 计算摇摆偏移
        sway_offset = math.sin(self.swaying) * self.sway_amplitude * (1 if self.is_growing else 0.3)
        
        # 绘制树干
        trunk_height = self.height * self.trunk_ratio * self.growth
        trunk_color = random.choice(self.theme['trunk'])
        trunk_width = max(1, int(12 * self.growth * (1 + self.audio_features['volume'] * 0.5)))
        
        # 根据样式调整树干绘制
        if self.style == 'spiral':
            self._draw_spiral_trunk(canvas, trunk_height, trunk_color, trunk_width, sway_offset)
        else:
            canvas.create_line(
                self.x, self.y,
                self.x + sway_offset, self.y - trunk_height,
                width=trunk_width,
                fill=trunk_color,
                capstyle=tk.ROUND
            )
        
        # 绘制树枝和叶子
        if self.growth > 0.2:
            branch_growth = (self.growth - 0.2) / 0.8
            branch_start_x = self.x + sway_offset
            branch_start_y = self.y - trunk_height
            
            if self.style == 'weeping':
                self._draw_weeping_branches(canvas, branch_start_x, branch_start_y, branch_growth)
            elif self.style == 'fractal':
                self._draw_fractal_branches(canvas, branch_start_x, branch_start_y, branch_growth)
            else:
                self._draw_standard_branches(canvas, branch_start_x, branch_start_y, branch_growth)
    
    def _draw_branches(self, canvas, x, y, angle, length, branches_left, depth):
        """递归绘制树枝"""
        if branches_left <= 0 or length < 10 or depth > 4:
            # 绘制叶子
            if length < 20:
                self._draw_leaves(canvas, x, y)
            return
        
        # 计算新位置
        rad = math.radians(angle)
        new_x = x + length * math.cos(rad)
        new_y = y + length * math.sin(rad)
        
        # 绘制当前枝干
        trunk_color = random.choice(self.theme['trunk'])
        width = max(1, int(6 - depth))
        
        canvas.create_line(
            x, y, new_x, new_y,
            width=width,
            fill=trunk_color,
            capstyle=tk.ROUND
        )
        
        # 递归绘制子分枝
        angle_var = self.angle_variance * (1 - depth * 0.2)
        new_length = length * random.uniform(0.6, 0.8)
        
        # 左分枝
        left_angle = angle - random.uniform(15, angle_var)
        self._draw_branches(
            canvas, new_x, new_y, left_angle, 
            new_length, branches_left - 1, depth + 1
        )
        
        # 右分枝
        right_angle = angle + random.uniform(15, angle_var)
        self._draw_branches(
            canvas, new_x, new_y, right_angle, 
            new_length, branches_left - 1, depth + 1
        )
    
    def _draw_spiral_trunk(self, canvas, height, color, width, sway_offset):
        """绘制螺旋树干"""
        points = []
        steps = int(height / 5)
        for i in range(steps + 1):
            progress = i / steps
            y_pos = self.y - height * progress
            spiral_angle = math.radians(self.spiral_factor * progress)
            x_offset = math.sin(spiral_angle) * 10 * progress
            points.extend([self.x + x_offset + sway_offset, y_pos])
        
        if len(points) >= 4:
            canvas.create_line(points, width=width, fill=color, smooth=True)
    
    def _draw_weeping_branches(self, canvas, start_x, start_y, growth):
        """绘制垂柳样式的树枝"""
        branch_length = self.height * (1 - self.trunk_ratio) * growth
        
        for i in range(self.branches):
            angle = -60 + (120 / max(1, self.branches - 1)) * i
            length = branch_length * random.uniform(0.7, 1.0)
            
            # 垂柳效果：枝条下垂
            points = []
            segments = 8
            for j in range(segments + 1):
                progress = j / segments
                
                # 初始方向
                x_offset = length * progress * math.cos(math.radians(angle))
                y_offset = -length * progress * math.sin(math.radians(angle))
                
                # 添加下垂效果
                droop = progress * progress * self.weeping_factor * 50
                
                points.extend([
                    start_x + x_offset,
                    start_y + y_offset + droop
                ])
            
            if len(points) >= 4:
                trunk_color = random.choice(self.theme['trunk'])
                canvas.create_line(points, width=max(1, int(4 * growth)), 
                                 fill=trunk_color, smooth=True)
                
                # 在枝条末端绘制叶子
                if len(points) >= 2:
                    end_x, end_y = points[-2], points[-1]
                    self._draw_enhanced_leaves(canvas, end_x, end_y, 'weeping')
    
    def _draw_fractal_branches(self, canvas, start_x, start_y, growth):
        """绘制分形样式的树枝"""
        initial_length = self.height * (1 - self.trunk_ratio) * growth
        self._draw_fractal_recursive(
            canvas, start_x, start_y, -90, initial_length, 
            self.fractal_depth, growth
        )
    
    def _draw_fractal_recursive(self, canvas, x, y, angle, length, depth, growth):
        """递归绘制分形树枝"""
        if depth <= 0 or length < 5:
            self._draw_enhanced_leaves(canvas, x, y, 'fractal')
            return
        
        # 绘制当前枝干
        end_x = x + length * math.cos(math.radians(angle))
        end_y = y + length * math.sin(math.radians(angle))
        
        trunk_color = random.choice(self.theme['trunk'])
        width = max(1, int((depth + 1) * growth))
        
        canvas.create_line(x, y, end_x, end_y, width=width, fill=trunk_color)
        
        # 递归绘制子分支
        new_length = length * random.uniform(0.6, 0.8)
        left_angle = angle - random.uniform(20, 40)
        right_angle = angle + random.uniform(20, 40)
        
        self._draw_fractal_recursive(canvas, end_x, end_y, left_angle, new_length, depth - 1, growth)
        self._draw_fractal_recursive(canvas, end_x, end_y, right_angle, new_length, depth - 1, growth)
    
    def _draw_standard_branches(self, canvas, start_x, start_y, growth):
        """绘制标准样式的树枝"""
        branch_length = self.height * (1 - self.trunk_ratio) * growth
        
        for i in range(self.branches):
            angle = -90 - self.angle_variance + (2 * self.angle_variance / max(1, self.branches - 1)) * i
            length = branch_length * random.uniform(0.6, 1.0)
            
            self._draw_branches(canvas, start_x, start_y, angle, length, 
                              random.randint(1, 3), 0, growth)
    
    def _draw_branches(self, canvas, x, y, angle, length, branches_left, depth, growth=1.0):
        """递归绘制树枝（改进版）"""
        if branches_left <= 0 or length < 8 or depth > 5:
            self._draw_enhanced_leaves(canvas, x, y, self.style)
            return
        
        # 计算新位置
        rad = math.radians(angle)
        new_x = x + length * math.cos(rad)
        new_y = y + length * math.sin(rad)
        
        # 绘制当前枝干
        trunk_color = random.choice(self.theme['trunk'])
        width = max(1, int((6 - depth) * growth))
        
        canvas.create_line(x, y, new_x, new_y, width=width, fill=trunk_color, capstyle=tk.ROUND)
        
        # 递归绘制子分枝
        angle_var = self.angle_variance * (1 - depth * 0.15)
        new_length = length * random.uniform(0.6, 0.85)
        
        # 多分支
        branch_count = random.randint(2, 3) if depth < 2 else 2
        for i in range(branch_count):
            if i == 0:
                new_angle = angle - random.uniform(15, angle_var)
            elif i == 1:
                new_angle = angle + random.uniform(15, angle_var)
            else:
                new_angle = angle + random.uniform(-10, 10)
            
            self._draw_branches(canvas, new_x, new_y, new_angle, new_length, 
                              branches_left - 1, depth + 1, growth)
    
    def _draw_enhanced_leaves(self, canvas, x, y, style_hint=None):
        """绘制增强版叶子"""
        leaf_count = int(random.randint(2, 8) * self.leaf_density)
        leaf_colors = self.theme['leaves']
        
        for _ in range(leaf_count):
            offset_x = random.uniform(-12, 12)
            offset_y = random.uniform(-12, 12)
            
            # 根据样式调整叶子
            if style_hint == 'weeping':
                offset_y += abs(offset_y) * 0.5  # 叶子向下
                size = random.uniform(2, 6)
            elif style_hint == 'fractal':
                size = random.uniform(1, 4)
            else:
                size = random.uniform(3, 7)
            
            leaf_color = random.choice(leaf_colors)
            
            # 随机选择叶子形状
            leaf_shape = random.choice(['oval', 'polygon', 'star'])
            
            if leaf_shape == 'oval':
                canvas.create_oval(
                    x + offset_x - size, y + offset_y - size,
                    x + offset_x + size, y + offset_y + size,
                    fill=leaf_color, outline=leaf_color
                )
            elif leaf_shape == 'polygon':
                # 三角形叶子
                points = [
                    x + offset_x, y + offset_y - size,
                    x + offset_x - size, y + offset_y + size,
                    x + offset_x + size, y + offset_y + size
                ]
                canvas.create_polygon(points, fill=leaf_color, outline=leaf_color)
            elif leaf_shape == 'star':
                # 星形叶子
                self._draw_star_leaf(canvas, x + offset_x, y + offset_y, size, leaf_color)
    
    def _draw_star_leaf(self, canvas, cx, cy, size, color):
        """绘制星形叶子"""
        points = []
        for i in range(10):  # 5个尖角的星
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.4
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.extend([x, y])
        
        canvas.create_polygon(points, fill=color, outline=color)


class EchoGarden:
    """Echo Garden 主应用类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echo Garden - 交互式生成艺术")
        self.root.geometry("1000x700")
        
        # 主题
        self.themes = [ColorTheme.WARM, ColorTheme.COOL, ColorTheme.MONO]
        self.current_theme_index = 0
        self.current_theme = self.themes[self.current_theme_index]
        
        # 音频处理
        self.audio_processor = RealTimeAudioProcessor() if AUDIO_AVAILABLE else None
        self.sound_simulator = SoundSimulator()
        
        # 树木列表
        self.trees = []
        
        # 实时音频状态
        self.is_live_mode = False
        self.last_audio_features = None
        
        # 波形显示
        self.waveform_canvas = None
        
        # 创建界面
        self.create_widgets()
        
        # 绑定事件
        self.bind_events()
        
        # 启动动画循环
        self.last_time = time.time()
        self.animate()
        
        # 显示帮助信息
        self.show_help()
    
    def create_widgets(self):
        """创建界面组件"""
        # 顶部信息栏
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.theme_label = tk.Label(
            info_frame, 
            text=f"当前主题: {self.current_theme['name']}", 
            font=("Arial", 12)
        )
        self.theme_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            info_frame, 
            text="状态: 就绪", 
            font=("Arial", 12)
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # 主内容区域
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧：波形显示
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # 波形显示标签
        waveform_label = tk.Label(left_frame, text="实时波形", font=("Arial", 10, "bold"))
        waveform_label.pack()
        
        # 波形显示画布
        self.waveform_canvas = tk.Canvas(
            left_frame, 
            bg='black',
            width=200, 
            height=400
        )
        self.waveform_canvas.pack(pady=5)
        
        # 音频信息显示
        self.audio_info_label = tk.Label(
            left_frame, 
            text="音量: --\n音调: --\n能量: --", 
            font=("Arial", 9),
            justify=tk.LEFT,
            bg='lightgray',
            relief=tk.SUNKEN
        )
        self.audio_info_label.pack(fill=tk.X, pady=5)
        
        # 右侧：主画布
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 主画布
        self.canvas = tk.Canvas(
            right_frame, 
            bg=self.current_theme['background'],
            width=750, 
            height=500
        )
        self.canvas.pack()
        
        # 控制按钮
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            control_frame, 
            text="� 声音种树", 
            command=self.record_and_plant,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🌱 随机种树", 
            command=self.plant_random_tree,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🎨 切换主题", 
            command=self.switch_theme,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🗑️ 清空", 
            command=self.clear_garden,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="💾 保存", 
            command=self.save_art,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="❓ 帮助", 
            command=self.show_help,
            font=("Arial", 12)
        ).pack(side=tk.RIGHT, padx=5)
    
    def bind_events(self):
        """绑定事件"""
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()  # 确保窗口可以接收键盘事件
    
    def on_click(self, event):
        """处理鼠标点击事件"""
        self.plant_tree_at(event.x, event.y)
    
    def on_key_press(self, event):
        """处理键盘事件"""
        key = event.keysym.lower()
        
        if key in ['1', '2', '3']:
            theme_index = int(key) - 1
            if theme_index < len(self.themes):
                self.current_theme_index = theme_index
                self.current_theme = self.themes[theme_index]
                self.update_theme()
        elif key == 'c':
            self.clear_garden()
        elif key == 's':
            self.save_art()
        elif key == 'space' or key == 'return':
            self.record_and_plant()
    
    def plant_tree_at(self, x, y):
        """在指定位置种树"""
        if y < 50:  # 避免在顶部信息栏种树
            y = 50
        
        tree = Tree(x, y, self.current_theme)
        self.trees.append(tree)
        self.status_label.config(text=f"状态: 种下新树 ({len(self.trees)} 棵树)")
    
    def plant_random_tree(self):
        """种植随机树"""
        x = random.randint(50, 930)
        y = random.randint(200, 580)
        self.plant_tree_at(x, y)
    
    def record_and_plant(self):
        """通过文本输入模拟声音并种树"""
        if self.is_recording:
            return
        
        # 获取用户输入
        sound_input = simpledialog.askstring(
            "声音输入", 
            "请输入描述声音的文字\n(例如: 高音、低音、大声、轻柔、节奏、旋律等):",
            parent=self.root
        )
        
        if sound_input is None:  # 用户取消
            return
        
        def process_sound():
            self.is_recording = True
            self.status_label.config(text="状态: 正在分析声音特征...")
            
            try:
                # 分析文本输入生成音频特征
                audio_features = self.sound_simulator.analyze_text_input(sound_input)
                
                # 在随机位置种树
                x = random.randint(100, 880)
                y = random.randint(200, 580)
                
                tree = Tree(x, y, self.current_theme, audio_features)
                self.trees.append(tree)
                
                self.status_label.config(
                    text=f"状态: 声音树已种植 - '{sound_input}' ({len(self.trees)} 棵树)"
                )
                
            except Exception as e:
                self.status_label.config(text=f"状态: 种植失败 - {str(e)}")
            
            finally:
                self.is_recording = False
        
        threading.Thread(target=process_sound, daemon=True).start()
    
    def switch_theme(self):
        """切换主题"""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme = self.themes[self.current_theme_index]
        self.update_theme()
    
    def update_theme(self):
        """更新主题"""
        self.canvas.config(bg=self.current_theme['background'])
        self.theme_label.config(text=f"当前主题: {self.current_theme['name']}")
        
        # 更新现有树木的主题
        for tree in self.trees:
            tree.theme = self.current_theme
        
        self.status_label.config(text=f"状态: 切换到{self.current_theme['name']}")
    
    def clear_garden(self):
        """清空花园"""
        self.trees.clear()
        self.canvas.delete("all")
        self.status_label.config(text="状态: 花园已清空")
    
    def save_art(self):
        """保存艺术作品为 EPS 文件"""
        if not self.trees:
            messagebox.showwarning("警告", "没有树木可以保存！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("EPS files", "*.eps"), ("All files", "*.*")],
            title="保存 Echo Garden 作品"
        )
        
        if filename:
            try:
                self.canvas.postscript(file=filename)
                self.status_label.config(text=f"状态: 已保存到 {filename}")
                messagebox.showinfo("成功", f"作品已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def animate(self):
        """动画循环"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # 更新树木成长
        for tree in self.trees:
            tree.update(dt)
        
        # 重绘画布
        self.redraw()
        
        # 继续动画循环
        self.root.after(50, self.animate)
    
    def redraw(self):
        """重绘画布"""
        self.canvas.delete("all")
        
        # 绘制所有树木
        for tree in self.trees:
            tree.draw(self.canvas)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🌳 Echo Garden - 交互式生成艺术 🌳

操作说明:
• 鼠标点击: 在点击位置种下随机树木
• � 声音种树: 输入声音描述文字，生成对应特征的树木
• 键盘 1/2/3: 切换主题 (1=暖色调, 2=冷色调, 3=单色调)
• 键盘 C: 清空整个花园
• 键盘 S: 保存当前作品为 .eps 文件
• 空格键/回车: 声音种树 (快捷键)

声音描述词汇:
� 高音/低音: 影响树的分枝角度
🔊 大声/轻柔: 影响树的高度和粗细
🎵 节奏/旋律: 影响树的分枝数量
🎼 和谐/激烈: 影响树的整体形态

特色功能:
🎨 实时成长: 树木会动态成长到完整形态
🌈 多主题: 三种精美配色主题
💾 矢量保存: 保存为高质量 EPS 矢量图形
✨ 纯Python: 仅使用Python标准库，无需外部依赖

开始创作你的声音花园吧! 🎶🌿
        """
        messagebox.showinfo("Echo Garden 帮助", help_text)
    
    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序已退出")


def main():
    """主函数"""
    print("🌳 启动 Echo Garden - 交互式生成艺术 🌳")
    print("✨ 纯Python标准库实现，通过文字描述声音来创造艺术")
    
    app = EchoGarden()
    app.run()


if __name__ == "__main__":
    main()
