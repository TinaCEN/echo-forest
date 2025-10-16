#!/usr/bin/env python3
"""
Echo Garden Multi-Style - 多风格艺术主题版
支持多种艺术风格：字符艺术、点阵、数字艺术、马赛克、波普艺术等
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import math
import random
import colorsys
import threading
import queue
import time
import string
import gc  # 垃圾回收

# 尝试导入音频库
try:
    import pyaudio
    import numpy as np
    AUDIO_AVAILABLE = True
    print("🎵 PyAudio 可用 - 支持实时音频")
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  PyAudio 不可用 - 使用模拟音频模式")

class AudioProcessor:
    """音频处理和波形生成器"""
    
    def __init__(self):
        self.is_recording = False
        self.audio_queue = queue.Queue(maxsize=100)
        self.waveform_data = [0] * 200
        
        if AUDIO_AVAILABLE:
            self.setup_audio()
        else:
            self.setup_mock_audio()
    
    def setup_audio(self):
        """设置真实音频输入"""
        try:
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self.audio_callback
            )
        except Exception as e:
            print(f"音频初始化失败: {e}")
            self.setup_mock_audio()
    
    def setup_mock_audio(self):
        """设置模拟音频数据"""
        self.mock_thread = threading.Thread(target=self.generate_mock_audio, daemon=True)
        self.mock_thread.start()
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频回调函数"""
        if not self.is_recording:
            return (None, pyaudio.paContinue)
        
        try:
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            if len(audio_data) >= 200:
                self.audio_queue.put(audio_data[:200].tolist())
            else:
                padded_data = list(audio_data) + [0] * (200 - len(audio_data))
                self.audio_queue.put(padded_data)
        except Exception as e:
            print(f"音频处理错误: {e}")
        
        return (None, pyaudio.paContinue)
    
    def generate_mock_audio(self):
        """生成模拟音频波形"""
        t = 0
        while True:
            if self.is_recording:
                mock_data = []
                for i in range(200):
                    wave1 = 0.3 * math.sin(2 * math.pi * 440 * (t + i/44100))
                    wave2 = 0.2 * math.sin(2 * math.pi * 880 * (t + i/44100))
                    wave3 = 0.1 * math.sin(2 * math.pi * 220 * (t + i/44100))
                    noise = 0.05 * (random.random() - 0.5)
                    total_wave = wave1 + wave2 + wave3 + noise
                    mock_data.append(total_wave)
                
                try:
                    self.audio_queue.put(mock_data, timeout=0.1)
                except queue.Full:
                    pass
                
                t += 200/44100
            
            time.sleep(0.02)
    
    def start_recording(self):
        """开始录音"""
        self.is_recording = True
        if AUDIO_AVAILABLE and hasattr(self, 'stream'):
            self.stream.start_stream()
    
    def stop_recording(self):
        """停止录音"""
        self.is_recording = False
        if AUDIO_AVAILABLE and hasattr(self, 'stream'):
            self.stream.stop_stream()
    
    def get_latest_waveform(self):
        """获取最新的波形数据"""
        try:
            while not self.audio_queue.empty():
                self.waveform_data = self.audio_queue.get_nowait()
        except queue.Empty:
            pass
        return self.waveform_data
    
    def cleanup(self):
        """清理资源"""
        self.stop_recording()
        if AUDIO_AVAILABLE and hasattr(self, 'stream'):
            self.stream.close()
            self.pa.terminate()

class MultiStyleRenderer:
    """多风格渲染器 - 支持多种艺术风格"""
    
    def __init__(self, canvas, style="dots"):
        self.canvas = canvas
        self.style = style
        
        # 字符集合
        self.char_sets = {
            "letters": list(string.ascii_uppercase),
            "numbers": list("0123456789"),
            "symbols": list("●○◐◑◒◓◔◕◖◗"),
            "shapes": ["▲", "▼", "◆", "■", "□", "●", "○", "★", "☆"],
            "chinese": ["福", "禄", "寿", "喜", "春", "夏", "秋", "冬"]
        }
    
    def set_style(self, style):
        """设置渲染风格"""
        self.style = style
    
    def draw_styled_line(self, x1, y1, x2, y2, color="#333333", width=2):
        """根据当前风格绘制线条"""
        if self.style == "dots":
            self._draw_dots_line(x1, y1, x2, y2, color, width)
        elif self.style == "characters":
            self._draw_characters_line(x1, y1, x2, y2, color, width)
        elif self.style == "numbers":
            self._draw_numbers_line(x1, y1, x2, y2, color, width)
        elif self.style == "mosaic":
            self._draw_mosaic_line(x1, y1, x2, y2, color, width)
        elif self.style == "pop_art":
            self._draw_pop_art_line(x1, y1, x2, y2, color, width)
        elif self.style == "chinese":
            self._draw_chinese_line(x1, y1, x2, y2, color, width)
    
    def draw_styled_circle(self, x, y, radius, color="#4CAF50", density_factor=1.0):
        """根据当前风格绘制圆形"""
        if self.style == "dots":
            self._draw_dots_circle(x, y, radius, color, density_factor)
        elif self.style == "characters":
            self._draw_characters_circle(x, y, radius, color, density_factor)
        elif self.style == "numbers":
            self._draw_numbers_circle(x, y, radius, color, density_factor)
        elif self.style == "mosaic":
            self._draw_mosaic_circle(x, y, radius, color, density_factor)
        elif self.style == "pop_art":
            self._draw_pop_art_circle(x, y, radius, color, density_factor)
        elif self.style == "chinese":
            self._draw_chinese_circle(x, y, radius, color, density_factor)
    
    def _draw_dots_line(self, x1, y1, x2, y2, color, width):
        """点阵风格线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        num_dots = max(1, int(distance * 0.7))
        
        for i in range(num_dots):
            t = i / max(1, num_dots - 1) if num_dots > 1 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            offset_x = random.uniform(-0.8, 0.8)
            offset_y = random.uniform(-0.8, 0.8)
            dot_size = random.uniform(width * 0.8, width * 1.5)
            
            self.canvas.create_oval(
                x - dot_size/2 + offset_x, y - dot_size/2 + offset_y,
                x + dot_size/2 + offset_x, y + dot_size/2 + offset_y,
                fill=color, outline="", tags="tree"
            )
    
    def _draw_characters_line(self, x1, y1, x2, y2, color, width):
        """字符艺术风格线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        num_chars = max(1, int(distance / 15))  # 调整字符密度
        
        for i in range(num_chars):
            t = i / max(1, num_chars - 1) if num_chars > 1 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)
            
            char = random.choice(self.char_sets["letters"])
            font_size = max(8, int(width * 2))
            
            self.canvas.create_text(
                x + offset_x, y + offset_y,
                text=char, fill=color, font=("Arial", font_size, "bold"),
                tags="tree"
            )
    
    def _draw_numbers_line(self, x1, y1, x2, y2, color, width):
        """数字艺术风格线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        num_numbers = max(1, int(distance / 12))
        
        for i in range(num_numbers):
            t = i / max(1, num_numbers - 1) if num_numbers > 1 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            
            number = random.choice(self.char_sets["numbers"])
            font_size = max(6, int(width * 1.5))
            
            self.canvas.create_text(
                x + offset_x, y + offset_y,
                text=number, fill=color, font=("Courier", font_size, "bold"),
                tags="tree"
            )
    
    def _draw_mosaic_line(self, x1, y1, x2, y2, color, width):
        """马赛克风格线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        tile_size = max(3, int(width * 1.5))
        num_tiles = max(1, int(distance / tile_size))
        
        for i in range(num_tiles):
            t = i / max(1, num_tiles - 1) if num_tiles > 1 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            
            # 创建小方块马赛克
            self.canvas.create_rectangle(
                x - tile_size/2 + offset_x, y - tile_size/2 + offset_y,
                x + tile_size/2 + offset_x, y + tile_size/2 + offset_y,
                fill=color, outline="", tags="tree"
            )
    
    def _draw_pop_art_line(self, x1, y1, x2, y2, color, width):
        """波普艺术风格线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        num_shapes = max(1, int(distance / 10))
        
        for i in range(num_shapes):
            t = i / max(1, num_shapes - 1) if num_shapes > 1 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            offset_x = random.uniform(-4, 4)
            offset_y = random.uniform(-4, 4)
            
            # 随机选择波普艺术形状
            shape_type = random.choice(["circle", "square", "triangle"])
            size = max(3, int(width * 2))
            
            if shape_type == "circle":
                self.canvas.create_oval(
                    x - size/2 + offset_x, y - size/2 + offset_y,
                    x + size/2 + offset_x, y + size/2 + offset_y,
                    fill=color, outline="black", width=1, tags="tree"
                )
            elif shape_type == "square":
                self.canvas.create_rectangle(
                    x - size/2 + offset_x, y - size/2 + offset_y,
                    x + size/2 + offset_x, y + size/2 + offset_y,
                    fill=color, outline="black", width=1, tags="tree"
                )
            elif shape_type == "triangle":
                points = [
                    x + offset_x, y - size/2 + offset_y,
                    x - size/2 + offset_x, y + size/2 + offset_y,
                    x + size/2 + offset_x, y + size/2 + offset_y
                ]
                self.canvas.create_polygon(
                    points, fill=color, outline="black", width=1, tags="tree"
                )
    
    def _draw_chinese_line(self, x1, y1, x2, y2, color, width):
        """中文字符艺术风格线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        num_chars = max(1, int(distance / 20))
        
        for i in range(num_chars):
            t = i / max(1, num_chars - 1) if num_chars > 1 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)
            
            char = random.choice(self.char_sets["chinese"])
            font_size = max(10, int(width * 2.5))
            
            self.canvas.create_text(
                x + offset_x, y + offset_y,
                text=char, fill=color, font=("SimHei", font_size, "bold"),
                tags="tree"
            )
    
    def _draw_dots_circle(self, x, y, radius, color, density_factor):
        """点阵风格圆形"""
        circumference = 2 * math.pi * radius
        num_dots = max(3, int(circumference * 0.7 * density_factor))
        
        for i in range(num_dots):
            angle = (i / num_dots) * 2 * math.pi
            radial_offset = random.uniform(0.3, 1.0)
            actual_radius = radius * radial_offset
            
            dot_x = x + actual_radius * math.cos(angle)
            dot_y = y + actual_radius * math.sin(angle)
            dot_size = random.uniform(1, 3)
            
            self.canvas.create_oval(
                dot_x - dot_size/2, dot_y - dot_size/2,
                dot_x + dot_size/2, dot_y + dot_size/2,
                fill=color, outline="", tags="tree"
            )
    
    def _draw_characters_circle(self, x, y, radius, color, density_factor):
        """字符艺术风格圆形"""
        circumference = 2 * math.pi * radius
        num_chars = max(3, int(circumference / 15 * density_factor))
        
        for i in range(num_chars):
            angle = (i / num_chars) * 2 * math.pi
            radial_offset = random.uniform(0.5, 1.0)
            actual_radius = radius * radial_offset
            
            char_x = x + actual_radius * math.cos(angle)
            char_y = y + actual_radius * math.sin(angle)
            
            char = random.choice(self.char_sets["letters"])
            font_size = max(6, int(radius / 3))
            
            self.canvas.create_text(
                char_x, char_y,
                text=char, fill=color, font=("Arial", font_size, "bold"),
                tags="tree"
            )
    
    def _draw_numbers_circle(self, x, y, radius, color, density_factor):
        """数字艺术风格圆形"""
        circumference = 2 * math.pi * radius
        num_numbers = max(3, int(circumference / 12 * density_factor))
        
        for i in range(num_numbers):
            angle = (i / num_numbers) * 2 * math.pi
            radial_offset = random.uniform(0.5, 1.0)
            actual_radius = radius * radial_offset
            
            num_x = x + actual_radius * math.cos(angle)
            num_y = y + actual_radius * math.sin(angle)
            
            number = random.choice(self.char_sets["numbers"])
            font_size = max(6, int(radius / 3))
            
            self.canvas.create_text(
                num_x, num_y,
                text=number, fill=color, font=("Courier", font_size, "bold"),
                tags="tree"
            )
    
    def _draw_mosaic_circle(self, x, y, radius, color, density_factor):
        """马赛克风格圆形"""
        num_tiles = max(3, int(radius * density_factor))
        
        for i in range(num_tiles):
            angle = (i / num_tiles) * 2 * math.pi
            radial_offset = random.uniform(0.3, 1.0)
            actual_radius = radius * radial_offset
            
            tile_x = x + actual_radius * math.cos(angle)
            tile_y = y + actual_radius * math.sin(angle)
            tile_size = max(2, int(radius / 4))
            
            self.canvas.create_rectangle(
                tile_x - tile_size/2, tile_y - tile_size/2,
                tile_x + tile_size/2, tile_y + tile_size/2,
                fill=color, outline="", tags="tree"
            )
    
    def _draw_pop_art_circle(self, x, y, radius, color, density_factor):
        """波普艺术风格圆形"""
        num_shapes = max(3, int(radius * density_factor * 0.8))
        
        for i in range(num_shapes):
            angle = (i / num_shapes) * 2 * math.pi
            radial_offset = random.uniform(0.3, 1.0)
            actual_radius = radius * radial_offset
            
            shape_x = x + actual_radius * math.cos(angle)
            shape_y = y + actual_radius * math.sin(angle)
            
            shape_type = random.choice(["circle", "square", "star"])
            size = max(3, int(radius / 3))
            
            if shape_type == "circle":
                self.canvas.create_oval(
                    shape_x - size/2, shape_y - size/2,
                    shape_x + size/2, shape_y + size/2,
                    fill=color, outline="black", width=1, tags="tree"
                )
            elif shape_type == "square":
                self.canvas.create_rectangle(
                    shape_x - size/2, shape_y - size/2,
                    shape_x + size/2, shape_y + size/2,
                    fill=color, outline="black", width=1, tags="tree"
                )
            elif shape_type == "star":
                star_symbol = random.choice(["★", "☆"])
                font_size = max(8, size)
                self.canvas.create_text(
                    shape_x, shape_y,
                    text=star_symbol, fill=color, font=("Arial", font_size),
                    tags="tree"
                )
    
    def _draw_chinese_circle(self, x, y, radius, color, density_factor):
        """中文字符艺术风格圆形"""
        circumference = 2 * math.pi * radius
        num_chars = max(3, int(circumference / 20 * density_factor))
        
        for i in range(num_chars):
            angle = (i / num_chars) * 2 * math.pi
            radial_offset = random.uniform(0.5, 1.0)
            actual_radius = radius * radial_offset
            
            char_x = x + actual_radius * math.cos(angle)
            char_y = y + actual_radius * math.sin(angle)
            
            char = random.choice(self.char_sets["chinese"])
            font_size = max(8, int(radius / 2.5))
            
            self.canvas.create_text(
                char_x, char_y,
                text=char, fill=color, font=("SimHei", font_size, "bold"),
                tags="tree"
            )

