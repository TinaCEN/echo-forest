#!/usr/bin/env python3
"""
Echo Garden Premium Real-time - 高级实时音频点阵艺术版
基于现代设计美学的点阵艺术风格，支持实时音频波形显示和改进的树木形状
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import random
import colorsys
import threading
import queue
import time

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
        self.waveform_data = [0] * 200  # 波形数据缓冲区
        
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
            # 简化处理，只取前200个样本作为波形
            if len(audio_data) >= 200:
                self.audio_queue.put(audio_data[:200].tolist())
            else:
                # 如果数据不足，用零填充
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
                # 生成复合波形：多个频率的正弦波
                mock_data = []
                for i in range(200):
                    # 基础正弦波
                    wave1 = 0.3 * math.sin(2 * math.pi * 440 * (t + i/44100))
                    # 高频成分
                    wave2 = 0.2 * math.sin(2 * math.pi * 880 * (t + i/44100))
                    # 低频成分
                    wave3 = 0.1 * math.sin(2 * math.pi * 220 * (t + i/44100))
                    # 添加随机噪声
                    noise = 0.05 * (random.random() - 0.5)
                    
                    total_wave = wave1 + wave2 + wave3 + noise
                    mock_data.append(total_wave)
                
                try:
                    self.audio_queue.put(mock_data, timeout=0.1)
                except queue.Full:
                    pass  # 如果队列满了，忽略这一帧
                
                t += 200/44100  # 更新时间
            
            time.sleep(0.02)  # ~50 FPS
    
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

class DottedRenderer:
    """点阵渲染器 - 实现点状艺术效果"""
    
    def __init__(self, canvas, dot_density=0.7):
        self.canvas = canvas
        self.dot_density = dot_density
    
    def draw_dotted_line(self, x1, y1, x2, y2, color="#333333", width=2):
        """绘制点阵线条"""
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance == 0:
            return
        
        # 计算点的数量
        num_dots = max(1, int(distance * self.dot_density))
        
        for i in range(num_dots):
            t = i / max(1, num_dots - 1) if num_dots > 1 else 0
            
            # 线性插值计算点位置
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            # 添加轻微的随机偏移
            offset_x = random.uniform(-0.8, 0.8)
            offset_y = random.uniform(-0.8, 0.8)
            
            # 点的大小随机变化
            dot_size = random.uniform(width * 0.8, width * 1.5)
            
            self.canvas.create_oval(
                x - dot_size/2 + offset_x, 
                y - dot_size/2 + offset_y,
                x + dot_size/2 + offset_x, 
                y + dot_size/2 + offset_y,
                fill=color, outline="", tags="tree"
            )
    
    def draw_dotted_circle(self, x, y, radius, color="#4CAF50", density_factor=1.0):
        """绘制点阵圆形（叶子）"""
        # 根据半径调整点的数量
        circumference = 2 * math.pi * radius
        num_dots = max(3, int(circumference * self.dot_density * density_factor))
        
        for i in range(num_dots):
            angle = (i / num_dots) * 2 * math.pi
            
            # 在圆周上分布点，添加径向随机偏移
            radial_offset = random.uniform(0.3, 1.0)
            actual_radius = radius * radial_offset
            
            dot_x = x + actual_radius * math.cos(angle)
            dot_y = y + actual_radius * math.sin(angle)
            
            # 点大小变化
            dot_size = random.uniform(1, 3)
            
            self.canvas.create_oval(
                dot_x - dot_size/2, dot_y - dot_size/2,
                dot_x + dot_size/2, dot_y + dot_size/2,
                fill=color, outline="", tags="tree"
            )

class ImprovedTree:
    """改进的树木类 - 更真实的树木形状"""
    
    def __init__(self, canvas, renderer, palette, x, y):
        self.canvas = canvas
        self.renderer = renderer
        self.palette = palette
        self.start_x = x
        self.start_y = y
        
        # 随机化树木属性
        self._randomize_properties()
        
        self.growth_progress = 0.0
        self.branches = []
        self.leaves = []
    
    def _randomize_properties(self):
        """随机化树木属性"""
        # 基础形态
        self.max_height = random.uniform(80, 200)
        self.trunk_width = random.uniform(4, 12)
        self.branch_factor = random.uniform(0.6, 0.9)  # 分枝衰减因子
        
        # 生长特性
        self.growth_speed = random.uniform(0.01, 0.04)
        self.branch_angle_base = random.uniform(25, 45)  # 基础分枝角度
        self.branch_probability = random.uniform(0.4, 0.8)
        
        # 视觉特性
        self.leaf_density = random.uniform(0.8, 1.5)
        self.trunk_taper = random.uniform(0.7, 0.95)  # 树干锥度
        self.asymmetry = random.uniform(0.1, 0.3)  # 不对称因子
        
        # 分枝结构
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
        
        # 清除之前的绘制
        self.canvas.delete("current_tree")
        
        # 绘制树干
        self._draw_improved_trunk()
        
        # 绘制分枝系统
        if self.growth_progress > 0.3:
            self._draw_branch_system()
        
        # 绘制叶子
        if self.growth_progress > 0.6:
            self._draw_leaves()
    
    def _draw_improved_trunk(self):
        """绘制改进的树干"""
        current_height = self.max_height * min(1.0, self.growth_progress * 1.5)
        
        # 树干分段绘制，实现锥形效果
        segments = max(5, int(current_height / 10))
        
        for i in range(segments):
            # 计算段的位置
            segment_progress = i / segments
            y_pos = self.start_y - (current_height * segment_progress)
            
            if y_pos > self.start_y - current_height:
                # 计算当前段的宽度（锥形）
                width_factor = 1.0 - (segment_progress * (1 - self.trunk_taper))
                current_width = self.trunk_width * width_factor
                
                # 添加轻微的弯曲效果
                curve_offset = self.asymmetry * 15 * math.sin(segment_progress * math.pi)
                x_pos = self.start_x + curve_offset
                
                # 下一段的位置
                next_segment_progress = (i + 1) / segments
                next_y = self.start_y - (current_height * next_segment_progress)
                next_width_factor = 1.0 - (next_segment_progress * (1 - self.trunk_taper))
                next_width = self.trunk_width * next_width_factor
                next_curve = self.asymmetry * 15 * math.sin(next_segment_progress * math.pi)
                next_x = self.start_x + next_curve
                
                # 绘制树干段
                trunk_color = random.choice(self.palette.primary_colors)
                self.renderer.draw_dotted_line(
                    x_pos - current_width/2, y_pos,
                    next_x - next_width/2, next_y,
                    trunk_color, current_width/2
                )
                self.renderer.draw_dotted_line(
                    x_pos + current_width/2, y_pos,
                    next_x + next_width/2, next_y,
                    trunk_color, current_width/2
                )
    
    def _draw_branch_system(self):
        """绘制分枝系统"""
        branch_progress = max(0, (self.growth_progress - 0.3) / 0.7)
        
        # 主分枝点（在树干的不同高度）
        branch_points = []
        for level in range(self.max_branch_levels):
            if branch_progress > level / self.max_branch_levels:
                height_ratio = 0.3 + (level / self.max_branch_levels) * 0.6
                branch_y = self.start_y - (self.max_height * height_ratio)
                
                # 在这个高度创建分枝
                for branch_idx in range(self.branches_per_level):
                    if random.random() < self.branch_probability:
                        # 分枝角度
                        base_angle = (branch_idx / self.branches_per_level) * 360
                        angle_variation = random.uniform(-20, 20)
                        branch_angle = base_angle + angle_variation
                        
                        # 分枝长度
                        branch_length = (self.max_height * 0.3) * (self.branch_factor ** level)
                        branch_length *= random.uniform(0.7, 1.3)
                        
                        # 计算分枝终点
                        end_x = self.start_x + branch_length * math.cos(math.radians(branch_angle))
                        end_y = branch_y - branch_length * math.sin(math.radians(branch_angle)) * 0.5
                        
                        # 分枝宽度
                        branch_width = self.trunk_width * (self.branch_factor ** (level + 1))
                        
                        # 绘制分枝
                        branch_color = random.choice(self.palette.primary_colors)
                        self.renderer.draw_dotted_line(
                            self.start_x, branch_y,
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
                # 在分枝端点周围绘制叶子簇
                num_leaves = random.randint(3, 8)
                
                for _ in range(num_leaves):
                    # 叶子位置（在分枝点周围）
                    leaf_x = branch_x + random.uniform(-15, 15)
                    leaf_y = branch_y + random.uniform(-10, 10)
                    
                    # 叶子大小
                    leaf_size = random.uniform(3, 8) * (1.2 - level * 0.2)
                    
                    # 叶子颜色
                    leaf_color = random.choice(self.palette.dot_colors)
                    
                    # 绘制点阵叶子
                    self.renderer.draw_dotted_circle(
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
        # 清除之前的波形
        self.canvas.delete("waveform")
        
        # 绘制背景框
        self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            outline=self.palette.primary_colors[0], width=2, fill="", tags="waveform"
        )
        
        # 绘制标题
        self.canvas.create_text(
            self.x + self.width/2, self.y - 15,
            text="🎵 实时音频波形", font=("Arial", 12, "bold"),
            fill=self.palette.primary_colors[0], tags="waveform"
        )
        
        # 绘制波形数据
        if not self.waveform_data:
            return
        
        # 计算波形点
        points = []
        center_y = self.y + self.height / 2
        
        for i, amplitude in enumerate(self.waveform_data):
            x_pos = self.x + (i / len(self.waveform_data)) * self.width
            # 限制振幅范围
            y_offset = max(-self.height/2 + 10, min(self.height/2 - 10, amplitude * self.height/2))
            y_pos = center_y + y_offset
            points.extend([x_pos, y_pos])
        
        # 绘制波形线
        if len(points) >= 4:
            self.canvas.create_line(
                points, fill=self.palette.dot_colors[2], width=2, 
                smooth=True, tags="waveform"
            )
        
        # 绘制中心线
        self.canvas.create_line(
            self.x, center_y, self.x + self.width, center_y,
            fill=self.palette.primary_colors[1], width=1, dash=(5, 5), tags="waveform"
        )

class PremiumColorPalette:
    """高级配色方案"""
    
    def __init__(self):
        self.schemes = {
            "organic_flow": {
                "name": "有机流动",
                "background": ["#f8f6f0", "#fcfaf6", "#f5f3ed"],
                "primary": ["#d45087", "#4ecdc4", "#5f27cd", "#ff9ff3"],
                "dots": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#f0932b", 
                        "#eb4d4b", "#6c5ce7", "#a29bfe", "#fd79a8", "#fdcb6e",
                        "#e17055", "#00b894", "#00cec9", "#0984e3", "#6c5ce7",
                        "#fd79a8", "#fdcb6e", "#55a3ff", "#26de81", "#fc5c65"],
                "decorations": ["#ffeaa7", "#fab1a0", "#e17055", "#74b9ff"]
            },
            "ceramic_dots": {
                "name": "陶艺点阵", 
                "background": ["#faf8f5", "#fffef9", "#f7f5f2"],
                "primary": ["#c44569", "#40739e", "#487eb0", "#8c7ae6"],
                "dots": ["#e58e26", "#f8b500", "#8e44ad", "#2c3e50", "#e74c3c", 
                        "#3498db", "#1abc9c", "#f39c12", "#d35400", "#c0392b",
                        "#9b59b6", "#34495e", "#16a085", "#27ae60", "#2980b9",
                        "#8e44ad"], 
                "decorations": ["#f4d03f", "#85c1e9", "#f8c471", "#a9dfbf"]
            }
        }
        self.current_scheme = "organic_flow"
    
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
    def decoration_colors(self):
        return self.schemes[self.current_scheme]["decorations"]
    
    @property
    def scheme_name(self):
        return self.schemes[self.current_scheme]["name"]

class EchoGardenPremiumRealtime:
    """Echo Garden Premium Real-time - 主应用类"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.setup_audio()
        self.bind_events()
        self.start_animation()
        
        print("🎨 Echo Garden Premium Real-time 启动成功!")
        print("✨ 支持实时音频波形显示和改进的树木形状")
    
    def setup_window(self):
        """设置窗口"""
        self.root.title("🎨 Echo Garden Premium Real-time - 高级实时音频点阵艺术版")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f6f0")
        
        # 窗口居中
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1200) // 2
        y = (self.root.winfo_screenheight() - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
    
    def setup_variables(self):
        """初始化变量"""
        self.palette = PremiumColorPalette()
        self.trees = []
        self.max_trees = 25
        self.animation_active = True
        
        # 音频相关
        self.audio_processor = None
        self.waveform_display = None
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
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
        
        # 音频控制按钮
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
        
        # 右侧 - 主画布区域
        right_panel = tk.Frame(main_frame, bg="#f8f6f0")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            right_panel, 
            text="🌳 Echo Garden Premium Real-time", 
            font=("Arial", 18, "bold"),
            bg="#f8f6f0", fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # 画布
        canvas_frame = tk.Frame(right_panel, bg="#ffffff", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#ffffff")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.renderer = DottedRenderer(self.canvas, dot_density=0.8)
        
        # 底部控制栏
        control_frame = tk.Frame(right_panel, bg="#f8f6f0")
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 声音输入
        input_frame = tk.Frame(control_frame, bg="#f8f6f0")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="🎵 声音描述:", bg="#f8f6f0", font=("Arial", 12)).pack(side=tk.LEFT)
        self.sound_entry = tk.Entry(input_frame, font=("Arial", 12), width=40)
        self.sound_entry.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        
        tk.Button(
            input_frame, text="🌱 种树", 
            command=self.plant_tree_from_text,
            font=("Arial", 12), bg="#2196F3", fg="white"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        # 快捷按钮
        button_frame = tk.Frame(control_frame, bg="#f8f6f0")
        button_frame.pack(fill=tk.X, pady=5)
        
        buttons = [
            ("🎨 配色1", lambda: self.switch_palette("organic_flow"), "#d45087"),
            ("🎨 配色2", lambda: self.switch_palette("ceramic_dots"), "#c44569"),
            ("🌲 森林", self.generate_forest, "#4CAF50"),
            ("🧹 清空", self.clear_canvas, "#f44336"),
            ("💾 保存", self.save_artwork, "#FF9800")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame, text=text, command=command,
                font=("Arial", 10), bg=color, fg="white", width=8
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # 状态栏
        self.status_label = tk.Label(
            control_frame, text=f"🎨 当前配色: {self.palette.scheme_name} | 树木数量: 0/{self.max_trees}",
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
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        self.sound_entry.bind("<Return>", lambda e: self.plant_tree_from_text())
    
    def toggle_recording(self):
        """切换录音状态"""
        if not self.audio_processor:
            return
        
        if self.audio_processor.is_recording:
            self.audio_processor.stop_recording()
            self.record_button.config(text="🎤 开始录音", bg="#4CAF50")
        else:
            self.audio_processor.start_recording()
            self.record_button.config(text="⏹️ 停止录音", bg="#f44336")
    
    def on_canvas_click(self, event):
        """画布点击事件"""
        self.create_tree(event.x, event.y)
    
    def on_key_press(self, event):
        """按键事件"""
        key = event.keysym
        if key == "1":
            self.switch_palette("organic_flow")
        elif key == "2":
            self.switch_palette("ceramic_dots")
        elif key.lower() == "f":
            self.generate_forest()
        elif key.lower() == "c":
            self.clear_canvas()
        elif key.lower() == "s":
            self.save_artwork()
    
    def create_tree(self, x, y, audio_features=None):
        """创建新树"""
        if len(self.trees) >= self.max_trees:
            self.trees.pop(0)  # 移除最老的树
        
        tree = ImprovedTree(self.canvas, self.renderer, self.palette, x, y)
        self.trees.append(tree)
        self.update_status()
    
    def plant_tree_from_text(self):
        """从文本描述种树"""
        text = self.sound_entry.get().strip()
        if not text:
            return
        
        # 在画布中心创建树
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        x = canvas_width // 2 + random.uniform(-100, 100)
        y = canvas_height - 50
        
        self.create_tree(x, y)
        self.sound_entry.delete(0, tk.END)
    
    def switch_palette(self, scheme_name):
        """切换配色方案"""
        self.palette.switch_scheme(scheme_name)
        self.update_background()
        self.update_status()
    
    def generate_forest(self):
        """生成艺术森林"""
        self.clear_canvas()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.generate_forest)
            return
        
        # 生成8棵随机树
        for _ in range(8):
            x = random.uniform(50, canvas_width - 50)
            y = random.uniform(canvas_height * 0.6, canvas_height - 50)
            self.create_tree(x, y)
    
    def clear_canvas(self):
        """清空画布"""
        self.canvas.delete("tree")
        self.trees.clear()
        self.update_status()
    
    def update_background(self):
        """更新背景"""
        bg_color = random.choice(self.palette.background_colors)
        self.canvas.config(bg=bg_color)
    
    def update_status(self):
        """更新状态栏"""
        self.status_label.config(
            text=f"🎨 当前配色: {self.palette.scheme_name} | 树木数量: {len(self.trees)}/{self.max_trees}"
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
            
            # 更新音频特征显示
            if self.audio_processor.is_recording:
                self.update_audio_features_display(latest_waveform)
        
        # 更新树木生长
        for tree in self.trees:
            if tree.update_growth():
                tree.draw()
        
        # 继续动画循环
        self.root.after(50, self.animation_loop)  # ~20 FPS
    
    def update_audio_features_display(self, waveform_data):
        """更新音频特征显示"""
        if not waveform_data:
            return
        
        # 简单计算一些音频特征
        try:
            volume = max(abs(x) for x in waveform_data) if waveform_data else 0
            energy = sum(x*x for x in waveform_data) / len(waveform_data) if waveform_data else 0
            
            feature_text = f"音量: {volume:.3f}\n能量: {energy:.3f}\n状态: 录音中"
            self.audio_features_label.config(text=feature_text)
        except:
            pass
    
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
    
    def cleanup(self):
        """清理资源"""
        self.animation_active = False
        if self.audio_processor:
            self.audio_processor.cleanup()

def main():
    """主函数"""
    print("🎨 启动 Echo Garden Premium Real-time - 高级实时音频点阵艺术版 🎨")
    print("✨ 支持实时音频波形显示和改进的树木形状")
    
    root = tk.Tk()
    app = EchoGardenPremiumRealtime(root)
    
    # 优雅退出处理
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
