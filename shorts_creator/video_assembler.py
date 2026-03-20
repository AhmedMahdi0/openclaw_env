#!/usr/bin/env python3
"""
Video Assembler for AI Shorts Creator
Combines generated videos with audio to create final Shorts
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import random
from datetime import datetime

# Try to import video editing libraries
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
    from moviepy.video.fx.all import fadein, fadeout
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False
    print("⚠️ moviepy not installed. Some features may be limited.")

# Load environment variables
load_dotenv()

class VideoAssembler:
    def __init__(self):
        self.input_dir = os.getenv('GENERATED_VIDEOS_DIR', './generated_videos')
        self.output_dir = os.getenv('FINAL_VIDEOS_DIR', './final_videos')
        self.audio_dir = os.getenv('AUDIO_DIR', './audio')
        self.video_width = int(os.getenv('VIDEO_WIDTH', 1080))
        self.video_height = int(os.getenv('VIDEO_HEIGHT', 1920))
        
        # Create directories
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.audio_dir).mkdir(parents=True, exist_ok=True)
    
    def get_generated_videos(self):
        """Get all generated video files"""
        video_extensions = ('.mp4', '.mov', '.avi', '.mkv')
        video_files = []
        
        for file in os.listdir(self.input_dir):
            if file.lower().endswith(video_extensions):
                video_files.append(os.path.join(self.input_dir, file))
        
        print(f"Found {len(video_files)} generated video(s)")
        return sorted(video_files)
    
    def get_audio_files(self):
        """Get audio files for background music and voiceover"""
        audio_extensions = ('.mp3', '.wav', '.m4a', '.ogg')
        audio_files = []
        
        if os.path.exists(self.audio_dir):
            for file in os.listdir(self.audio_dir):
                if file.lower().endswith(audio_extensions):
                    audio_files.append(os.path.join(self.audio_dir, file))
        
        return sorted(audio_files)
    
    def generate_text_to_speech(self, text, output_path):
        """Generate text-to-speech audio (mock implementation)"""
        print(f"Generating TTS for: {text[:50]}...")
        
        # In a real implementation, use:
        # - Google TTS (gTTS)
        # - ElevenLabs API
        # - OpenAI TTS
        
        # For now, create a placeholder
        if not HAS_MOVIEPY:
            # Create placeholder file
            with open(output_path.replace('.mp3', '.txt'), 'w') as f:
                f.write(f"TTS Audio should be here:\n{text}")
            return output_path.replace('.mp3', '.txt')
        
        return None
    
    def create_title_card(self, title, duration=3):
        """Create a title card for the video"""
        if not HAS_MOVIEPY:
            return None
        
        try:
            # Create a simple title card
            txt_clip = TextClip(
                title, 
                fontsize=70, 
                color='white',
                font='Arial-Bold',
                size=(self.video_width * 0.9, None),
                method='caption'
            )
            
            # Center the text
            txt_clip = txt_clip.set_position('center').set_duration(duration)
            
            # Create background
            from moviepy.editor import ColorClip
            bg_clip = ColorClip(
                size=(self.video_width, self.video_height), 
                color=(30, 30, 50),  # Dark blue
                duration=duration
            )
            
            # Composite text over background
            title_card = CompositeVideoClip([bg_clip, txt_clip])
            title_card = title_card.fadein(0.5).fadeout(0.5)
            
            return title_card
            
        except Exception as e:
            print(f"Error creating title card: {e}")
            return None
    
    def create_caption_overlay(self, text, duration, position="bottom"):
        """Create caption overlay for a video segment"""
        if not HAS_MOVIEPY:
            return None
        
        try:
            # Create caption text
            txt_clip = TextClip(
                text, 
                fontsize=40, 
                color='white',
                font='Arial',
                size=(self.video_width * 0.8, None),
                method='caption',
                bg_color='rgba(0,0,0,0.5)',
                stroke_color='black',
                stroke_width=1
            )
            
            # Position caption
            if position == "top":
                y_pos = 50
            elif position == "bottom":
                y_pos = self.video_height - txt_clip.h - 50
            else:  # center
                y_pos = (self.video_height - txt_clip.h) // 2
            
            txt_clip = txt_clip.set_position(('center', y_pos)).set_duration(duration)
            
            return txt_clip
            
        except Exception as e:
            print(f"Error creating caption: {e}")
            return None
    
    def assemble_short(self, video_files, output_name, 
                       title="AI Generated Memories",
                       captions=None,
                       add_music=True,
                       max_duration=60):
        """Assemble multiple videos into a final Short"""
        if not HAS_MOVIEPY:
            print("❌ moviepy is required for video assembly")
            print("Install with: pip install moviepy")
            return None
        
        try:
            print(f"Assembling short video: {output_name}")
            
            clips = []
            
            # 1. Add title card
            title_card = self.create_title_card(title, duration=3)
            if title_card:
                clips.append(title_card)
            
            # 2. Add video clips with optional captions
            for i, video_file in enumerate(video_files):
                print(f"Adding clip {i+1}/{len(video_files)}: {Path(video_file).name}")
                
                try:
                    clip = VideoFileClip(video_file)
                    
                    # Trim if too long
                    max_clip_duration = 5  # seconds per clip max
                    if clip.duration > max_clip_duration:
                        clip = clip.subclip(0, max_clip_duration)
                    
                    # Add fade effects
                    clip = clip.fadein(0.5).fadeout(0.5)
                    
                    # Add caption if provided
                    if captions and i < len(captions):
                        caption_clip = self.create_caption_overlay(
                            captions[i], 
                            clip.duration,
                            position="bottom" if i % 2 == 0 else "top"
                        )
                        if caption_clip:
                            clip = CompositeVideoClip([clip, caption_clip])
                    
                    clips.append(clip)
                    
                except Exception as e:
                    print(f"Error loading clip {video_file}: {e}")
                    continue
            
            # 3. Concatenate all clips
            if not clips:
                print("❌ No valid clips to assemble")
                return None
            
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # 4. Trim to max duration for Shorts
            if final_clip.duration > max_duration:
                print(f"Trimming video from {final_clip.duration:.1f}s to {max_duration}s")
                final_clip = final_clip.subclip(0, max_duration)
            
            # 5. Add background music if available
            audio_files = self.get_audio_files()
            if add_music and audio_files:
                try:
                    music_file = random.choice(audio_files)
                    music_clip = AudioFileClip(music_file)
                    
                    # Loop music if shorter than video
                    while music_clip.duration < final_clip.duration:
                        music_clip = music_clip.append(music_clip)
                    
                    # Trim to video length and lower volume
                    music_clip = music_clip.subclip(0, final_clip.duration)
                    music_clip = music_clip.volumex(0.3)  # 30% volume
                    
                    # Combine with video audio (if any)
                    final_audio = music_clip
                    if final_clip.audio:
                        final_audio = final_clip.audio.volumex(0.7).set_fps(music_clip.fps)
                        final_audio = CompositeAudioClip([final_audio, music_clip])
                    
                    final_clip = final_clip.set_audio(final_audio)
                    
                    print(f"Added background music: {Path(music_file).name}")
                    
                except Exception as e:
                    print(f"Error adding music: {e}")
            
            # 6. Add outro/CTA
            outro_text = "Made with AI 🎬\nFollow for more!"
            outro_card = self.create_title_card(outro_text, duration=2)
            if outro_card:
                final_clip = concatenate_videoclips([final_clip, outro_card], method="compose")
            
            # 7. Export final video
            output_path = os.path.join(self.output_dir, output_name)
            
            print(f"Exporting final video to: {output_name}")
            final_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Cleanup
            for clip in clips:
                if hasattr(clip, 'close'):
                    clip.close()
            if hasattr(final_clip, 'close'):
                final_clip.close()
            
            print(f"\n✅ Successfully created: {output_name}")
            print(f"Duration: {final_clip.duration:.1f} seconds")
            print(f"Size: {self.video_width}x{self.video_height} (Vertical)")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error assembling video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_story_captions(self, video_count):
        """Generate story captions based on video count"""
        story_templates = [
            ["This was me in 2010...", "Fast forward to 2015...", "And this is me today! 🎉"],
            ["Memory 1: Childhood days", "Memory 2: School years", "Memory 3: Growing up"],
            ["The beginning of the journey...", "Challenges along the way...", "Success at last! ✨"],
            ["First chapter: Dreams", "Second chapter: Hard work", "Final chapter: Achievement"],
            ["Then: Full of energy", "Now: Full of wisdom", "Always: Full of love ❤️"]
        ]
        
        # Select and adjust template
        template = random.choice(story_templates)
        if len(template) > video_count:
            template = template[:video_count]
        elif len(template) < video_count:
            # Extend template
            while len(template) < video_count:
                template.append(f"Memory {len(template) + 1}")
        
        return template
    
    def auto_assemble(self):
        """Automatically assemble all generated videos"""
        video_files = self.get_generated_videos()
        
        if not video_files:
            print("No generated videos found.")
            print("Run video_generator.py first to generate videos.")
            return None
        
        print(f"Found {len(video_files)} video(s) to assemble")
        
        # Limit to 3-5 videos for a short
        if len(video_files) > 5:
            print(f"Selecting first 5 videos for Short")
            video_files = video_files[:5]
        
        # Generate story captions
        captions = self.create_story_captions(len(video_files))
        
        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"ai_short_{timestamp}.mp4"
        
        # Title
        title_options = [
            "AI Brings Memories to Life",
            "From Photos to Motion",
            "Digital Memories Animated",
            "The Past in Motion",
            "AI Animated Memories"
        ]
        title = random.choice(title_options)
        
        # Assemble the short
        output_path = self.assemble_short(
            video_files=video_files,
            output_name=output_name,
            title=title,
            captions=captions,
            add_music=True,
            max_duration=45  # Optimal for Shorts engagement
        )
        
        return output_path

def main():
    """Main function"""
    print("=" * 60)
    print("AI Video Shorts - Video Assembler")
    print("=" * 60)
    
    if not HAS_MOVIEPY:
        print("\n⚠️ Required libraries not installed.")
        print("Please install moviepy and related dependencies:")
        print("pip install moviepy pillow numpy")
        print("\nSome features will be limited.")
    
    assembler = VideoAssembler()
    
    print("\nOptions:")
    print("1. Auto-assemble all generated videos")
    print("2. Custom assembly (coming soon)")
    
    choice = input("\nSelect option (1): ").strip() or "1"
    
    if choice == "1":
        output_path = assembler.auto_assemble()
        
        if output_path:
            print(f"\n🎉 Short video created successfully!")
            print(f"Location: {output_path}")
            print("\nYou can now upload this to YouTube Shorts, TikTok, or Instagram Reels!")
        else:
            print("\n❌ Failed to create short video.")
    else:
        print("Custom assembly not implemented yet. Using auto-assemble.")
        output_path = assembler.auto_assemble()

if __name__ == "__main__":
    main()