class AudioDrivenTree:
    """音频驱动的树木类 - 根据录音特征生成独特样式"""
    
    def __init__(self, canvas, renderer, palette, x, y, tree_id):
        self.canvas = canvas
        self.renderer = renderer
        self.palette = palette
        self.start_x = x
        self.start_y = y
        self.tree_id = tree_id
        
        # 树木类型 - 根据树ID决定（必须在初始化属性之前）
        self.tree_types = ['willow', 'maple', 'pine', 'oak', 'cherry']
        self.tree_type = self.tree_types[tree_id % len(self.tree_types)]
        
        # 风效果和动画
        self.wind_time = 0
        self.wind_strength = random.uniform(0.1, 0.3)
        self.wind_direction = random.uniform(0, 360)
        
        # 初始化基础属性
        self._initialize_base_properties()
        
        self.growth_progress = 0.0
        self.branches = []
        self.leaves = []
        self.is_growing = True
        self._can_grow = False  # 严格控制生长权限
        self.audio_features = None
        
        # 移动相关属性
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.current_x = x  # 当前实际位置
        self.current_y = y
    
    def _initialize_base_properties(self):
        """初始化基础属性"""
        # 根据树的ID创建基础差异
        random.seed(self.tree_id * 137)  # 使用固定种子确保一致性
        
        # 整体尺寸放大因子
        self.size_multiplier = random.uniform(1.2, 2.0)  # 随机大小差异
        
        # 根据树木类型设置不同的基础属性（放大尺寸）
        if self.tree_type == 'willow':
            self.base_height = random.uniform(150, 300) * self.size_multiplier
            self.base_trunk_width = random.uniform(8, 18) * self.size_multiplier
            self.drooping_factor = random.uniform(0.6, 0.9)  # 下垂系数
        elif self.tree_type == 'maple':
            self.base_height = random.uniform(120, 240) * self.size_multiplier
            self.base_trunk_width = random.uniform(7, 15) * self.size_multiplier
            self.branching_density = random.uniform(0.7, 1.2)  # 分枝密度
        elif self.tree_type == 'pine':
            self.base_height = random.uniform(180, 330) * self.size_multiplier
            self.base_trunk_width = random.uniform(6, 12) * self.size_multiplier
            self.cone_factor = random.uniform(0.3, 0.6)  # 锥形因子
        elif self.tree_type == 'oak':
            self.base_height = random.uniform(135, 255) * self.size_multiplier
            self.base_trunk_width = random.uniform(12, 22) * self.size_multiplier
            self.spreading_factor = random.uniform(0.8, 1.3)  # 伸展因子
        else:  # cherry
            self.base_height = random.uniform(105, 210) * self.size_multiplier
            self.base_trunk_width = random.uniform(6, 12) * self.size_multiplier
            self.flower_density = random.uniform(0.5, 1.0)  # 花朵密度
        
        self.base_growth_speed = random.uniform(0.02, 0.06)  # 增加生长速度
        
        # 重置随机种子
        random.seed()
    
    def apply_audio_features(self, audio_features):
        """根据音频特征调整树的属性"""
        self.audio_features = audio_features
        
        # 音量影响高度和粗细
        volume_factor = audio_features.get('volume', 0.5)
        self.max_height = self.base_height * (0.5 + volume_factor * 1.5)
        self.trunk_width = self.base_trunk_width * (0.6 + volume_factor * 0.8)
        
        # 能量影响分枝数量和角度
        energy_factor = audio_features.get('energy', 0.5)
        self.branch_probability = 0.3 + energy_factor * 0.6
        self.branch_angle_base = 20 + energy_factor * 40
        
        # 频率影响形态
        frequency_factor = audio_features.get('frequency', 0.5)
        self.asymmetry = frequency_factor * 0.4
        self.trunk_taper = 0.6 + frequency_factor * 0.3
        
        # 变化影响叶子
        variation_factor = audio_features.get('variation', 0.5)
        self.leaf_density = 0.5 + variation_factor * 1.5
        
        # 根据音频特征选择生长速度（更快）
        self.growth_speed = self.base_growth_speed * (0.8 + energy_factor * 0.7)
        
        print(f"树 #{self.tree_id} 音频特征应用: 高度={self.max_height:.1f}, 粗细={self.trunk_width:.1f}, 分枝率={self.branch_probability:.2f}, 尺寸={self.size_multiplier:.2f}")
    
    def update_growth(self):
        """更新生长进度"""
        # 严格控制：只有明确标记为正在生长且进度未完成才允许生长
        if (self.is_growing and 
            self.growth_progress < 1.0 and 
            hasattr(self, '_can_grow') and 
            getattr(self, '_can_grow', False)):
            # 只有在录音期间才生长
            self.growth_progress += self.growth_speed if hasattr(self, 'growth_speed') else self.base_growth_speed
            
        # 更新风效果动画（降低频率减少计算）
        self.wind_time += 0.02  # 从0.05减少到0.02，降低风效果计算频率
        return True
    
    def stop_growing(self):
        """停止生长"""
        self.is_growing = False
        self._can_grow = False  # 撤销生长权限
    
    def move_to(self, new_x, new_y):
        """移动树到新位置"""
        self.current_x = new_x
        self.current_y = new_y
        # 不改变start_x和start_y，保持原始种植点用于相对计算
    
    def is_point_inside_tree(self, x, y):
        """检查点是否在树的范围内（用于拖拽检测）"""
        # 简单的矩形碰撞检测
        if hasattr(self, 'max_height'):
            tree_height = self.max_height
            tree_width = self.trunk_width if hasattr(self, 'trunk_width') else self.base_trunk_width
        else:
            tree_height = self.base_height
            tree_width = self.base_trunk_width
        
        # 扩大检测范围以便于拖拽
        margin = 30
        left = self.current_x - tree_width/2 - margin
        right = self.current_x + tree_width/2 + margin
        top = self.current_y - tree_height - margin
        bottom = self.current_y + margin
        
        return left <= x <= right and top <= y <= bottom
    
    def draw(self):
        """绘制树木"""
        if self.growth_progress <= 0:
            return
        
        # 性能优化：只在必要时清除和重绘
        progress_changed = not hasattr(self, '_last_draw_progress') or abs(self._last_draw_progress - self.growth_progress) > 0.01
        position_changed = (not hasattr(self, '_last_draw_x') or 
                          not hasattr(self, '_last_draw_y') or
                          abs(self._last_draw_x - self.current_x) > 1 or
                          abs(self._last_draw_y - self.current_y) > 1)
        is_dragging = hasattr(self, 'is_dragging') and self.is_dragging
        
        if progress_changed or position_changed or is_dragging:
            # 清除之前的绘制
            self.canvas.delete(f"tree_{self.tree_id}")
            self._last_draw_progress = self.growth_progress
            self._last_draw_x = self.current_x
            self._last_draw_y = self.current_y
        else:
            # 如果进度和位置都没有显著变化，跳过重绘
            return
        
        # 使用树ID作为标签
        self.tag = f"tree_{self.tree_id}"
        
        # 根据树木类型绘制不同形状
        if self.tree_type == 'willow':
            self._draw_willow_tree()
        elif self.tree_type == 'maple':
            self._draw_maple_tree()
        elif self.tree_type == 'pine':
            self._draw_pine_tree()
        elif self.tree_type == 'oak':
            self._draw_oak_tree()
        else:  # cherry
            self._draw_cherry_tree()
    
    def _draw_trunk(self):
        """绘制树干"""
        if not hasattr(self, 'max_height'):
            current_height = self.base_height * min(1.0, self.growth_progress * 1.2)
            trunk_width = self.base_trunk_width
            asymmetry = 0.1
            trunk_taper = 0.8
        else:
            current_height = self.max_height * min(1.0, self.growth_progress * 1.2)
            trunk_width = self.trunk_width
            asymmetry = self.asymmetry
            trunk_taper = self.trunk_taper
        
        segments = max(4, int(current_height / 12))
        
        for i in range(segments):
            segment_progress = i / segments
            y_pos = self.start_y - (current_height * segment_progress)
            
            if y_pos > self.start_y - current_height:
                # 计算宽度锥度
                width_factor = 1.0 - (segment_progress * (1 - trunk_taper))
                current_width = trunk_width * width_factor
                
                # 计算弯曲
                curve_offset = asymmetry * 20 * math.sin(segment_progress * math.pi)
                x_pos = self.current_x + curve_offset
                
                # 下一段
                next_segment_progress = (i + 1) / segments
                next_y = self.current_y - (current_height * next_segment_progress)
                next_width_factor = 1.0 - (next_segment_progress * (1 - trunk_taper))
                next_width = trunk_width * next_width_factor
                next_curve = asymmetry * 20 * math.sin(next_segment_progress * math.pi)
                next_x = self.current_x + next_curve
                
                # 绘制树干两侧
                trunk_color = random.choice(self.palette.primary_colors)
                
                # 左侧轮廓
                self.renderer.draw_styled_line(
                    x_pos - current_width/2, y_pos,
                    next_x - next_width/2, next_y,
                    trunk_color, max(1, current_width/3)
                )
                
                # 右侧轮廓
                self.renderer.draw_styled_line(
                    x_pos + current_width/2, y_pos,
                    next_x + next_width/2, next_y,
                    trunk_color, max(1, current_width/3)
                )
    
    def _draw_branches(self):
        """绘制分枝"""
        if not hasattr(self, 'branch_probability'):
            return
        
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        max_branches = 3 + int(self.branch_probability * 8)
        
        # 生成分枝点
        branch_points = []
        for i in range(max_branches):
            if branch_progress > i / max_branches:
                height_ratio = 0.2 + (i / max_branches) * 0.7
                branch_y = self.start_y - (self.max_height * height_ratio * branch_progress)
                
                # 分枝角度
                angle = (i * 360 / max_branches) + random.uniform(-30, 30)
                branch_length = (self.max_height * 0.2) * random.uniform(0.6, 1.2)
                
                end_x = self.current_x + branch_length * math.cos(math.radians(angle))
                end_y = branch_y - branch_length * math.sin(math.radians(angle)) * 0.4
                
                # 绘制分枝
                branch_color = random.choice(self.palette.primary_colors)
                branch_width = self.trunk_width * 0.4 * random.uniform(0.7, 1.3)
                
                self.renderer.draw_styled_line(
                    self.current_x, branch_y,
                    end_x, end_y,
                    branch_color, max(1, branch_width)
                )
                
                branch_points.append((end_x, end_y))
        
        self.branch_points = branch_points
    
    def _draw_leaves(self):
        """绘制叶子"""
        if not hasattr(self, 'branch_points') or not hasattr(self, 'leaf_density'):
            return
        
        leaf_progress = max(0, (self.growth_progress - 0.6) / 0.4)
        
        for branch_x, branch_y in self.branch_points:
            if random.random() < leaf_progress * self.leaf_density:
                num_leaves = random.randint(2, 6)
                
                for _ in range(num_leaves):
                    leaf_x = branch_x + random.uniform(-12, 12)
                    leaf_y = branch_y + random.uniform(-8, 8)
                    
                    leaf_size = random.uniform(3, 7)
                    leaf_color = random.choice(self.palette.dot_colors)
                    
                    self.renderer.draw_styled_circle(
                        leaf_x, leaf_y, leaf_size, leaf_color, 
                        density_factor=self.leaf_density
                    )
    
    def _get_wind_offset(self, height_ratio, strength_multiplier=1.0):
        """计算风效果偏移"""
        wind_offset_x = math.sin(self.wind_time + height_ratio * 2) * self.wind_strength * strength_multiplier * 15
        wind_offset_y = math.cos(self.wind_time * 0.7 + height_ratio) * self.wind_strength * strength_multiplier * 8
        return wind_offset_x, wind_offset_y
    
    def _draw_willow_tree(self):
        """绘制柳树 - 垂柳效果"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.2) if hasattr(self, 'max_height') else self.base_height * min(1.0, self.growth_progress * 1.2)
        trunk_width = self.trunk_width if hasattr(self, 'trunk_width') else self.base_trunk_width
        
        # 绘制主干
        segments = max(6, int(current_height / 15))
        for i in range(segments):
            segment_progress = i / segments
            y_pos = self.current_y - (current_height * segment_progress)
            
            # 风效果
            wind_x, wind_y = self._get_wind_offset(segment_progress, 0.5)
            
            width_factor = 1.0 - (segment_progress * 0.3)
            current_width = trunk_width * width_factor
            
            x_pos = self.current_x + wind_x + segment_progress * 5  # 轻微弯曲
            
            if i < segments - 1:
                next_segment_progress = (i + 1) / segments
                next_y = self.current_y - (current_height * next_segment_progress)
                next_wind_x, next_wind_y = self._get_wind_offset(next_segment_progress, 0.5)
                next_width_factor = 1.0 - (next_segment_progress * 0.3)
                next_width = trunk_width * next_width_factor
                next_x = self.current_x + next_wind_x + next_segment_progress * 5
                
                trunk_color = random.choice(self.palette.primary_colors)
                self.renderer.draw_styled_line(
                    x_pos, y_pos, next_x, next_y,
                    trunk_color, max(1, current_width/2)
                )
        
        # 绘制垂柳枝条（生长到40%后开始）
        if self.growth_progress > 0.4:
            self._draw_willow_branches(current_height, trunk_width)
    
    def _draw_willow_branches(self, tree_height, trunk_width):
        """绘制柳树的垂枝"""
        branch_progress = max(0, (self.growth_progress - 0.4) / 0.6)
        num_branches = int(8 * branch_progress)
        
        for i in range(num_branches):
            # 分枝起点在树干的上半部分
            start_height = tree_height * (0.4 + (i / num_branches) * 0.5)
            branch_start_y = self.current_y - start_height
            
            # 风效果
            wind_x, wind_y = self._get_wind_offset(start_height / tree_height)
            branch_start_x = self.current_x + wind_x
            
            # 垂柳效果 - 枝条向下弯曲
            angle = random.uniform(-30, 30)  # 初始角度
            branch_length = random.uniform(tree_height * 0.3, tree_height * 0.8)
            
            # 绘制弯曲的枝条
            segments = max(5, int(branch_length / 20))
            prev_x, prev_y = branch_start_x, branch_start_y
            
            for j in range(1, segments + 1):
                segment_ratio = j / segments
                
                # 重力效果 - 越往下弯曲越厉害
                gravity_bend = segment_ratio * segment_ratio * 80
                wind_bend_x, wind_bend_y = self._get_wind_offset(segment_ratio, 1.5)
                
                current_x = branch_start_x + math.sin(math.radians(angle)) * branch_length * segment_ratio + wind_bend_x
                current_y = branch_start_y + gravity_bend + wind_bend_y
                
                # 枝条颜色
                branch_color = random.choice(self.palette.primary_colors)
                branch_width = max(1, trunk_width * 0.2 * (1 - segment_ratio * 0.7))
                
                self.renderer.draw_styled_line(
                    prev_x, prev_y, current_x, current_y,
                    branch_color, branch_width
                )
                
                # 在枝条上绘制叶子
                if self.growth_progress > 0.7 and random.random() < 0.6:
                    for _ in range(random.randint(1, 3)):
                        leaf_x = current_x + random.uniform(-8, 8)
                        leaf_y = current_y + random.uniform(-5, 5)
                        leaf_size = random.uniform(2, 5)
                        leaf_color = random.choice(self.palette.dot_colors)
                        
                        self.renderer.draw_styled_circle(
                            leaf_x, leaf_y, leaf_size, leaf_color, 0.8
                        )
                
                prev_x, prev_y = current_x, current_y
    
    def _draw_maple_tree(self):
        """绘制枫树 - 丰富的分枝结构"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.2) if hasattr(self, 'max_height') else self.base_height * min(1.0, self.growth_progress * 1.2)
        trunk_width = self.trunk_width if hasattr(self, 'trunk_width') else self.base_trunk_width
        
        # 绘制主干
        self._draw_basic_trunk(current_height, trunk_width, curvature=0.2)
        
        # 绘制丰富的分枝结构
        if self.growth_progress > 0.3:
            self._draw_maple_branches(current_height, trunk_width)
    
    def _draw_maple_branches(self, tree_height, trunk_width):
        """绘制枫树的分枝"""
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        
        # 多层分枝
        for level in range(4):
            if branch_progress > level / 4:
                level_height = tree_height * (0.3 + level * 0.15)
                branches_at_level = 3 + level
                
                for i in range(branches_at_level):
                    angle = (i / branches_at_level) * 360 + random.uniform(-20, 20)
                    branch_length = tree_height * (0.4 - level * 0.08) * random.uniform(0.7, 1.2)
                    
                    self._draw_branching_segment(
                        self.current_x, self.current_y - level_height,
                        angle, branch_length, trunk_width * (0.8 - level * 0.15),
                        level + 1, 3 - level
                    )
    
    def _draw_branching_segment(self, start_x, start_y, angle, length, width, depth, max_depth):
        """递归绘制分枝段"""
        if depth > max_depth or length < 10:
            return
        
        # 风效果
        wind_x, wind_y = self._get_wind_offset(depth / max_depth, 0.3)
        
        end_x = start_x + length * math.cos(math.radians(angle)) + wind_x
        end_y = start_y - length * math.sin(math.radians(angle)) + wind_y
        
        # 绘制分枝
        branch_color = random.choice(self.palette.primary_colors)
        self.renderer.draw_styled_line(start_x, start_y, end_x, end_y, branch_color, max(1, width))
        
        # 在末端绘制叶子
        if self.growth_progress > 0.6 and depth >= max_depth - 1:
            for _ in range(random.randint(2, 5)):
                leaf_x = end_x + random.uniform(-10, 10)
                leaf_y = end_y + random.uniform(-8, 8)
                leaf_size = random.uniform(3, 6)
                # 枫叶用红色系
                maple_colors = ['#FF4500', '#FF6347', '#FFD700', '#FF8C00', '#DC143C']
                leaf_color = random.choice(maple_colors)
                
                self.renderer.draw_styled_circle(leaf_x, leaf_y, leaf_size, leaf_color, 1.0)
        
        # 递归绘制子分枝
        if random.random() < 0.7:
            new_angle1 = angle + random.uniform(20, 50)
            new_angle2 = angle - random.uniform(20, 50)
            new_length = length * random.uniform(0.6, 0.8)
            new_width = width * 0.7
            
            self._draw_branching_segment(end_x, end_y, new_angle1, new_length, new_width, depth + 1, max_depth)
            if random.random() < 0.6:
                self._draw_branching_segment(end_x, end_y, new_angle2, new_length, new_width, depth + 1, max_depth)
    
    def _draw_pine_tree(self):
        """绘制松树 - 锥形结构"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.2) if hasattr(self, 'max_height') else self.base_height * min(1.0, self.growth_progress * 1.2)
        trunk_width = self.trunk_width if hasattr(self, 'trunk_width') else self.base_trunk_width
        
        # 绘制笔直的主干
        self._draw_basic_trunk(current_height, trunk_width, curvature=0.05)
        
        # 绘制锥形分层
        if self.growth_progress > 0.3:
            self._draw_pine_layers(current_height, trunk_width)
    
    def _draw_pine_layers(self, tree_height, trunk_width):
        """绘制松树的分层结构"""
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        layers = 6
        
        for layer in range(layers):
            if branch_progress > layer / layers:
                layer_height = tree_height * (0.2 + layer * 0.13)
                layer_y = self.current_y - layer_height
                
                # 每层的半径递减
                layer_radius = (tree_height * 0.3) * (1 - layer / layers * 0.6)
                branches_in_layer = 8
                
                for i in range(branches_in_layer):
                    angle = (i / branches_in_layer) * 360
                    branch_length = layer_radius * random.uniform(0.8, 1.1)
                    
                    # 风效果
                    wind_x, wind_y = self._get_wind_offset(layer / layers, 0.2)
                    
                    end_x = self.current_x + branch_length * math.cos(math.radians(angle)) + wind_x
                    end_y = layer_y + wind_y
                    
                    # 绘制针状分枝
                    branch_color = random.choice(['#228B22', '#006400', '#32CD32'])
                    self.renderer.draw_styled_line(self.current_x, layer_y, end_x, end_y, branch_color, 2)
                    
                    # 针叶效果
                    if self.growth_progress > 0.7:
                        for j in range(random.randint(3, 6)):
                            needle_ratio = j / 6
                            needle_x = self.current_x + (end_x - self.current_x) * needle_ratio + random.uniform(-3, 3)
                            needle_y = layer_y + (end_y - layer_y) * needle_ratio + random.uniform(-2, 2)
                            
                            self.renderer.draw_styled_circle(needle_x, needle_y, 1, branch_color, 0.5)
    
    def _draw_oak_tree(self):
        """绘制橡树 - 粗壮伸展"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.2) if hasattr(self, 'max_height') else self.base_height * min(1.0, self.growth_progress * 1.2)
        trunk_width = self.trunk_width if hasattr(self, 'trunk_width') else self.base_trunk_width
        
        # 绘制粗壮的主干
        self._draw_basic_trunk(current_height, trunk_width * 1.3, curvature=0.1)
        
        # 绘制伸展的枝条
        if self.growth_progress > 0.3:
            self._draw_oak_branches(current_height, trunk_width)
    
    def _draw_oak_branches(self, tree_height, trunk_width):
        """绘制橡树的伸展枝条"""
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        
        # 主要分枝 - 水平伸展
        main_branches = 5
        for i in range(main_branches):
            if branch_progress > i / main_branches:
                branch_height = tree_height * (0.4 + i * 0.12)
                branch_y = self.current_y - branch_height
                
                # 左右伸展
                for direction in [-1, 1]:
                    angle = direction * random.uniform(60, 120)
                    branch_length = tree_height * random.uniform(0.4, 0.7)
                    
                    # 风效果
                    wind_x, wind_y = self._get_wind_offset(i / main_branches, 0.4)
                    
                    end_x = self.current_x + branch_length * math.cos(math.radians(angle)) + wind_x
                    end_y = branch_y + branch_length * math.sin(math.radians(angle)) * 0.3 + wind_y
                    
                    # 绘制主枝
                    branch_color = random.choice(self.palette.primary_colors)
                    self.renderer.draw_styled_line(self.current_x, branch_y, end_x, end_y, branch_color, trunk_width * 0.4)
                    
                    # 小分枝
                    if self.growth_progress > 0.6:
                        self._draw_oak_sub_branches(end_x, end_y, angle, branch_length * 0.4, trunk_width * 0.2)
    
    def _draw_oak_sub_branches(self, start_x, start_y, base_angle, length, width):
        """绘制橡树的子分枝"""
        sub_branches = random.randint(2, 4)
        for i in range(sub_branches):
            angle = base_angle + random.uniform(-40, 40)
            sub_length = length * random.uniform(0.5, 0.8)
            
            wind_x, wind_y = self._get_wind_offset(random.random(), 0.6)
            
            end_x = start_x + sub_length * math.cos(math.radians(angle)) + wind_x
            end_y = start_y + sub_length * math.sin(math.radians(angle)) + wind_y
            
            branch_color = random.choice(self.palette.primary_colors)
            self.renderer.draw_styled_line(start_x, start_y, end_x, end_y, branch_color, max(1, width))
            
            # 橡树叶子 - 簇状
            if self.growth_progress > 0.7:
                for _ in range(random.randint(3, 7)):
                    leaf_x = end_x + random.uniform(-12, 12)
                    leaf_y = end_y + random.uniform(-8, 8)
                    leaf_size = random.uniform(4, 7)
                    oak_colors = ['#228B22', '#32CD32', '#90EE90', '#9ACD32']
                    leaf_color = random.choice(oak_colors)
                    
                    self.renderer.draw_styled_circle(leaf_x, leaf_y, leaf_size, leaf_color, 1.2)
    
    def _draw_cherry_tree(self):
        """绘制樱花树 - 优雅的分枝和花朵"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.2) if hasattr(self, 'max_height') else self.base_height * min(1.0, self.growth_progress * 1.2)
        trunk_width = self.trunk_width if hasattr(self, 'trunk_width') else self.base_trunk_width
        
        # 绘制优雅的主干
        self._draw_basic_trunk(current_height, trunk_width, curvature=0.15)
        
        # 绘制樱花枝条
        if self.growth_progress > 0.3:
            self._draw_cherry_branches(current_height, trunk_width)
    
    def _draw_cherry_branches(self, tree_height, trunk_width):
        """绘制樱花树的枝条"""
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        
        # 优雅的上升枝条
        branches = 6
        for i in range(branches):
            if branch_progress > i / branches:
                branch_height = tree_height * (0.3 + i * 0.12)
                branch_y = self.current_y - branch_height
                
                angle = random.uniform(30, 150)
                branch_length = tree_height * random.uniform(0.3, 0.5)
                
                # 风效果
                wind_x, wind_y = self._get_wind_offset(i / branches, 0.5)
                
                end_x = self.current_x + branch_length * math.cos(math.radians(angle)) + wind_x
                end_y = branch_y - branch_length * math.sin(math.radians(angle)) * 0.6 + wind_y
                
                # 绘制枝条
                branch_color = random.choice(self.palette.primary_colors)
                self.renderer.draw_styled_line(self.current_x, branch_y, end_x, end_y, branch_color, trunk_width * 0.3)
                
                # 樱花
                if self.growth_progress > 0.7:
                    self._draw_cherry_blossoms(end_x, end_y, branch_length)
    
    def _draw_cherry_blossoms(self, branch_x, branch_y, branch_length):
        """绘制樱花"""
        blossom_count = int(branch_length / 10)
        
        for i in range(blossom_count):
            # 沿着枝条分布花朵
            ratio = i / max(1, blossom_count - 1)
            flower_x = self.current_x + (branch_x - self.current_x) * ratio + random.uniform(-5, 5)
            flower_y = branch_y + random.uniform(-3, 3)
            
            # 风中飘动的花朵
            wind_x, wind_y = self._get_wind_offset(ratio, 0.8)
            flower_x += wind_x
            flower_y += wind_y
            
            # 樱花颜色
            cherry_colors = ['#FFB6C1', '#FFC0CB', '#FF69B4', '#FFFFFF', '#FFEFD5']
            flower_color = random.choice(cherry_colors)
            flower_size = random.uniform(2, 4)
            
            self.renderer.draw_styled_circle(flower_x, flower_y, flower_size, flower_color, 0.7)
    
    def _draw_basic_trunk(self, height, width, curvature=0.1):
        """绘制基础树干"""
        segments = max(6, int(height / 12))
        
        for i in range(segments):
            segment_progress = i / segments
            y_pos = self.current_y - (height * segment_progress)
            
            # 风效果和自然弯曲
            wind_x, wind_y = self._get_wind_offset(segment_progress, 0.3)
            curve_offset = curvature * 20 * math.sin(segment_progress * math.pi)
            
            width_factor = 1.0 - (segment_progress * 0.4)
            current_width = width * width_factor
            
            x_pos = self.current_x + curve_offset + wind_x
            
            if i < segments - 1:
                next_segment_progress = (i + 1) / segments
                next_y = self.current_y - (height * next_segment_progress)
                next_wind_x, next_wind_y = self._get_wind_offset(next_segment_progress, 0.3)
                next_curve = curvature * 20 * math.sin(next_segment_progress * math.pi)
                next_width_factor = 1.0 - (next_segment_progress * 0.4)
                next_width = width * next_width_factor
                next_x = self.current_x + next_curve + next_wind_x
                
                trunk_color = random.choice(self.palette.primary_colors)
                self.renderer.draw_styled_line(
                    x_pos, y_pos, next_x, next_y,
                    trunk_color, max(2, current_width/2)
                )

class MultiStyleTree:
    """多风格树木类 - 保留用于兼容性"""
    
    def __init__(self, canvas, renderer, palette, x, y):
        self.canvas = canvas
        self.renderer = renderer
        self.palette = palette
        self.start_x = x
        self.start_y = y
        
        self._randomize_properties()
        
        self.growth_progress = 0.0
        self.branches = []
        self.leaves = []
    
    def _randomize_properties(self):
        """随机化树木属性"""
        self.max_height = random.uniform(80, 200)
        self.trunk_width = random.uniform(4, 12)
        self.branch_factor = random.uniform(0.6, 0.9)
        
        self.growth_speed = random.uniform(0.01, 0.04)
        self.branch_angle_base = random.uniform(25, 45)
        self.branch_probability = random.uniform(0.4, 0.8)
        
        self.leaf_density = random.uniform(0.8, 1.5)
        self.trunk_taper = random.uniform(0.7, 0.95)
        self.asymmetry = random.uniform(0.1, 0.3)
        
        self.max_branch_levels = random.randint(3, 6)
        self.branches_per_level = random.randint(2, 5)
    
    def update_growth(self):
        """更新生长进度"""
        if self.growth_progress < 1.0:
            self.growth_progress += self.growth_speed
            return True
        return False
    
    def draw(self):
        """绘制完整树木"""
        if self.growth_progress <= 0:
            return
        
        self.canvas.delete("current_tree")
        
        self._draw_improved_trunk()
        
        if self.growth_progress > 0.3:
            self._draw_branch_system()
        
        if self.growth_progress > 0.6:
            self._draw_leaves()
    
    def _draw_improved_trunk(self):
        """绘制改进的树干"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.5)
        
        segments = max(5, int(current_height / 10))
        
        for i in range(segments):
            segment_progress = i / segments
            y_pos = self.start_y - (current_height * segment_progress)
            
            if y_pos > self.start_y - current_height:
                width_factor = 1.0 - (segment_progress * (1 - self.trunk_taper))
                current_width = self.trunk_width * width_factor
                
                curve_offset = self.asymmetry * 15 * math.sin(segment_progress * math.pi)
                x_pos = self.current_x + curve_offset
                
                next_segment_progress = (i + 1) / segments
                next_y = self.current_y - (current_height * next_segment_progress)
                next_width_factor = 1.0 - (next_segment_progress * (1 - self.trunk_taper))
                next_width = self.trunk_width * next_width_factor
                next_curve = self.asymmetry * 15 * math.sin(next_segment_progress * math.pi)
                next_x = self.current_x + next_curve
                
                trunk_color = random.choice(self.palette.primary_colors)
                self.renderer.draw_styled_line(
                    x_pos - current_width/2, y_pos,
                    next_x - next_width/2, next_y,
                    trunk_color, current_width/2
                )
                self.renderer.draw_styled_line(
                    x_pos + current_width/2, y_pos,
                    next_x + next_width/2, next_y,
                    trunk_color, current_width/2
                )
    
    def _draw_branch_system(self):
        """绘制分枝系统"""
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        
        branch_points = []
        for level in range(self.max_branch_levels):
            if branch_progress > level / self.max_branch_levels:
                height_ratio = 0.3 + (level / self.max_branch_levels) * 0.6
                branch_y = self.start_y - (self.max_height * height_ratio)
                
                for branch_idx in range(self.branches_per_level):
                    if random.random() < self.branch_probability:
                        base_angle = (branch_idx / self.branches_per_level) * 360
                        angle_variation = random.uniform(-20, 20)
                        branch_angle = base_angle + angle_variation
                        
                        branch_length = (self.max_height * 0.3) * (self.branch_factor ** level)
                        branch_length *= random.uniform(0.7, 1.3)
                        
                        end_x = self.current_x + branch_length * math.cos(math.radians(branch_angle))
                        end_y = branch_y - branch_length * math.sin(math.radians(branch_angle)) * 0.5
                        
                        branch_width = self.trunk_width * (self.branch_factor ** (level + 1))
                        
                        branch_color = random.choice(self.palette.primary_colors)
                        self.renderer.draw_styled_line(
                            self.current_x, branch_y,
                            end_x, end_y,
                            branch_color, max(1, branch_width)
                        )
                        
                        branch_points.append((end_x, end_y, level))
        
        self.branch_points = branch_points
    
    def _draw_leaves(self):
        """绘制叶子"""
        if not hasattr(self, 'branch_points'):
            return
        
        leaf_progress = max(0, (self.growth_progress - 0.6) / 0.4)
        
        for branch_x, branch_y, level in self.branch_points:
            if random.random() < leaf_progress * self.leaf_density:
                num_leaves = random.randint(3, 8)
                
                for _ in range(num_leaves):
                    leaf_x = branch_x + random.uniform(-15, 15)
                    leaf_y = branch_y + random.uniform(-10, 10)
                    
                    leaf_size = random.uniform(3, 8) * (1.2 - level * 0.2)
                    
                    leaf_color = random.choice(self.palette.dot_colors)
                    
                    self.renderer.draw_styled_circle(
                        leaf_x, leaf_y, leaf_size, leaf_color, 
                        density_factor=self.leaf_density
                    )

