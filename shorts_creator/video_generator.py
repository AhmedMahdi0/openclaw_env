#!/usr/bin/env python3
"""
AI Video Generator for Shorts Creator
Generates videos from images using AI services
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

class VideoGenerator:
    def __init__(self):
        self.input_dir = os.getenv('ENHANCED_IMAGES_DIR', './enhanced_images')
        self.output_dir = os.getenv('GENERATED_VIDEOS_DIR', './generated_videos')
        self.video_duration = int(os.getenv('VIDEO_DURATION_PER_IMAGE', 3))
        
        # API Keys
        self.runwayml_api_key = os.getenv('RUNWAYML_API_KEY')
        self.pika_api_key = os.getenv('PIKA_API_KEY')
        
        # Create directories
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def get_enhanced_images(self):
        """Get all enhanced images from input directory"""
        image_extensions = ('.jpg', '.jpeg', '.png')
        image_files = []
        
        for file in os.listdir(self.input_dir):
            if file.lower().endswith(image_extensions) and 'enhanced' in file.lower():
                image_files.append(os.path.join(self.input_dir, file))
        
        print(f"Found {len(image_files)} enhanced image(s)")
        return sorted(image_files)
    
    def image_to_base64(self, image_path):
        """Convert image to base64 string"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if needed (APIs often have size limits)
                max_size = 1024
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = BytesIO()
                img.save(buffered, format="JPEG", quality=90)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                return img_str
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return None
    
    def generate_with_runwayml(self, image_path, prompt):
        """Generate video using RunwayML API"""
        if not self.runwayml_api_key:
            print("⚠️ RunwayML API key not set. Using mock generation.")
            return self.mock_generate_video(image_path, prompt, "RunwayML")
        
        try:
            print(f"Generating video with RunwayML: {Path(image_path).name}")
            
            # Convert image to base64
            image_base64 = self.image_to_base64(image_path)
            if not image_base64:
                return None
            
            # Prepare request
            url = "https://api.runwayml.com/v1/video/generate"
            headers = {
                "Authorization": f"Bearer {self.runwayml_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "image": f"data:image/jpeg;base64,{image_base64}",
                "prompt": prompt,
                "seed": int(time.time()) % 10000,
                "motion": "subtle",  # subtle, medium, high
                "duration": self.video_duration,
                "upscale": True
            }
            
            # Send request
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            video_url = result.get("video_url")
            
            if video_url:
                # Download video
                video_response = requests.get(video_url, timeout=60)
                output_path = os.path.join(self.output_dir, 
                                         f"{Path(image_path).stem}_runway.mp4")
                
                with open(output_path, 'wb') as f:
                    f.write(video_response.content)
                
                print(f"✅ Video generated: {Path(output_path).name}")
                return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"RunwayML API error: {e}")
        except Exception as e:
            print(f"Error with RunwayML: {e}")
        
        return None
    
    def generate_with_pika(self, image_path, prompt):
        """Generate video using Pika Labs API"""
        if not self.pika_api_key:
            print("⚠️ Pika API key not set. Using mock generation.")
            return self.mock_generate_video(image_path, prompt, "Pika")
        
        try:
            print(f"Generating video with Pika: {Path(image_path).name}")
            
            # Convert image to base64
            image_base64 = self.image_to_base64(image_path)
            if not image_base64:
                return None
            
            # Prepare request (Pika API structure may vary)
            url = "https://api.pika.art/v1/generate"
            headers = {
                "Authorization": f"Bearer {self.pika_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "image": image_base64,
                "prompt": prompt,
                "duration": self.video_duration,
                "style": "cinematic",
                "motion": 0.3  # 0-1 motion strength
            }
            
            # Send request
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            video_url = result.get("url") or result.get("video_url")
            
            if video_url:
                # Download video
                video_response = requests.get(video_url, timeout=60)
                output_path = os.path.join(self.output_dir, 
                                         f"{Path(image_path).stem}_pika.mp4")
                
                with open(output_path, 'wb') as f:
                    f.write(video_response.content)
                
                print(f"✅ Video generated: {Path(output_path).name}")
                return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"Pika API error: {e}")
        except Exception as e:
            print(f"Error with Pika: {e}")
        
        return None
    
    def mock_generate_video(self, image_path, prompt, service_name):
        """Mock video generation for testing (creates simple slideshow)"""
        try:
            print(f"Mock generating with {service_name}: {Path(image_path).name}")
            
            # Create a simple video using PIL and moviepy
            from moviepy.editor import ImageClip, concatenate_videoclips
            
            output_path = os.path.join(self.output_dir, 
                                     f"{Path(image_path).stem}_{service_name.lower()}.mp4")
            
            # Create a simple video with the image
            clip = ImageClip(image_path, duration=self.video_duration)
            
            # Add text overlay with prompt
            # (In a real scenario, you'd add text overlay here)
            
            # Write video
            clip.write_videofile(output_path, fps=24, verbose=False, logger=None)
            
            print(f"✅ Mock video created: {Path(output_path).name}")
            return output_path
            
        except ImportError:
            print("⚠️ moviepy not installed for mock generation")
            # Create a placeholder file
            output_path = os.path.join(self.output_dir, 
                                     f"{Path(image_path).stem}_{service_name.lower()}.txt")
            with open(output_path, 'w') as f:
                f.write(f"Mock video for: {prompt}\nImage: {image_path}")
            
            print(f"✅ Placeholder created: {Path(output_path).name}")
            return output_path
        except Exception as e:
            print(f"Error in mock generation: {e}")
            return None
    
    def generate_prompt_for_image(self, image_path):
        """Generate a creative prompt based on the image"""
        filename = Path(image_path).stem.lower()
        
        # Simple prompt generation based on filename/content
        prompts = [
            f"Beautiful cinematic animation of {filename}, subtle motion, soft lighting",
            f"Magical transformation of {filename}, dreamy atmosphere, gentle movement",
            f"{filename} coming to life with elegant motion, cinematic quality",
            f"Artistic animation of {filename}, emotional depth, visual poetry",
            f"{filename} with delicate movement, atmospheric, storybook style"
        ]
        
        # Use a hash of the filename to pick a prompt consistently
        import hashlib
        hash_val = int(hashlib.md5(filename.encode()).hexdigest(), 16)
        prompt = prompts[hash_val % len(prompts)]
        
        return prompt
    
    def batch_generate(self, service="mock"):
        """Generate videos for all enhanced images"""
        image_files = self.get_enhanced_images()
        
        if not image_files:
            print("No enhanced images found.")
            print("Run image_processor.py first to enhance your images.")
            return []
        
        generated_videos = []
        
        for i, image_file in enumerate(image_files):
            print(f"\n[{i+1}/{len(image_files)}] Processing: {Path(image_file).name}")
            
            # Generate creative prompt
            prompt = self.generate_prompt_for_image(image_file)
            print(f"Prompt: {prompt}")
            
            # Generate video
            if service.lower() == "runwayml":
                video_path = self.generate_with_runwayml(image_file, prompt)
            elif service.lower() == "pika":
                video_path = self.generate_with_pika(image_file, prompt)
            else:
                video_path = self.mock_generate_video(image_file, prompt, "Mock")
            
            if video_path:
                generated_videos.append(video_path)
            
            # Small delay to avoid rate limiting
            if i < len(image_files) - 1:
                time.sleep(1)
        
        return generated_videos

def main():
    """Main function"""
    print("=" * 60)
    print("AI Video Shorts - Video Generator")
    print("=" * 60)
    print("\nAvailable services:")
    print("1. mock    - Mock generation (no API needed)")
    print("2. runwayml - RunwayML API (requires API key)")
    print("3. pika    - Pika Labs API (requires API key)")
    
    service = input("\nSelect service (mock/runwayml/pika): ").strip().lower()
    if not service:
        service = "mock"
    
    generator = VideoGenerator()
    
    # Generate videos
    print(f"\nStarting video generation with {service}...")
    generated_videos = generator.batch_generate(service)
    
    if generated_videos:
        print(f"\n🎉 Generated {len(generated_videos)} video(s)")
        print(f"Videos saved in: {generator.output_dir}")
        print("\nNext step: Run video_assembler.py to create final short.")
    else:
        print("\n⚠️ No videos were generated.")

if __name__ == "__main__":
    main()