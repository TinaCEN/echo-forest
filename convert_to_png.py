#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert SVG showcases to PNG images
"""

import os
import cairosvg
from PIL import Image

def convert_svgs_to_png():
    """Convert all SVG files to high-quality PNG"""
    
    showcase_dir = "showcase_images"
    svg_files = [f for f in os.listdir(showcase_dir) if f.endswith('.svg')]
    
    print(f"🖼️  Converting {len(svg_files)} SVG files to PNG...")
    
    for svg_file in svg_files:
        svg_path = os.path.join(showcase_dir, svg_file)
        png_file = svg_file.replace('.svg', '.png')
        png_path = os.path.join(showcase_dir, png_file)
        
        try:
            print(f"📸 Converting {svg_file} to PNG...")
            
            # Convert SVG to PNG with high resolution
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                output_width=1900,  # High resolution
                output_height=1100
            )
            
            print(f"✅ Created: {png_path}")
            
        except Exception as e:
            print(f"❌ Failed to convert {svg_file}: {e}")
    
    print(f"\n🎉 PNG conversion complete!")
    
    # List all files
    print("\n📁 Generated files:")
    for file in sorted(os.listdir(showcase_dir)):
        if file.endswith(('.png', '.svg', '.html', '.eps')):
            print(f"   • {file}")

if __name__ == "__main__":
    convert_svgs_to_png()
