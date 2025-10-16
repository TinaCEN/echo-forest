#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden - Interactive Generative Art
Generate tree artwork through real-time microphone input

Features:
- Mouse Click: Plant seeds, generate random trees
- Keyboard 1/2/3: Switch themes (warm/cool/mono)
- Keyboard C: Clear canvas
- Keyboard S: Save as .eps file
- Real-time Audio: Microphone input with real-time waveform display and tree generation
- Diverse Trees: Various random tree styles generation
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
    print("⚠️  PyAudio not installed, using simulated audio mode")
    print("   To enable real microphone, run: pip install pyaudio")


class ColorTheme:
    """Gradient Color Theme Class"""
    
    WARM = {
        'name': 'Warm Gradient',
        'trunk': ['#8B4513', '#A0522D', '#CD853F', '#D2691E', '#DEB887'],
        'leaves': [
            '#FF6B35', '#FF7F50', '#FF8C69', '#FFA500', '#FFB347',
            '#F7931E', '#FFD700', '#FFFF99', '#FFEFD5', '#FFE4B5'
        ],
        'gradients': [
            ('#FF6B35', '#FFD700'),  # 橙到金
            ('#FF7F50', '#FFFF99'),  # 珊瑚到黄
            ('#FFA500', '#FFE4B5')   # 橙到米色
        ],
        'background': 'linear-gradient(135deg, #FFF8DC, #FFEBCD)',
        'bg_color': '#FFF8DC',
        'grass_base': '#9ACD32'  # 黄绿色草地
    }
    
    COOL = {
        'name': 'Cool Gradient', 
        'trunk': ['#2F4F4F', '#708090', '#778899', '#87CEEB', '#B0C4DE'],
        'leaves': [
            '#00CED1', '#20B2AA', '#48D1CC', '#87CEEB', '#B0E0E6',
            '#4682B4', '#5F9EA0', '#6495ED', '#7B68EE', '#9370DB'
        ],
        'gradients': [
            ('#00CED1', '#87CEEB'),  # 暗绿松石到天蓝
            ('#20B2AA', '#B0E0E6'),  # 浅海洋绿到粉蓝
            ('#4682B4', '#9370DB')   # 钢蓝到紫
        ],
        'background': 'linear-gradient(135deg, #F0F8FF, #E6F3FF)', 
        'bg_color': '#F0F8FF',
        'grass_base': '#4682B4'  # 钢蓝色草地
    }
    
    MONO = {
        'name': 'Galaxy Gradient',
        'trunk': ['#2F2F2F', '#4F4F4F', '#696969', '#808080', '#A9A9A9'],
        'leaves': [
            '#696969', '#778899', '#808080', '#A9A9A9', '#C0C0C0',
            '#D3D3D3', '#DCDCDC', '#E5E5E5', '#F0F0F0', '#F8F8FF'
        ],
        'gradients': [
            ('#696969', '#D3D3D3'),  # 暗灰到浅灰
            ('#808080', '#F0F0F0'),  # 灰到白
            ('#A9A9A9', '#F8F8FF')   # 深灰到幽灵白
        ],
        'background': 'linear-gradient(135deg, #F5F5F5, #FAFAFA)',
        'bg_color': '#F5F5F5',
        'grass_base': '#808080'  # 灰色草地
    }
    
    SUNSET = {
        'name': 'Sunset Gradient',
        'trunk': ['#8B4513', '#CD853F', '#DEB887', '#F4A460', '#FFDAB9'],
        'leaves': [
            '#FF69B4', '#FF1493', '#FF6347', '#FF4500', '#FF8C00',
            '#FFD700', '#FFFF00', '#ADFF2F', '#32CD32', '#00FF7F'
        ],
        'gradients': [
            ('#FF69B4', '#FFD700'),  # 粉红到金
            ('#FF1493', '#ADFF2F'),  # 深粉到绿黄
            ('#FF4500', '#32CD32')   # 橙红到绿
        ],
        'background': 'linear-gradient(135deg, #FFE4E1, #FFF0F5)',
        'bg_color': '#FFE4E1',
        'grass_base': '#32CD32'  # 酸橙绿草地
    }
    
    AURORA = {
        'name': 'Aurora Gradient',
        'trunk': ['#2F4F4F', '#483D8B', '#6A5ACD', '#9370DB', '#BA55D3'],
        'leaves': [
            '#00FFFF', '#00BFFF', '#1E90FF', '#0000FF', '#4169E1',
            '#9370DB', '#8A2BE2', '#9400D3', '#FF00FF', '#FF1493'
        ],
        'gradients': [
            ('#00FFFF', '#9370DB'),  # 青到紫
            ('#1E90FF', '#FF00FF'),  # 蓝到洋红
            ('#0000FF', '#FF1493')   # 蓝到粉红
        ],
        'background': 'linear-gradient(135deg, #191970, #000080)',
        'bg_color': '#191970',
        'grass_base': '#00FFFF'  # 青色草地
    }


