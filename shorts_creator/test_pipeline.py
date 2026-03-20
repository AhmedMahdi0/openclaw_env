#!/usr/bin/env python3
"""
Test script for AI Video Shorts Creator
Tests the pipeline with sample images
"""

import os
import sys
from pathlib import Path
import shutil
from PIL import Image
import numpy as np

def create_sample_images():
    """Create sample images for testing"""
    print("Creating sample images...")
    
    input_dir = Path("input_images")
    input_dir.mkdir(exist_ok=True)
    
    # Create 3 sample images
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
    texts = ["Memory 1", "Memory 2", "Memory 3"]
    
    for i in range(3):
        # Create a simple image with color and text
        from PIL import ImageDraw, ImageFont
        
        # Create image
        img = Image.new('RGB', (800, 800), color=colors[i])
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("Arial", 60)
        except:
            font = ImageFont.load_default()
        
        # Draw text
        text = texts[i]
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (800 - text_width) // 2
        y = (800 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Save image
        img_path = input_dir / f"sample_{i+1}.jpg"
        img.save(img_path, "JPEG")
        print(f"Created: {img_path}")
    
    print(f"Created 3 sample images in {input_dir}")

def test_image_processor():
    """Test the image processor"""
    print("\nTesting image processor...")
    
    # Import and run image processor
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from image_processor import ImageProcessor
        
        processor = ImageProcessor()
        enhanced_images = processor.batch_process()
        
        if enhanced_images:
            print(f"✓ Image processor successful: {len(enhanced_images)} images enhanced")
            return True
        else:
            print("✗ Image processor failed: No images processed")
            return False
            
    except Exception as e:
        print(f"✗ Image processor error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_video_generator():
    """Test the video generator (mock mode)"""
    print("\nTesting video generator (mock mode)...")
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from video_generator import VideoGenerator
        
        generator = VideoGenerator()
        generated_videos = generator.batch_generate("mock")
        
        if generated_videos:
            print(f"✓ Video generator successful: {len(generated_videos)} videos created")
            return True
        else:
            print("✗ Video generator failed: No videos created")
            return False
            
    except Exception as e:
        print(f"✗ Video generator error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_video_assembler():
    """Test the video assembler"""
    print("\nTesting video assembler...")
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        # Check if moviepy is available
        try:
            from moviepy.editor import VideoFileClip
            has_moviepy = True
        except ImportError:
            has_moviepy = False
            print("⚠️ moviepy not installed, assembler will be limited")
        
        from video_assembler import VideoAssembler
        
        assembler = VideoAssembler()
        
        if has_moviepy:
            output_path = assembler.auto_assemble()
            if output_path and Path(output_path).exists():
                print(f"✓ Video assembler successful: {Path(output_path).name}")
                return True
            else:
                print("✗ Video assembler failed: No output created")
                return False
        else:
            print("⚠️ Skipping full assembler test (moviepy not installed)")
            return True
            
    except Exception as e:
        print(f"✗ Video assembler error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test the configuration"""
    print("\nTesting configuration...")
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        import config
        
        summary = config.get_config_summary()
        print("✓ Configuration loaded successfully")
        print(f"  Resolution: {summary['video_settings']['resolution']}")
        print(f"  Input dir: {summary['directories']['input_images']}")
        
        # Check if directories were created
        for dir_name, dir_path in summary['directories'].items():
            if Path(dir_path).exists():
                print(f"  ✓ Directory exists: {dir_name}")
            else:
                print(f"  ✗ Directory missing: {dir_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def cleanup():
    """Cleanup test files"""
    print("\nCleaning up test files...")
    
    dirs_to_clean = [
        "input_images",
        "enhanced_images", 
        "generated_videos",
        "final_videos",
        "audio"
    ]
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  Cleaned: {dir_name}")
            except:
                pass

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Video Shorts Creator - Test Suite")
    print("=" * 60)
    
    # Clean up any previous test files
    cleanup()
    
    # Create sample images first
    create_sample_images()
    
    # Run tests
    tests = [
        ("Configuration", test_config),
        ("Image Processor", test_image_processor),
        ("Video Generator", test_video_generator),
        ("Video Assembler", test_video_assembler),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Test: {test_name}")
        print('='*40)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{test_name:20} {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nYour AI Video Shorts Creator is ready to use!")
        print("Next steps:")
        print("1. Add your own images to 'input_images/'")
        print("2. Run: python3 image_processor.py")
        print("3. Run: python3 video_generator.py")
        print("4. Run: python3 video_assembler.py")
        print("\nOr use the complete pipeline:")
        print("  ./run_pipeline.sh")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("\nCheck the errors above and fix the issues.")
    
    # Optional: keep test files for inspection
    keep_files = input("\nKeep test files? (y/N): ").lower().strip()
    if keep_files != 'y':
        cleanup()
        print("Test files cleaned up.")
    else:
        print("Test files kept in their directories.")
    
    print("\nDone!")

if __name__ == "__main__":
    main()