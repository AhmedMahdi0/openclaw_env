#!/bin/bash

# AI Video Shorts Creator - Complete Pipeline
# This script runs the entire pipeline from images to final Short

set -e  # Exit on error

echo "================================================================"
echo "🤖 AI Video Shorts Creator - Complete Pipeline"
echo "================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[STATUS]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION detected"
}

# Install dependencies
install_dependencies() {
    print_status "Checking dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip."
        exit 1
    fi
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip3 install -r requirements.txt --user 2>/dev/null || {
        print_warning "Failed to install with --user flag, trying without..."
        pip3 install -r requirements.txt
    }
    
    # Check if moviepy is installed (critical for assembly)
    if ! python3 -c "import moviepy" 2>/dev/null; then
        print_warning "MoviePy not installed. Video assembly will be limited."
        print_status "Installing MoviePy..."
        pip3 install moviepy --user || pip3 install moviepy
    fi
    
    print_success "Dependencies installed"
}

# Step 1: Image Processing
step1_image_processing() {
    echo ""
    echo "================================================================"
    echo "📸 Step 1: Image Processing"
    echo "================================================================"
    
    # Check if input directory exists and has images
    INPUT_DIR=${INPUT_IMAGES_DIR:-"./input_images"}
    
    if [ ! -d "$INPUT_DIR" ]; then
        print_warning "Input directory '$INPUT_DIR' not found. Creating it."
        mkdir -p "$INPUT_DIR"
        print_status "Please add your images to: $INPUT_DIR"
        print_status "Supported formats: JPG, PNG, JPEG, BMP, GIF, WebP"
        return 1
    fi
    
    IMAGE_COUNT=$(find "$INPUT_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.bmp" -o -name "*.gif" -o -name "*.webp" \) | wc -l)
    
    if [ "$IMAGE_COUNT" -eq 0 ]; then
        print_warning "No images found in '$INPUT_DIR'"
        print_status "Please add at least 1-3 images to create a short video"
        return 1
    fi
    
    print_status "Found $IMAGE_COUNT image(s) in input directory"
    
    # Run image processor
    print_status "Enhancing images for AI video generation..."
    python3 image_processor.py
    
    if [ $? -eq 0 ]; then
        print_success "Image processing completed"
        return 0
    else
        print_error "Image processing failed"
        return 1
    fi
}

# Step 2: AI Video Generation
step2_video_generation() {
    echo ""
    echo "================================================================"
    echo "🎬 Step 2: AI Video Generation"
    echo "================================================================"
    
    # Check if enhanced images exist
    ENHANCED_DIR=${ENHANCED_IMAGES_DIR:-"./enhanced_images"}
    
    if [ ! -d "$ENHANCED_DIR" ] || [ -z "$(ls -A "$ENHANCED_DIR" 2>/dev/null)" ]; then
        print_warning "No enhanced images found. Running image processing first..."
        step1_image_processing
        if [ $? -ne 0 ]; then
            return 1
        fi
    fi
    
    # Ask for service selection
    echo ""
    echo "Select AI video generation service:"
    echo "  1) Mock Generation (no API needed - for testing)"
    echo "  2) RunwayML API (requires API key)"
    echo "  3) Pika Labs API (requires API key)"
    echo ""
    read -p "Enter choice (1-3, default: 1): " SERVICE_CHOICE
    
    case $SERVICE_CHOICE in
        1|"")
            SERVICE="mock"
            ;;
        2)
            SERVICE="runwayml"
            ;;
        3)
            SERVICE="pika"
            ;;
        *)
            print_warning "Invalid choice. Using mock generation."
            SERVICE="mock"
            ;;
    esac
    
    print_status "Generating videos using $SERVICE service..."
    python3 video_generator.py <<< "$SERVICE"
    
    if [ $? -eq 0 ]; then
        print_success "Video generation completed"
        return 0
    else
        print_error "Video generation failed"
        return 1
    fi
}