class WaveformDisplay:
    """音频波形显示器"""
    
    def __init__(self, canvas, x, y, width, height, palette):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.palette = palette
        self.waveform_data = [0] * 200
        
    def update_waveform(self, audio_data):
        """更新波形数据"""
        if audio_data and len(audio_data) > 0:
            self.waveform_data = audio_data[:200]
    
    def draw(self):
        """绘制波形"""
        self.canvas.delete("waveform")
        
        self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            outline=self.palette.primary_colors[0], width=2, fill="", tags="waveform"
        )
        
        self.canvas.create_text(
            self.x + self.width/2, self.y - 15,
            text="🎵 实时音频波形", font=("Arial", 12, "bold"),
            fill=self.palette.primary_colors[0], tags="waveform"
        )
        
        if not self.waveform_data:
            return
        
        points = []
        center_y = self.y + self.height / 2
        
        for i, amplitude in enumerate(self.waveform_data):
            x_pos = self.x + (i / len(self.waveform_data)) * self.width
            y_offset = max(-self.height/2 + 10, min(self.height/2 - 10, amplitude * self.height/2))
            y_pos = center_y + y_offset
            points.extend([x_pos, y_pos])
        
        if len(points) >= 4:
            self.canvas.create_line(
                points, fill=self.palette.dot_colors[2], width=2, 
                smooth=True, tags="waveform"
            )
        
        self.canvas.create_line(
            self.x, center_y, self.x + self.width, center_y,
            fill=self.palette.primary_colors[1], width=1, dash=(5, 5), tags="waveform"
        )

