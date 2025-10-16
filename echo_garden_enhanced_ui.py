#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden Enhanced UI - 美观优化版本
Enhanced beautiful interface version of interactive generative art

New Features:
- Modern rounded buttons with gradients
- Enhanced color schemes with visual depth
- Improved typography and spacing
- Beautiful animated backgrounds
- Professional control panels
- Enhanced waveform visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
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


class ModernColorTheme:
    """现代化颜色主题类 - 增强版"""
    
    AURORA = {
        'name': '极光幻境',
        'primary': '#1a1a2e',
        'secondary': '#16213e', 
        'accent': '#0f3460',
        'highlight': '#e94560',
        'text': '#eee',
        'canvas_bg': '#0a0a23',
        'trunk': ['#2c3e50', '#34495e', '#3d566e', '#465e7d'],
        'leaves': [
            '#00d2ff', '#3a7bd5', '#667eea', '#764ba2',
            '#f093fb', '#f5576c', '#4facfe', '#00f2fe'
        ],
        'gradients': [
            ('#00d2ff', '#3a7bd5'),
            ('#667eea', '#764ba2'), 
            ('#f093fb', '#f5576c')
        ],
        'button_bg': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'panel_bg': 'rgba(26, 26, 46, 0.95)'
    }
    
    FOREST = {
        'name': '翠绿森林',
        'primary': '#0d2818',
        'secondary': '#1e4d30',
        'accent': '#2d7249', 
        'highlight': '#5cb85c',
        'text': '#f8f9fa',
        'canvas_bg': '#0f1f13',
        'trunk': ['#3e2723', '#5d4037', '#6d4c41', '#795548'],
        'leaves': [
            '#4caf50', '#66bb6a', '#81c784', '#a5d6a7',
            '#2e7d32', '#388e3c', '#43a047', '#4caf50'
        ],
        'gradients': [
            ('#4caf50', '#81c784'),
            ('#2e7d32', '#66bb6a'),
            ('#388e3c', '#a5d6a7')
        ],
        'button_bg': 'linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)',
        'panel_bg': 'rgba(13, 40, 24, 0.95)'
    }
    
    SUNSET = {
        'name': '日落晚霞',
        'primary': '#2c1810',
        'secondary': '#4a2c17',
        'accent': '#68401f',
        'highlight': '#ff7043',
        'text': '#fff8f3',
        'canvas_bg': '#1a0f08',
        'trunk': ['#5d4037', '#6d4c41', '#795548', '#8d6e63'],
        'leaves': [
            '#ff6b35', '#ff7043', '#ff8a65', '#ffab91',
            '#ff5722', '#f4511e', '#d84315', '#bf360c'
        ],
        'gradients': [
            ('#ff6b35', '#ff8a65'),
            ('#ff5722', '#ffab91'),
            ('#f4511e', '#ff7043')
        ],
        'button_bg': 'linear-gradient(135deg, #ff6b35 0%, #ff5722 100%)',
        'panel_bg': 'rgba(44, 24, 16, 0.95)'
    }
    
    OCEAN = {
        'name': '深海蓝调',
        'primary': '#0c1821',
        'secondary': '#1b2631',
        'accent': '#2a3441',
        'highlight': '#3498db',
        'text': '#ecf0f1',
        'canvas_bg': '#040810',
        'trunk': ['#2c3e50', '#34495e', '#5d6d7e', '#85929e'],
        'leaves': [
            '#3498db', '#5dade2', '#85c1e9', '#aed6f1',
            '#2980b9', '#1f618d', '#154360', '#0b2161'
        ],
        'gradients': [
            ('#3498db', '#85c1e9'),
            ('#2980b9', '#5dade2'),
            ('#1f618d', '#aed6f1')
        ],
        'button_bg': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
        'panel_bg': 'rgba(12, 24, 33, 0.95)'
    }
    
    COSMIC = {
        'name': '宇宙星河',
        'primary': '#1a0033',
        'secondary': '#2d1b45',
        'accent': '#403757',
        'highlight': '#9b59b6',
        'text': '#f4f1fb',
        'canvas_bg': '#0d001a',
        'trunk': ['#2c2c54', '#474787', '#6c5ce7', '#a29bfe'],
        'leaves': [
            '#9b59b6', '#bb74e0', '#d2a3f4', '#e8cdf0',
            '#8e44ad', '#7d3c98', '#6c3483', '#5b2c6f'
        ],
        'gradients': [
            ('#9b59b6', '#d2a3f4'),
            ('#8e44ad', '#bb74e0'),
            ('#7d3c98', '#e8cdf0')
        ],
        'button_bg': 'linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)',
        'panel_bg': 'rgba(26, 0, 51, 0.95)'
    }


