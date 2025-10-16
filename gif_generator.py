#!/usr/bin/env python3
"""
Echo Garden GIF Generator
Generates animated GIFs showing how audio controls tree growth
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont
import imageio
import random
import math
import colorsys
import os
import time
import threading
from typing import List, Tuple, Dict, Optional

class AudioSimulator:
    """Simulates audio input with different patterns"""
    
    def __init__(self):
        self.patterns = {
            'quiet': self._quiet_pattern,
            'steady_beat': self._steady_beat,
            'crescendo': self._crescendo,
            'random_bursts': self._random_bursts,
            'rhythmic': self._rhythmic_pattern
        }
    
    def _quiet_pattern(self, frame: int) -> float:
        """Very quiet ambient sound"""
        return 0.1 + 0.05 * random.random()
    
    def _steady_beat(self, frame: int) -> float:
        """Steady beat pattern"""
        beat = math.sin(frame * 0.3) * 0.5 + 0.5
        return 0.2 + beat * 0.6
    
    def _crescendo(self, frame: int) -> float:
        """Gradually increasing volume"""
        progress = min(frame / 100, 1.0)
        base = 0.1 + progress * 0.7
        return base + 0.1 * math.sin(frame * 0.5)
    
    def _random_bursts(self, frame: int) -> float:
        """Random audio bursts"""
        if random.random() < 0.1:
            return 0.8 + 0.2 * random.random()
        return 0.1 + 0.1 * random.random()
    
    def _rhythmic_pattern(self, frame: int) -> float:
        """Complex rhythmic pattern"""
        beat1 = math.sin(frame * 0.2) * 0.3
        beat2 = math.sin(frame * 0.15) * 0.2
        beat3 = math.sin(frame * 0.35) * 0.1
        return 0.3 + beat1 + beat2 + beat3

class TreeNode:
    """Represents a node in the fractal tree"""
    
    def __init__(self, x: float, y: float, angle: float, length: float, depth: int, growth: float = 0.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
        self.depth = depth
        self.growth = growth
        self.max_growth = 1.0
        self.children: List['TreeNode'] = []
        self.width = max(1, 8 - depth)
        
    def grow(self, audio_level: float, dt: float):
        """Grow this node based on audio level"""
        if self.growth < self.max_growth:
            growth_rate = audio_level * 2.0 * dt
            self.growth = min(self.max_growth, self.growth + growth_rate)
    
    def get_end_pos(self) -> Tuple[float, float]:
        """Get the end position of this branch"""
        actual_length = self.length * self.growth
        end_x = self.x + math.cos(self.angle) * actual_length
        end_y = self.y + math.sin(self.angle) * actual_length
        return end_x, end_y
    
    def spawn_children(self, audio_level: float):
        """Spawn child branches when growth is sufficient"""
        if (self.growth > 0.8 and self.depth < 6 and 
            len(self.children) == 0 and audio_level > 0.3):
            
            end_x, end_y = self.get_end_pos()
            
            # Create 2-3 child branches
            num_children = 2 if random.random() < 0.7 else 3
            angle_spread = 0.6 + audio_level * 0.4
            
            for i in range(num_children):
                child_angle = self.angle + (i - num_children/2 + 0.5) * angle_spread
                child_length = self.length * (0.7 + 0.2 * random.random())
                
                child = TreeNode(end_x, end_y, child_angle, child_length, self.depth + 1)
                self.children.append(child)

class EchoGardenGIF:
    """Main GIF generator class"""
    
    def __init__(self):
        self.width = 800
        self.height = 600
        self.trees: List[TreeNode] = []
        self.audio_sim = AudioSimulator()
        self.frame_count = 0
        self.frames: List[Image.Image] = []
        
        # Gradient themes
        self.themes = {
            'sunset': [(255, 94, 77), (255, 154, 0), (255, 206, 84)],
            'ocean': [(64, 224, 208), (70, 130, 180), (123, 104, 238)],
            'forest': [(34, 139, 34), (107, 142, 35), (154, 205, 50)],
            'cosmic': [(138, 43, 226), (75, 0, 130), (72, 61, 139)],
            'aurora': [(0, 255, 127), (64, 224, 208), (135, 206, 235)]
        }
        
        self.current_theme = 'forest'
        self.background_color = (20, 25, 30)
        
    def create_gradient_background(self) -> Image.Image:
        """Create a gradient background"""
        img = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(img)
        
        colors = self.themes[self.current_theme]
        
        # Create vertical gradient
        for y in range(self.height):
            progress = y / self.height
            
            if progress < 0.5:
                # Blend between first and second color
                blend_progress = progress * 2
                color = self._blend_colors(colors[0], colors[1], blend_progress)
            else:
                # Blend between second and third color
                blend_progress = (progress - 0.5) * 2
                color = self._blend_colors(colors[1], colors[2], blend_progress)
            
            draw.line([(0, y), (self.width, y)], fill=color)
        
        return img
    
    def _blend_colors(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Blend two colors"""
        return (
            int(color1[0] * (1 - t) + color2[0] * t),
            int(color1[1] * (1 - t) + color2[1] * t),
            int(color1[2] * (1 - t) + color2[2] * t)
        )
    
    def plant_initial_trees(self):
        """Plant initial tree seeds"""
        self.trees = []
        
        # Plant 3-5 trees at the bottom
        num_trees = random.randint(3, 5)
        for i in range(num_trees):
            x = (i + 1) * self.width / (num_trees + 1) + random.randint(-50, 50)
            y = self.height - 50
            angle = -math.pi/2 + random.uniform(-0.2, 0.2)  # Mostly upward
            length = 40 + random.randint(-10, 10)
            
            tree = TreeNode(x, y, angle, length, 0)
            self.trees.append(tree)
    
    def update_trees(self, audio_level: float, dt: float = 0.1):
        """Update all trees based on audio level"""
        def update_node(node: TreeNode):
            node.grow(audio_level, dt)
            node.spawn_children(audio_level)
            
            for child in node.children:
                update_node(child)
        
        for tree in self.trees:
            update_node(tree)
    
    def draw_trees(self, draw: ImageDraw.Draw, audio_level: float = 0.5):
        """Draw all trees"""
        def draw_node(node: TreeNode):
            if node.growth > 0.01:
                end_x, end_y = node.get_end_pos()
                
                # Calculate color based on depth and growth
                colors = self.themes[self.current_theme]
                depth_factor = min(node.depth / 5.0, 1.0)
                
                if node.depth <= 1:
                    color = colors[0]  # Trunk color
                elif node.depth <= 3:
                    color = self._blend_colors(colors[0], colors[1], depth_factor)
                else:
                    color = colors[2]  # Leaf color
                
                # Add some brightness based on recent growth
                brightness = 1.0 + min(audio_level * 0.3, 0.5)
                color = tuple(min(255, int(c * brightness)) for c in color)
                
                # Draw the branch
                width = max(1, int(node.width * (0.5 + node.growth * 0.5)))
                
                if width > 1:
                    # Draw thick lines as polygons for better appearance
                    dx = math.cos(node.angle + math.pi/2) * width/2
                    dy = math.sin(node.angle + math.pi/2) * width/2
                    
                    points = [
                        (node.x - dx, node.y - dy),
                        (node.x + dx, node.y + dy),
                        (end_x + dx, end_y + dy),
                        (end_x - dx, end_y - dy)
                    ]
                    draw.polygon(points, fill=color)
                else:
                    draw.line([(node.x, node.y), (end_x, end_y)], fill=color, width=1)
            
            # Draw children
            for child in node.children:
                draw_node(child)
        
        for tree in self.trees:
            draw_node(tree)
    
    def add_audio_visualization(self, draw: ImageDraw.Draw, audio_level: float):
        """Add audio level visualization"""
        # Draw audio level bar
        bar_width = 20
        bar_height = 200
        bar_x = self.width - 40
        bar_y = 50
        
        # Background bar
        draw.rectangle([(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)], 
                      fill=(40, 40, 40), outline=(100, 100, 100))
        
        # Audio level fill
        fill_height = int(bar_height * audio_level)
        if fill_height > 0:
            colors = self.themes[self.current_theme]
            color = colors[1] if audio_level < 0.5 else colors[2]
            
            draw.rectangle([(bar_x, bar_y + bar_height - fill_height), 
                          (bar_x + bar_width, bar_y + bar_height)], 
                          fill=color)
        
        # Add text label
        try:
            font = ImageFont.truetype("Arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw.text((bar_x - 10, bar_y + bar_height + 10), "Audio", 
                 fill=(200, 200, 200), font=font)
    
    def generate_frame(self, audio_level: float) -> Image.Image:
        """Generate a single frame"""
        # Create background
        img = self.create_gradient_background()
        draw = ImageDraw.Draw(img)
        
        # Update and draw trees
        self.update_trees(audio_level)
        self.draw_trees(draw, audio_level)
        
        # Add audio visualization
        self.add_audio_visualization(draw, audio_level)
        
        # Add frame counter
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((20, 20), f"Frame: {self.frame_count}", fill=(200, 200, 200), font=font)
        
        return img
    
    def generate_gif(self, pattern_name: str, duration: int = 5, fps: int = 10) -> str:
        """Generate a GIF for a specific audio pattern"""
        print(f"🎬 Generating GIF for '{pattern_name}' pattern...")
        
        self.frame_count = 0
        self.frames = []
        
        # Reset trees
        self.plant_initial_trees()
        
        # Get audio pattern function
        audio_pattern = self.audio_sim.patterns[pattern_name]
        
        total_frames = duration * fps
        
        for frame in range(total_frames):
            self.frame_count = frame
            
            # Get audio level for this frame
            audio_level = audio_pattern(frame)
            
            # Generate frame
            img = self.generate_frame(audio_level)
            self.frames.append(img)
            
            if frame % 10 == 0:
                print(f"  Generated frame {frame}/{total_frames}")
        
        # Save GIF
        filename = f"audio_growth_{pattern_name}.gif"
        filepath = os.path.join("showcase_images", filename)
        
        # Create showcase_images directory if it doesn't exist
        os.makedirs("showcase_images", exist_ok=True)
        
        # Save as GIF
        self.frames[0].save(
            filepath,
            save_all=True,
            append_images=self.frames[1:],
            duration=int(1000/fps),  # Duration in milliseconds
            loop=0,
            optimize=True
        )
        
        print(f"✅ Saved GIF: {filename}")
        return filepath