class MultiStyleColorPalette:
    """多风格配色方案 - 每种风格都有独特的配色"""
    
    def __init__(self):
        self.schemes = {
            "dots": {
                "name": "🔴 经典点阵",
                "background": ["#f8f6f0", "#fcfaf6", "#f5f3ed"],
                "primary": ["#d45087", "#4ecdc4", "#5f27cd", "#ff9ff3"],
                "dots": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#f0932b", 
                        "#eb4d4b", "#6c5ce7", "#a29bfe", "#fd79a8", "#fdcb6e",
                        "#e17055", "#00b894", "#00cec9", "#0984e3", "#6c5ce7"]
            },
            "characters": {
                "name": "🔤 字母艺术",
                "background": ["#1e1e2e", "#2d2d44", "#181825"],
                "primary": ["#cba6f7", "#f38ba8", "#a6e3a1", "#f9e2af"],
                "dots": ["#cdd6f4", "#f38ba8", "#cba6f7", "#f9e2af", "#a6e3a1",
                        "#fab387", "#f2cdcd", "#89b4fa", "#94e2d5", "#b4befe",
                        "#eba0ac", "#f5c2e7", "#ddb6f2", "#e8a2af", "#f28fad"]
            },
            "numbers": {
                "name": "🔢 数字矩阵",
                "background": ["#0f0f23", "#1a1a2e", "#16213e"],
                "primary": ["#00ff41", "#ff0040", "#00bfff", "#ffff00"],
                "dots": ["#00ff41", "#39ff14", "#32cd32", "#00fa9a", "#98fb98",
                        "#00ff7f", "#90ee90", "#adff2f", "#7fff00", "#7cfc00",
                        "#00ff00", "#00e600", "#00cc00", "#00b300", "#009900"]
            },
            "mosaic": {
                "name": "🟦 马赛克",
                "background": ["#fef9e7", "#fdf2e9", "#f8f9fa"],
                "primary": ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"],
                "dots": ["#e74c3c", "#c0392b", "#3498db", "#2980b9", "#2ecc71",
                        "#27ae60", "#f39c12", "#d35400", "#9b59b6", "#8e44ad",
                        "#34495e", "#2c3e50", "#1abc9c", "#16a085", "#f1c40f"]
            },
            "pop_art": {
                "name": "🎨 波普艺术",
                "background": ["#ffeb3b", "#ff9800", "#f44336"],
                "primary": ["#e91e63", "#9c27b0", "#673ab7", "#3f51b5"],
                "dots": ["#ff1744", "#e91e63", "#ad1457", "#880e4f", "#d500f9",
                        "#aa00ff", "#6200ea", "#3d5afe", "#2979ff", "#00b0ff",
                        "#00e5ff", "#1de9b6", "#00e676", "#76ff03", "#c6ff00"]
            },
            "chinese": {
                "name": "🏮 中国风",
                "background": ["#fdf5e6", "#f5f5dc", "#fffaf0"],
                "primary": ["#dc143c", "#b8860b", "#228b22", "#4169e1"],
                "dots": ["#dc143c", "#b22222", "#cd5c5c", "#f08080", "#fa8072",
                        "#b8860b", "#daa520", "#ffd700", "#228b22", "#32cd32",
                        "#90ee90", "#4169e1", "#6495ed", "#87ceeb", "#add8e6"]
            }
        }
        self.current_scheme = "dots"
    
    def switch_scheme(self, scheme_name):
        """切换配色方案"""
        if scheme_name in self.schemes:
            self.current_scheme = scheme_name
            return True
        return False
    
    @property
    def background_colors(self):
        return self.schemes[self.current_scheme]["background"]
    
    @property
    def primary_colors(self):
        return self.schemes[self.current_scheme]["primary"]
    
    @property
    def dot_colors(self):
        return self.schemes[self.current_scheme]["dots"]
    
    @property
    def scheme_name(self):
        return self.schemes[self.current_scheme]["name"]
    
    @property
    def current_style(self):
        return self.current_scheme

