#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden Premium - 高级点阵艺术版
Premium dotted art style version inspired by ceramic studio design

Features:
- Sophisticated dotted art style rendering
- Rich color palettes with organic gradients
- Highly randomized tree generation
- Varied growth speeds and trunk thickness
- Premium visual aesthetics
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import math
import time
import colorsys

# 尝试导入音频库
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


class PremiumColorPalette:
    """高级配色方案 - 基于您提供的设计参考"""
    
    ORGANIC_FLOW = {
        'name': '有机流动',
        'bg': '#f8f6f0',
        'canvas_bg': '#fcfaf6',
        'panel_bg': '#f5f3ed',
        'accent': '#e8e6e0',
        'text': '#2c2c2c',
        'secondary_text': '#666666',
        
        # 主色调 - 基于您的图片
        'primary_colors': [
            '#d45087', '#ff6b9d', '#f95e8a',  # 粉红系
            '#4ecdc4', '#44a08d', '#096dd9',  # 青绿蓝系
            '#feca57', '#ff9ff3', '#54a0ff', # 黄紫蓝系
            '#5f27cd', '#00d2d3', '#ff9f43', # 紫青橙系
        ],
        
        # 点阵颜色 - 丰富的渐变色
        'dot_colors': [
            '#ff6b9d', '#f8b500', '#4ecdc4', '#096dd9',
            '#5f27cd', '#00d2d3', '#ff9f43', '#d45087',
            '#44a08d', '#feca57', '#ff9ff3', '#54a0ff',
            '#26de81', '#fd79a8', '#fdcb6e', '#6c5ce7',
            '#74b9ff', '#a29bfe', '#fd79a8', '#fdcb6e'
        ],
        
        # 树干颜色
        'trunk_colors': [
            '#8b7355', '#a0895a', '#6d5a47', '#9b8b74',
            '#7a6b5d', '#8f7e6a', '#6b5b4a', '#a1907d'
        ],
        
        # 背景装饰色
        'decoration_colors': [
            '#e8f4f8', '#f8e8f4', '#f4f8e8', '#f8f4e8',
            '#e8f8f4', '#f4e8f8', '#fffbf0', '#f0f8ff'
        ]
    }
    
    CERAMIC_DOTS = {
        'name': '陶艺点阵',
        'bg': '#faf8f5',
        'canvas_bg': '#fffef9',
        'panel_bg': '#f7f5f2',
        'accent': '#e5e3e0',
        'text': '#3c3c3c',
        'secondary_text': '#787878',
        
        'primary_colors': [
            '#e74c3c', '#3498db', '#2ecc71', '#f39c12',
            '#9b59b6', '#1abc9c', '#e67e22', '#34495e'
        ],
        
        'dot_colors': [
            '#e74c3c', '#c0392b', '#3498db', '#2980b9',
            '#2ecc71', '#27ae60', '#f39c12', '#d68910',
            '#9b59b6', '#8e44ad', '#1abc9c', '#16a085',
            '#e67e22', '#d35400', '#95a5a6', '#7f8c8d'
        ],
        
        'trunk_colors': [
            '#34495e', '#2c3e50', '#7f8c8d', '#95a5a6'
        ],
        
        'decoration_colors': [
            '#ecf0f1', '#f8f9fa', '#e8f5e8', '#f0f8ff'
        ]
    }


