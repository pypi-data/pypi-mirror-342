import os
import time
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from wraipperz.api import (
    generate_video_from_image,
    get_video_status,
    download_video,
)

# Load environment variables from .env file
load_dotenv()

# Make sure you have set FAL_KEY in your environment or .env file
# You can get an API key from https://fal.ai/dashboard


def fal_image_to_video_example():
    """Example of generating a video from an image using fal.ai"""
    print("\n=== fal.ai Image-to-Video Example ===")
    
    # You can use either a URL or a local image path
    # Option 1: URL (preferred for production use)
    image_url = "https://example.com/your-image.jpg"
    
    # Option 2: Local file path (will be automatically encoded as base64)
    local_image_path = "examples/sample_images/mountain.jpg"
    
    # Option 3: PIL Image object (will be automatically encoded as base64)
    # pil_image = Image.open(local_image_path)
    
    # Choose which image source to use for this example
    if Path(local_image_path).exists():
        image_source = local_image_path
        print(f"Using local image: {local_image_path}")
    else:
        image_source = image_url
        print(f"Using image URL: {image_url}")
    
    prompt = "A beautiful mountain scene with gentle motion in the clouds and water"
    
    print(f"Generating video from image with prompt: '{prompt}'")
    
    try:
        # Generate video - automatically handles local files by converting to base64
        result = generate_video_from_image(
            model="fal/kling-video-v2-master",  # Using Kling 2.0 Master
            image_path=image_source,  # Works with URL, local path, or PIL Image
            prompt=prompt,
            negative_prompt="blur, distort, low quality, text, watermark",
            duration="5",  # "5" or "10" seconds
            aspect_ratio="16:9",  # "16:9", "9:16", or "1:1"
            cfg_scale=0.5  # Guidance scale (0.0 to 1.0)
        )
        
        print(f"Video generation started with request ID: {result['request_id']}")
        
        # Wait for completion by polling status
        # Note: for fal.ai, we pass the entire result dict as the video_id
        while True:
            status = get_video_status(
                model="fal/kling-video-v2-master",
                video_id=result  # Pass the entire result dict
            )
            
            if status["status"] == "success":
                print(f"Video generation complete! URL: {status['url']}")
                
                # Download the video
                output_file = "examples/generated_videos/fal_kling_video.mp4"
                downloaded_path = download_video(
                    model="fal/kling-video-v2-master",
                    video_url=status['url'],
                    output_path=output_file
                )
                print(f"Video downloaded to: {downloaded_path}")
                break
            elif status["status"] == "failed":
                print(f"Video generation failed: {status.get('error', 'Unknown error')}")
                break
            else:
                print(f"Still processing... (status: {status['status']})")
                time.sleep(5)
    
    except Exception as e:
        print(f"Error: {e}")


def fal_all_in_one_example():
    """Example of using fal.ai with auto wait and download"""
    print("\n=== fal.ai All-in-One Example ===")
    
    # Create a sample directory if it doesn't exist
    sample_dir = Path("examples/sample_images")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # For this example, let's create a simple colored image if none exists
    sample_image_path = sample_dir / "sample.png"
    if not sample_image_path.exists():
        print(f"Creating sample image at {sample_image_path}")
        # Create a simple gradient image
        img = Image.new('RGB', (800, 600), color='white')
        pixels = img.load()
        
        # Create a simple color gradient
        for i in range(img.width):
            for j in range(img.height):
                r = int(255 * i / img.width)
                g = int(255 * (1 - i / img.width))
                b = int(255 * j / img.height)
                pixels[i, j] = (r, g, b)
        
        img.save(sample_image_path)
    
    # Use the PIL Image object directly
    pil_image = Image.open(sample_image_path)
    
    prompt = "A colorful ocean scene with gentle waves and clouds moving in the sky"
    
    print(f"Generating video from PIL Image with prompt: '{prompt}'")
    
    try:
        # Generate video with automatic wait and download
        result = generate_video_from_image(
            model="fal/minimax-video",
            image_path=pil_image,  # Works directly with PIL Image objects
            prompt=prompt,
            wait_for_completion=True,  # Wait for video to complete
            output_path="examples/generated_videos/fal_gradient",  # Extension will be added automatically
            max_wait_time=600  # Wait up to 10 minutes
        )
        
        print(f"Video generation complete! Downloaded to: {result['file_path']}")
        print(f"Video URL: {result['url']}")
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Check if API key is set
    if not os.getenv("FAL_KEY"):
        print("FAL_KEY environment variable not set. Please set it in your .env file.")
        print("You can get an API key from https://fal.ai/dashboard")
        return
    
    # Create directories for output
    Path("examples/generated_videos").mkdir(parents=True, exist_ok=True)
    Path("examples/sample_images").mkdir(parents=True, exist_ok=True)
    
    # Run examples
    fal_image_to_video_example()
    
    # Uncomment to run the all-in-one example that creates and uses a PIL Image
    # fal_all_in_one_example()


if __name__ == "__main__":
    main() 