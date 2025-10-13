#!/usr/bin/env python3
"""
Realistic Audio-Tree Growth GIF Generator
Creates high-quality GIFs that closely mimic the actual Echo Garden behavior
"""

import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import imageio
import random
import math
import colorsys
import os
import time
import numpy as np
from typing import List, Tuple, Dict, Optional

class RealisticTreeGrowth:
    """More realistic tree growth simulation matching Echo Garden's behavior"""
    
    def __init__(self, width: int = 1200, height: int = 800):
        self.width = width
        self.height = height
        self.trees = []
        self.grass_patches = []
        self.audio_history = []
        self.frame_count = 0
        
        # Growth parameters
        self.growth_speed = 0.015
        self.branch_threshold = 0.7
        self.max_depth = 8
        
        # Themes matching Echo Garden
        self.themes = {
            'Sunset Dreams': {
                'colors': [(255, 94, 77), (255, 154, 0), (255, 206, 84)],
                'bg': (25, 15, 35)
            },
            'Ocean Breeze': {
                'colors': [(64, 224, 208), (70, 130, 180), (123, 104, 238)],
                'bg': (15, 25, 35)
            },
            'Forest Whisper': {
                'colors': [(34, 139, 34), (107, 142, 35), (154, 205, 50)],
                'bg': (20, 30, 20)
            },
            'Cosmic Dance': {
                'colors': [(138, 43, 226), (75, 0, 130), (72, 61, 139)],
                'bg': (15, 10, 25)
            },
            'Aurora Magic': {
                'colors': [(0, 255, 127), (64, 224, 208), (135, 206, 235)],
                'bg': (20, 25, 35)
            }
        }
        
        self.current_theme = 'Forest Whisper'
        
    def simulate_microphone_input(self, pattern: str, frame: int) -> float:
        """Simulate realistic microphone patterns"""
        patterns = {
            'speaking': self._speaking_pattern,
            'music_beat': self._music_pattern, 
            'whistling': self._whistling_pattern,
            'clapping': self._clapping_pattern,
            'singing': self._singing_pattern,
            'silence_to_noise': self._silence_to_noise
        }
        
        return patterns.get(pattern, self._speaking_pattern)(frame)
    
    def _speaking_pattern(self, frame: int) -> float:
        """Simulate someone speaking"""
        # Simulate speech with pauses and emphasis
        cycle = frame % 60
        if cycle < 15:  # Speaking
            base = 0.4 + 0.3 * math.sin(frame * 0.8)
            emphasis = 0.2 * math.sin(frame * 2.5) if cycle % 4 == 0 else 0
            return max(0.1, base + emphasis + 0.1 * random.random())
        elif cycle < 25:  # Pause
            return 0.1 + 0.05 * random.random()
        elif cycle < 40:  # Speaking again
            return 0.5 + 0.2 * math.sin(frame * 1.2) + 0.1 * random.random()
        else:  # Longer pause
            return 0.08 + 0.03 * random.random()
    
    def _music_pattern(self, frame: int) -> float:
        """Simulate rhythmic music"""
        beat = math.sin(frame * 0.4) ** 2
        bass = 0.3 * math.sin(frame * 0.1)
        treble = 0.2 * math.sin(frame * 1.2)
        return 0.2 + beat * 0.5 + bass + treble
    
    def _whistling_pattern(self, frame: int) -> float:
        """Simulate whistling a tune"""
        melody = 0.4 + 0.3 * math.sin(frame * 0.3 + math.sin(frame * 0.05))
        vibrato = 0.1 * math.sin(frame * 3.0)
        return melody + vibrato
    
    def _clapping_pattern(self, frame: int) -> float:
        """Simulate rhythmic clapping"""
        clap_cycle = frame % 20
        if clap_cycle < 2:
            return 0.9 + 0.1 * random.random()
        elif clap_cycle < 5:
            return 0.3 * (1 - (clap_cycle - 2) / 3)
        else:
            return 0.05 + 0.05 * random.random()
    
    def _singing_pattern(self, frame: int) -> float:
        """Simulate singing with varying pitch and volume"""
        note_length = 25
        note_in_phrase = (frame // note_length) % 8
        
        # Different notes have different volumes
        note_volumes = [0.6, 0.7, 0.5, 0.8, 0.6, 0.4, 0.7, 0.3]
        base_volume = note_volumes[note_in_phrase]
        
        # Add vibrato and breath
        vibrato = 0.1 * math.sin(frame * 1.5)
        breath = 0.05 * math.sin(frame * 0.1)
        
        return base_volume + vibrato + breath
    
    def _silence_to_noise(self, frame: int) -> float:
        """Gradual transition from silence to activity"""
        progress = min(frame / 120.0, 1.0)
        if progress < 0.3:
            return 0.05 + 0.02 * random.random()
        elif progress < 0.6:
            return 0.1 + progress * 0.3 + 0.1 * random.random()
        else:
            return 0.3 + 0.4 * math.sin(frame * 0.5) + 0.1 * random.random()

class TreeBranch:
    """Individual branch of a tree"""
    
    def __init__(self, start_x: float, start_y: float, angle: float, 
                 length: float, depth: int, parent=None):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
        self.base_length = length
        self.current_length = 0.0
        self.growth = 0.0
        self.depth = depth
        self.parent = parent
        self.children = []
        
        self.width = max(1, 12 - depth * 1.5)
        self.grown = False
        self.can_branch = True
        
    def get_end_pos(self) -> Tuple[float, float]:
        """Calculate current end position"""
        actual_length = self.current_length
        end_x = self.start_x + math.cos(self.angle) * actual_length
        end_y = self.start_y + math.sin(self.angle) * actual_length
        return end_x, end_y
    
    def grow(self, audio_level: float, growth_speed: float):
        """Grow this branch based on audio"""
        if self.current_length < self.base_length:
            # Growth rate depends on audio level
            rate = growth_speed * (0.5 + audio_level * 1.5)
            self.current_length = min(self.base_length, self.current_length + rate * self.base_length)
            self.growth = self.current_length / self.base_length
            
            if self.growth >= 1.0 and not self.grown:
                self.grown = True
    
    def should_branch(self, audio_level: float) -> bool:
        """Determine if this branch should create children"""
        return (self.grown and 
                self.can_branch and 
                self.depth < 8 and 
                len(self.children) == 0 and
                audio_level > 0.25 and
                random.random() < 0.3)
    
    def create_children(self):
        """Create child branches"""
        if not self.can_branch:
            return
            
        end_x, end_y = self.get_end_pos()
        
        # Create 2-3 children with natural angles
        num_children = random.choice([2, 2, 3])  # Favor 2 children
        angle_spread = 0.8 + random.uniform(-0.2, 0.2)
        
        for i in range(num_children):
            child_angle = self.angle + (i - num_children/2 + 0.5) * angle_spread
            child_length = self.base_length * random.uniform(0.6, 0.8)
            
            child = TreeBranch(end_x, end_y, child_angle, child_length, self.depth + 1, self)
            self.children.append(child)
        
        self.can_branch = False

class HighQualityGIFGenerator:
    """High-quality GIF generator"""
    
    def __init__(self):
        self.tree_growth = RealisticTreeGrowth(1200, 800)
        self.frames = []
        
    def create_gradient_background(self) -> Image.Image:
        """Create smooth gradient background"""
        width, height = self.tree_growth.width, self.tree_growth.height
        theme = self.tree_growth.themes[self.tree_growth.current_theme]
        colors = theme['colors']
        bg_color = theme['bg']
        
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Create multi-point gradient
        for y in range(height):
            progress = y / height
            
            if progress < 0.4:
                # Top gradient
                t = progress / 0.4
                color = self._blend_colors(colors[2], colors[1], t)
            elif progress < 0.7:
                # Middle gradient  
                t = (progress - 0.4) / 0.3
                color = self._blend_colors(colors[1], colors[0], t)
            else:
                # Bottom gradient (darker)
                t = (progress - 0.7) / 0.3
                dark_color = tuple(int(c * 0.3) for c in colors[0])
                color = self._blend_colors(colors[0], dark_color, t)
            
            draw.line([(0, y), (width, y)], fill=color)
        
        return img
    
    def _blend_colors(self, c1: Tuple[int, int, int], c2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Blend two colors smoothly"""
        return (
            int(c1[0] * (1-t) + c2[0] * t),
            int(c1[1] * (1-t) + c2[1] * t), 
            int(c1[2] * (1-t) + c2[2] * t)
        )
    
    def plant_seed_trees(self):
        """Plant initial tree seeds"""
        trees = []
        width, height = self.tree_growth.width, self.tree_growth.height
        
        # Plant 4-6 trees along the bottom
        num_trees = random.randint(4, 6)
        for i in range(num_trees):
            x = (i + 1) * width / (num_trees + 1) + random.randint(-80, 80)
            y = height - 40 - random.randint(0, 20)
            
            # Mostly upward with slight variation
            angle = -math.pi/2 + random.uniform(-0.15, 0.15)
            length = random.uniform(60, 100)
            
            trunk = TreeBranch(x, y, angle, length, 0)
            trees.append(trunk)
        
        return trees
    
    def update_trees(self, trees: List[TreeBranch], audio_level: float):
        """Update all trees recursively"""
        def update_branch(branch: TreeBranch):
            # Grow this branch
            branch.grow(audio_level, self.tree_growth.growth_speed)
            
            # Check for branching
            if branch.should_branch(audio_level):
                branch.create_children()
            
            # Update children
            for child in branch.children:
                update_branch(child)
        
        for tree in trees:
            update_branch(tree)
    
    def draw_trees(self, draw: ImageDraw.Draw, trees: List[TreeBranch], audio_level: float):
        """Draw all trees with realistic appearance"""
        theme = self.tree_growth.themes[self.tree_growth.current_theme]
        colors = theme['colors']
        
        def draw_branch(branch: TreeBranch):
            if branch.current_length > 1:
                end_x, end_y = branch.get_end_pos()
                
                # Color based on depth
                if branch.depth == 0:
                    color = colors[0]  # Trunk
                elif branch.depth <= 3:
                    # Blend trunk to branch color
                    t = min(branch.depth / 3.0, 1.0)
                    color = self._blend_colors(colors[0], colors[1], t)
                else:
                    # Leaf colors
                    color = colors[2]
                
                # Brightness based on audio
                brightness = 1.0 + audio_level * 0.4
                color = tuple(min(255, int(c * brightness)) for c in color)
                
                # Width tapers with depth
                width = max(1, int(branch.width * (1 - branch.depth * 0.1)))
                
                # Draw branch
                if width > 2:
                    # Draw as polygon for thick branches
                    dx = math.cos(branch.angle + math.pi/2) * width/2
                    dy = math.sin(branch.angle + math.pi/2) * width/2
                    
                    points = [
                        (branch.start_x - dx, branch.start_y - dy),
                        (branch.start_x + dx, branch.start_y + dy),
                        (end_x + dx, end_y + dy),
                        (end_x - dx, end_y - dy)
                    ]
                    draw.polygon(points, fill=color)
                else:
                    draw.line([(branch.start_x, branch.start_y), (end_x, end_y)], 
                             fill=color, width=width)
            
            # Draw children
            for child in branch.children:
                draw_branch(child)
        
        for tree in trees:
            draw_branch(tree)
    
    def add_ui_elements(self, draw: ImageDraw.Draw, audio_level: float, pattern_name: str, frame: int):
        """Add UI elements like in the real application"""
        width, height = self.tree_growth.width, self.tree_growth.height
        
        # Audio level indicator (like the real app)
        indicator_size = 30
        indicator_x = width - 60
        indicator_y = 40
        
        # Background circle
        draw.ellipse([(indicator_x - indicator_size, indicator_y - indicator_size),
                     (indicator_x + indicator_size, indicator_y + indicator_size)],
                    fill=(40, 40, 40, 180), outline=(100, 100, 100))
        
        # Audio level fill
        if audio_level > 0.1:
            fill_size = indicator_size * audio_level
            theme_colors = self.tree_growth.themes[self.tree_growth.current_theme]['colors']
            color = theme_colors[1] if audio_level < 0.5 else theme_colors[2]
            
            draw.ellipse([(indicator_x - fill_size, indicator_y - fill_size),
                         (indicator_x + fill_size, indicator_y + fill_size)],
                        fill=color)
        
        # Load font
        try:
            title_font = ImageFont.truetype("Arial.ttf", 24)
            text_font = ImageFont.truetype("Arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Title and info
        draw.text((30, 30), "Echo Garden - Audio Growth Demo", 
                 fill=(255, 255, 255), font=title_font)
        
        draw.text((30, 70), f"Pattern: {pattern_name.replace('_', ' ').title()}", 
                 fill=(200, 200, 200), font=text_font)
        
        draw.text((30, 100), f"Theme: {self.tree_growth.current_theme}", 
                 fill=(200, 200, 200), font=text_font)
        
        draw.text((30, height - 60), f"Audio Level: {audio_level:.2f}", 
                 fill=(200, 200, 200), font=text_font)
        
        draw.text((30, height - 30), f"Frame: {frame}", 
                 fill=(150, 150, 150), font=text_font)
    
    def generate_demo_gif(self, pattern_name: str, theme_name: str, 
                         duration: int = 8, fps: int = 12) -> str:
        """Generate a high-quality demo GIF"""
        print(f"🎬 Creating {pattern_name} demo with {theme_name} theme...")
        
        self.tree_growth.current_theme = theme_name
        self.frames = []
        
        # Plant trees
        trees = self.plant_seed_trees()
        
        total_frames = duration * fps
        
        for frame in range(total_frames):
            # Get audio level for this pattern
            audio_level = self.tree_growth.simulate_microphone_input(pattern_name, frame)
            
            # Create frame
            img = self.create_gradient_background()
            draw = ImageDraw.Draw(img)
            
            # Update and draw trees
            self.update_trees(trees, audio_level)
            self.draw_trees(draw, trees, audio_level)
            
            # Add UI elements
            self.add_ui_elements(draw, audio_level, pattern_name, frame)
            
            self.frames.append(img)
            
            if frame % 15 == 0:
                print(f"  Frame {frame}/{total_frames} - Audio: {audio_level:.2f}")
        
        # Save GIF
        filename = f"demo_{pattern_name}_{theme_name.lower().replace(' ', '_')}.gif"
        filepath = os.path.join("showcase_images", filename)
        
        os.makedirs("showcase_images", exist_ok=True)
        
        self.frames[0].save(
            filepath,
            save_all=True,
            append_images=self.frames[1:],
            duration=int(1000/fps),
            loop=0,
            optimize=True,
            quality=95
        )
        
        file_size = os.path.getsize(filepath) / (1024 * 1024)
        print(f"✅ Saved: {filename} ({file_size:.1f} MB)")
        
        return filepath

def main():
    """Generate demonstration GIFs"""
    generator = HighQualityGIFGenerator()
    
    demos = [
        ('speaking', 'Forest Whisper'),
        ('music_beat', 'Cosmic Dance'),
        ('clapping', 'Ocean Breeze'),
        ('singing', 'Aurora Magic'),
        ('silence_to_noise', 'Sunset Dreams')
    ]
    
    print("🌳 Echo Garden - Realistic Audio Growth Demo Generator")
    print("=" * 60)
    
    generated_files = []
    
    for pattern, theme in demos:
        filepath = generator.generate_demo_gif(pattern, theme, duration=10, fps=10)
        generated_files.append(filepath)
        print()
    
    print("=" * 60)
    print(f"🎉 Generated {len(generated_files)} demonstration GIFs!")
    
    total_size = 0
    for filepath in generated_files:
        size = os.path.getsize(filepath) / (1024 * 1024)
        total_size += size
        print(f"  📁 {os.path.basename(filepath)} ({size:.1f} MB)")
    
    print(f"\n📊 Total size: {total_size:.1f} MB")
    print("📂 Location: showcase_images/")
    print("\n🎯 These GIFs demonstrate realistic audio-responsive tree growth!")
    print("   Each shows different microphone input patterns and their effects.")

if __name__ == "__main__":
    main()