def main():
    """Generate GIFs for different audio patterns"""
    generator = EchoGardenGIF()
    
    patterns_to_generate = [
        ('quiet', 'Quiet ambient sounds'),
        ('steady_beat', 'Steady beat pattern'),
        ('crescendo', 'Gradually increasing volume'),
        ('random_bursts', 'Random audio bursts'),
        ('rhythmic', 'Complex rhythmic pattern')
    ]
    
    print("🌳 Echo Garden GIF Generator")
    print("=" * 50)
    
    generated_files = []
    
    for pattern_name, description in patterns_to_generate:
        print(f"\n📊 Pattern: {description}")
        
        # Use different themes for variety
        themes = list(generator.themes.keys())
        generator.current_theme = themes[len(generated_files) % len(themes)]
        print(f"🎨 Using theme: {generator.current_theme}")
        
        filepath = generator.generate_gif(pattern_name, duration=6, fps=8)
        generated_files.append(filepath)
    
    print("\n" + "=" * 50)
    print("🎉 GIF Generation Complete!")
    print(f"Generated {len(generated_files)} GIF files:")
    
    for filepath in generated_files:
        file_size = os.path.getsize(filepath) / (1024 * 1024)  # Size in MB
        print(f"  📁 {os.path.basename(filepath)} ({file_size:.1f} MB)")
    
    print(f"\n📂 All files saved to: showcase_images/")
    print("🎬 These GIFs demonstrate how audio controls tree growth in Echo Garden!")

if __name__ == "__main__":
    main()
