import os
from wraipperz import generate_video_from_image
from PIL import Image

from dotenv import load_dotenv

load_dotenv()

# Set your API key

# Works with local image paths (auto-encoded as base64)
result = generate_video_from_image(
    # model="fal/kling-video-v2-master",  # Using Kling 2.0 Master
    model="fal-ai/veo2/image-to-video",
    image_path="test_image.png",  # Local image path
    prompt="A beautiful mountain scene with gentle motion in the clouds and water",
    duration="5",  # "5" or "10" seconds
    aspect_ratio="9:16",  # "16:9", "9:16", or "1:1"
    wait_for_completion=True,
    output_path="fal_mountain_scene.mp4"
)

print(f"Video downloaded to: {result['file_path']}")