class ModernButton(tk.Canvas):
    """现代化圆角渐变按钮"""
    
    def __init__(self, parent, text, command=None, width=120, height=35, 
                 bg_color='#667eea', hover_color='#764ba2', text_color='white', **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bd=0, **kwargs)
        
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
        self.draw_button()
        self.bind_events()
    
    def draw_button(self):
        """绘制圆角渐变按钮"""
        self.delete("all")
        
        # 选择颜色
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # 绘制圆角矩形背景
        self.create_rounded_rect(2, 2, self.width-4, self.height-4, 
                                radius=8, fill=color, outline='')
        
        # 添加轻微的边框效果
        if not self.is_hovered:
            self.create_rounded_rect(4, 4, self.width-2, self.height-2,
                                   radius=8, fill='', outline='#ffffff', width=1)
        
        # 绘制文本
        self.create_text(self.width//2, self.height//2, text=self.text,
                        fill=self.text_color, font=('Arial', 11, 'bold'))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """创建圆角矩形"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def bind_events(self):
        """绑定鼠标事件"""
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
    
    def on_hover(self, event):
        """鼠标悬停"""
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")
    
    def on_leave(self, event):
        """鼠标离开"""
        self.is_hovered = False
        self.draw_button()
        self.config(cursor="")
    
    def on_click(self, event):
        """按钮点击"""
        if self.command:
            self.command()


class GlassPanel(tk.Frame):
    """毛玻璃效果面板"""
    
    def __init__(self, parent, bg_color='#1a1a2e', alpha=0.9, **kwargs):
        super().__init__(parent, **kwargs)
        self.bg_color = bg_color
        self.alpha = alpha
        
        # 配置样式
        style = ttk.Style()
        style.configure("Glass.TFrame", 
                       background=bg_color,
                       borderwidth=1,
                       relief="solid")
        
        self.configure(style="Glass.TFrame", bg=bg_color)


class WaveformVisualizer(tk.Canvas):
    """现代化波形可视化器"""
    
    def __init__(self, parent, width=220, height=420, theme=None, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg='#0a0a23', highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.theme = theme or ModernColorTheme.AURORA
        self.wave_history = deque(maxlen=100)
        
    def update_waveform(self, waveform_data, audio_features):
        """更新波形显示"""
        self.delete("all")
        
        # 绘制背景渐变
        self.draw_background()
        
        # 绘制网格线
        self.draw_grid()
        
        # 绘制波形
        if waveform_data:
            self.draw_waveform(waveform_data)
            
        # 绘制音频特征可视化
        self.draw_audio_features(audio_features)
        
        # 绘制边框
        self.draw_border()
    
    def draw_background(self):
        """绘制渐变背景"""
        # 创建垂直渐变效果
        for i in range(self.height):
            alpha = i / self.height
            # 简单的颜色渐变模拟
            intensity = int(10 + alpha * 25)
            color = f'#{intensity:02x}{intensity:02x}{intensity*2:02x}'
            self.create_line(0, i, self.width, i, fill=color, width=1)
    
    def draw_grid(self):
        """绘制网格线"""
        # 垂直网格线
        for i in range(0, self.width, 40):
            self.create_line(i, 0, i, self.height, fill='#333333', width=1)
        
        # 水平网格线
        center_y = self.height // 2
        for i in range(0, self.height, 30):
            color = '#666666' if i == center_y else '#333333'
            self.create_line(0, i, self.width, i, fill=color, width=1)
    
    def draw_waveform(self, waveform_data):
        """绘制波形"""
        if len(waveform_data) < 2:
            return
            
        center_y = self.height // 2
        points = []
        
        # 处理波形数据
        for i, value in enumerate(waveform_data[:100]):
            x = i * (self.width / 100)
            y = center_y - (value * center_y * 0.7)  # 0.7是振幅系数
            points.extend([x, y])
        
            # 绘制主波形
            if len(points) >= 4:
                self.create_line(points, fill='#00ff88', width=3, smooth=True)
                
                # 添加发光效果（简化版）
                self.create_line(points, fill='#66ffaa', width=6, smooth=True)
                self.create_line(points, fill='#ccffdd', width=12, smooth=True)
    
    def draw_audio_features(self, features):
        """绘制音频特征可视化"""
        if not features:
            return
            
        volume = features.get('volume', 0)
        pitch = features.get('pitch', 0)
        energy = features.get('energy', 0)
        
        # 音量指示器（左侧）
        vol_height = volume * (self.height - 40)
        self.create_rectangle(10, self.height - 20, 25, self.height - 20 - vol_height,
                            fill='#ff6b35', outline='')
        self.create_text(18, self.height - 5, text='VOL', fill='white', font=('Arial', 8))
        
        # 音调指示器（中间）
        pitch_height = pitch * (self.height - 40)
        self.create_rectangle(self.width//2 - 8, self.height - 20, 
                            self.width//2 + 7, self.height - 20 - pitch_height,
                            fill='#3498db', outline='')
        self.create_text(self.width//2, self.height - 5, text='PITCH', fill='white', font=('Arial', 8))
        
        # 能量指示器（右侧）
        energy_height = energy * (self.height - 40)
        self.create_rectangle(self.width - 25, self.height - 20,
                            self.width - 10, self.height - 20 - energy_height,
                            fill='#9b59b6', outline='')
        self.create_text(self.width - 18, self.height - 5, text='NRG', fill='white', font=('Arial', 8))
    
    def draw_border(self):
        """绘制边框"""
        self.create_rectangle(1, 1, self.width-1, self.height-1,
                            fill='', outline='#ffffff30', width=2)


class EnhancedTree:
    """增强版树木类 - 更美观的渲染"""
    
    TREE_STYLES = ['sakura', 'pine', 'oak', 'willow', 'maple', 'bamboo', 'bonsai']
    
    def __init__(self, x, y, theme, audio_features=None, style=None):
        self.x = x
        self.y = y
        self.theme = theme
        self.audio_features = audio_features or self._get_random_features()
        self.style = style or random.choice(self.TREE_STYLES)
        
        # 生成美观的渐变色
        self.primary_gradient = random.choice(theme['gradients'])
        self.secondary_colors = theme['leaves'][:4]
        
        self._init_properties()
        
        self.growth = 0.0
        self.is_growing = True
        self.sway_phase = random.random() * math.pi * 2
        self.glow_intensity = 0.0
        
        # 生成粒子效果
        self.particles = []
        self.is_blooming = False
        
    def _get_random_features(self):
        return {
            'volume': random.uniform(0.3, 0.8),
            'pitch': random.uniform(0.2, 0.8),
            'energy': random.uniform(0.4, 0.7)
        }
    
    def _init_properties(self):
        """根据音频特征初始化属性"""
        volume = self.audio_features['volume']
        pitch = self.audio_features['pitch']
        energy = self.audio_features['energy']
        
        # 基础属性
        self.height = 60 + volume * 150
        self.trunk_width = 8 + volume * 12
        self.branch_count = int(3 + energy * 8)
        self.leaf_density = 0.8 + pitch * 1.2
        
        # 根据风格调整
        if self.style == 'sakura':  # 樱花
            self.height *= 0.9
            self.branch_angle = 35 + pitch * 30
            self.leaf_size_range = (3, 8)
            self.bloom_chance = 0.7
        elif self.style == 'pine':  # 松树
            self.height *= 1.3
            self.branch_angle = 15 + pitch * 20
            self.leaf_size_range = (1, 4)
            self.bloom_chance = 0.1
        elif self.style == 'bamboo':  # 竹子
            self.height *= 1.4
            self.trunk_width *= 0.6
            self.branch_count = int(2 + energy * 4)
            self.leaf_size_range = (2, 5)
        
        # 动画属性
        self.growth_speed = 0.01 + energy * 0.02
        self.sway_speed = 1.0 + pitch * 2.0
        self.sway_amplitude = volume * 8
    
    def update(self, dt, audio_features=None):
        """更新树木状态"""
        # 成长动画
        if self.is_growing:
            self.growth = min(1.0, self.growth + self.growth_speed * dt)
            if self.growth >= 1.0:
                self.is_growing = False
                if random.random() < getattr(self, 'bloom_chance', 0.3):
                    self.start_blooming()
        
        # 摇摆动画
        self.sway_phase += self.sway_speed * dt
        
        # 发光效果
        if audio_features:
            volume = audio_features.get('volume', 0)
            self.glow_intensity = volume * 0.8
        else:
            self.glow_intensity *= 0.95  # 逐渐消失
        
        # 更新粒子效果
        self.update_particles(dt)
    
    def start_blooming(self):
        """开始开花效果"""
        self.is_blooming = True
        # 生成花瓣粒子
        for _ in range(8):
            particle = {
                'x': self.x + random.uniform(-30, 30),
                'y': self.y - self.height * 0.8 + random.uniform(-20, 20),
                'vx': random.uniform(-15, 15),
                'vy': random.uniform(-5, -15),
                'life': 1.0,
                'size': random.uniform(2, 5),
                'color': random.choice(self.secondary_colors)
            }
            self.particles.append(particle)
    
    def update_particles(self, dt):
        """更新粒子效果"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt * 60
            particle['y'] += particle['vy'] * dt * 60
            particle['vy'] += 20 * dt  # 重力
            particle['life'] -= dt * 0.5
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, canvas):
        """绘制增强版树木"""
        if self.growth <= 0:
            return
        
        # 计算摇摆
        sway_x = math.sin(self.sway_phase) * self.sway_amplitude * self.growth
        
        # 绘制发光效果
        if self.glow_intensity > 0.1:
            self.draw_glow_effect(canvas, sway_x)
        
        # 绘制树干
        self.draw_trunk(canvas, sway_x)
        
        # 绘制树枝和叶子
        if self.growth > 0.3:
            self.draw_branches(canvas, sway_x)
        
        # 绘制粒子效果
        self.draw_particles(canvas)
    
    def draw_glow_effect(self, canvas, sway_x):
        """绘制发光效果"""
        glow_radius = int(30 * self.glow_intensity)
        glow_color = self.primary_gradient[0]
        
        # 创建多层发光 - 使用简化的颜色
        colors = ['#ffffff', '#cccccc', '#999999']
        for i in range(3):
            radius = glow_radius + i * 10
            # 简化发光效果为圆形
            canvas.create_oval(
                self.x + sway_x - radius, self.y - self.height - radius,
                self.x + sway_x + radius, self.y - self.height + radius,
                fill=colors[i], outline="", stipple='gray50'
            )
    
    def draw_trunk(self, canvas, sway_x):
        """绘制渐变树干"""
        trunk_height = self.height * 0.4 * self.growth
        trunk_width = self.trunk_width * self.growth
        
        # 多段绘制实现渐变效果
        segments = 10
        for i in range(segments):
            segment_height = trunk_height / segments
            y_top = self.y - i * segment_height
            y_bottom = self.y - (i + 1) * segment_height
            
            # 计算渐变色
            progress = i / segments
            color = self.interpolate_color(
                self.theme['trunk'][0], 
                self.theme['trunk'][-1], 
                progress
            )
            
            # 计算宽度变化
            width_factor = 1 - progress * 0.3
            segment_width = trunk_width * width_factor
            
            sway_factor = progress * 0.7  # 上部摇摆更多
            segment_sway = sway_x * sway_factor
            
            canvas.create_line(
                self.x + segment_sway - segment_width/2, y_top,
                self.x + segment_sway + segment_width/2, y_bottom,
                width=int(segment_width), fill=color, capstyle=tk.ROUND
            )
    
    def draw_branches(self, canvas, sway_x):
        """绘制分枝系统"""
        branch_start_y = self.y - self.height * 0.4 * self.growth
        branch_height = self.height * 0.6 * self.growth
        
        for i in range(self.branch_count):
            # 计算分枝角度和位置
            angle_base = -90 + (i - self.branch_count/2) * 25
            angle_variance = random.uniform(-15, 15)
            angle = angle_base + angle_variance
            
            branch_length = branch_height * random.uniform(0.6, 0.9)
            branch_sway = sway_x * (0.5 + i * 0.1)
            
            # 绘制分枝
            self.draw_single_branch(canvas, 
                                  self.x + branch_sway, 
                                  branch_start_y - i * (branch_height / self.branch_count),
                                  angle, branch_length, 0)
    
    def draw_single_branch(self, canvas, x, y, angle, length, depth):
        """递归绘制单个分枝"""
        if depth > 4 or length < 10:
            # 绘制叶子群
            self.draw_leaf_cluster(canvas, x, y)
            return
        
        # 计算分枝端点
        rad = math.radians(angle)
        end_x = x + length * math.cos(rad)
        end_y = y + length * math.sin(rad)
        
        # 绘制分枝
        branch_color = random.choice(self.theme['trunk'])
        branch_width = max(1, int(6 - depth))
        
        canvas.create_line(x, y, end_x, end_y,
                         width=branch_width, fill=branch_color, capstyle=tk.ROUND)
        
        # 递归绘制子分枝
        if depth < 3:
            sub_branches = random.randint(2, 3)
            for i in range(sub_branches):
                new_angle = angle + random.uniform(-30, 30)
                new_length = length * random.uniform(0.6, 0.8)
                self.draw_single_branch(canvas, end_x, end_y, new_angle, new_length, depth + 1)
    
    def draw_leaf_cluster(self, canvas, x, y):
        """绘制叶子群"""
        leaf_count = int(random.randint(3, 8) * self.leaf_density)
        
        for i in range(leaf_count):
            # 随机分布
            offset_x = random.uniform(-15, 15)
            offset_y = random.uniform(-15, 15)
            leaf_x = x + offset_x
            leaf_y = y + offset_y
            
            # 叶子大小
            min_size, max_size = getattr(self, 'leaf_size_range', (3, 7))
            leaf_size = random.uniform(min_size, max_size)
            
            # 选择叶子颜色（使用渐变）
            color_progress = random.random()
            leaf_color = self.interpolate_color(
                self.primary_gradient[0],
                self.primary_gradient[1], 
                color_progress
            )
            
            # 绘制不同形状的叶子
            leaf_shape = random.choice(['oval', 'heart', 'star'])
            
            if leaf_shape == 'oval':
                canvas.create_oval(
                    leaf_x - leaf_size, leaf_y - leaf_size,
                    leaf_x + leaf_size, leaf_y + leaf_size,
                    fill=leaf_color, outline=''
                )
            elif leaf_shape == 'heart':
                self.draw_heart_leaf(canvas, leaf_x, leaf_y, leaf_size, leaf_color)
            elif leaf_shape == 'star':
                self.draw_star_leaf(canvas, leaf_x, leaf_y, leaf_size, leaf_color)
    
    def draw_heart_leaf(self, canvas, x, y, size, color):
        """绘制心形叶子"""
        # 简化的心形路径
        points = []
        for i in range(16):
            t = i * math.pi / 8
            heart_x = 16 * math.sin(t)**3
            heart_y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            
            # 缩放和平移
            points.extend([
                x + heart_x * size / 20,
                y + heart_y * size / 20
            ])
        
        if len(points) >= 6:
            canvas.create_polygon(points, fill=color, outline='', smooth=True)
    
    def draw_star_leaf(self, canvas, x, y, size, color):
        """绘制星形叶子"""
        points = []
        for i in range(10):  # 5个尖角的星
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.4
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.extend([px, py])
        
        canvas.create_polygon(points, fill=color, outline='', smooth=True)
    
    def draw_particles(self, canvas):
        """绘制粒子效果"""
        for particle in self.particles:
            size = particle['size'] * particle['life']
            
            # 使用固定颜色避免alpha通道问题
            color = particle['color'] if particle['life'] > 0.5 else '#ffcccc'
            
            canvas.create_oval(
                particle['x'] - size, particle['y'] - size,
                particle['x'] + size, particle['y'] + size,
                fill=color, outline=''
            )
    
    def interpolate_color(self, color1, color2, factor):
        """颜色插值"""
        if not color1.startswith('#') or not color2.startswith('#'):
            return color1
        
        try:
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (g2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color1


class EchoGardenEnhanced:
    """Echo Garden 美观增强版"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echo Garden Enhanced - 美观互动生成艺术")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a23')
        
        # 主题系统
        self.themes = [
            ModernColorTheme.AURORA,
            ModernColorTheme.FOREST, 
            ModernColorTheme.SUNSET,
            ModernColorTheme.OCEAN,
            ModernColorTheme.COSMIC
        ]
        self.current_theme_index = 0
        self.current_theme = self.themes[self.current_theme_index]
        
        # 音频处理
        try:
            from echo_garden_realtime import RealTimeAudioProcessor, SimulatedAudioProcessor
            self.audio_processor = RealTimeAudioProcessor() if AUDIO_AVAILABLE else SimulatedAudioProcessor()
        except:
            # 简化的音频处理器
            self.audio_processor = self.create_simple_audio_processor()
        
        self.trees = []
        self.is_live_mode = False
        self.last_audio_features = None
        
        # 创建界面
        self.create_enhanced_ui()
        self.bind_events()
        
        # 动画系统
        self.last_time = time.time()
        self.animate()
        
        # 显示欢迎信息
        self.show_welcome()
    
    def create_simple_audio_processor(self):
        """创建简单的音频处理器"""
        class SimpleProcessor:
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
        
        return SimpleProcessor()
    
    def create_enhanced_ui(self):
        """创建增强版用户界面"""
        # 主标题栏
        self.create_header()
        
        # 主内容区域
        main_container = tk.Frame(self.root, bg=self.current_theme['primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # 左侧面板
        left_panel = self.create_left_panel(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # 右侧主画布区域
        right_panel = self.create_right_panel(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 底部控制栏
        self.create_control_bar()
    
    def create_header(self):
        """创建标题栏"""
        header = tk.Frame(self.root, bg=self.current_theme['primary'], height=60)
        header.pack(fill=tk.X, padx=15, pady=(15, 0))
        header.pack_propagate(False)
        
        # 主标题
        title = tk.Label(
            header,
            text="🌳 Echo Garden Enhanced",
            font=('Arial', 24, 'bold'),
            fg=self.current_theme['text'],
            bg=self.current_theme['primary']
        )
        title.pack(side=tk.LEFT, pady=15)
        
        # 状态信息
        self.status_frame = tk.Frame(header, bg=self.current_theme['primary'])
        self.status_frame.pack(side=tk.RIGHT, pady=15)
        
        self.theme_label = tk.Label(
            self.status_frame,
            text=f"主题: {self.current_theme['name']}",
            font=('Arial', 12),
            fg=self.current_theme['accent'],
            bg=self.current_theme['primary']
        )
        self.theme_label.pack(anchor=tk.E)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="状态: 就绪",
            font=('Arial', 11),
            fg=self.current_theme['highlight'],
            bg=self.current_theme['primary']
        )
        self.status_label.pack(anchor=tk.E)
    
    def create_left_panel(self, parent):
        """创建左侧面板"""
        panel = tk.Frame(parent, bg=self.current_theme['secondary'], width=280)
        panel.pack_propagate(False)
        
        # 波形显示区域
        wave_frame = tk.Frame(panel, bg=self.current_theme['secondary'])
        wave_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # 波形标题
        wave_title = tk.Label(
            wave_frame,
            text="🎵 实时音频监测",
            font=('Arial', 14, 'bold'),
            fg=self.current_theme['text'],
            bg=self.current_theme['secondary']
        )
        wave_title.pack(anchor=tk.W, pady=(0, 10))
        
        # 波形可视化器
        self.waveform_viz = WaveformVisualizer(
            wave_frame, 
            width=250, 
            height=350, 
            theme=self.current_theme
        )
        self.waveform_viz.pack()
        
        # 音频控制区域
        audio_controls = tk.Frame(panel, bg=self.current_theme['secondary'])
        audio_controls.pack(fill=tk.X, padx=15, pady=10)
        
        # 实时模式按钮
        if hasattr(self.audio_processor, 'start_recording'):
            self.live_button = ModernButton(
                audio_controls, 
                text="🎤 开启实时模式",
                command=self.toggle_live_mode,
                width=220, height=40,
                bg_color=self.current_theme['highlight']
            )
            self.live_button.pack(pady=5)
        
        return panel
    
    def create_right_panel(self, parent):
        """创建右侧主画布区域"""
        panel = tk.Frame(parent, bg=self.current_theme['accent'])
        
        # 画布容器
        canvas_container = tk.Frame(panel, bg=self.current_theme['accent'])
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 主画布
        self.canvas = tk.Canvas(
            canvas_container,
            bg=self.current_theme['canvas_bg'],
            width=1000,
            height=600,
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 添加画布边框效果
        self.canvas.create_rectangle(
            2, 2, 998, 598,
            outline=self.current_theme['accent'], 
            width=3
        )
        
        return panel
    
    def create_control_bar(self):
        """创建底部控制栏"""
        control_bar = tk.Frame(self.root, bg=self.current_theme['primary'], height=80)
        control_bar.pack(fill=tk.X, padx=15, pady=15)
        control_bar.pack_propagate(False)
        
        # 按钮容器
        button_container = tk.Frame(control_bar, bg=self.current_theme['primary'])
        button_container.pack(expand=True)
        
        # 控制按钮
        buttons = [
            ("🎵 声音种树", self.text_sound_plant, self.current_theme['highlight']),
            ("🌱 随机种树", self.plant_random_tree, '#4caf50'),
            ("🎨 切换主题", self.switch_theme, '#9c27b0'),
            ("🗑️ 清空画布", self.clear_garden, '#f44336'),
            ("💾 保存作品", self.save_art, '#ff9800'),
            ("❓ 帮助", self.show_help, '#607d8b')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = ModernButton(
                button_container,
                text=text,
                command=command,
                width=140, 
                height=45,
                bg_color=color,
                hover_color=self.darken_color(color)
            )
            btn.grid(row=0, column=i, padx=8, pady=10)
    
    def darken_color(self, color):
        """使颜色变暗"""
        try:
            if color.startswith('#'):
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
                return f'#{r:02x}{g:02x}{b:02x}'
        except:
            pass
        return color
    
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
        elif key == 'space':
            self.text_sound_plant()
    
    def toggle_live_mode(self):
        """切换实时模式"""
        if self.is_live_mode:
            self.audio_processor.stop_recording()
            self.is_live_mode = False
            self.live_button.text = "🎤 开启实时模式"
            self.live_button.draw_button()
            self.status_label.config(text="状态: 实时模式已关闭")
        else:
            if self.audio_processor.start_recording():
                self.is_live_mode = True
                self.live_button.text = "🔴 关闭实时模式"
                self.live_button.draw_button()
                self.status_label.config(text="状态: 实时音频模式已启用")
            else:
                messagebox.showerror("错误", "无法启动音频录制！")
    
    def plant_tree_at(self, x, y, audio_features=None):
        """在指定位置种植树木"""
        if y < 50:
            y = 50
            
        if audio_features is None:
            audio_features = {
                'volume': random.uniform(0.3, 0.8),
                'pitch': random.uniform(0.2, 0.8),
                'energy': random.uniform(0.4, 0.7)
            }
        
        tree = EnhancedTree(x, y, self.current_theme, audio_features)
        self.trees.append(tree)
        
        self.status_label.config(text=f"状态: 新树已种植 ({len(self.trees)} 棵树)")
    
    def plant_random_tree(self):
        """种植随机树木"""
        x = random.randint(50, 950)
        y = random.randint(200, 550)
        self.plant_tree_at(x, y)
    
    def text_sound_plant(self):
        """文本声音种植"""
        sound_input = simpledialog.askstring(
            "声音描述",
            "请输入描述声音特征的文字:\n(例如: 轻柔的高音、激烈的节拍、温和的旋律等)",
            parent=self.root
        )
        
        if sound_input:
            # 简单的文本分析
            features = self.analyze_text_features(sound_input)
            x = random.randint(100, 900)
            y = random.randint(200, 550)
            self.plant_tree_at(x, y, features)
            
            self.status_label.config(text=f"状态: 声音树已种植 - '{sound_input}'")
    
    def analyze_text_features(self, text):
        """分析文本特征"""
        text = text.lower()
        
        # 初始值
        features = {'volume': 0.5, 'pitch': 0.5, 'energy': 0.5}
        
        # 音量关键词
        if any(word in text for word in ['大声', '响亮', '激烈', '强']):
            features['volume'] = random.uniform(0.7, 0.9)
        elif any(word in text for word in ['轻', '柔', '小', '弱']):
            features['volume'] = random.uniform(0.2, 0.4)
            
        # 音调关键词  
        if any(word in text for word in ['高', '尖', '细']):
            features['pitch'] = random.uniform(0.7, 0.9)
        elif any(word in text for word in ['低', '沉', '厚']):
            features['pitch'] = random.uniform(0.1, 0.3)
            
        # 能量关键词
        if any(word in text for word in ['节拍', '律动', '活跃', '快']):
            features['energy'] = random.uniform(0.7, 0.9)
        elif any(word in text for word in ['平静', '慢', '稳']):
            features['energy'] = random.uniform(0.2, 0.4)
        
        return features
    
    def switch_theme(self):
        """切换主题"""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme = self.themes[self.current_theme_index]
        self.update_theme()
    
    def update_theme(self):
        """更新主题"""
        # 更新界面颜色
        self.root.configure(bg=self.current_theme['primary'])
        self.canvas.configure(bg=self.current_theme['canvas_bg'])
        self.theme_label.config(text=f"主题: {self.current_theme['name']}")
        
        # 更新树木主题
        for tree in self.trees:
            tree.theme = self.current_theme
            tree.primary_gradient = random.choice(self.current_theme['gradients'])
        
        self.status_label.config(text=f"状态: 已切换到 {self.current_theme['name']} 主题")
    
    def clear_garden(self):
        """清空花园"""
        self.trees.clear()
        self.canvas.delete("all")
        
        # 重绘画布边框
        self.canvas.create_rectangle(
            2, 2, 998, 598,
            outline=self.current_theme['accent'], 
            width=3
        )
        
        self.status_label.config(text="状态: 花园已清空")
    
    def save_art(self):
        """保存艺术作品"""
        if not self.trees:
            messagebox.showwarning("警告", "没有树木可以保存！")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("EPS files", "*.eps"), ("PNG files", "*.png"), ("All files", "*.*")],
            title="保存 Echo Garden 作品"
        )
        
        if filename:
            try:
                if filename.endswith('.eps'):
                    self.canvas.postscript(file=filename)
                else:
                    # 对于其他格式，使用 EPS 后转换（需要额外库支持）
                    self.canvas.postscript(file=filename)
                
                self.status_label.config(text=f"状态: 作品已保存到 {filename}")
                messagebox.showinfo("成功", f"作品已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def animate(self):
        """动画主循环"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # 更新音频数据
        if self.is_live_mode:
            self.last_audio_features = self.audio_processor.get_current_features()
            waveform_data = self.audio_processor.get_waveform_data()
        else:
            self.last_audio_features = self.audio_processor.get_current_features()
            waveform_data = self.audio_processor.get_waveform_data()
        
        # 更新波形显示
        if hasattr(self, 'waveform_viz'):
            self.waveform_viz.update_waveform(waveform_data, self.last_audio_features)
        
        # 更新树木
        for tree in self.trees:
            tree.update(dt, self.last_audio_features)
        
        # 重绘场景
        self.redraw()
        
        # 继续动画循环
        self.root.after(50, self.animate)
    
    def redraw(self):
        """重绘场景"""
        self.canvas.delete("all")
        
        # 绘制画布边框
        self.canvas.create_rectangle(
            2, 2, 998, 598,
            outline=self.current_theme['accent'], 
            width=3
        )
        
        # 绘制背景效果（星空或渐变）
        self.draw_background_effects()
        
        # 绘制所有树木
        for tree in self.trees:
            tree.draw(self.canvas)
    
    def draw_background_effects(self):
        """绘制背景效果"""
        # 根据主题绘制不同的背景效果
        if self.current_theme['name'] in ['极光幻境', '宇宙星河']:
            # 绘制星点
            for _ in range(30):
                x = random.randint(10, 990)
                y = random.randint(10, 590)
                size = random.randint(1, 3)
                
                self.canvas.create_oval(
                    x-size, y-size, x+size, y+size,
                    fill='white', outline=''
                )
    
    def show_welcome(self):
        """显示欢迎信息"""
        welcome_text = f"""
🌟 欢迎使用 Echo Garden Enhanced！

✨ 本版本新特性:
• 全新现代化界面设计
• 5种精美主题 ({', '.join(theme['name'] for theme in self.themes)})
• 增强的树木渲染效果
• 实时音频波形可视化
• 美丽的粒子动画效果
• 更丰富的交互体验

🎮 快速开始:
1. 点击画布任意位置种植树木
2. 使用 🎵 声音种树 输入文字描述
3. 按键 1-5 切换不同主题
4. 尝试 🎤 实时模式 体验音频互动

开始创造您的专属声音花园吧！🌳✨
        """
        
        messagebox.showinfo("Echo Garden Enhanced", welcome_text)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🌳 Echo Garden Enhanced 操作指南

🎨 主题切换:
• 键盘 1: 极光幻境 - 梦幻的蓝紫色调
• 键盘 2: 翠绿森林 - 自然的绿色系
• 键盘 3: 日落晚霞 - 温暖的橙红色
• 键盘 4: 深海蓝调 - 宁静的海洋色
• 键盘 5: 宇宙星河 - 神秘的紫色系

🎵 声音输入建议:
• 轻柔的高音 → 纤细优美的树形
• 激烈的节拍 → 粗壮有力的枝干
• 温和的旋律 → 平衡协调的造型
• 低沉的轰鸣 → 厚重深邃的色彩

🌟 特色功能:
• 🌸 樱花绽放动画效果
• ✨ 发光粒子系统
• 🎭 7种艺术化树木样式
• 🌊 实时音频响应

享受您的创作之旅！🎶🌿
        """
        
        messagebox.showinfo("操作帮助", help_text)
    
    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序已退出")
        finally:
            if hasattr(self.audio_processor, 'stop_recording'):
                self.audio_processor.stop_recording()


def main():
    """主函数"""
    print("🌳 启动 Echo Garden Enhanced - 美观互动生成艺术 🌳")
    print("✨ 全新界面设计，带来更佳的视觉体验")
    
    app = EchoGardenEnhanced()
    app.run()


if __name__ == "__main__":
    main()
