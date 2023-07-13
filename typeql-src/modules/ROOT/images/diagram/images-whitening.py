from PIL import Image
import os


def replace_transparent_with_white(image_path):
    image = Image.open(image_path)

    # Check if the image has an alpha channel
    if image.mode == 'RGBA':
        # Create a new image with white background
        white_image = Image.new('RGB', image.size, (255, 255, 255))
        white_image.paste(image, mask=image.split()[3])

        # Save the image, overwriting the original file
        white_image.save(image_path)
        print(f"Processed: {image_path}")
    else:
        print(f"Skipped (Not RGBA): {image_path}")


# Get a list of all PNG files in the current directory
png_files = [file for file in os.listdir() if file.lower().endswith('.png')]

# Process each PNG file
for file in png_files:
    replace_transparent_with_white(file)
    