class DottedRenderer:
    """点阵渲染器 - 实现点状艺术效果"""
    
    def __init__(self, canvas, palette):
        self.canvas = canvas
        self.palette = palette
        self.dot_size_range = (1, 4)
        self.density = 0.7  # 点的密度
    
    def draw_dotted_line(self, x1, y1, x2, y2, colors, width=3, style='organic'):
        """绘制点阵线条"""
        # 计算线条长度和方向
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if length == 0:
            return
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        # 沿线条绘制点
        dot_spacing = 3 + random.uniform(-1, 1)
        num_dots = int(length / dot_spacing)
        
        for i in range(num_dots):
            progress = i / max(1, num_dots - 1)
            
            # 基础位置
            base_x = x1 + dx * i * dot_spacing
            base_y = y1 + dy * i * dot_spacing
            
            # 添加有机偏移
            if style == 'organic':
                offset_x = random.uniform(-width/2, width/2) * math.sin(progress * math.pi * 3)
                offset_y = random.uniform(-width/2, width/2) * math.cos(progress * math.pi * 2)
            else:
                offset_x = random.uniform(-width/3, width/3)
                offset_y = random.uniform(-width/3, width/3)
            
            x = base_x + offset_x
            y = base_y + offset_y
            
            # 选择颜色
            if isinstance(colors, list):
                color = random.choice(colors)
            else:
                color = colors
            
            # 变化点的大小
            size = random.uniform(*self.dot_size_range) * (0.8 + progress * 0.4)
            
            # 绘制点
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline='', tags="tree_dot"
            )
    
    def draw_dotted_circle(self, cx, cy, radius, colors, density=1.0):
        """绘制点阵圆形 - 用于叶子"""
        num_dots = int(radius * 8 * density)
        
        for _ in range(num_dots):
            # 在圆形区域内随机分布点
            angle = random.uniform(0, 2 * math.pi)
            r = radius * math.sqrt(random.uniform(0, 1))
            
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            
            # 颜色选择
            color = random.choice(colors) if isinstance(colors, list) else colors
            
            # 大小变化
            size = random.uniform(1, 3) * (1.2 - r/radius * 0.5)
            
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline='', tags="tree_dot"
            )
    
    def draw_dotted_area(self, points, colors, density=0.8):
        """绘制点阵区域"""
        if len(points) < 6:
            return
        
        # 计算边界
        xs = [points[i] for i in range(0, len(points), 2)]
        ys = [points[i] for i in range(1, len(points), 2)]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # 在区域内随机分布点
        area = (max_x - min_x) * (max_y - min_y)
        num_dots = int(area * density * 0.01)
        
        for _ in range(num_dots):
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            
            # 简化的点在多边形内判断
            if self._point_in_polygon(x, y, points):
                color = random.choice(colors) if isinstance(colors, list) else colors
                size = random.uniform(1, 2.5)
                
                self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill=color, outline='', tags="tree_dot"
                )
    
    def _point_in_polygon(self, x, y, points):
        """简化的点在多边形内判断"""
        # 简单边界框检查
        xs = [points[i] for i in range(0, len(points), 2)]
        ys = [points[i] for i in range(1, len(points), 2)]
        return min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys)


