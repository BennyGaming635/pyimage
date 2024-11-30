import sys
import subprocess
from PIL import Image
import os

# Function to check and install missing libraries
def check_install_library(library_name, import_name=None):
    try:
        __import__(import_name or library_name)
    except ImportError:
        print(f"Library '{library_name}' is not installed.")
        response = input(f"Do you want to install '{library_name}' now? (y/n): ").lower()
        if response == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install '{library_name}'. Please install it manually.")
                sys.exit(1)
        else:
            print(f"Cannot proceed without '{library_name}'. Exiting.")
            sys.exit(1)

# Check for Pillow, imported as PIL
check_install_library("Pillow", "PIL")

# Function to convert a single image to PNG
def convert_to_png(input_path, output_path):
    """
    Convert a single image to PNG format.
    """
    try:
        img = Image.open(input_path)
        output_file = os.path.splitext(os.path.basename(input_path))[0] + ".png"
        output_file_path = os.path.join(output_path, output_file)
        img.save(output_file_path, format="PNG")
        print(f"Converted: {input_path} -> {output_file_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

# Function to convert all images in a folder to PNG
def batch_convert_to_png(input_folder, output_folder):
    """
    Convert all images in a folder to PNG format.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)

        if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff', 'webp')):
            convert_to_png(input_path, output_folder)
        else:
            print(f"Skipping non-image file: {file_name}")

# Main Program
if __name__ == "__main__":
    print("Welcome to PyImage!")
    input_folder = input("Enter the path to the folder with images: ").strip()
    output_folder = input("Enter the path for the converted PNG images: ").strip()

    if os.path.exists(input_folder):
        batch_convert_to_png(input_folder, output_folder)
        print("Conversion complete!")
    else:
        print("Input folder does not exist. Please check the path and try again.")