class RealTimeAudioProcessor:
    """Real-time Audio Processor"""
    
    def __init__(self):
        self.chunk = 1024
        self.format = None
        self.channels = 1
        self.rate = 44100
        self.audio = None
        self.stream = None
        self.is_recording = False
        self.audio_buffer = deque(maxlen=100)
        
        if AUDIO_AVAILABLE:
            try:
                self.audio = pyaudio.PyAudio()
                self.format = pyaudio.paInt16
                print("✅ Audio device initialized successfully")
            except Exception as e:
                print(f"❌ 音频初始化失败: {e}")
                self.audio = None
    
    def start_recording(self):
        """开始录音"""
        if not self.audio or self.is_recording:
            return False
        
        try:
            # 首先尝试获取默认输入设备
            device_info = self.audio.get_default_input_device_info()
            print(f"🎤 Using audio device: {device_info['name']}")
            
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index=device_info['index']
            )
            self.stream.start_stream()
            self.is_recording = True
            print("🎤 Starting real-time recording")
            
            # 启动轮询线程来读取音频数据
            self._start_audio_thread()
            return True
        except Exception as e:
            print(f"❌ 录音启动失败: {e}")
            print("尝试不指定设备...")
            try:
                # 备用方案：不指定设备
                self.stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk
                )
                self.stream.start_stream()
                self.is_recording = True
                print("🎤 Starting real-time recording (fallback)")
                self._start_audio_thread()
                return True
            except Exception as e2:
                print(f"❌ 备用方案也失败: {e2}")
                return False
    
    def _start_audio_thread(self):
        """启动音频读取线程"""
        def audio_loop():
            while self.is_recording:
                try:
                    if self.stream and self.stream.is_active():
                        data = self.stream.read(self.chunk, exception_on_overflow=False)
                        audio_data = struct.unpack(f'{len(data)//2}h', data)
                        self.audio_buffer.append(audio_data)
                        # print(f"📊 音频数据长度: {len(audio_data)}, RMS: {math.sqrt(sum(x*x for x in audio_data)/len(audio_data))}")
                except Exception as e:
                    print(f"⚠️ 音频读取错误: {e}")
                    break
                time.sleep(0.01)  # 10ms间隔
        
        self.audio_thread = threading.Thread(target=audio_loop, daemon=True)
        self.audio_thread.start()
    
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            print("🔇 Recording stopped")
    

    
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


class SimulatedAudioProcessor:
    """Simulated Audio Processor - used when PyAudio is not available"""
    
    def __init__(self):
        self.is_recording = False
        self.sim_time = 0
    
    def start_recording(self):
        self.is_recording = True
        return True
    
    def stop_recording(self):
        self.is_recording = False
    
    def get_current_features(self):
        """生成模拟的音频特征"""
        self.sim_time += 0.1
        return {
            'volume': 0.5 + 0.3 * math.sin(self.sim_time),
            'pitch': 0.4 + 0.4 * math.sin(self.sim_time * 0.7),
            'energy': 0.3 + 0.4 * math.sin(self.sim_time * 1.3),
            'raw_data': []
        }
    
    def get_waveform_data(self):
        """生成模拟的波形数据"""
        return [math.sin(i * 0.2 + self.sim_time) * (0.5 + 0.5 * math.sin(self.sim_time * 0.3)) 
                for i in range(100)]


class SoundSimulator:
    """Sound Simulator - for text input simulation"""
    
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


class Grass:
    """Ground Grass Class"""
    
    def __init__(self, x, y, tree_colors, theme):
        self.x = x
        self.y = y
        self.tree_colors = tree_colors  # 附近树木的颜色
        self.theme = theme
        
        # 草地属性
        self.height = random.uniform(8, 15)
        self.width = random.uniform(3, 8)
        self.sway = 0.0
        self.growth = 0.0
        self.is_growing = True
        
        # 生成与树木相关但略有差异的颜色
        self.color = self._generate_grass_color()
        
    def _generate_grass_color(self):
        """基于附近树木颜色生成草地颜色"""
        if not self.tree_colors:
            # 如果没有树木颜色，使用主题的基本绿色
            return self.theme.get('grass_base', '#228B22')
        
        # 从附近树木颜色中选择一个作为基础
        base_color = random.choice(self.tree_colors)
        
        # 解析颜色
        if base_color.startswith('#'):
            try:
                r = int(base_color[1:3], 16)
                g = int(base_color[3:5], 16)  
                b = int(base_color[5:7], 16)
                
                # 增加绿色成分，调整颜色使其更像草地
                g = min(255, int(g * 1.2 + 30))
                r = max(0, int(r * 0.7))
                b = max(0, int(b * 0.6))
                
                # 添加随机变化
                r = max(0, min(255, r + random.randint(-20, 20)))
                g = max(0, min(255, g + random.randint(-15, 15)))
                b = max(0, min(255, b + random.randint(-20, 20)))
                
                return f'#{r:02x}{g:02x}{b:02x}'
            except:
                return '#228B22'  # 默认绿色
        
        return '#228B22'
    
    def update(self, dt):
        """更新草地动画"""
        if self.is_growing and self.growth < 1.0:
            self.growth = min(1.0, self.growth + dt * 1.2)
            if self.growth >= 1.0:
                self.is_growing = False
        
        # 轻微摆动
        self.sway += dt * 3
        
    def draw(self, canvas):
        """绘制草地"""
        if self.growth <= 0:
            return
            
        # 计算摆动偏移
        sway_offset = math.sin(self.sway) * 2
        
        # 绘制草叶
        current_height = self.height * self.growth
        
        # 绘制多根草叶
        for i in range(3):
            offset_x = (i - 1) * self.width * 0.3
            leaf_x = self.x + offset_x + sway_offset * (0.5 + i * 0.2)
            leaf_height = current_height * (0.8 + i * 0.1)
            
            canvas.create_line(
                self.x + offset_x, self.y,
                leaf_x, self.y - leaf_height,
                width=max(1, int(2 * self.growth)),
                fill=self.color,
                capstyle=tk.ROUND
            )

