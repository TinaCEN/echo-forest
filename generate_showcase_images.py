#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden - Showcase Image Generator
Generate beautiful showcase images for each theme
"""

import tkinter as tk
from tkinter import messagebox
import random
import math
import time
import os
from PIL import Image, ImageDraw, ImageFont
import sys

# Import the main classes from echo_garden_realtime
sys.path.append(os.path.dirname(__file__))
from echo_garden_realtime import ColorTheme, Tree, Grass, SoundSimulator

class ShowcaseGenerator:
    """Generate showcase images for each theme"""
    
    def __init__(self):
        self.themes = [ColorTheme.WARM, ColorTheme.COOL, ColorTheme.MONO, ColorTheme.SUNSET, ColorTheme.AURORA]
        self.canvas_width = 950
        self.canvas_height = 550
        self.output_dir = "showcase_images"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_sample_trees(self, theme, num_trees=15):
        """Create sample trees for showcase"""
        trees = []
        sound_simulator = SoundSimulator()
        
        # Define some interesting sound descriptions for variety
        sound_descriptions = [
            "melodic harmony", "deep bass", "bright treble", "rhythmic beat",
            "gentle whisper", "powerful crescendo", "flowing melody", "sharp staccato",
            "warm resonance", "crystal clear", "rich overtones", "dynamic pulse",
            "ethereal ambient", "vibrant energy", "peaceful calm"
        ]
        
        for i in range(num_trees):
            # Create varied positions
            x = random.randint(80, self.canvas_width - 80)
            y = random.randint(180, self.canvas_height - 80)
            
            # Generate audio features from sound descriptions
            description = random.choice(sound_descriptions)
            features = sound_simulator.analyze_text_input(description)
            
            # Create tree with random style
            tree_styles = ['classic', 'weeping', 'bushy', 'tall', 'wide', 'spiral', 'fractal']
            style = random.choice(tree_styles)
            
            tree = Tree(x, y, theme, features, style)
            # Make trees fully grown for showcase
            tree.growth = 1.0
            tree.is_growing = False
            
            trees.append(tree)
        
        return trees
    
    def create_sample_grasses(self, theme, trees):
        """Create sample grasses for showcase"""
        grasses = []
        
        # Generate grasses based on tree positions
        for _ in range(len(trees) // 2):
            x = random.randint(20, self.canvas_width - 20)
            y = random.randint(450, self.canvas_height - 20)
            
            # Collect nearby tree colors
            nearby_colors = []
            for tree in trees:
                distance = math.sqrt((tree.x - x)**2 + (tree.y - y)**2)
                if distance < 150:
                    if hasattr(tree, 'leaves_colors') and tree.leaves_colors:
                        nearby_colors.extend(tree.leaves_colors[:2])
            
            if not nearby_colors and theme.get('leaves'):
                nearby_colors = theme['leaves'][:3]
            
            grass = Grass(x, y, nearby_colors, theme)
            # Make grass fully grown
            grass.growth = 1.0
            grass.is_growing = False
            
            grasses.append(grass)
        
        return grasses
    
    def create_showcase_image(self, theme):
        """Create a showcase image for a theme"""
        # Create PIL image
        img = Image.new('RGB', (self.canvas_width, self.canvas_height), theme['bg_color'])
        draw = ImageDraw.Draw(img)
        
        # Create mock canvas for tree drawing
        class MockCanvas:
            def __init__(self, draw, width, height):
                self.draw = draw
                self.width = width
                self.height = height
                
            def create_line(self, *args, **kwargs):
                if len(args) >= 4:
                    coords = args[0] if isinstance(args[0], list) else args[:4]
                    if len(coords) >= 4:
                        # Convert coordinates to pairs
                        if len(coords) > 4:  # Multiple points
                            points = [(coords[i], coords[i+1]) for i in range(0, len(coords)-1, 2)]
                            for j in range(len(points)-1):
                                self.draw.line([points[j], points[j+1]], 
                                             fill=kwargs.get('fill', 'black'), 
                                             width=kwargs.get('width', 1))
                        else:  # Single line
                            self.draw.line(coords, 
                                         fill=kwargs.get('fill', 'black'), 
                                         width=kwargs.get('width', 1))
                            
            def create_oval(self, *args, **kwargs):
                if len(args) >= 4:
                    bbox = args[:4]
                    self.draw.ellipse(bbox, 
                                    fill=kwargs.get('fill', 'black'), 
                                    outline=kwargs.get('outline', None))
                                    
            def create_polygon(self, points, **kwargs):
                if points and len(points) >= 6:  # At least 3 points (6 coordinates)
                    # Convert flat list to tuples
                    if isinstance(points[0], (int, float)):
                        point_tuples = [(points[i], points[i+1]) for i in range(0, len(points), 2)]
                    else:
                        point_tuples = points
                    self.draw.polygon(point_tuples, 
                                    fill=kwargs.get('fill', 'black'), 
                                    outline=kwargs.get('outline', None))
                                    
            def create_rectangle(self, *args, **kwargs):
                # Skip rectangles (info panels) for cleaner showcase
                pass
                
            def create_text(self, *args, **kwargs):
                # Skip text for cleaner showcase  
                pass
        
        mock_canvas = MockCanvas(draw, self.canvas_width, self.canvas_height)
        
        # Generate trees and grasses
        trees = self.create_sample_trees(theme, 18)
        grasses = self.create_sample_grasses(theme, trees)
        
        # Draw grasses first (background)
        for grass in grasses:
            grass.draw(mock_canvas)
        
        # Draw trees
        for tree in trees:
            tree.draw(mock_canvas)
        
        # Add title text
        try:
            # Try to use a nice font, fall back to default if not available
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw title
            title = f"Echo Garden - {theme['name']}"
            bbox = draw.textbbox((0, 0), title, font=font)
            title_width = bbox[2] - bbox[0]
            draw.text(((self.canvas_width - title_width) // 2, 20), title, 
                     fill='#2F4F4F', font=font)
            
            # Draw tree count
            tree_info = f"{len(trees)} Trees • {len(grasses)} Grass Patches"
            bbox = draw.textbbox((0, 0), tree_info, font=small_font)
            info_width = bbox[2] - bbox[0]
            draw.text(((self.canvas_width - info_width) // 2, 50), tree_info, 
                     fill='#696969', font=small_font)
                     
        except Exception as e:
            print(f"Font rendering error: {e}")
        
        return img
    
    def generate_all_showcases(self):
        """Generate showcase images for all themes"""
        print("🎨 Generating Echo Garden showcase images...")
        
        for i, theme in enumerate(self.themes, 1):
            print(f"📸 Creating showcase for {theme['name']} ({i}/{len(self.themes)})...")
            
            # Create showcase image
            img = self.create_showcase_image(theme)
            
            # Save image
            filename = f"{theme['name'].lower().replace(' ', '_')}_showcase.png"
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath, 'PNG', quality=95, optimize=True)
            
            print(f"✅ Saved: {filepath}")
        
        # Create a combined overview image
        self.create_overview_image()
        
        print(f"\n🎉 All showcase images generated successfully!")
        print(f"📁 Images saved in: {os.path.abspath(self.output_dir)}")
    
    def create_overview_image(self):
        """Create a combined overview image showing all themes"""
        print("🖼️  Creating overview image...")
        
        # Create a larger overview image
        overview_width = self.canvas_width * 2
        overview_height = self.canvas_height * 3
        
        overview_img = Image.new('RGB', (overview_width, overview_height), '#F5F5F5')
        draw = ImageDraw.Draw(overview_img)
        
        # Draw title
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        title = "Echo Garden - All Gradient Themes"
        bbox = draw.textbbox((0, 0), title, font=font)
        title_width = bbox[2] - bbox[0]
        draw.text(((overview_width - title_width) // 2, 30), title, 
                 fill='#2F4F4F', font=font)
        
        # Arrange theme showcases in a grid
        positions = [
            (50, 100), (self.canvas_width + 50, 100),  # Top row
            (50, 100 + self.canvas_height), (self.canvas_width + 50, 100 + self.canvas_height),  # Middle row  
            ((overview_width - self.canvas_width) // 2, 100 + self.canvas_height * 2)  # Bottom center
        ]
        
        for i, theme in enumerate(self.themes):
            if i < len(positions):
                # Create mini showcase
                theme_img = self.create_showcase_image(theme)
                # Resize to fit in grid
                theme_img = theme_img.resize((self.canvas_width, self.canvas_height), Image.Resampling.LANCZOS)
                
                # Paste into overview
                x, y = positions[i]
                overview_img.paste(theme_img, (x, y))
        
        # Save overview
        overview_path = os.path.join(self.output_dir, "echo_garden_all_themes_overview.png")
        overview_img.save(overview_path, 'PNG', quality=95, optimize=True)
        print(f"✅ Overview saved: {overview_path}")

def main():
    """Generate all showcase images"""
    try:
        generator = ShowcaseGenerator()
        generator.generate_all_showcases()
    except Exception as e:
        print(f"❌ Error generating showcases: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
