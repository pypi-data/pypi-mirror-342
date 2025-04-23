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

# Make sure you have set KLING_API_KEY in your environment or .env file
# You can get an API key from https://app.klingai.com/

def kling_text_to_video_example():
    """Example of generating a video from a text prompt using Kling AI"""
    print("\n=== Kling AI Text-to-Video Example ===")
    
    # Generate a video from text
    prompt = "A futuristic cityscape with flying cars and neon lights at night"
    negative_prompt = "poor quality, blurry, distorted"
    
    print(f"Generating video with prompt: '{prompt}'")
    
    # Generate with automatic wait and download
    result = generate_video_from_text(
        model="kling/text-to-video",
        prompt=prompt,
        negative_prompt=negative_prompt,
        duration=5,  # 5 seconds
        width=768, 
        height=432,
        fps=24,
        wait_for_completion=True,
        output_path="examples/generated_videos/kling_city",  # Extension will be added automatically
        max_wait_time=600  # Wait up to 10 minutes
    )
    
    print(f"Video generation complete! Downloaded to: {result['file_path']}")
    print(f"Video URL: {result['url']}")


def kling_image_to_video_example():
    """Example of generating a video from an image using Kling AI"""
    print("\n=== Kling AI Image-to-Video Example ===")
    
    # Path to your image file
    # Replace with your own image path
    image_path = "examples/mountain_lake.jpg"
    
    # Check if the image exists
    if not Path(image_path).exists():
        print(f"Image not found at {image_path}. Please update the path.")
        return
    
    prompt = "Add gentle waves to the water and clouds moving in the sky"
    negative_prompt = "poor quality, distortion"
    
    print(f"Generating video from image with prompt: '{prompt}'")
    
    try:
        # Generate without automatic wait
        result = generate_video_from_image(
            model="kling/image-to-video",
            image_path=image_path,
            prompt=prompt,
            negative_prompt=negative_prompt,
            duration=5,
            fps=24
        )
        
        print(f"Video generation started with task ID: {result['task_id']}")
        
        # Poll for status manually
        task_id = result["task_id"]
        print("Checking status every 15 seconds...")
        
        while True:
            status = get_video_status(
                model="kling/image-to-video",
                video_id=task_id
            )
            
            if status["status"] == "success":
                print(f"Video generation complete! URL: {status['url']}")
                
                # Download the video after it's ready
                output_file = "examples/generated_videos/kling_mountain_lake.mp4"
                downloaded_path = download_video(
                    model="kling/image-to-video",
                    video_url=status['url'],
                    output_path=output_file
                )
                print(f"Video downloaded to: {downloaded_path}")
                break
            elif status["status"] == "failed":
                print(f"Video generation failed")
                break
            else:
                print(f"Still processing... (status: {status['status']}, progress: {status['progress']}%)")
                time.sleep(15)
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Check if API key is set
    if not os.getenv("KLING_API_KEY"):
        print("KLING_API_KEY environment variable not set. Please set it in your .env file.")
        return
    
    # Create directory for output videos if it doesn't exist
    Path("examples/generated_videos").mkdir(parents=True, exist_ok=True)
    
    # Run examples
    kling_text_to_video_example()
    
    # Uncomment the line below to run the image-to-video example
    # Make sure you have a valid image file at the specified path
    # kling_image_to_video_example()


if __name__ == "__main__":
    main() 