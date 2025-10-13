#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden - Automated Showcase Generator
Create beautiful example gardens for each theme
"""

import tkinter as tk
import random
import math
import time
import os
import sys

# Import from the main program
from echo_garden_realtime import EchoGarden, ColorTheme, Tree, Grass, SoundSimulator

class AutoShowcaseGenerator(EchoGarden):
    """Automated showcase generator that extends EchoGarden"""
    
    def __init__(self, auto_mode=True):
        super().__init__()
        self.auto_mode = auto_mode
        self.current_theme_index = 0
        self.showcase_count = 0
        self.output_dir = "showcase_images"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        if auto_mode:
            # Schedule automatic generation
            self.root.after(1000, self.generate_next_showcase)
    
    def create_beautiful_garden(self, theme, tree_count=15):
        """Create a beautiful garden for the given theme"""
        # Clear existing garden
        self.trees.clear()
        self.grasses.clear()
        
        # Set theme
        self.current_theme = theme
        self.canvas.config(bg=theme['bg_color'])
        
        sound_simulator = SoundSimulator()
        
        # Define interesting sound descriptions for variety
        sound_descriptions = [
            "melodic harmony flowing", "deep bass resonating", "bright crystal treble", 
            "rhythmic energetic beat", "gentle morning whisper", "powerful crescendo wave",
            "flowing water melody", "sharp staccato rhythm", "warm golden resonance", 
            "crystal clear notes", "rich overtones", "dynamic pulse wave",
            "ethereal ambient space", "vibrant spring energy", "peaceful evening calm",
            "thunderous deep boom", "delicate wind chimes", "soaring high notes",
            "mysterious forest sounds", "celebration fanfare", "quiet meditation"
        ]
        
        # Create trees in artistic positions
        for i in range(tree_count):
            # Create natural clusters and spacing
            if i < 5:  # Main cluster
                x = random.randint(200, 400)
                y = random.randint(200, 400)
            elif i < 10:  # Secondary cluster  
                x = random.randint(500, 750)
                y = random.randint(180, 380)
            else:  # Scattered trees
                x = random.randint(80, 850)
                y = random.randint(150, 450)
            
            # Generate varied audio features
            description = random.choice(sound_descriptions)
            features = sound_simulator.analyze_text_input(description)
            
            # Create tree with specific style distribution
            tree_styles = ['classic', 'weeping', 'bushy', 'tall', 'wide', 'spiral', 'fractal']
            style_weights = [3, 2, 2, 2, 1, 1, 1]  # Prefer classic and natural styles
            style = random.choices(tree_styles, weights=style_weights)[0]
            
            tree = Tree(x, y, theme, features, style)
            # Make trees fully grown for showcase
            tree.growth = 1.0
            tree.is_growing = False
            
            self.trees.append(tree)
        
        # Generate grass after trees (10+ trees trigger grass)
        self.check_grass_generation()
        # Make all grass fully grown
        for grass in self.grasses:
            grass.growth = 1.0
            grass.is_growing = False
        
        # Force redraw
        self.redraw()
        self.root.update()
    
    def save_current_showcase(self, theme_name):
        """Save current garden as EPS and try to convert to PNG"""
        timestamp = int(time.time())
        base_filename = f"{theme_name.lower().replace(' ', '_')}_showcase_{timestamp}"
        
        # Save as EPS first
        eps_filename = f"{base_filename}.eps"
        eps_path = os.path.join(self.output_dir, eps_filename)
        
        try:
            self.canvas.postscript(file=eps_path, colormode='color', 
                                 width=self.canvas.winfo_width(), 
                                 height=self.canvas.winfo_height())
            print(f"✅ Saved EPS: {eps_path}")
            
            # Try to convert EPS to PNG using PIL if available
            try:
                from PIL import Image
                png_filename = f"{base_filename}.png"
                png_path = os.path.join(self.output_dir, png_filename)
                
                # Open and convert EPS to PNG
                img = Image.open(eps_path)
                img.save(png_path, 'PNG', quality=95, optimize=True)
                print(f"✅ Converted to PNG: {png_path}")
                
                # Remove EPS file to keep only PNG
                os.remove(eps_path)
                return png_path
                
            except ImportError:
                print("⚠️  PIL not available, keeping EPS format")
                return eps_path
            except Exception as e:
                print(f"⚠️  PNG conversion failed: {e}, keeping EPS")
                return eps_path
                
        except Exception as e:
            print(f"❌ Failed to save showcase: {e}")
            return None
    
    def generate_next_showcase(self):
        """Generate the next theme showcase"""
        if self.current_theme_index >= len(self.themes):
            print(f"\n🎉 All {len(self.themes)} showcase images generated!")
            print(f"📁 Images saved in: {os.path.abspath(self.output_dir)}")
            
            # Show completion message
            tk.messagebox.showinfo("Showcase Complete", 
                                 f"Generated {len(self.themes)} beautiful showcase images!\n\n"
                                 f"Saved in: {os.path.abspath(self.output_dir)}")
            return
        
        # Get current theme
        theme = self.themes[self.current_theme_index]
        theme_name = theme['name']
        
        print(f"🎨 Generating showcase {self.current_theme_index + 1}/{len(self.themes)}: {theme_name}")
        
        # Create beautiful garden
        self.create_beautiful_garden(theme)
        
        # Wait a moment for rendering
        self.root.after(500, lambda: self.save_and_continue(theme_name))
    
    def save_and_continue(self, theme_name):
        """Save current showcase and continue to next"""
        # Save current showcase
        saved_path = self.save_current_showcase(theme_name)
        
        if saved_path:
            print(f"📸 Showcase for '{theme_name}' saved successfully")
        
        # Move to next theme
        self.current_theme_index += 1
        
        # Schedule next showcase generation
        self.root.after(1000, self.generate_next_showcase)
    
    def run(self):
        """Run the showcase generator"""
        print("🌳 Starting Echo Garden Showcase Generator 🌳")
        print(f"📸 Will generate {len(self.themes)} showcase images...")
        print("🎨 Generating beautiful examples for each theme:")
        for i, theme in enumerate(self.themes, 1):
            print(f"   {i}. {theme['name']}")
        print()
        
        super().run()

def main():
    """Generate showcase images for all themes"""
    try:
        generator = AutoShowcaseGenerator(auto_mode=True)
        generator.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
