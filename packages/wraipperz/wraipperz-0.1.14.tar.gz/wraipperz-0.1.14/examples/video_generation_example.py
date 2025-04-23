import os
import time
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from wraipperz.api import (
    generate_video_from_text,
    generate_video_from_image,
    get_video_status,
    wait_for_video_completion,
    download_video,
)

# Load environment variables from .env file
load_dotenv()

# Make sure you have set PIXVERSE_API_KEY in your environment or .env file
# You can get an API key from https://platform.pixverse.ai/

def text_to_video_example():
    """Example of generating a video from a text prompt"""
    print("\n=== Text-to-Video Example ===")
    
    # Generate a video from text
    prompt = "A serene mountain lake at sunrise, with mist rising from the water. Birds fly overhead as the morning unfolds."
    negative_prompt = "blurry, distorted, low quality, text, watermark"
    
    print(f"Generating video with prompt: '{prompt}'")
    
    # Method 1: Generate and poll for status manually
    result = generate_video_from_text(
        model="pixverse/text-to-video-v3.5",
        prompt=prompt,
        negative_prompt=negative_prompt,
        duration=5,  # 5 seconds
        quality="720p",
        style="3d_animation",  # Optional style: "anime", "3d_animation", "day", "cyberpunk", "comic"
    )
    
    print(f"Video generation started with ID: {result['video_id']}")
    
    # Poll for status until complete
    video_id = result["video_id"]
    print("Checking status every 10 seconds...")
    
    while True:
        status = get_video_status(
            model="pixverse/text-to-video-v3.5",
            video_id=video_id
        )
        
        if status["status"] == 1:  # Complete
            print(f"Video generation complete! URL: {status['url']}")
            
            # Optional: Download the video after it's ready
            output_file = "examples/generated_videos/mountain_lake_manual.mp4"
            downloaded_path = download_video(
                model="pixverse/text-to-video-v3.5",
                video_url=status['url'],
                output_path=output_file
            )
            print(f"Video downloaded to: {downloaded_path}")
            break
        elif status["status"] in [7, 8]:  # Failed
            print(f"Video generation failed with status {status['status']}")
            break
        else:
            print(f"Still processing... (status: {status['status']})")
            time.sleep(10)
    
    # Method 2: Generate, wait for completion, and download all in one call
    print("\nGenerating another video with automatic download...")
    result = generate_video_from_text(
        model="pixverse/text-to-video-v3.5",
        prompt="A beautiful sunset over mountains with clouds changing colors",
        negative_prompt=negative_prompt,
        duration=5,
        quality="720p",
        style="day",
        # Automatically wait for completion
        wait_for_completion=True,
        # Automatically download when complete
        output_path="examples/generated_videos/sunset_mountains",  # Extension will be added automatically
        # Additional wait parameters
        polling_interval=5,  # Check every 5 seconds
        max_wait_time=300,  # Wait up to 5 minutes
    )
    
    print(f"Video generation complete! Downloaded to: {result['file_path']}")
    print(f"Video URL: {result['url']}")


def image_to_video_example():
    """Example of generating a video from an image"""
    print("\n=== Image-to-Video Example ===")
    
    # Path to your image file
    # Replace with your own image path
    image_path = "examples/mountain_lake.jpg"
    
    # Alternatively, you can use a PIL Image
    # img = Image.open("examples/mountain_lake.jpg")
    
    # Check if the image exists
    if not Path(image_path).exists():
        print(f"Image not found at {image_path}. Please update the path.")
        return
    
    prompt = "A beautiful mountain lake scene with gentle ripples and birds flying"
    negative_prompt = "blurry, distorted, low quality, text, watermark"
    
    print(f"Generating video from image with prompt: '{prompt}'")
    try:
        # Use both wait_for_completion and output_path for convenience
        result = generate_video_from_image(
            model="pixverse/image-to-video-v3.5",
            image_path=image_path,
            prompt=prompt,
            negative_prompt=negative_prompt,
            duration=5,
            quality="720p",
            wait_for_completion=True,  # This will block until the video is ready
            output_path="examples/generated_videos/from_image.mp4",  # Specify full path with extension
            max_wait_time=300  # Wait up to 5 minutes
        )
        
        print(f"Video generation complete! Downloaded to: {result['file_path']}")
        print(f"Video URL: {result['url']}")
    except TimeoutError as e:
        print(f"Timeout error: {e}")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    # Check if API key is set
    if not os.getenv("PIXVERSE_API_KEY"):
        print("PIXVERSE_API_KEY environment variable not set. Please set it in your .env file.")
        return
    
    # Create directory for output videos if it doesn't exist
    Path("examples/generated_videos").mkdir(parents=True, exist_ok=True)
    
    # Run examples
    text_to_video_example()
    
    # Uncomment the line below to run the image-to-video example
    # Make sure you have a valid image file at the specified path
    # image_to_video_example()


if __name__ == "__main__":
    main() 