class RandomizedTree:
    """高度随机化的树木类"""
    
    def __init__(self, x, y, palette, audio_features=None):
        self.x = x
        self.y = y
        self.palette = palette
        self.audio_features = audio_features or self._generate_features()
        
        # 高度随机化的属性
        self._randomize_properties()
        
        # 生长状态
        self.growth = 0.0
        self.is_growing = True
        self.age = 0.0
        
        # 动画属性
        self.sway_phase = random.uniform(0, math.pi * 2)
        self.growth_stage = 0  # 0: 种子, 1: 幼苗, 2: 成长, 3: 成熟
        
        # 分枝记录
        self.branches = []
        self.leaves_clusters = []
    
    def _generate_features(self):
        """生成随机音频特征"""
        return {
            'volume': random.uniform(0.2, 0.9),
            'pitch': random.uniform(0.1, 0.9),
            'energy': random.uniform(0.2, 0.8),
            'timbre': random.uniform(0.0, 1.0),  # 新增音色特征
            'harmony': random.uniform(0.0, 1.0)  # 新增和声特征
        }
    
    def _randomize_properties(self):
        """随机化树木属性"""
        volume = self.audio_features['volume']
        pitch = self.audio_features['pitch']
        energy = self.audio_features['energy']
        timbre = self.audio_features.get('timbre', 0.5)
        harmony = self.audio_features.get('harmony', 0.5)
        
        # 基础尺寸 - 更大的变化范围
        self.base_height = 40 + volume * 180 + random.uniform(-30, 30)
        self.trunk_thickness = 3 + volume * 15 + random.uniform(-2, 8)
        
        # 生长速度 - 高度随机化
        self.growth_speed = 0.005 + energy * 0.03 + random.uniform(-0.01, 0.02)
        
        # 分枝特性
        self.branch_probability = 0.3 + energy * 0.5 + random.uniform(-0.2, 0.2)
        self.branch_angle_variance = 15 + pitch * 60 + random.uniform(-10, 15)
        self.max_branches = int(2 + energy * 12 + random.uniform(-1, 4))
        
        # 形态特征
        self.asymmetry_factor = random.uniform(0.1, 0.9)  # 不对称程度
        self.bend_tendency = pitch * 0.8 + random.uniform(-0.3, 0.3)  # 弯曲倾向
        self.thickness_variation = random.uniform(0.3, 1.2)  # 粗细变化
        
        # 叶子特性
        self.leaf_density = 0.5 + harmony * 1.5 + random.uniform(-0.3, 0.5)
        self.leaf_size_variation = random.uniform(0.5, 2.0)
        self.leaf_color_variation = random.uniform(0.3, 1.0)
        
        # 颜色倾向
        self.color_preference = random.randint(0, len(self.palette['primary_colors']) - 1)
        self.color_mutation_rate = random.uniform(0.1, 0.6)
        
        # 特殊形态
        self.spiral_tendency = timbre * 0.5 + random.uniform(-0.2, 0.2)
        self.droop_factor = (1 - energy) * 0.4 + random.uniform(-0.1, 0.2)
    
    def update(self, dt):
        """更新树木状态"""
        if self.is_growing:
            # 非线性生长
            growth_factor = 1.0
            if self.growth < 0.3:  # 幼苗期快速生长
                growth_factor = 1.5
            elif self.growth > 0.7:  # 成熟期缓慢生长
                growth_factor = 0.3
            
            self.growth += self.growth_speed * growth_factor * dt * 60
            
            if self.growth >= 1.0:
                self.growth = 1.0
                self.is_growing = False
        
        # 年龄增长
        self.age += dt * 0.5
        
        # 摇摆动画 - 基于风的模拟
        wind_strength = 0.3 + 0.7 * math.sin(time.time() * 0.5)
        self.sway_phase += (1.0 + self.audio_features['pitch']) * wind_strength * dt
        
        # 更新生长阶段
        if self.growth < 0.2:
            self.growth_stage = 0  # 种子
        elif self.growth < 0.5:
            self.growth_stage = 1  # 幼苗
        elif self.growth < 0.8:
            self.growth_stage = 2  # 成长
        else:
            self.growth_stage = 3  # 成熟
    
    def draw(self, canvas, renderer):
        """使用点阵渲染器绘制树木"""
        if self.growth <= 0.05:
            return
        
        # 清除之前的绘制
        canvas.delete("tree_dot")
        
        # 计算当前摇摆
        sway_amplitude = 3 + self.audio_features['volume'] * 8
        sway_x = math.sin(self.sway_phase) * sway_amplitude * self.growth
        sway_y = math.cos(self.sway_phase * 0.7) * sway_amplitude * 0.3
        
        # 根据生长阶段绘制
        if self.growth_stage == 0:
            self._draw_seed(canvas, renderer)
        elif self.growth_stage >= 1:
            self._draw_full_tree(canvas, renderer, sway_x, sway_y)
    
    def _draw_seed(self, canvas, renderer):
        """绘制种子阶段"""
        seed_colors = [self.palette['dot_colors'][self.color_preference]]
        renderer.draw_dotted_circle(self.x, self.y, 2 + self.growth * 3, seed_colors, 0.8)
    
    def _draw_full_tree(self, canvas, renderer, sway_x, sway_y):
        """绘制完整树木"""
        current_height = self.base_height * self.growth
        current_thickness = self.trunk_thickness * self.growth
        
        # 绘制主树干
        self._draw_trunk(canvas, renderer, current_height, current_thickness, sway_x, sway_y)
        
        # 绘制分枝系统
        if self.growth > 0.3:
            self._draw_branch_system(canvas, renderer, current_height, sway_x, sway_y)
        
        # 绘制叶子
        if self.growth > 0.5:
            self._draw_leaves(canvas, renderer, sway_x, sway_y)
    
    def _draw_trunk(self, canvas, renderer, height, thickness, sway_x, sway_y):
        """绘制树干"""
        trunk_colors = self.palette['trunk_colors']
        
        # 分段绘制树干以实现厚度变化
        segments = max(5, int(height / 15))
        
        for i in range(segments):
            progress = i / segments
            
            # 计算位置
            segment_height = height / segments
            y_start = self.y - i * segment_height
            y_end = self.y - (i + 1) * segment_height
            
            # 厚度变化
            thickness_factor = (1 - progress * 0.6) * self.thickness_variation
            segment_thickness = thickness * thickness_factor
            
            # 弯曲效果
            bend_offset = self.bend_tendency * progress * progress * 20
            spiral_offset = math.sin(progress * math.pi * 4) * self.spiral_tendency * 10
            
            x_start = self.x + bend_offset + sway_x * (progress * 0.8)
            x_end = self.x + bend_offset + spiral_offset + sway_x * ((progress + 0.1) * 0.8)
            
            # 绘制树干段
            renderer.draw_dotted_line(
                x_start, y_start + sway_y * progress,
                x_end, y_end + sway_y * (progress + 0.1),
                trunk_colors, 
                width=segment_thickness,
                style='organic'
            )
    
    def _draw_branch_system(self, canvas, renderer, trunk_height, sway_x, sway_y):
        """绘制分枝系统"""
        branch_colors = self.palette['dot_colors']
        
        # 清除旧的分枝记录
        if len(self.branches) == 0:
            self._generate_branches(trunk_height)
        
        for branch in self.branches:
            if self.growth >= branch['min_growth']:
                branch_growth = min(1.0, (self.growth - branch['min_growth']) / 0.3)
                
                # 计算分枝位置
                trunk_x = self.x + branch['trunk_offset_x'] + sway_x * branch['sway_factor']
                trunk_y = self.y - branch['height_on_trunk'] + sway_y * branch['sway_factor']
                
                # 分枝端点
                branch_length = branch['length'] * branch_growth
                end_x = trunk_x + branch_length * math.cos(branch['angle'])
                end_y = trunk_y + branch_length * math.sin(branch['angle'])
                
                # 绘制分枝
                colors_subset = [branch_colors[i % len(branch_colors)] 
                               for i in range(branch['color_start'], branch['color_start'] + 3)]
                
                renderer.draw_dotted_line(
                    trunk_x, trunk_y, end_x, end_y,
                    colors_subset,
                    width=branch['thickness'] * branch_growth,
                    style='organic'
                )
                
                # 记录分枝端点用于绘制叶子
                branch['end_x'] = end_x
                branch['end_y'] = end_y
                branch['current_growth'] = branch_growth
    
    def _generate_branches(self, trunk_height):
        """生成分枝数据"""
        num_branches = random.randint(2, self.max_branches)
        
        for i in range(num_branches):
            # 分枝高度分布
            height_ratio = 0.3 + (i / num_branches) * 0.6 + random.uniform(-0.1, 0.1)
            height_on_trunk = trunk_height * height_ratio
            
            # 分枝角度 - 增加不对称性
            base_angle = -90 + random.uniform(-self.branch_angle_variance, self.branch_angle_variance)
            if i % 2 == 0:  # 不对称处理
                base_angle *= self.asymmetry_factor
            
            branch = {
                'height_on_trunk': height_on_trunk,
                'angle': math.radians(base_angle),
                'length': random.uniform(20, 60) * (0.7 + self.audio_features['energy'] * 0.6),
                'thickness': random.uniform(1, 4) * self.growth,
                'trunk_offset_x': random.uniform(-5, 5) * self.bend_tendency,
                'sway_factor': 0.3 + height_ratio * 0.7,
                'min_growth': 0.3 + i * 0.1,
                'color_start': random.randint(0, len(self.palette['dot_colors']) - 3),
                'end_x': 0, 'end_y': 0, 'current_growth': 0
            }
            self.branches.append(branch)
    
    def _draw_leaves(self, canvas, renderer, sway_x, sway_y):
        """绘制叶子"""
        leaf_colors = self.palette['dot_colors']
        
        for branch in self.branches:
            if branch['current_growth'] > 0.5:
                # 在分枝端点绘制叶子群
                num_clusters = random.randint(1, 3)
                
                for j in range(num_clusters):
                    cluster_offset_x = random.uniform(-15, 15)
                    cluster_offset_y = random.uniform(-10, 10)
                    
                    cluster_x = branch['end_x'] + cluster_offset_x
                    cluster_y = branch['end_y'] + cluster_offset_y
                    
                    # 叶子大小随机化
                    leaf_size = random.uniform(3, 8) * self.leaf_size_variation * branch['current_growth']
                    
                    # 颜色选择 - 基于树木的颜色倾向
                    preferred_colors = [
                        leaf_colors[(self.color_preference + k) % len(leaf_colors)]
                        for k in range(4)
                    ]
                    
                    # 颜色变异
                    if random.random() < self.color_mutation_rate:
                        cluster_colors = [random.choice(leaf_colors) for _ in range(3)]
                    else:
                        cluster_colors = preferred_colors[:3]
                    
                    renderer.draw_dotted_circle(
                        cluster_x, cluster_y, 
                        leaf_size, 
                        cluster_colors, 
                        self.leaf_density
                    )


