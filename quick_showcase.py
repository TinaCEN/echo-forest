#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden - Quick Showcase Creator
Create sample gardens and save them as images
"""

import tkinter as tk
import random
import time
import os
from echo_garden_realtime import EchoGarden, ColorTheme, Tree, SoundSimulator

class QuickShowcase(EchoGarden):
    """Quick showcase creator"""
    
    def __init__(self):
        super().__init__()
        self.output_dir = "showcase_images"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Add a button for manual showcase generation
        self.create_showcase_buttons()
    
    def create_showcase_buttons(self):
        """Add showcase generation buttons"""
        # Create showcase frame
        showcase_frame = tk.Frame(self.root)
        showcase_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        tk.Label(showcase_frame, text="📸 Showcase Generation:", 
                font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Individual theme buttons
        themes = [
            ("Warm", ColorTheme.WARM),
            ("Cool", ColorTheme.COOL), 
            ("Galaxy", ColorTheme.MONO),
            ("Sunset", ColorTheme.SUNSET),
            ("Aurora", ColorTheme.AURORA)
        ]
        
        for name, theme in themes:
            tk.Button(showcase_frame, 
                     text=f"🎨 {name}", 
                     command=lambda t=theme: self.create_theme_showcase(t),
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=2)
        
        # Generate all button
        tk.Button(showcase_frame, 
                 text="🌟 Generate All", 
                 command=self.generate_all_showcases,
                 font=("Arial", 10, "bold"),
                 bg='lightgreen').pack(side=tk.RIGHT, padx=5)
    
    def create_theme_showcase(self, theme):
        """Create showcase for a single theme"""
        print(f"🎨 Creating showcase for {theme['name']}...")
        
        # Clear and set theme
        self.clear_garden()
        self.current_theme = theme
        self.canvas.config(bg=theme['bg_color'])
        self.theme_label.config(text=f"Current Theme: {theme['name']}")
        
        # Create beautiful garden
        self.create_sample_garden()
        
        # Update display
        self.root.update()
        time.sleep(0.5)  # Let it render
        
        # Save showcase
        self.save_themed_showcase(theme['name'])
    
    def create_sample_garden(self):
        """Create a beautiful sample garden"""
        sound_simulator = SoundSimulator()
        
        # Interesting sound descriptions
        descriptions = [
            "melodic flowing harmony", "deep resonant bass", "bright crystal chimes",
            "rhythmic pulsing beat", "gentle whispered melody", "powerful crescendo",
            "flowing water sounds", "sharp percussive hits", "warm golden tones",
            "ethereal ambient space", "vibrant energetic burst", "peaceful calm notes",
            "mysterious forest echo", "celebration fanfare", "meditative silence",
            "thunderous dramatic boom", "delicate wind chimes", "soaring high melody"
        ]
        
        # Create 15-20 trees in artistic arrangement
        num_trees = random.randint(15, 20)
        
        for i in range(num_trees):
            # Create natural clustering
            if i < 6:  # Main cluster (left-center)
                x = random.randint(150, 350)
                y = random.randint(200, 400)
            elif i < 12:  # Secondary cluster (right)
                x = random.randint(500, 750)
                y = random.randint(180, 380)
            elif i < 16:  # Background trees
                x = random.randint(100, 800)
                y = random.randint(150, 250)
            else:  # Scattered foreground
                x = random.randint(80, 850)
                y = random.randint(350, 480)
            
            # Generate audio features
            description = random.choice(descriptions)
            features = sound_simulator.analyze_text_input(description)
            
            # Artistic style selection
            styles = ['classic', 'weeping', 'bushy', 'tall', 'wide', 'spiral', 'fractal']
            weights = [4, 3, 3, 2, 2, 1, 1]  # Prefer natural styles
            style = random.choices(styles, weights=weights)[0]
            
            # Create and add tree
            tree = Tree(x, y, self.current_theme, features, style)
            # Make it fully grown for showcase
            tree.growth = 1.0
            tree.is_growing = False
            self.trees.append(tree)
        
        # Generate grass (automatic for 10+ trees)
        self.check_grass_generation()
        
        # Make all grass fully grown
        for grass in self.grasses:
            grass.growth = 1.0
            grass.is_growing = False
        
        print(f"✅ Created garden with {len(self.trees)} trees and {len(self.grasses)} grass patches")
    
    def save_themed_showcase(self, theme_name):
        """Save current garden as showcase"""
        timestamp = int(time.time())
        filename = f"{theme_name.lower().replace(' ', '_')}_showcase_{timestamp}"
        
        try:
            # Use the existing save_art method
            eps_path = os.path.join(self.output_dir, f"{filename}.eps")
            
            # Save as PostScript
            self.canvas.postscript(file=eps_path, colormode='color',
                                 width=self.canvas.winfo_width(),
                                 height=self.canvas.winfo_height())
            
            print(f"✅ Saved showcase: {eps_path}")
            
            # Try to convert to PNG using Pillow
            try:
                from PIL import Image
                png_path = os.path.join(self.output_dir, f"{filename}.png")
                
                # Convert EPS to PNG
                with Image.open(eps_path) as img:
                    img.load(scale=2)  # Higher resolution
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(png_path, 'PNG', quality=95, optimize=True)
                
                print(f"✅ Converted to PNG: {png_path}")
                
                # Keep both formats
                self.status_label.config(text=f"Status: Showcase saved - {theme_name}")
                
            except Exception as e:
                print(f"⚠️  PNG conversion: {e}")
                self.status_label.config(text=f"Status: EPS saved - {theme_name}")
                
        except Exception as e:
            print(f"❌ Save error: {e}")
            self.status_label.config(text=f"Status: Save failed - {e}")
    
    def generate_all_showcases(self):
        """Generate showcases for all themes"""
        themes = [ColorTheme.WARM, ColorTheme.COOL, ColorTheme.MONO, 
                 ColorTheme.SUNSET, ColorTheme.AURORA]
        
        print(f"\n🌟 Generating showcases for all {len(themes)} themes...")
        
        for i, theme in enumerate(themes):
            print(f"\n📸 Theme {i+1}/{len(themes)}: {theme['name']}")
            self.create_theme_showcase(theme)
            time.sleep(1)  # Brief pause between generations
        
        print(f"\n🎉 All showcases generated!")
        print(f"📁 Check folder: {os.path.abspath(self.output_dir)}")
        
        # Show completion message
        tk.messagebox.showinfo("Showcases Complete!", 
                             f"Generated beautiful showcases for all {len(themes)} themes!\n\n"
                             f"Saved in: showcase_images/\n\n"
                             f"Formats: EPS and PNG (if Pillow available)")

def main():
    print("🎨 Starting Echo Garden Quick Showcase Creator...")
    app = QuickShowcase()
    app.run()

if __name__ == "__main__":
    main()
