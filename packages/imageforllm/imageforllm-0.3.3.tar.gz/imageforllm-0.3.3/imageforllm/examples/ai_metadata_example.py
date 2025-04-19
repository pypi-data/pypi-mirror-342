"""
Example showing how to add AI generation metadata to images
"""

import os
import sys
import imageforllm

# First, check if we have an image file to work with
if len(sys.argv) < 2:
    print("Usage: python ai_metadata_example.py <image_file>")
    sys.exit(1)

image_path = sys.argv[1]

# Ensure the file exists
if not os.path.isfile(image_path):
    print(f"Error: File '{image_path}' does not exist", file=sys.stderr)
    sys.exit(1)

# Example AI metadata to add
model = "stable-diffusion-xl-1.0"
prompt = "A serene mountain landscape with a lake reflecting the sunset"
parameters = {
    "seed": 42,
    "guidance_scale": 7.5,
    "num_inference_steps": 50,
    "width": 1024,
    "height": 1024
}

print(f"Adding AI metadata to '{image_path}'...")

# Add the metadata to the image
success = imageforllm.add_ai_metadata(image_path, model, prompt, parameters)

if success:
    print("Metadata added successfully!")
    
    # Now extract and display the metadata to verify
    print("\nReading back the metadata:")
    
    # Extract just the AI metadata
    ai_info = imageforllm.extract_ai_metadata(image_path)
    print("\nAI Metadata:")
    for key, value in ai_info.items():
        print(f"  {key}: {value}")
    
    # Get all metadata as JSON
    print("\nAll Metadata (JSON):")
    all_info = imageforllm.get_all_metadata_json(image_path)
    for key, value in all_info.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")
else:
    print("Failed to add metadata to the image.", file=sys.stderr) 