class PremiumAudioProcessor:
    """高级音频处理器"""
    
    def __init__(self):
        self.sim_time = 0
        self.noise_factors = [random.uniform(-0.1, 0.1) for _ in range(5)]
    
    def get_current_features(self):
        self.sim_time += 0.05
        
        # 更复杂的模拟音频特征
        base_volume = 0.5 + 0.3 * math.sin(self.sim_time + self.noise_factors[0])
        base_pitch = 0.4 + 0.4 * math.sin(self.sim_time * 0.7 + self.noise_factors[1])
        base_energy = 0.3 + 0.4 * math.sin(self.sim_time * 1.3 + self.noise_factors[2])
        
        return {
            'volume': max(0, min(1, base_volume + random.uniform(-0.1, 0.1))),
            'pitch': max(0, min(1, base_pitch + random.uniform(-0.1, 0.1))),
            'energy': max(0, min(1, base_energy + random.uniform(-0.1, 0.1))),
            'timbre': 0.5 + 0.3 * math.sin(self.sim_time * 0.9 + self.noise_factors[3]),
            'harmony': 0.5 + 0.3 * math.cos(self.sim_time * 1.1 + self.noise_factors[4])
        }
    
    def get_waveform_data(self):
        data = []
        for i in range(100):
            wave = math.sin(i * 0.2 + self.sim_time) * (0.5 + 0.5 * math.sin(self.sim_time * 0.3))
            noise = random.uniform(-0.1, 0.1)
            data.append(wave + noise)
        return data


