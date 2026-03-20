#!/usr/bin/env python3
"""
Image Processor for AI Video Shorts Creator
Enhances and prepares images for AI video generation
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ImageProcessor:
    def __init__(self):
        self.input_dir = os.getenv('INPUT_IMAGES_DIR', './input_images')
        self.output_dir = os.getenv('ENHANCED_IMAGES_DIR', './enhanced_images')
        self.video_width = int(os.getenv('VIDEO_WIDTH', 1080))
        self.video_height = int(os.getenv('VIDEO_HEIGHT', 1920))
        
        # Create directories if they don't exist
        Path(self.input_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def get_image_files(self):
        """Get all image files from input directory"""
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
        image_files = []
        
        for file in os.listdir(self.input_dir):
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(self.input_dir, file))
        
        print(f"Found {len(image_files)} image(s) in {self.input_dir}")
        return sorted(image_files)
    
    def enhance_image(self, image_path):
        """Enhance image quality and prepare for video generation"""
        try:
            # Open image
            img = Image.open(image_path)
            filename = Path(image_path).stem
            output_path = os.path.join(self.output_dir, f"{filename}_enhanced.jpg")
            
            print(f"Processing: {Path(image_path).name}")
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate new dimensions while maintaining aspect ratio
            original_width, original_height = img.size
            target_ratio = self.video_width / self.video_height
            original_ratio = original_width / original_height
            
            if original_ratio > target_ratio:
                # Image is wider than target, crop width
                new_width = int(original_height * target_ratio)
                left = (original_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, original_height))
            else:
                # Image is taller than target, crop height
                new_height = int(original_width / target_ratio)
                top = (original_height - new_height) // 2
                img = img.crop((0, top, original_width, top + new_height))
            
            # Resize to target dimensions
            img = img.resize((self.video_width, self.video_height), Image.Resampling.LANCZOS)
            
            # Enhance image quality
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)  # Increase saturation
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)  # Increase contrast
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)  # Increase sharpness
            
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.05)  # Slight brightness increase
            
            # Save enhanced image
            img.save(output_path, 'JPEG', quality=95)
            print(f"Saved enhanced image: {Path(output_path).name}")
            
            return output_path
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def create_image_grid(self, image_paths, output_path):
        """Create a grid of images for comparison (optional)"""
        if len(image_paths) < 2:
            return
        
        try:
            images = [Image.open(path) for path in image_paths[:4]]
            
            # Resize all images to same size
            grid_size = min(2, len(images))
            cell_width = self.video_width // grid_size
            cell_height = self.video_height // grid_size
            
            resized_images = []
            for img in images:
                img_resized = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
                resized_images.append(img_resized)
            
            # Create grid
            grid = Image.new('RGB', (self.video_width, self.video_height))
            
            for i, img in enumerate(resized_images):
                x = (i % grid_size) * cell_width
                y = (i // grid_size) * cell_height
                grid.paste(img, (x, y))
            
            grid.save(output_path, 'JPEG', quality=95)
            print(f"Created image grid: {Path(output_path).name}")
            
        except Exception as e:
            print(f"Error creating image grid: {e}")
    
    def batch_process(self):
        """Process all images in input directory"""
        image_files = self.get_image_files()
        
        if not image_files:
            print("No images found in input directory.")
            print(f"Please place images in: {self.input_dir}")
            return []
        
        enhanced_paths = []
        for image_file in image_files:
            enhanced_path = self.enhance_image(image_file)
            if enhanced_path:
                enhanced_paths.append(enhanced_path)
        
        # Create before/after grid if we have at least 2 images
        if len(enhanced_paths) >= 2:
            grid_path = os.path.join(self.output_dir, "comparison_grid.jpg")
            self.create_image_grid([image_files[0], enhanced_paths[0]], grid_path)
        
        print(f"\n✅ Enhanced {len(enhanced_paths)} image(s)")
        print(f"Enhanced images saved in: {self.output_dir}")
        
        return enhanced_paths

def main():
    """Main function"""
    print("=" * 60)
    print("AI Video Shorts - Image Processor")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Process all images
    enhanced_images = processor.batch_process()
    
    if enhanced_images:
        print("\n🎉 Image processing completed successfully!")
        print("Next step: Run video_generator.py to create AI videos from these images.")
    else:
        print("\n⚠️ No images were processed. Please check your input directory.")

if __name__ == "__main__":
    main()