class EchoGardenMultiStyle:
    """Echo Garden Multi-Style - 主应用类"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.setup_audio()
        self.bind_events()
        self.start_animation()
        
        print("🎨 Echo Garden Multi-Style 启动成功!")
        print("✨ 支持6种艺术风格：点阵、字符、数字、马赛克、波普、中国风")
    
    def setup_window(self):
        """设置窗口"""
        self.root.title("🎨 Echo Garden Multi-Style - 多风格艺术主题版")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f8f6f0")
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1400) // 2
        y = (self.root.winfo_screenheight() - 900) // 2
        self.root.geometry(f"1400x900+{x}+{y}")
    
    def setup_variables(self):
        """初始化变量"""
        self.palette = MultiStyleColorPalette()
        self.trees = []
        self.max_trees = 25
        self.animation_active = True
        
        self.audio_processor = None
        self.waveform_display = None
        
        # 自定义背景颜色
        self.custom_background = None
        self.use_custom_background = False
        
        # 录音驱动的树木生长控制
        self.current_growing_tree = None
        self.is_recording_for_tree = False
        self.audio_samples_buffer = []  # 存储录音期间的音频样本
        self.tree_counter = 0  # 树木计数器
        
        # 树木位置管理 - 避免重叠
        self.tree_positions = []  # 存储已占用的位置 (x, width)
        self.min_tree_distance = 80  # 树木之间的最小距离
        
        # 性能优化计数器
        self.animation_frame_count = 0
        self.gc_interval = 100  # 每100帧执行一次垃圾回收
    
    def create_widgets(self):
        """创建界面组件"""
        main_frame = tk.Frame(self.root, bg="#f8f6f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧面板 - 音频波形显示
        left_panel = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.config(width=300)
        left_panel.pack_propagate(False)
        
        # 波形显示画布
        waveform_canvas = tk.Canvas(left_panel, width=280, height=200, bg="#ffffff")
        waveform_canvas.pack(pady=20)
        
        self.waveform_display = WaveformDisplay(
            waveform_canvas, 10, 10, 260, 180, self.palette
        )
        
        # 音频控制
        audio_frame = tk.Frame(left_panel, bg="#ffffff")
        audio_frame.pack(pady=10)
        
        self.record_button = tk.Button(
            audio_frame, text="🎤 开始录音", 
            command=self.toggle_recording,
            font=("Arial", 12), bg="#4CAF50", fg="white"
        )
        self.record_button.pack(pady=5)
        
        # 音频特征显示
        features_frame = tk.LabelFrame(left_panel, text="🎵 音频特征", bg="#ffffff")
        features_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.audio_features_label = tk.Label(
            features_frame, text="等待音频输入...", 
            bg="#ffffff", font=("Arial", 10), justify=tk.LEFT
        )
        self.audio_features_label.pack(pady=5)
        
        # 风格选择面板
        style_frame = tk.LabelFrame(left_panel, text="🎨 艺术风格", bg="#ffffff")
        style_frame.pack(fill=tk.X, padx=10, pady=10)
        
        style_buttons = [
            ("🔴 点阵", "dots", "#d45087"),
            ("🔤 字母", "characters", "#cba6f7"),
            ("🔢 数字", "numbers", "#00ff41"),
            ("🟦 马赛克", "mosaic", "#3498db"),
            ("🎨 波普", "pop_art", "#e91e63"),
            ("🏮 中国风", "chinese", "#dc143c")
        ]
        
        for i, (text, style, color) in enumerate(style_buttons):
            btn = tk.Button(
                style_frame, text=text, 
                command=lambda s=style: self.switch_style(s),
                font=("Arial", 9), bg=color, fg="white", width=8
            )
            btn.pack(pady=2, fill=tk.X)
        
        # 背景颜色自定义面板
        bg_frame = tk.LabelFrame(left_panel, text="🌈 背景颜色", bg="#ffffff")
        bg_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 当前背景颜色显示
        self.bg_color_display = tk.Frame(bg_frame, height=30, bg="#ffffff", relief=tk.SUNKEN, bd=2)
        self.bg_color_display.pack(fill=tk.X, padx=5, pady=5)
        
        # 背景颜色控制按钮
        bg_buttons_frame = tk.Frame(bg_frame, bg="#ffffff")
        bg_buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(
            bg_buttons_frame, text="🎨 选择颜色", 
            command=self.choose_custom_background,
            font=("Arial", 9), bg="#FF5722", fg="white", width=10
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            bg_buttons_frame, text="🔄 重置", 
            command=self.reset_background,
            font=("Arial", 9), bg="#607D8B", fg="white", width=8
        ).pack(side=tk.RIGHT, padx=2)
        
        # 预设背景颜色
        preset_frame = tk.Frame(bg_frame, bg="#ffffff")
        preset_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(preset_frame, text="快速选择:", bg="#ffffff", font=("Arial", 8)).pack(anchor=tk.W)
        
        preset_colors_frame = tk.Frame(preset_frame, bg="#ffffff")
        preset_colors_frame.pack(fill=tk.X)
        
        preset_colors = [
            ("⚫", "#2c3e50"),  # 深灰
            ("🔴", "#e74c3c"),  # 红色
            ("🔵", "#3498db"),  # 蓝色
            ("🟢", "#2ecc71"),  # 绿色
            ("🟡", "#f1c40f"),  # 黄色
            ("🟣", "#9b59b6"),  # 紫色
            ("🟤", "#8b4513"),  # 棕色
            ("⚪", "#ecf0f1")   # 浅灰
        ]
        
        for i, (emoji, color) in enumerate(preset_colors):
            btn = tk.Button(
                preset_colors_frame, text=emoji,
                command=lambda c=color: self.set_preset_background(c),
                font=("Arial", 10), bg=color, fg="white" if color != "#ecf0f1" else "black",
                width=2, height=1
            )
            btn.pack(side=tk.LEFT, padx=1)
        
        # 右侧 - 主画布区域
        right_panel = tk.Frame(main_frame, bg="#f8f6f0")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            right_panel, 
            text="🌳 Echo Garden Multi-Style", 
            font=("Arial", 20, "bold"),
            bg="#f8f6f0", fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # 画布
        canvas_frame = tk.Frame(right_panel, bg="#ffffff", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#ffffff")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.renderer = MultiStyleRenderer(self.canvas, style="dots")
        
        # 底部控制栏
        control_frame = tk.Frame(right_panel, bg="#f8f6f0")
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 录音控制说明
        info_frame = tk.Frame(control_frame, bg="#f8f6f0")
        info_frame.pack(fill=tk.X, pady=5)
        
        info_text = "🎵 点击左侧「开始录音」按钮种植新树，「停止录音」结束当前树的生长"
        tk.Label(
            info_frame, text=info_text, 
            bg="#f8f6f0", font=("Arial", 12), fg="#34495e"
        ).pack(pady=5)
        
        # 快捷按钮
        button_frame = tk.Frame(control_frame, bg="#f8f6f0")
        button_frame.pack(fill=tk.X, pady=5)
        
        buttons = [
            ("🧹 清空画布", self.clear_canvas, "#f44336"),
            ("💾 保存作品", self.save_artwork, "#FF9800"),
            ("🎲 随机风格", self.random_style, "#9C27B0"),
            ("🌈 背景颜色", self.choose_custom_background, "#FF5722")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame, text=text, command=command,
                font=("Arial", 10), bg=color, fg="white", width=10
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # 状态栏
        self.status_label = tk.Label(
            control_frame, text=f"🎨 当前风格: {self.palette.scheme_name} | 树木数量: 0/{self.max_trees}",
            bg="#f8f6f0", font=("Arial", 10), relief=tk.SUNKEN
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))
    
    def setup_audio(self):
        """设置音频处理"""
        try:
            self.audio_processor = AudioProcessor()
        except Exception as e:
            print(f"音频设置失败: {e}")
            messagebox.showwarning("音频警告", "音频功能不可用，将使用模拟模式")
    
    def bind_events(self):
        """绑定事件"""
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        
        # 鼠标事件用于拖拽树木
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # 拖拽状态
        self.dragging_tree = None
    
    def switch_style(self, style_name):
        """切换艺术风格"""
        self.palette.switch_scheme(style_name)
        self.renderer.set_style(style_name)
        self.update_background()
        self.update_status()
        
        # 重新绘制所有树木以应用新风格
        for tree in self.trees:
            tree.draw()
    
    def random_style(self):
        """随机切换风格"""
        styles = list(self.palette.schemes.keys())
        current_style = self.palette.current_scheme
        available_styles = [s for s in styles if s != current_style]
        new_style = random.choice(available_styles)
        self.switch_style(new_style)
    
    def toggle_recording(self):
        """切换录音状态 - 控制树木的生长"""
        if not self.audio_processor:
            return
        
        if self.audio_processor.is_recording:
            # 停止录音 - 立即结束当前树的生长
            self.audio_processor.stop_recording()
            self.record_button.config(text="🎤 开始录音", bg="#4CAF50")
            self.is_recording_for_tree = False
            
            # 立即停止当前树的生长状态
            if self.current_growing_tree:
                self.current_growing_tree.is_growing = False
                self.current_growing_tree._can_grow = False  # 撤销生长权限
                self.current_growing_tree.stop_growing()  # 调用停止方法
                self.finalize_current_tree()
            
        else:
            # 开始录音 - 种植新树并开始生长
            self.audio_processor.start_recording()
            self.record_button.config(text="⏹️ 停止录音", bg="#f44336")
            self.is_recording_for_tree = True
            self.audio_samples_buffer = []  # 清空音频缓冲区
            
            # 创建新树
            self.create_new_tree_from_recording()
    
    def on_canvas_click(self, event):
        """画布点击事件"""
        self.create_tree(event.x, event.y)
    
    def on_key_press(self, event):
        """按键事件"""
        key = event.keysym
        if key == "1":
            self.switch_style("dots")
        elif key == "2":
            self.switch_style("characters")
        elif key == "3":
            self.switch_style("numbers")
        elif key == "4":
            self.switch_style("mosaic")
        elif key == "5":
            self.switch_style("pop_art")
        elif key == "6":
            self.switch_style("chinese")
        elif key.lower() == "c":
            self.clear_canvas()
        elif key.lower() == "s":
            self.save_artwork()
        elif key.lower() == "r":
            self.random_style()
        elif key.lower() == "b":
            self.choose_custom_background()
        elif key == "space":
            self.toggle_recording()  # 空格键快速录音
    
    def on_mouse_press(self, event):
        """鼠标按下事件 - 开始拖拽检测"""
        # 检查是否点击了某棵树
        for tree in reversed(self.trees):  # 从上层开始检查
            if isinstance(tree, AudioDrivenTree) and tree.is_point_inside_tree(event.x, event.y):
                self.dragging_tree = tree
                tree.is_dragging = True
                tree.drag_offset_x = event.x - tree.current_x
                tree.drag_offset_y = event.y - tree.current_y
                print(f"🖱️ 开始拖拽树 #{tree.tree_id}，位置: ({tree.current_x}, {tree.current_y})")
                break
    
    def on_mouse_drag(self, event):
        """鼠标拖拽事件"""
        if self.dragging_tree:
            new_x = event.x - self.dragging_tree.drag_offset_x
            new_y = event.y - self.dragging_tree.drag_offset_y
            
            # 限制在画布范围内
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            new_x = max(50, min(canvas_width - 50, new_x))
            new_y = max(50, min(canvas_height - 20, new_y))
            
            self.dragging_tree.move_to(new_x, new_y)
            # 强制重绘移动的树木
            self.dragging_tree.draw()
            # print(f"🌲 拖拽中: ({new_x}, {new_y})")  # 取消注释以查看拖拽轨迹
    
    def on_mouse_release(self, event):
        """鼠标释放事件 - 结束拖拽"""
        if self.dragging_tree:
            # 更新位置记录
            self.update_tree_position_record(self.dragging_tree)
            print(f"🌳 树 #{self.dragging_tree.tree_id} 移动完成，新位置: ({self.dragging_tree.current_x}, {self.dragging_tree.current_y})")
            
            self.dragging_tree.is_dragging = False
            self.dragging_tree = None
    
    def update_tree_position_record(self, moved_tree):
        """更新被移动树木的位置记录"""
        tree_width = 60  # 估算的树木宽度
        
        # 找到并更新对应的位置记录
        for i, (recorded_x, recorded_width) in enumerate(self.tree_positions):
            # 通过树木ID或初始位置识别对应的记录
            if abs(recorded_x - moved_tree.start_x) < 10:  # 如果是原始位置附近
                self.tree_positions[i] = (moved_tree.current_x, tree_width)
                break
    
    def is_position_available(self, x, tree_width):
        """检查位置是否可用（避免重叠）"""
        for occupied_x, occupied_width in self.tree_positions:
            # 计算两棵树的边界
            new_left = x - tree_width // 2
            new_right = x + tree_width // 2
            occupied_left = occupied_x - occupied_width // 2
            occupied_right = occupied_x + occupied_width // 2
            
            # 检查是否重叠（包括最小距离）
            if (new_right + self.min_tree_distance > occupied_left and 
                new_left - self.min_tree_distance < occupied_right):
                return False
        return True
    
    def find_available_position(self, canvas_width, preferred_x=None):
        """寻找可用的位置"""
        tree_width = 60  # 估算的树木宽度
        
        if preferred_x and self.is_position_available(preferred_x, tree_width):
            return preferred_x
        
        # 尝试在画布上找到合适的位置
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            # 随机生成位置，但确保不在边界
            x = random.uniform(tree_width + 50, canvas_width - tree_width - 50)
            
            if self.is_position_available(x, tree_width):
                return x
            
            attempts += 1
        
        # 如果找不到随机位置，使用网格排列
        return self.find_grid_position(canvas_width, tree_width)
    
    def find_grid_position(self, canvas_width, tree_width):
        """使用网格排列找到位置"""
        spacing = tree_width + self.min_tree_distance
        start_x = spacing
        
        # 计算网格位置
        grid_positions = []
        x = start_x
        while x < canvas_width - tree_width:
            grid_positions.append(x)
            x += spacing
        
        # 找到第一个未被占用的网格位置
        for grid_x in grid_positions:
            if self.is_position_available(grid_x, tree_width):
                return grid_x
        
        # 如果所有网格位置都被占用，返回画布中心
        return canvas_width // 2

    def create_new_tree_from_recording(self):
        """从录音创建新树"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # 画布还没有准备好，延迟创建
            self.root.after(100, self.create_new_tree_from_recording)
            return
        
        # 计算树的位置 - 森林风格，所有树在同一水平线上，避免重叠
        self.tree_counter += 1
        
        # 森林底线 - 统一的地平线
        forest_ground_level = canvas_height - 40
        y = forest_ground_level  # 所有树都在同一水平线上
        
        # 智能位置分配，避免重叠
        if self.tree_counter == 1:
            # 第一棵树在中央
            preferred_x = canvas_width // 2
            x = self.find_available_position(canvas_width, preferred_x)
        else:
            # 后续树木智能分布，确保不重叠
            x = self.find_available_position(canvas_width)
        
        # 记录新树的位置
        tree_width = 60  # 估算的树木宽度
        self.tree_positions.append((x, tree_width))
        
        # 创建新树但先不添加到列表
        tree = AudioDrivenTree(self.canvas, self.renderer, self.palette, x, y, self.tree_counter)
        self.current_growing_tree = tree
        
        # 将树添加到列表
        if len(self.trees) >= self.max_trees:
            self.trees.pop(0)
        self.trees.append(tree)
        
        self.update_status()
        print(f"🌱 开始种植第 {self.tree_counter} 棵树，位置: ({x:.0f}, {y:.0f})")
    
    def finalize_current_tree(self):
        """完成当前树的生长"""
        if self.current_growing_tree:
            # 确保树木完全停止生长
            self.current_growing_tree.is_growing = False
            self.current_growing_tree._can_grow = False
            self.current_growing_tree.stop_growing()
            
            if self.audio_samples_buffer:
                # 根据录音数据分析树的最终特征
                audio_features = self.analyze_audio_features(self.audio_samples_buffer)
                self.current_growing_tree.apply_audio_features(audio_features)
                print(f"🌳 第 {self.current_growing_tree.tree_id} 棵树生长完成，特征: {audio_features}")
        
        self.current_growing_tree = None
        self.audio_samples_buffer = []
    
    def analyze_audio_features(self, audio_samples):
        """分析音频样本，提取特征"""
        if not audio_samples:
            return {
                'volume': 0.3,
                'energy': 0.3,
                'frequency': 0.5,
                'variation': 0.3
            }
        
        # 将所有音频样本合并
        all_samples = []
        for sample_array in audio_samples:
            all_samples.extend(sample_array)
        
        if not all_samples:
            return {
                'volume': 0.3,
                'energy': 0.3,
                'frequency': 0.5,
                'variation': 0.3
            }
        
        try:
            # 音量 (最大振幅)
            volume = min(1.0, max(abs(x) for x in all_samples) * 3)
            
            # 能量 (RMS)
            energy = min(1.0, math.sqrt(sum(x*x for x in all_samples) / len(all_samples)) * 5)
            
            # 频率特征 (零交叉率的简化版本)
            zero_crossings = sum(1 for i in range(1, len(all_samples)) 
                               if all_samples[i] * all_samples[i-1] < 0)
            frequency = min(1.0, zero_crossings / len(all_samples) * 20)
            
            # 变化度 (标准差)
            mean_val = sum(all_samples) / len(all_samples)
            variance = sum((x - mean_val)**2 for x in all_samples) / len(all_samples)
            variation = min(1.0, math.sqrt(variance) * 4)
            
            return {
                'volume': volume,
                'energy': energy,
                'frequency': frequency,
                'variation': variation
            }
        except Exception as e:
            print(f"音频分析错误: {e}")
            return {
                'volume': 0.5,
                'energy': 0.5,
                'frequency': 0.5,
                'variation': 0.5
            }
    

    
    def clear_canvas(self):
        """清空画布"""
        self.canvas.delete("tree")
        # 删除所有树木标签
        for i in range(1, self.tree_counter + 1):
            self.canvas.delete(f"tree_{i}")
        
        self.trees.clear()
        self.tree_counter = 0
        self.current_growing_tree = None
        self.is_recording_for_tree = False
        self.audio_samples_buffer = []
        self.tree_positions.clear()  # 清空位置记录
        self.update_status()
    
    def update_background(self):
        """更新背景"""
        if self.use_custom_background and self.custom_background:
            bg_color = self.custom_background
        else:
            bg_color = random.choice(self.palette.background_colors)
        
        self.canvas.config(bg=bg_color)
        
        # 更新背景颜色显示
        if hasattr(self, 'bg_color_display'):
            self.bg_color_display.config(bg=bg_color)
    
    def update_status(self):
        """更新状态栏"""
        bg_status = "自定义背景" if self.use_custom_background else "默认背景"
        self.status_label.config(
            text=f"🎨 当前风格: {self.palette.scheme_name} | {bg_status} | 树木数量: {len(self.trees)}/{self.max_trees}"
        )
    
    def start_animation(self):
        """开始动画循环"""
        self.animation_loop()
    
    def animation_loop(self):
        """动画循环"""
        if not self.animation_active:
            return
        
        # 更新音频波形显示
        if self.audio_processor and self.waveform_display:
            latest_waveform = self.audio_processor.get_latest_waveform()
            self.waveform_display.update_waveform(latest_waveform)
            self.waveform_display.draw()
            
            if self.audio_processor.is_recording:
                self.update_audio_features_display(latest_waveform)
                # 收集音频样本用于分析 - 限制缓冲区大小防止内存泄漏
                if latest_waveform and self.is_recording_for_tree:
                    self.audio_samples_buffer.append(latest_waveform.copy())
                    # 限制缓冲区最大大小，避免内存过度使用
                    if len(self.audio_samples_buffer) > 100:  # 只保留最近100个样本
                        self.audio_samples_buffer.pop(0)
        
        # 更新树木生长 - 严格控制生长权限和绘制优化
        trees_need_redraw = False
        
        for tree in self.trees:
            # 只有当前正在录音的树才会生长
            if isinstance(tree, AudioDrivenTree):
                if tree == self.current_growing_tree and self.is_recording_for_tree:
                    tree.is_growing = True
                    tree._can_grow = True  # 明确授予生长权限
                else:
                    tree.is_growing = False
                    tree._can_grow = False  # 明确撤销生长权限
                    # 确保非活动树完全停止生长
                    if tree != self.current_growing_tree:
                        tree.stop_growing()
            
            # 只有生长中的树或风效果变化的树才重绘
            if tree.update_growth():
                if tree.is_growing or (hasattr(tree, 'wind_time') and int(tree.wind_time * 10) % 3 == 0):
                    tree.draw()
                    trees_need_redraw = True
        
        # 性能优化：定期垃圾回收
        self.animation_frame_count += 1
        if self.animation_frame_count % self.gc_interval == 0:
            gc.collect()  # 定期清理内存
        
        # 降低更新频率以减少卡顿 (从50ms提升到100ms)
        self.root.after(100, self.animation_loop)
    
    def update_audio_features_display(self, waveform_data):
        """更新音频特征显示"""
        if not waveform_data:
            return
        
        try:
            volume = max(abs(x) for x in waveform_data) if waveform_data else 0
            energy = sum(x*x for x in waveform_data) / len(waveform_data) if waveform_data else 0
            
            # 计算零交叉率 (频率指示)
            zero_crossings = sum(1 for i in range(1, len(waveform_data)) 
                               if waveform_data[i] * waveform_data[i-1] < 0)
            frequency_indicator = zero_crossings / len(waveform_data) if waveform_data else 0
            
            if self.current_growing_tree:
                tree_type_names = {
                    'willow': '垂柳', 'maple': '枫树', 'pine': '松树', 
                    'oak': '橡树', 'cherry': '樱花'
                }
                tree_type_name = tree_type_names.get(self.current_growing_tree.tree_type, '未知')
                current_tree_text = f"第 {self.tree_counter} 棵树 ({tree_type_name})"
            else:
                current_tree_text = "无"
            
            feature_text = (f"🎤 录音中 - {current_tree_text}\n"
                          f"音量: {volume:.3f}\n"
                          f"能量: {energy:.3f}\n"
                          f"频率: {frequency_indicator:.3f}\n"
                          f"样本数: {len(self.audio_samples_buffer)}")
            
            self.audio_features_label.config(text=feature_text)
        except Exception as e:
            print(f"特征显示错误: {e}")
    
    def save_artwork(self):
        """保存艺术作品"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".eps",
                filetypes=[("EPS files", "*.eps"), ("All files", "*.*")]
            )
            if filename:
                self.canvas.postscript(file=filename)
                messagebox.showinfo("保存成功", f"艺术作品已保存至: {filename}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存时发生错误: {e}")
    
    def choose_custom_background(self):
        """选择自定义背景颜色"""
        color = colorchooser.askcolor(title="选择背景颜色")
        if color[1]:  # 如果用户选择了颜色
            self.custom_background = color[1]
            self.use_custom_background = True
            self.update_background()
            self.update_status()
    
    def set_preset_background(self, color):
        """设置预设背景颜色"""
        self.custom_background = color
        self.use_custom_background = True
        self.update_background()
        self.update_status()
    
    def reset_background(self):
        """重置到默认背景"""
        self.use_custom_background = False
        self.custom_background = None
        self.update_background()
        self.update_status()
    
    def cleanup(self):
        """清理资源"""
        self.animation_active = False
        if self.audio_processor:
            self.audio_processor.cleanup()

def main():
    """主函数"""
    print("🎨 启动 Echo Garden Multi-Style - 多风格艺术主题版 🎨")
    print("✨ 支持6种艺术风格：点阵、字符、数字、马赛克、波普、中国风")
    
    root = tk.Tk()
    app = EchoGardenMultiStyle(root)
    
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
        app.cleanup()

if __name__ == "__main__":
    main()