class EchoGardenPremium:
    """Echo Garden 高级版本"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echo Garden Premium - 高级点阵艺术版")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f6f0')
        
        # 主题系统
        self.palettes = [
            PremiumColorPalette.ORGANIC_FLOW,
            PremiumColorPalette.CERAMIC_DOTS
        ]
        self.current_palette_index = 0
        self.current_palette = self.palettes[self.current_palette_index]
        
        # 渲染系统
        self.renderer = None
        
        # 音频处理
        self.audio_processor = PremiumAudioProcessor()
        
        # 树木系统
        self.trees = []
        self.max_trees = 25  # 限制树木数量以保持性能
        
        # 状态
        self.last_audio_features = None
        
        # 创建界面
        self.create_premium_ui()
        self.bind_events()
        
        # 动画系统
        self.last_time = time.time()
        self.animate()
        
        # 欢迎信息
        self.show_premium_welcome()
    
    def create_premium_ui(self):
        """创建高级界面"""
        # 顶部标题区
        header = tk.Frame(self.root, bg=self.current_palette['bg'], height=80)
        header.pack(fill=tk.X, padx=20, pady=(20, 0))
        header.pack_propagate(False)
        
        # 标题
        title = tk.Label(
            header,
            text="🎨 Echo Garden Premium",
            font=('Helvetica', 32, 'bold'),
            fg=self.current_palette['text'],
            bg=self.current_palette['bg']
        )
        title.pack(side=tk.LEFT, pady=20)
        
        # 主题标签
        self.palette_label = tk.Label(
            header,
            text=f"主题: {self.current_palette['name']}",
            font=('Helvetica', 14),
            fg=self.current_palette['secondary_text'],
            bg=self.current_palette['bg']
        )
        self.palette_label.pack(side=tk.RIGHT, pady=20)
        
        # 主内容区
        main_frame = tk.Frame(self.root, bg=self.current_palette['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧画布区域
        canvas_frame = tk.Frame(main_frame, bg=self.current_palette['panel_bg'])
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # 主画布
        self.canvas = tk.Canvas(
            canvas_frame,
            bg=self.current_palette['canvas_bg'],
            width=1000,
            height=650,
            highlightthickness=0
        )
        self.canvas.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # 初始化渲染器
        self.renderer = DottedRenderer(self.canvas, self.current_palette)
        
        # 底部状态栏
        self.create_status_bar()
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        panel = tk.Frame(parent, bg=self.current_palette['panel_bg'], width=320)
        panel.pack(side=tk.LEFT, fill=tk.Y)
        panel.pack_propagate(False)
        
        # 面板标题
        title = tk.Label(
            panel,
            text="🎛️ 创作控制",
            font=('Helvetica', 18, 'bold'),
            fg=self.current_palette['text'],
            bg=self.current_palette['panel_bg']
        )
        title.pack(pady=(20, 15))
        
        # 音频可视化区域
        audio_frame = tk.Frame(panel, bg=self.current_palette['accent'], height=120)
        audio_frame.pack(fill=tk.X, padx=20, pady=10)
        audio_frame.pack_propagate(False)
        
        self.audio_display = tk.Label(
            audio_frame,
            text="🎵 音频监测\n音量: --\n音调: --\n能量: --\n音色: --\n和声: --",
            font=('Helvetica', 11),
            fg=self.current_palette['text'],
            bg=self.current_palette['accent'],
            justify=tk.LEFT
        )
        self.audio_display.pack(expand=True)
        
        # 控制按钮
        button_frame = tk.Frame(panel, bg=self.current_palette['panel_bg'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        button_style = {
            'font': ('Helvetica', 12, 'bold'),
            'fg': 'white',
            'relief': tk.FLAT,
            'bd': 0,
            'pady': 12
        }
        
        # 声音种树
        sound_btn = tk.Button(
            button_frame,
            text="🎵 声音种树",
            command=self.sound_plant,
            bg='#ff6b9d',
            **button_style
        )
        sound_btn.pack(fill=tk.X, pady=5)
        
        # 随机种树
        random_btn = tk.Button(
            button_frame,
            text="🌱 随机种树",
            command=self.random_plant,
            bg='#4ecdc4',
            **button_style
        )
        random_btn.pack(fill=tk.X, pady=5)
        
        # 切换主题
        theme_btn = tk.Button(
            button_frame,
            text="🎨 切换主题",
            command=self.switch_palette,
            bg='#5f27cd',
            **button_style
        )
        theme_btn.pack(fill=tk.X, pady=5)
        
        # 高级选项
        advanced_frame = tk.LabelFrame(
            panel,
            text="🔧 高级选项",
            font=('Helvetica', 12, 'bold'),
            fg=self.current_palette['text'],
            bg=self.current_palette['panel_bg']
        )
        advanced_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 树木密度控制
        density_btn = tk.Button(
            advanced_frame,
            text="🌳 生成树林",
            command=self.generate_forest,
            bg='#096dd9',
            **button_style
        )
        density_btn.pack(fill=tk.X, pady=5)
        
        # 清空和保存
        action_frame = tk.Frame(panel, bg=self.current_palette['panel_bg'])
        action_frame.pack(fill=tk.X, padx=20, pady=20)
        
        clear_btn = tk.Button(
            action_frame,
            text="🗑️ 清空画布",
            command=self.clear_garden,
            bg='#e74c3c',
            **button_style
        )
        clear_btn.pack(fill=tk.X, pady=5)
        
        save_btn = tk.Button(
            action_frame,
            text="💾 保存作品",
            command=self.save_artwork,
            bg='#27ae60',
            **button_style
        )
        save_btn.pack(fill=tk.X, pady=5)
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.root, bg=self.current_palette['bg'])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="状态: 就绪 - 点击画布创作点阵艺术树木",
            font=('Helvetica', 12),
            fg=self.current_palette['secondary_text'],
            bg=self.current_palette['bg']
        )
        self.status_label.pack(side=tk.LEFT, pady=5)
        
        # 树木计数
        self.tree_count_label = tk.Label(
            status_frame,
            text=f"树木: {len(self.trees)} / {self.max_trees}",
            font=('Helvetica', 11),
            fg=self.current_palette['text'],
            bg=self.current_palette['bg']
        )
        self.tree_count_label.pack(side=tk.RIGHT, pady=5)
    
    def bind_events(self):
        """绑定事件"""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
    
    def on_canvas_click(self, event):
        """画布点击事件"""
        if len(self.trees) < self.max_trees:
            self.plant_tree_at(event.x, event.y)
        else:
            self.status_label.config(text="提示: 已达到最大树木数量，请先清空部分树木")
    
    def on_key_press(self, event):
        """键盘事件"""
        key = event.keysym.lower()
        
        if key in ['1', '2']:
            palette_index = int(key) - 1
            if palette_index < len(self.palettes):
                self.current_palette_index = palette_index
                self.current_palette = self.palettes[palette_index]
                self.update_palette()
        elif key == 'c':
            self.clear_garden()
        elif key == 's':
            self.save_artwork()
        elif key == 'space':
            self.sound_plant()
        elif key == 'f':
            self.generate_forest()
    
    def plant_tree_at(self, x, y, audio_features=None):
        """在指定位置种植树木"""
        if y < 50:
            y = 50
        
        features = audio_features or self.last_audio_features or self.audio_processor.get_current_features()
        tree = RandomizedTree(x, y, self.current_palette, features)
        self.trees.append(tree)
        
        self.update_status()
    
    def sound_plant(self):
        """声音种植"""
        sound_input = simpledialog.askstring(
            "声音艺术创作",
            "请输入声音描述 (支持更丰富的特征):\n" +
            "音量: 轻柔/响亮/震撼\n" +
            "音调: 低沉/清脆/尖锐\n" +
            "能量: 平静/活跃/狂野\n" +
            "音色: 纯净/粗糙/温暖\n" +
            "和声: 简单/复杂/丰富",
            parent=self.root
        )
        
        if sound_input and len(self.trees) < self.max_trees:
            features = self.analyze_enhanced_sound_text(sound_input)
            x = random.randint(50, 950)
            y = random.randint(200, 600)
            self.plant_tree_at(x, y, features)
            
            self.status_label.config(text=f"状态: 点阵艺术树已创作 - '{sound_input}'")
    
    def analyze_enhanced_sound_text(self, text):
        """分析增强的声音文本"""
        text = text.lower()
        features = {
            'volume': 0.5, 'pitch': 0.5, 'energy': 0.5,
            'timbre': 0.5, 'harmony': 0.5
        }
        
        # 音量分析
        volume_words = {
            '轻柔': 0.2, '微弱': 0.15, '小声': 0.25,
            '中等': 0.5, '正常': 0.5,
            '响亮': 0.8, '大声': 0.85, '震撼': 0.95
        }
        
        # 音调分析
        pitch_words = {
            '低沉': 0.1, '深厚': 0.15, '浑厚': 0.2,
            '中音': 0.5, '平稳': 0.5,
            '清脆': 0.8, '尖锐': 0.9, '刺耳': 0.95
        }
        
        # 能量分析
        energy_words = {
            '平静': 0.1, '安静': 0.15, '温和': 0.3,
            '稳定': 0.5, '普通': 0.5,
            '活跃': 0.7, '激烈': 0.85, '狂野': 0.95
        }
        
        # 音色分析
        timbre_words = {
            '纯净': 0.9, '清澈': 0.85, '透明': 0.8,
            '自然': 0.5, '普通': 0.5,
            '粗糙': 0.2, '嘈杂': 0.1, '失真': 0.05
        }
        
        # 和声分析
        harmony_words = {
            '简单': 0.2, '单调': 0.1,
            '和谐': 0.5, '平衡': 0.6,
            '复杂': 0.8, '丰富': 0.9, '层次': 0.85
        }
        
        # 应用关键词
        for word, value in volume_words.items():
            if word in text:
                features['volume'] = value
        
        for word, value in pitch_words.items():
            if word in text:
                features['pitch'] = value
        
        for word, value in energy_words.items():
            if word in text:
                features['energy'] = value
        
        for word, value in timbre_words.items():
            if word in text:
                features['timbre'] = value
        
        for word, value in harmony_words.items():
            if word in text:
                features['harmony'] = value
        
        # 添加随机变化
        for key in features:
            features[key] = max(0, min(1, features[key] + random.uniform(-0.1, 0.1)))
        
        return features
    
    def random_plant(self):
        """随机种植"""
        if len(self.trees) < self.max_trees:
            x = random.randint(50, 950)
            y = random.randint(200, 600)
            self.plant_tree_at(x, y)
    
    def generate_forest(self):
        """生成树林"""
        if len(self.trees) >= self.max_trees:
            messagebox.showinfo("提示", "已达到最大树木数量！")
            return
        
        remaining_slots = self.max_trees - len(self.trees)
        forest_size = min(8, remaining_slots)
        
        for _ in range(forest_size):
            x = random.randint(80, 920)
            y = random.randint(250, 580)
            
            # 确保不会重叠
            too_close = False
            for tree in self.trees:
                if math.sqrt((tree.x - x)**2 + (tree.y - y)**2) < 60:
                    too_close = True
                    break
            
            if not too_close:
                self.plant_tree_at(x, y)
        
        self.status_label.config(text=f"状态: 已生成 {forest_size} 棵森林树木")
    
    def switch_palette(self):
        """切换配色方案"""
        self.current_palette_index = (self.current_palette_index + 1) % len(self.palettes)
        self.current_palette = self.palettes[self.current_palette_index]
        self.update_palette()
    
    def update_palette(self):
        """更新配色方案"""
        # 更新界面颜色
        self.root.configure(bg=self.current_palette['bg'])
        self.canvas.configure(bg=self.current_palette['canvas_bg'])
        self.palette_label.config(text=f"主题: {self.current_palette['name']}")
        
        # 更新渲染器
        self.renderer = DottedRenderer(self.canvas, self.current_palette)
        
        # 更新树木配色
        for tree in self.trees:
            tree.palette = self.current_palette
        
        self.status_label.config(text=f"状态: 已切换到 {self.current_palette['name']} 配色")
    
    def clear_garden(self):
        """清空花园"""
        self.trees.clear()
        self.canvas.delete("all")
        self.update_status()
    
    def save_artwork(self):
        """保存作品"""
        if not self.trees:
            messagebox.showwarning("提示", "没有树木可保存！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("EPS files", "*.eps"), ("All files", "*.*")],
            title="保存点阵艺术作品"
        )
        
        if filename:
            try:
                self.canvas.postscript(file=filename)
                self.status_label.config(text=f"状态: 点阵艺术作品已保存")
                messagebox.showinfo("成功", f"高级点阵艺术作品已保存！\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def update_status(self):
        """更新状态显示"""
        self.tree_count_label.config(text=f"树木: {len(self.trees)} / {self.max_trees}")
        
        if len(self.trees) == 0:
            self.status_label.config(text="状态: 画布已清空 - 开始新的创作")
        else:
            self.status_label.config(text=f"状态: 当前有 {len(self.trees)} 棵点阵艺术树木")
    
    def animate(self):
        """动画循环"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # 更新音频数据
        self.last_audio_features = self.audio_processor.get_current_features()
        
        # 更新音频显示
        features = self.last_audio_features
        audio_text = f"🎵 音频监测\n"
        audio_text += f"音量: {features['volume']:.2f}\n"
        audio_text += f"音调: {features['pitch']:.2f}\n"
        audio_text += f"能量: {features['energy']:.2f}\n"
        audio_text += f"音色: {features['timbre']:.2f}\n"
        audio_text += f"和声: {features['harmony']:.2f}"
        
        self.audio_display.config(text=audio_text)
        
        # 更新树木
        for tree in self.trees:
            tree.update(dt)
        
        # 重绘
        self.redraw()
        
        # 继续动画
        self.root.after(50, self.animate)
    
    def redraw(self):
        """重绘场景"""
        # 清除画布但保留背景
        self.canvas.delete("tree_dot")
        
        # 绘制背景装饰
        self.draw_background_art()
        
        # 绘制所有树木
        for tree in self.trees:
            tree.draw(self.canvas, self.renderer)
    
    def draw_background_art(self):
        """绘制背景艺术效果"""
        canvas_width = max(1000, self.canvas.winfo_width() or 1000)
        canvas_height = max(650, self.canvas.winfo_height() or 650)
        
        # 确保尺寸有效
        if canvas_width < 50 or canvas_height < 50:
            return
        
        # 根据主题绘制不同的背景点阵
        if self.current_palette['name'] == '有机流动':
            # 绘制流动的背景点
            for _ in range(30):
                x = random.randint(30, canvas_width - 30)
                y = random.randint(30, canvas_height - 30)
                color = random.choice(self.current_palette['decoration_colors'])
                size = random.uniform(0.5, 2)
                
                self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill=color, outline='', tags="background"
                )
    
    def show_premium_welcome(self):
        """显示高级版欢迎信息"""
        welcome = f"""
🎨 欢迎使用 Echo Garden Premium！

✨ 高级特性：
• 点阵艺术风格渲染
• 高度随机化的树木生成
• 丰富的音频特征分析
• 两套专业配色方案
• 有机流动的视觉效果

🌳 创作特色：
• 每棵树都有独特的形态
• 支持5种音频特征输入
• 树干粗细和生长速度随机
• 分枝系统高度多样化
• 点阵叶子艺术效果

🎮 操作指南：
• 点击画布创建艺术树木
• 使用声音种树输入详细描述
• 按1-2切换配色方案
• 按F键生成艺术森林
• 按C清空，S保存

开始您的高级点阵艺术创作之旅！
        """
        
        messagebox.showinfo("Echo Garden Premium", welcome)
    
    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序已退出")


def main():
    """主函数"""
    print("🎨 启动 Echo Garden Premium - 高级点阵艺术版 🎨")
    print("✨ 基于现代设计美学的点阵艺术风格")
    
    app = EchoGardenPremium()
    app.run()


if __name__ == "__main__":
    main()