class Tree:
    """Diverse Tree Class"""
    
    TREE_STYLES = ['classic', 'weeping', 'bushy', 'tall', 'wide', 'spiral', 'fractal']
    
    def __init__(self, x, y, theme, audio_features=None, style=None):
        self.x = x
        self.y = y
        self.original_x = x  # 记录原始位置
        self.original_y = y
        self.theme = theme
        self.audio_features = audio_features or {
            'volume': random.uniform(0.3, 0.8),
            'pitch': random.uniform(0.2, 0.8),
            'energy': random.uniform(0.4, 0.7)
        }
        
        # 随机选择树木样式 (必须在生成声音代码之前)
        self.style = style or random.choice(self.TREE_STYLES)
        
        # 生成唯一的声音代码
        self.sound_code = self._generate_sound_code()
        
        # 根据音频特征和样式决定树的属性
        self._init_tree_properties()
        
        self.growth = 0.0
        self.is_growing = True
        self.swaying = 0.0
        
        # 拖拽相关属性
        self.is_dragging = False
        self.is_hovered = False
        self.bounding_box = None  # 碰撞检测框
        
        # 渐变颜色属性
        self.gradient_colors = self._select_gradient_colors()
    
    def _generate_sound_code(self):
        """生成基于音频特征的声音代码"""
        volume = self.audio_features['volume']
        pitch = self.audio_features['pitch'] 
        energy = self.audio_features['energy']
        
        # 将音频特征转换为代码
        vol_code = f"V{int(volume * 99):02d}"
        pitch_code = f"P{int(pitch * 99):02d}"  
        energy_code = f"E{int(energy * 99):02d}"
        
        # 生成风格代码
        style_codes = {
            'classic': 'CL', 'weeping': 'WP', 'bushy': 'BS',
            'tall': 'TL', 'wide': 'WD', 'spiral': 'SP', 'fractal': 'FR'
        }
        style_code = style_codes.get(self.style, 'XX')
        
        # 生成时间戳代码
        import time
        timestamp = int(time.time() * 1000) % 10000
        
        return f"{style_code}-{vol_code}-{pitch_code}-{energy_code}-{timestamp:04d}"
    
    def _select_gradient_colors(self):
        """选择渐变颜色"""
        if 'gradients' in self.theme:
            return random.choice(self.theme['gradients'])
        else:
            # 备用渐变
            return (random.choice(self.theme['leaves']), random.choice(self.theme['leaves']))
    
    def _init_tree_properties(self):
        """根据音频特征和样式初始化树的属性"""
        volume = self.audio_features['volume']
        pitch = self.audio_features['pitch']
        energy = self.audio_features['energy']
        
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
            
        elif self.style == 'weeping':
            self.height = base_height * 0.8
            self.branches = base_branches + 2
            self.angle_variance = base_angle * 0.5
            self.trunk_ratio = 0.4
            self.leaf_density = 1.5
            self.weeping_factor = 0.7
            
        elif self.style == 'bushy':
            self.height = base_height * 0.6
            self.branches = base_branches + 4
            self.angle_variance = base_angle * 1.5
            self.trunk_ratio = 0.2
            self.leaf_density = 2.0
            
        elif self.style == 'tall':
            self.height = base_height * 1.4
            self.branches = max(2, base_branches - 2)
            self.angle_variance = base_angle * 0.7
            self.trunk_ratio = 0.5
            self.leaf_density = 0.7
            
        elif self.style == 'wide':
            self.height = base_height * 0.9
            self.branches = base_branches + 3
            self.angle_variance = base_angle * 1.3
            self.trunk_ratio = 0.25
            self.leaf_density = 1.2
            
        elif self.style == 'spiral':
            self.height = base_height * 1.1
            self.branches = base_branches
            self.angle_variance = base_angle
            self.trunk_ratio = 0.3
            self.leaf_density = 1.0
            self.spiral_factor = pitch * 360
            
        elif self.style == 'fractal':
            self.height = base_height
            self.branches = max(2, int(base_branches * 0.7))
            self.angle_variance = base_angle * 0.8
            self.trunk_ratio = 0.35
            self.leaf_density = 0.8
            self.fractal_depth = int(4 + energy * 3)
        
        # 动画属性 - 减缓生长速度
        self.growth_speed = 0.008 + energy * 0.015
        self.sway_speed = 0.5 + pitch * 1.5
        self.sway_amplitude = volume * 5
    
    def contains_point(self, x, y):
        """检查点是否在树木范围内"""
        if self.bounding_box is None:
            return False
        
        min_x, min_y, max_x, max_y = self.bounding_box
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def start_drag(self, x, y):
        """开始拖拽"""
        self.is_dragging = True
        self.drag_offset_x = x - self.x
        self.drag_offset_y = y - self.y
    
    def drag_to(self, x, y):
        """拖拽到指定位置"""
        if self.is_dragging:
            self.x = x - self.drag_offset_x
            self.y = y - self.drag_offset_y
    
    def end_drag(self):
        """结束拖拽"""
        self.is_dragging = False
    
    def set_hover(self, hover):
        """设置悬停状态"""
        self.is_hovered = hover
    
    def get_info_text(self):
        """Get tree information text"""
        info = [
            f"Sound Code: {self.sound_code}",
            f"Style: {self.style.upper()}",
            f"Volume: {self.audio_features['volume']:.2f}",
            f"Pitch: {self.audio_features['pitch']:.2f}",
            f"Energy: {self.audio_features['energy']:.2f}",
            f"Height: {self.height:.0f}px",
            f"Branches: {self.branches}"
        ]
        return "\n".join(info)
    
    def update(self, dt, audio_features=None):
        """更新树的成长和动画"""
        if self.is_growing:
            self.growth += self.growth_speed * dt
            if self.growth >= 1.0:
                self.growth = 1.0
                self.is_growing = False
        
        self.swaying += self.sway_speed * dt
        
        if audio_features and not self.is_growing:
            volume = audio_features.get('volume', 0)
            self.sway_amplitude = volume * 8
    
    def _hex_to_rgb(self, hex_color):
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb):
        """将RGB颜色转换为十六进制"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _interpolate_color(self, color1, color2, factor):
        """在两个颜色之间插值"""
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        interpolated = tuple(
            int(rgb1[i] + (rgb2[i] - rgb1[i]) * factor)
            for i in range(3)
        )
        return self._rgb_to_hex(interpolated)
    
    def _get_gradient_color(self, position_factor):
        """根据位置获取渐变颜色"""
        color1, color2 = self.gradient_colors
        return self._interpolate_color(color1, color2, position_factor)

    def draw(self, canvas):
        """绘制多样化树木"""
        if self.growth <= 0:
            return
        
        # 计算摇摆偏移
        sway_offset = math.sin(self.swaying) * self.sway_amplitude * (1 if self.is_growing else 0.3)
        
        # 绘制树干
        trunk_height = self.height * self.trunk_ratio * self.growth
        trunk_color = self._get_gradient_color(0.2)  # 使用渐变色
        trunk_width = max(1, int(12 * self.growth * (1 + self.audio_features['volume'] * 0.5)))
        
        trunk_start_x = self.x
        trunk_start_y = self.y
        trunk_end_x = self.x + sway_offset
        trunk_end_y = self.y - trunk_height
        
        if self.style == 'spiral':
            self._draw_spiral_trunk(canvas, trunk_height, trunk_color, trunk_width, sway_offset)
        else:
            # 如果树木被悬停，添加高亮效果
            if self.is_hovered:
                canvas.create_line(
                    trunk_start_x, trunk_start_y, trunk_end_x, trunk_end_y,
                    width=trunk_width + 4, fill='gold', capstyle=tk.ROUND
                )
            
            canvas.create_line(
                trunk_start_x, trunk_start_y, trunk_end_x, trunk_end_y,
                width=trunk_width, fill=trunk_color, capstyle=tk.ROUND
            )
        
        # 更新碰撞检测框
        tree_width = max(50, self.height * 0.8)
        tree_height = self.height * self.growth
        self.bounding_box = (
            self.x - tree_width//2, self.y - tree_height,
            self.x + tree_width//2, self.y + 20
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
        
        # 移除原来的信息提示框绘制，改为在画面右下角显示
    
    def _draw_spiral_trunk(self, canvas, height, color, width, sway_offset):
        """绘制螺旋树干"""
        points = []
        steps = max(1, int(height / 5))  # Ensure steps is at least 1 to avoid division by zero
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
            
            points = []
            segments = 8
            for j in range(segments + 1):
                progress = j / segments
                
                x_offset = length * progress * math.cos(math.radians(angle))
                y_offset = -length * progress * math.sin(math.radians(angle))
                
                droop = progress * progress * self.weeping_factor * 50
                
                points.extend([
                    start_x + x_offset,
                    start_y + y_offset + droop
                ])
            
            if len(points) >= 4:
                trunk_color = random.choice(self.theme['trunk'])
                canvas.create_line(points, width=max(1, int(4 * growth)), 
                                 fill=trunk_color, smooth=True)
                
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
        
        end_x = x + length * math.cos(math.radians(angle))
        end_y = y + length * math.sin(math.radians(angle))
        
        trunk_color = random.choice(self.theme['trunk'])
        width = max(1, int((depth + 1) * growth))
        
        canvas.create_line(x, y, end_x, end_y, width=width, fill=trunk_color)
        
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
        """递归绘制树枝"""
        if branches_left <= 0 or length < 8 or depth > 5:
            self._draw_enhanced_leaves(canvas, x, y, self.style)
            return
        
        rad = math.radians(angle)
        new_x = x + length * math.cos(rad)
        new_y = y + length * math.sin(rad)
        
        trunk_color = random.choice(self.theme['trunk'])
        width = max(1, int((6 - depth) * growth))
        
        canvas.create_line(x, y, new_x, new_y, width=width, fill=trunk_color, capstyle=tk.ROUND)
        
        angle_var = self.angle_variance * (1 - depth * 0.15)
        new_length = length * random.uniform(0.6, 0.85)
        
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
    
    def _draw_info_tooltip(self, canvas):
        """绘制信息提示框"""
        info_text = self.get_info_text()
        
        # 计算提示框位置
        tooltip_x = self.x + 50
        tooltip_y = self.y - self.height * 0.8
        
        # 确保提示框不超出画布
        if tooltip_x > 600:
            tooltip_x = self.x - 200
        if tooltip_y < 50:
            tooltip_y = self.y - 50
        
        # 绘制背景框
        lines = info_text.split('\n')
        box_width = max(len(line) * 8 for line in lines) + 20
        box_height = len(lines) * 15 + 10
        
        canvas.create_rectangle(
            tooltip_x - 5, tooltip_y - 5,
            tooltip_x + box_width, tooltip_y + box_height,
            fill='lightyellow', outline='orange', width=2
        )
        
        # 绘制文本
        for i, line in enumerate(lines):
            canvas.create_text(
                tooltip_x + 5, tooltip_y + 10 + i * 15,
                text=line, anchor='nw', font=('Arial', 9),
                fill='darkblue'
            )

    def _draw_enhanced_leaves(self, canvas, x, y, style_hint=None):
        """绘制增强版渐变叶子"""
        leaf_count = int(random.randint(2, 8) * self.leaf_density)
        
        for i in range(leaf_count):
            offset_x = random.uniform(-12, 12)
            offset_y = random.uniform(-12, 12)
            
            if style_hint == 'weeping':
                offset_y += abs(offset_y) * 0.5
                size = random.uniform(2, 6)
            elif style_hint == 'fractal':
                size = random.uniform(1, 4)
            else:
                size = random.uniform(3, 7)
            
            # 使用渐变色
            position_factor = (i + random.random()) / leaf_count
            leaf_color = self._get_gradient_color(position_factor)
            
            # 添加一些随机的主题色彩
            if random.random() < 0.3:
                leaf_color = random.choice(self.theme['leaves'])
            
            leaf_shape = random.choice(['oval', 'polygon', 'star'])
            
            # 如果被悬停，增加叶子亮度
            if self.is_hovered:
                # 简单的亮度增强
                leaf_color = self._brighten_color(leaf_color)
            
            if leaf_shape == 'oval':
                canvas.create_oval(
                    x + offset_x - size, y + offset_y - size,
                    x + offset_x + size, y + offset_y + size,
                    fill=leaf_color, outline=leaf_color
                )
            elif leaf_shape == 'polygon':
                points = [
                    x + offset_x, y + offset_y - size,
                    x + offset_x - size, y + offset_y + size,
                    x + offset_x + size, y + offset_y + size
                ]
                canvas.create_polygon(points, fill=leaf_color, outline=leaf_color)
            elif leaf_shape == 'star':
                self._draw_star_leaf(canvas, x + offset_x, y + offset_y, size, leaf_color)
    
    def _brighten_color(self, color):
        """增亮颜色"""
        try:
            rgb = self._hex_to_rgb(color)
            brightened = tuple(min(255, int(c * 1.2)) for c in rgb)
            return self._rgb_to_hex(brightened)
        except:
            return color
    
    def _draw_star_leaf(self, canvas, cx, cy, size, color):
        """绘制星形叶子"""
        points = []
        for i in range(10):
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
    """Echo Garden Main Application Class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echo Garden - Real-time Audio Generative Art")
        self.root.geometry("1200x800")
        
        # 主题
        self.themes = [ColorTheme.WARM, ColorTheme.COOL, ColorTheme.MONO, ColorTheme.SUNSET, ColorTheme.AURORA]
        self.current_theme_index = 0
        self.current_theme = self.themes[self.current_theme_index]
        
        # 音频处理
        self.audio_processor = RealTimeAudioProcessor() if AUDIO_AVAILABLE else SimulatedAudioProcessor()
        
        # 树木列表
        self.trees = []
        
        # 草地列表  
        self.grasses = []
        
        # 悬浮信息显示
        self.hovered_tree = None
        
        # 实时音频状态
        self.is_live_mode = False
        self.last_audio_features = None
        
        # 波形显示
        self.waveform_canvas = None
        
        # 鼠标交互
        self.dragging_tree = None
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # 自动种树相关
        self.auto_plant_enabled = False
        self.last_auto_plant_time = 0
        self.volume_threshold = 0.3  # 音量阈值
        self.auto_plant_interval = 2.0  # 自动种树间隔（秒）
        
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
            text=f"Current Theme: {self.current_theme['name']}", 
            font=("Arial", 12)
        )
        self.theme_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            info_frame, 
            text="Status: Ready", 
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
        waveform_label = tk.Label(left_frame, text="Real-time Waveform", font=("Arial", 10, "bold"))
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
            text="Volume: --\nPitch: --\nEnergy: --", 
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
            bg=self.current_theme['bg_color'],
            width=950, 
            height=500
        )
        self.canvas.pack()
        
        # 控制按钮
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 实时音频按钮
        if AUDIO_AVAILABLE and hasattr(self.audio_processor, 'start_recording'):
            self.live_button = tk.Button(
                control_frame, 
                text="🎤 Start Live", 
                command=self.toggle_live_mode,
                font=("Arial", 12),
                bg='lightgreen'
            )
            self.live_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🎵 Sound Tree", 
            command=self.text_sound_plant,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        # 自动种树按钮
        self.auto_plant_button = tk.Button(
            control_frame, 
            text="🌱 Auto Plant", 
            command=self.toggle_auto_plant,
            font=("Arial", 12),
            bg='lightblue'
        )
        self.auto_plant_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🌱 Random Tree", 
            command=self.plant_random_tree,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🎨 Switch Theme", 
            command=self.switch_theme,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, 
            text="🗑️ Clear", 
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
            text="❓ Help", 
            command=self.show_help,
            font=("Arial", 12)
        ).pack(side=tk.RIGHT, padx=5)
    
    def bind_events(self):
        """绑定事件"""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
    
    def on_click(self, event):
        """处理鼠标点击事件"""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
        # 检查是否点击了树木
        clicked_tree = None
        for tree in self.trees:
            if tree.contains_point(event.x, event.y):
                clicked_tree = tree
                break
        
        if clicked_tree:
            # 开始拖拽树木
            clicked_tree.start_drag(event.x, event.y)
            self.dragging_tree = clicked_tree
        else:
            # 种植新树木
            features = self.last_audio_features if self.is_live_mode else None
            self.plant_tree_at(event.x, event.y, features)
    
    def on_drag(self, event):
        """处理拖拽事件"""
        if self.dragging_tree:
            self.dragging_tree.drag_to(event.x, event.y)
    
    def on_release(self, event):
        """处理鼠标释放事件"""
        if self.dragging_tree:
            self.dragging_tree.end_drag()
            self.dragging_tree = None
    
    def on_mouse_move(self, event):
        """处理鼠标移动事件"""
        # 更新树木悬停状态和当前悬浮的树木
        self.hovered_tree = None
        for tree in self.trees:
            is_hovering = tree.contains_point(event.x, event.y)
            tree.set_hover(is_hovering)
            if is_hovering:
                self.hovered_tree = tree
        
        # 更新鼠标样式
        hovering_any = any(tree.is_hovered for tree in self.trees)
        cursor = "hand2" if hovering_any else "arrow"
        self.canvas.config(cursor=cursor)
    
    def on_key_press(self, event):
        """处理键盘事件"""
        key = event.keysym.lower()
        
        if key in ['1', '2', '3', '4', '5']:
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
            if self.is_live_mode:
                features = self.last_audio_features
                x = random.randint(100, 850)
                y = random.randint(200, 480)
                self.plant_tree_at(x, y, features)
            else:
                self.text_sound_plant()
        elif key == 'a':  # 快捷键A切换自动种植
            self.toggle_auto_plant()
    
    def toggle_live_mode(self):
        """切换实时模式"""
        if not hasattr(self.audio_processor, 'start_recording'):
            messagebox.showwarning("警告", "实时音频不可用！")
            return
        
        if self.is_live_mode:
            # 停止实时模式
            self.audio_processor.stop_recording()
            self.is_live_mode = False
            self.live_button.config(text="🎤 Start Live", bg='lightgreen')
            self.status_label.config(text="Status: Live mode stopped")
        else:
            # 开始实时模式
            if self.audio_processor.start_recording():
                self.is_live_mode = True
                self.live_button.config(text="🔴 Stop Live", bg='lightcoral')
                
                # 显示使用提示
                self.status_label.config(text="Status: Live audio mode - Click canvas to plant or enable auto-planting")
                
                # 显示操作提示
                messagebox.showinfo(
                    "实时模式已启动", 
                    "🎤 麦克风已启用！\n\n" +
                    "现在您可以:\n" +
                    "• 发出声音后点击画布种植音频响应的树木\n" +
                    "• 点击'🌱 自动种植'按钮启用声控自动种树\n" +
                    "• 观察左侧的实时波形显示\n" +
                    "• 悬停在树木上查看声音代码"
                )
            else:
                messagebox.showerror("错误", "无法启动音频录制！")
    
    def toggle_auto_plant(self):
        """切换自动种植模式"""
        if not self.is_live_mode:
            messagebox.showwarning("提示", "请先开启实时音频模式！")
            return
        
        self.auto_plant_enabled = not self.auto_plant_enabled
        
        if self.auto_plant_enabled:
            self.auto_plant_button.config(text="🔴 Stop Auto", bg='lightcoral')
            self.status_label.config(text="Status: Auto-planting mode - Make sounds to auto-plant trees")
            messagebox.showinfo(
                "自动种植已启用",
                "🌱 自动种植模式已开启！\n\n" +
                f"当音量超过 {self.volume_threshold:.1f} 时会自动种树\n" +
                "每 {:.1f} 秒最多种植一棵树\n\n".format(self.auto_plant_interval) +
                "现在对着麦克风发出声音试试吧！"
            )
        else:
            self.auto_plant_button.config(text="🌱 Auto Plant", bg='lightblue')
            self.status_label.config(text="Status: Live audio mode - Manual mode")
    
    def plant_tree_at(self, x, y, audio_features=None):
        """在指定位置种树"""
        if y < 50:
            y = 50
        
        if audio_features is None:
            audio_features = {
                'volume': random.uniform(0.3, 0.8),
                'pitch': random.uniform(0.2, 0.8),
                'energy': random.uniform(0.4, 0.7)
            }
        
        tree = Tree(x, y, self.current_theme, audio_features)
        self.trees.append(tree)
        self.status_label.config(text=f"Status: New tree planted ({len(self.trees)} trees)")
        
        # 检查是否需要生成草地
        self.check_grass_generation()
    
    def plant_random_tree(self):
        """种植随机树"""
        x = random.randint(50, 900)
        y = random.randint(200, 480)
        self.plant_tree_at(x, y)
    
    def text_sound_plant(self):
        """通过文本输入模拟声音并种树"""
        sound_input = simpledialog.askstring(
            "Sound Input", 
            "Enter text describing the sound\n(e.g.: high pitch, low pitch, loud, soft, rhythm, melody, etc.):",
            parent=self.root
        )
        
        if sound_input is None:
            return
        
        # 分析文本输入生成音频特征
        sound_simulator = SoundSimulator()
        features = sound_simulator.analyze_text_input(sound_input)
        
        # 在随机位置种树
        x = random.randint(100, 850)
        y = random.randint(200, 480)
        
        tree = Tree(x, y, self.current_theme, features)
        self.trees.append(tree)
        
        self.status_label.config(
            text=f"Status: Sound tree planted - '{sound_input}' ({len(self.trees)} trees)"
        )
        
        # 检查是否需要生成草地
        self.check_grass_generation()
    
    def switch_theme(self):
        """切换主题"""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme = self.themes[self.current_theme_index]
        self.update_theme()
    
    def update_theme(self):
        """更新主题"""
        self.canvas.config(bg=self.current_theme['bg_color'])
        self.theme_label.config(text=f"Current Theme: {self.current_theme['name']}")
        
        # 更新现有树木的主题和渐变色
        for tree in self.trees:
            tree.theme = self.current_theme
            tree.gradient_colors = tree._select_gradient_colors()
        
        # 更新现有草地的主题颜色
        for grass in self.grasses:
            grass.theme = self.current_theme
            grass.color = grass._generate_grass_color()
        
        self.status_label.config(text=f"Status: Switched to {self.current_theme['name']}")
    
    def check_grass_generation(self):
        """检查是否需要生成草地"""
        if len(self.trees) >= 10:
            # 生成草地数量为树木数量的1/3到1/2
            target_grass_count = len(self.trees) // 2
            current_grass_count = len(self.grasses)
            
            if current_grass_count < target_grass_count:
                # 需要生成更多草地
                grass_to_generate = target_grass_count - current_grass_count
                
                for _ in range(grass_to_generate):
                    self.generate_random_grass()
    
    def generate_random_grass(self):
        """生成随机位置的草地"""
        # 在画布底部生成草地
        x = random.randint(20, 980)
        y = random.randint(450, 550)  # 地面区域
        
        # 收集附近树木的颜色
        nearby_tree_colors = []
        for tree in self.trees:
            # 检查树木是否在草地附近
            distance = math.sqrt((tree.x - x)**2 + (tree.y - y)**2)
            if distance < 150:  # 150像素范围内
                # 获取树木的叶子颜色
                if hasattr(tree, 'leaves_colors') and tree.leaves_colors:
                    nearby_tree_colors.extend(tree.leaves_colors[:2])  # 取前两个颜色
                elif hasattr(tree, 'trunk_color'):
                    nearby_tree_colors.append(tree.trunk_color)
        
        # 如果没有找到附近的树木颜色，使用当前主题的叶子颜色
        if not nearby_tree_colors and self.current_theme.get('leaves'):
            nearby_tree_colors = self.current_theme['leaves'][:3]
        
        grass = Grass(x, y, nearby_tree_colors, self.current_theme)
        self.grasses.append(grass)
    
    def clear_garden(self):
        """清空花园"""
        self.trees.clear()
        self.grasses.clear()  # 同时清空草地
        self.canvas.delete("all")
        self.status_label.config(text="Status: Garden cleared")
    
    def save_art(self):
        """保存艺术作品为 EPS 文件"""
        if not self.trees:
            messagebox.showwarning("Warning", "No trees to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("EPS files", "*.eps"), ("All files", "*.*")],
            title="保存 Echo Garden 作品"
        )
        
        if filename:
            try:
                self.canvas.postscript(file=filename)
                self.status_label.config(text=f"Status: Saved to {filename}")
                messagebox.showinfo("成功", f"作品已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def update_waveform_display(self):
        """更新波形显示"""
        if not self.waveform_canvas:
            return
        
        self.waveform_canvas.delete("all")
        
        canvas_width = 200
        canvas_height = 400
        center_y = canvas_height // 2
        
        # 始终绘制中线
        self.waveform_canvas.create_line(
            0, center_y, canvas_width, center_y,
            fill='gray', width=1
        )
        
        # 获取波形数据和音频特征
        if self.is_live_mode or not AUDIO_AVAILABLE:
            waveform_data = self.audio_processor.get_waveform_data()
            features = self.audio_processor.get_current_features()
            self.last_audio_features = features
            
            # 显示调试信息
            buffer_size = len(self.audio_processor.audio_buffer) if hasattr(self.audio_processor, 'audio_buffer') else 0
            recording_status = "录音中" if getattr(self.audio_processor, 'is_recording', False) else "未录音"
            
            # 绘制波形
            if waveform_data and len(waveform_data) > 0:
                points = []
                for i, value in enumerate(waveform_data[:100]):
                    x = i * (canvas_width / 100)
                    y = center_y - (value * center_y * 0.8)
                    points.extend([x, y])
                
                if len(points) >= 4:
                    self.waveform_canvas.create_line(
                        points, fill='lime', width=2, smooth=True
                    )
            else:
                # 如果没有数据，显示一条直线
                self.waveform_canvas.create_line(
                    0, center_y, canvas_width, center_y,
                    fill='red', width=2
                )
            
            # 更新音频信息显示
            info_text = f"Volume: {features['volume']:.2f}\n"
            info_text += f"Pitch: {features['pitch']:.2f}\n"
            info_text += f"Energy: {features['energy']:.2f}\n"
            info_text += f"Status: {recording_status}\n"
            info_text += f"Buffer: {buffer_size}"
            
            self.audio_info_label.config(text=info_text)
        else:
            # 非实时模式，显示静态信息
            self.audio_info_label.config(text="Volume: --\nPitch: --\nEnergy: --\nStatus: Offline\nBuffer: --")
    
    def animate(self):
        """动画循环"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # 更新波形显示
        self.update_waveform_display()
        
        # 自动种植检查
        if self.auto_plant_enabled and self.is_live_mode and self.last_audio_features:
            self.check_auto_plant(current_time)
        
        # 更新树木成长
        for tree in self.trees:
            tree.update(dt, self.last_audio_features)
        
        # 更新草地成长
        for grass in self.grasses:
            grass.update(dt)
        
        # 重绘画布
        self.redraw()
        
        # 继续动画循环
        self.root.after(50, self.animate)
    
    def check_auto_plant(self, current_time):
        """检查是否需要自动种植"""
        # 检查时间间隔
        if current_time - self.last_auto_plant_time < self.auto_plant_interval:
            return
        
        # 检查音量阈值
        volume = self.last_audio_features.get('volume', 0)
        if volume > self.volume_threshold:
            # 在随机位置种植树木
            x = random.randint(100, 850)
            y = random.randint(200, 480)
            
            self.plant_tree_at(x, y, self.last_audio_features)
            self.last_auto_plant_time = current_time
            
            # 更新状态显示
            self.status_label.config(
                text=f"Status: Auto-planted - Volume {volume:.2f} > {self.volume_threshold:.1f} - Tree planted!"
            )
    
    def redraw(self):
        """重绘画布"""
        self.canvas.delete("all")
        
        # 先绘制草地（在树木后面）
        for grass in self.grasses:
            grass.draw(self.canvas)
        
        # 绘制所有树木
        for tree in self.trees:
            tree.draw(self.canvas)
        
        # 在右下角绘制悬浮树木信息
        if self.hovered_tree and self.hovered_tree.growth > 0.3:
            self._draw_tree_info_panel()
    
    def _draw_tree_info_panel(self):
        """在画面右下角绘制树木信息面板"""
        if not self.hovered_tree:
            return
        
        # 获取树木信息
        info_text = self.hovered_tree.get_info_text()
        lines = info_text.split('\n')
        
        # 计算面板尺寸
        font_size = 10
        line_height = 14
        char_width = 8
        max_width = max(len(line) * char_width for line in lines)
        panel_width = max_width + 20
        panel_height = len(lines) * line_height + 20
        
        # 计算右下角位置（留出边距）
        canvas_width = self.canvas.winfo_width() or 950  # 默认宽度
        canvas_height = self.canvas.winfo_height() or 550  # 默认高度
        
        panel_x = canvas_width - panel_width - 15
        panel_y = canvas_height - panel_height - 15
        
        # 绘制背景面板
        self.canvas.create_rectangle(
            panel_x, panel_y,
            panel_x + panel_width, panel_y + panel_height,
            fill='#F0F8FF', outline='#4682B4', width=2,
            tags="info_panel"
        )
        
        # 绘制信息文本
        for i, line in enumerate(lines):
            text_y = panel_y + 10 + i * line_height
            self.canvas.create_text(
                panel_x + 10, text_y,
                text=line, anchor="nw",
                fill='#2F4F4F', font=('Arial', font_size),
                tags="info_panel"
            )
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🌳 Echo Garden - Real-time Audio Generative Art 🌳

🎮 Controls:
• 🎤 Live Mode: Enable microphone real-time monitoring, waveform display on left
• 🌱 Auto Plant: Enable automatic tree planting when sound exceeds threshold
• Mouse Click: Plant new trees (empty space) or drag existing trees
• 🎵 Sound Tree: Input text to describe sound characteristics
• Keyboard 1-5: Switch gradient themes
  1=Warm Gradient 2=Cool Gradient 3=Galaxy Gradient 4=Sunset Gradient 5=Aurora Gradient
• Keyboard A: Toggle auto-planting mode
• Keyboard C: Clear entire garden
• Keyboard S: Save current artwork as EPS file
• Space/Enter: Quick plant tree

🎨 New Features:
✨ Gradient Colors: Each tree has beautiful gradient leaves
🏷️ Sound Codes: Hover to show unique sound ID of trees
🖱️ Drag Function: Freely drag trees to rearrange layout
💡 Smart Tips: Hover to display complete tree information

🌳 Tree Styles:
🌿 Classic: Traditional symmetric tree  🌲 Weeping: Drooping elegant branches
🌳 Bushy: Low dense branching  🌴 Tall: Upright slender growth  
🌰 Wide: Horizontally spreading lush  🌀 Spiral: Rotating upward form
❄️ Fractal: Mathematical fractal structure

🎵 Sound Code Format:
Style-Volume-Pitch-Energy-Timestamp (e.g.: CL-V75-P82-E64-1234)

Start creating your sound garden! 🎶🌿✨
        """
        messagebox.showinfo("Echo Garden Help", help_text)
    
    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序已退出")
        finally:
            # 清理资源
            if hasattr(self.audio_processor, 'stop_recording'):
                self.audio_processor.stop_recording()


def main():
    """主函数"""
    print("🌳 Starting Echo Garden - Real-time Audio Generative Art 🌳")
    if AUDIO_AVAILABLE:
        print("✅ PyAudio available, real-time microphone input supported")
    else:
        print("⚠️  PyAudio not available, using simulated audio mode")
        print("   To enable real-time audio, run: pip install pyaudio")
    
    app = EchoGarden()
    app.run()


if __name__ == "__main__":
    main()
