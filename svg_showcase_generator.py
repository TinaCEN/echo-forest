#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Garden - Command Line Showcase Generator
Generate showcase images without GUI interaction
"""

import random
import time
import os
import sys

def create_showcase_data():
    """Create sample data for showcases"""
    
    # Theme configurations
    themes = {
        "warm_gradient": {
            'name': 'Warm Gradient',
            'trunk': ['#8B4513', '#A0522D', '#CD853F', '#D2691E', '#DEB887'],
            'leaves': [
                '#FF6B35', '#FF7F50', '#FF8C69', '#FFA500', '#FFB347',
                '#F7931E', '#FFD700', '#FFFF99', '#FFEFD5', '#FFE4B5'
            ],
            'bg_color': '#FFF8DC'
        },
        "cool_gradient": {
            'name': 'Cool Gradient',
            'trunk': ['#2F4F4F', '#708090', '#778899', '#87CEEB', '#B0C4DE'],
            'leaves': [
                '#00CED1', '#20B2AA', '#48D1CC', '#87CEEB', '#B0E0E6',
                '#4682B4', '#5F9EA0', '#6495ED', '#7B68EE', '#9370DB'
            ],
            'bg_color': '#F0F8FF'
        },
        "galaxy_gradient": {
            'name': 'Galaxy Gradient',
            'trunk': ['#2F2F2F', '#4F4F4F', '#696969', '#808080', '#A9A9A9'],
            'leaves': [
                '#696969', '#778899', '#808080', '#A9A9A9', '#C0C0C0',
                '#D3D3D3', '#DCDCDC', '#E5E5E5', '#F0F0F0', '#F8F8FF'
            ],
            'bg_color': '#F5F5F5'
        },
        "sunset_gradient": {
            'name': 'Sunset Gradient',
            'trunk': ['#8B4513', '#CD853F', '#DEB887', '#F4A460', '#FFDAB9'],
            'leaves': [
                '#FF69B4', '#FF1493', '#FF6347', '#FF4500', '#FF8C00',
                '#FFD700', '#FFFF00', '#ADFF2F', '#32CD32', '#00FF7F'
            ],
            'bg_color': '#FFE4E1'
        },
        "aurora_gradient": {
            'name': 'Aurora Gradient',
            'trunk': ['#2F4F4F', '#483D8B', '#6A5ACD', '#9370DB', '#BA55D3'],
            'leaves': [
                '#00FFFF', '#00BFFF', '#1E90FF', '#0000FF', '#4169E1',
                '#9370DB', '#8A2BE2', '#9400D3', '#FF00FF', '#FF1493'
            ],
            'bg_color': '#191970'
        }
    }
    
    # Sample tree data for each theme
    showcase_data = {}
    
    for theme_key, theme in themes.items():
        trees = []
        
        # Create 15-18 sample trees
        for i in range(random.randint(15, 18)):
            x = random.randint(80, 870)
            y = random.randint(150, 480)
            
            # Random tree properties
            style = random.choice(['classic', 'weeping', 'bushy', 'tall', 'wide', 'spiral', 'fractal'])
            height = random.randint(60, 150)
            branches = random.randint(3, 8)
            trunk_color = random.choice(theme['trunk'])
            leaf_colors = random.choices(theme['leaves'], k=3)
            
            trees.append({
                'x': x, 'y': y, 'style': style, 'height': height,
                'branches': branches, 'trunk_color': trunk_color,
                'leaf_colors': leaf_colors
            })
        
        showcase_data[theme_key] = {
            'theme': theme,
            'trees': trees
        }
    
    return showcase_data

def generate_html_showcase():
    """Generate HTML showcase with SVG graphics"""
    
    showcase_data = create_showcase_data()
    output_dir = "showcase_images"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🎨 Generating HTML/SVG showcases for all themes...")
    
    for theme_key, data in showcase_data.items():
        theme = data['theme']
        trees = data['trees']
        
        print(f"📸 Creating {theme['name']} showcase...")
        
        # Generate SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="950" height="550" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect width="950" height="550" fill="{theme['bg_color']}"/>
    
    <!-- Title -->
    <text x="475" y="30" text-anchor="middle" font-family="Arial" font-size="24" font-weight="bold" fill="#2F4F4F">
        Echo Garden - {theme['name']}
    </text>
    <text x="475" y="50" text-anchor="middle" font-family="Arial" font-size="14" fill="#696969">
        {len(trees)} Beautiful Trees Generated
    </text>
    
    <!-- Trees -->'''
        
        # Add trees to SVG
        for i, tree in enumerate(trees):
            x, y = tree['x'], tree['y']
            height = tree['height']
            trunk_color = tree['trunk_color']
            leaf_colors = tree['leaf_colors']
            
            # Draw trunk
            trunk_width = max(4, height // 15)
            svg_content += f'''
    <rect x="{x-trunk_width//2}" y="{y-height//3}" width="{trunk_width}" height="{height//3}" fill="{trunk_color}"/>'''
            
            # Draw canopy (simple circles for SVG)
            canopy_radius = height // 4
            for j, color in enumerate(leaf_colors):
                offset_x = random.randint(-15, 15)
                offset_y = random.randint(-10, 10)
                radius = canopy_radius + random.randint(-5, 10)
                svg_content += f'''
    <circle cx="{x + offset_x}" cy="{y - height//2 + offset_y}" r="{radius}" fill="{color}" opacity="0.8"/>'''
        
        # Generate some grass
        grass_count = len(trees) // 2
        for i in range(grass_count):
            x = random.randint(20, 930)
            y = random.randint(450, 540)
            grass_color = random.choice(theme['leaves'])
            
            # Simple grass blades
            for blade in range(3):
                blade_x = x + random.randint(-5, 5)
                blade_height = random.randint(8, 15)
                svg_content += f'''
    <line x1="{blade_x}" y1="{y}" x2="{blade_x + random.randint(-2, 2)}" y2="{y - blade_height}" 
          stroke="{grass_color}" stroke-width="2" opacity="0.6"/>'''
        
        svg_content += '''
</svg>'''
        
        # Save SVG file
        svg_filename = f"{theme_key}_showcase.svg"
        svg_path = os.path.join(output_dir, svg_filename)
        
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"✅ Saved SVG: {svg_path}")
        
        # Try to convert to PNG using Pillow if available
        try:
            from PIL import Image
            import cairosvg
            
            png_filename = f"{theme_key}_showcase.png"
            png_path = os.path.join(output_dir, png_filename)
            
            # Convert SVG to PNG
            cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), 
                           write_to=png_path, output_width=1900, output_height=1100)
            
            print(f"✅ Converted to PNG: {png_path}")
            
        except ImportError:
            print("⚠️  cairosvg not available for PNG conversion")
        except Exception as e:
            print(f"⚠️  PNG conversion failed: {e}")
    
    # Generate overview HTML
    generate_html_overview(showcase_data, output_dir)
    
    print(f"\n🎉 All showcases generated!")
    print(f"📁 Files saved in: {os.path.abspath(output_dir)}")

def generate_html_overview(showcase_data, output_dir):
    """Generate HTML overview page"""
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echo Garden - All Theme Showcases</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; color: #2F4F4F; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-top: 30px; }
        .showcase-item { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .showcase-item h3 { margin-top: 0; color: #2F4F4F; }
        .showcase-item img { width: 100%; height: auto; border-radius: 5px; }
        .info { margin: 10px 0; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌳 Echo Garden - All Theme Showcases 🌳</h1>
        <p style="text-align: center; color: #666;">Beautiful generative art with real-time audio input</p>
        
        <div class="gallery">'''
    
    for theme_key, data in showcase_data.items():
        theme = data['theme']
        svg_filename = f"{theme_key}_showcase.svg"
        
        html_content += f'''
            <div class="showcase-item">
                <h3>🎨 {theme['name']}</h3>
                <img src="{svg_filename}" alt="{theme['name']} Showcase">
                <div class="info">
                    <strong>Trees:</strong> {len(data['trees'])} beautiful specimens<br>
                    <strong>Style:</strong> Gradient color theme<br>
                    <strong>Features:</strong> Real-time audio responsive, drag & drop, multiple tree styles
                </div>
            </div>'''
    
    html_content += '''
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>🎵 Each tree is generated from unique sound characteristics</p>
            <p>🌱 Grass automatically grows when 10+ trees are planted</p>
            <p>🎨 Five beautiful gradient themes to choose from</p>
        </div>
    </div>
</body>
</html>'''
    
    html_path = os.path.join(output_dir, "echo_garden_showcase_overview.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated HTML overview: {html_path}")

def main():
    """Generate all showcases"""
    print("🌳 Echo Garden - Showcase Generator 🌳")
    print("🎨 Creating beautiful examples for all themes...")
    
    try:
        generate_html_showcase()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
