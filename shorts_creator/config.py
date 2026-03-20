"""
Configuration settings for AI Video Shorts Creator
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory paths
BASE_DIR = Path(__file__).parent.absolute()

INPUT_IMAGES_DIR = BASE_DIR / os.getenv('INPUT_IMAGES_DIR', 'input_images')
ENHANCED_IMAGES_DIR = BASE_DIR / os.getenv('ENHANCED_IMAGES_DIR', 'enhanced_images')
GENERATED_VIDEOS_DIR = BASE_DIR / os.getenv('GENERATED_VIDEOS_DIR', 'generated_videos')
FINAL_VIDEOS_DIR = BASE_DIR / os.getenv('FINAL_VIDEOS_DIR', 'final_videos')
AUDIO_DIR = BASE_DIR / os.getenv('AUDIO_DIR', 'audio')

# Video settings
VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1080))
VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1920))
VIDEO_FPS = int(os.getenv('VIDEO_FPS', 30))
VIDEO_DURATION_PER_IMAGE = int(os.getenv('VIDEO_DURATION_PER_IMAGE', 3))
MAX_SHORT_DURATION = 60  # Maximum duration for Shorts in seconds

# API keys (optional)
RUNWAYML_API_KEY = os.getenv('RUNWAYML_API_KEY')
PIKA_API_KEY = os.getenv('PIKA_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Create directories on import
for directory in [INPUT_IMAGES_DIR, ENHANCED_IMAGES_DIR, 
                  GENERATED_VIDEOS_DIR, FINAL_VIDEOS_DIR, AUDIO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Default prompts for different image types
IMAGE_PROMPTS = {
    'portrait': [
        "Cinematic portrait with subtle motion, soft lighting, emotional depth",
        "Elegant portrait coming to life, gentle movement, atmospheric",
        "Portrait with delicate animation, dreamy atmosphere, visual poetry"
    ],
    'landscape': [
        "Breathtaking landscape with gentle motion, cinematic quality, majestic",
        "Scenic view coming alive, natural movement, epic scale",
        "Landscape animation, atmospheric changes, serene and peaceful"
    ],
    'family': [
        "Family moment brought to life, warm and emotional, nostalgic",
        "Family memory animated with love, heartwarming, sentimental",
        "Cherished family moment, gentle movement, emotional depth"
    ],
    'travel': [
        "Travel memory animated, adventure vibe, dynamic movement",
        "Journey moment coming alive, exploratory, exciting",
        "Travel scene with motion, discovery feeling, wanderlust"
    ],
    'childhood': [
        "Childhood memory animated, innocent and playful, nostalgic",
        "Youthful moment coming to life, joyful movement, sentimental",
        "Kids playing, animated with fun and energy, heartwarming"
    ]
}

# Story templates for different video lengths
STORY_TEMPLATES = [
    # 3-part story
    ["The beginning...", "The journey...", "The achievement! ✨"],
    ["Memory 1: Dreams", "Memory 2: Challenges", "Memory 3: Success"],
    ["Then: Full of hope", "Now: Full of wisdom", "Always: Moving forward"],
    
    # 4-part story
    ["Chapter 1: The Start", "Chapter 2: Growth", "Chapter 3: Challenges", "Chapter 4: Victory"],
    ["First memory", "Second moment", "Third chapter", "Final achievement"],
    
    # 5-part story
    ["The early days", "Building up", "Facing obstacles", "Breaking through", "Reaching goals 🎯"],
]

# Music moods for different video types
MUSIC_MOODS = {
    'emotional': ['calm', 'sentimental', 'inspiring'],
    'happy': ['upbeat', 'joyful', 'celebratory'],
    'adventure': ['epic', 'dramatic', 'exploratory'],
    'nostalgic': ['melancholic', 'dreamy', 'reflective']
}

def get_config_summary():
    """Return a summary of the current configuration"""
    return {
        'directories': {
            'input_images': str(INPUT_IMAGES_DIR),
            'enhanced_images': str(ENHANCED_IMAGES_DIR),
            'generated_videos': str(GENERATED_VIDEOS_DIR),
            'final_videos': str(FINAL_VIDEOS_DIR),
            'audio': str(AUDIO_DIR)
        },
        'video_settings': {
            'resolution': f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
            'fps': VIDEO_FPS,
            'duration_per_image': f"{VIDEO_DURATION_PER_IMAGE}s",
            'max_short_duration': f"{MAX_SHORT_DURATION}s"
        },
        'apis_configured': {
            'runwayml': bool(RUNWAYML_API_KEY),
            'pika': bool(PIKA_API_KEY),
            'openai': bool(OPENAI_API_KEY),
            'elevenlabs': bool(ELEVENLABS_API_KEY)
        }
    }