# Step 3: Video Assembly
step3_video_assembly() {
    echo ""
    echo "================================================================"
    echo "🎵 Step 3: Video Assembly"
    echo "================================================================"
    
    # Check if generated videos exist
    GENERATED_DIR=${GENERATED_VIDEOS_DIR:-"./generated_videos"}
    
    if [ ! -d "$GENERATED_DIR" ] || [ -z "$(find "$GENERATED_DIR" -name "*.mp4" -o -name "*.mov" -o -name "*.avi" 2>/dev/null)" ]; then
        print_warning "No generated videos found. Running video generation first..."
        step2_video_generation
        if [ $? -ne 0 ]; then
            return 1
        fi
    fi
    
    # Check for audio files (optional)
    AUDIO_DIR=${AUDIO_DIR:-"./audio"}
    if [ -d "$AUDIO_DIR" ] && [ -n "$(ls -A "$AUDIO_DIR" 2>/dev/null)" ]; then
        AUDIO_COUNT=$(find "$AUDIO_DIR" -type f \( -name "*.mp3" -o -name "*.wav" -o -name "*.m4a" \) | wc -l)
        print_status "Found $AUDIO_COUNT audio file(s) for background music"
    else
        print_warning "No audio directory found. Video will have no background music."
        print_status "You can add MP3/WAV files to: $AUDIO_DIR"
    fi
    
    # Run video assembler
    print_status "Assembling final Short video..."
    python3 video_assembler.py <<< "1"  # Auto-assemble option
    
    if [ $? -eq 0 ]; then
        print_success "Video assembly completed"
        return 0
    else
        print_error "Video assembly failed"
        return 1
    fi
}

# Main pipeline
main() {
    echo ""
    echo "Select pipeline mode:"
    echo "  1) Complete pipeline (all steps)"
    echo "  2) Image processing only"
    echo "  3) Video generation only"
    echo "  4) Video assembly only"
    echo ""
    read -p "Enter choice (1-4, default: 1): " PIPELINE_CHOICE
    
    # Load environment variables if .env exists
    if [ -f ".env" ]; then
        print_status "Loading environment variables from .env"
        set -a
        source .env
        set +a
    else
        print_warning ".env file not found. Using default settings."
        print_status "Copy .env.example to .env and add your API keys for full functionality"
    fi
    
    case $PIPELINE_CHOICE in
        1|"")
            print_status "Running complete pipeline..."
            check_python
            install_dependencies
            step1_image_processing
            step2_video_generation
            step3_video_assembly
            ;;
        2)
            print_status "Running image processing only..."
            check_python
            step1_image_processing
            ;;
        3)
            print_status "Running video generation only..."
            check_python
            step2_video_generation
            ;;
        4)
            print_status "Running video assembly only..."
            check_python
            step3_video_assembly
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    # Final output
    echo ""
    echo "================================================================"
    echo "🚀 Pipeline Completed!"
    echo "================================================================"
    
    FINAL_DIR=${FINAL_VIDEOS_DIR:-"./final_videos"}
    
    if [ -d "$FINAL_DIR" ] && [ -n "$(ls -A "$FINAL_DIR" 2>/dev/null)" ]; then
        LATEST_VIDEO=$(ls -t "$FINAL_DIR"/*.mp4 2>/dev/null | head -1)
        
        if [ -n "$LATEST_VIDEO" ]; then
            print_success "Latest video created:"
            echo "  $LATEST_VIDEO"
            echo ""
            print_status "You can now upload this to:"
            echo "  • YouTube Shorts"
            echo "  • TikTok"
            echo "  • Instagram Reels"
            echo ""
            print_status "To upload directly from command line, you can use:"
            echo "  cp \"$LATEST_VIDEO\" ~/Desktop/  # Copy to Desktop"
        fi
    else
        print_warning "No final videos were created."
    fi
    
    echo ""
    print_status "Project structure:"
    echo "  input_images/     - Your source images"
    echo "  enhanced_images/  - Processed images"
    echo "  generated_videos/ - AI-generated video clips"
    echo "  final_videos/     - Complete Shorts"
    echo "  audio/           - Background music (optional)"
    echo ""
    print_success "AI Video Shorts Creator finished!"
}

# Run main function
main "$@"