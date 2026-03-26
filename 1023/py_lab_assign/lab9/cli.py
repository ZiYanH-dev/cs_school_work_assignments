import os
import sys
from PIL import Image
import numpy as np
from lab9 import convert_to_grayscale, adjust_brightness, otsu_thresholding, median_filter

def main():
    # Get the current directory of lab9.py
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Prompt the user for the image file name
    image_filename = input("Enter the image file name (with extension) in the same folder as lab9.py: ")
    image_path = os.path.join(current_directory, image_filename)

    # Check if the file exists
    if not os.path.isfile(image_path):
        print(f"Error: The file '{image_filename}' does not exist in the current directory.")
        return

    # Read the image
    image = Image.open(image_path)

    # Convert to grayscale and then to a NumPy array
    gray_image = convert_to_grayscale(image)
    pixel_array = np.array(gray_image)

    # Prompt the user for which routine to call

    # Prompt the user for which routine to call
    print("Select a routine to apply:")
    print("1. Brightness Adjustment")
    print("2. Otsu's Thresholding")
    print("3. Median Filtering")
    choice = input("Enter the number of your choice (1, 2, or 3): ")

    if choice == '1':
        # Prompt the user for brightness adjustment
        brightness_factor = float(input("Enter brightness adjustment factor (e.g., 1.2 for brighter, 0.8 for darker): "))
        adjusted_pixel_array = adjust_brightness(pixel_array, brightness_factor)

        # Convert the adjusted pixel array back to a PIL Image for display
        adjusted_image = Image.fromarray(adjusted_pixel_array)
        gray_image.show(title="Original Image")        
        adjusted_image.show(title="Brightness Adjusted Image")

    elif choice == '2':
        # Apply Otsu's thresholding
        binary_image_array, threshold = otsu_thresholding(pixel_array)

        # Convert the binary image array back to a PIL Image
        binary_image = Image.fromarray(binary_image_array)

        # Show results
        print(f"Otsu's Threshold: {threshold}")
        gray_image.show(title="Original Image")
        binary_image.show(title="Binary Image")

    elif choice == '3':
        # Apply median filtering
        filtered_image_array = median_filter(pixel_array)  # Apply median filter with NumPy array
        filtered_image = Image.fromarray(filtered_image_array)  # Convert back to Image for display
        gray_image.show(title="Original Image")        
        filtered_image.show(title="Filtered Image")

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()