import numpy as np
import math
from PIL import Image

def convert_to_grayscale(image: Image.Image) -> Image.Image:
    # Parameter:
    # image: This parameter is expected to be a color image object (from the Pillow library).
    #        It represents the image that you want to convert to grayscale.

    """Convert a color image to grayscale using Pillow."""
    return image.convert('L')  # Convert to grayscale mode 'L'

def adjust_brightness(pixel_array: np.ndarray, brightness_factor: float) -> np.ndarray:
    # Parameters:
    # pixel_array: This is a 2D NumPy array that contains pixel values of the image.
    #              Each value represents the intensity of a pixel in the range of 0 to 255.
    # brightness_factor: This is a scalar value (float) that determines how much to
    #                    adjust the brightness. A value greater than 1 increases
    #                    brightness, while a value less than 1 decreases it.
    # Note: You ARE NOT ALLOWED to use any loops for this task!

    """TODO: Adjust the brightness of a 2D NumPy array of pixel values."""
    # Your code here
    pixel_array=pixel_array*brightness_factor
    pixel_array=pixel_array.clip(0,255)
    return pixel_array.astype(np.int32)

def otsu_thresholding(pixel_array: np.ndarray) -> tuple[np.ndarray, float]:
    # Parameter:
    # pixel_array: This is a 2D NumPy array of pixel values representing
    #              a grayscale image. The function uses this array to compute
    #              an optimal threshold for converting the image into a binary format.

    """TODO: Perform Otsu's thresholding on a 2D NumPy array of pixel values."""
    # Your code here
    #each time we compare the new_threshold with the threshold we get last time

    threshold=pixel_array.mean()
    while True:
        g1=pixel_array[pixel_array<=threshold]
        g2=pixel_array[pixel_array>threshold]
        new_threshold=(g1.mean()+g2.mean())/2
        if math.isclose(new_threshold,threshold):
            pixel_array[pixel_array>threshold]=255
            pixel_array[pixel_array<threshold]=0
            return pixel_array,new_threshold
        threshold=new_threshold


def median_filter(pixel_array: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    # Parameters:
    # pixel_array: This is a 2D NumPy array of pixel values representing the image
    #              to which the median filter will be applied.
    # kernel_size: This is an optional parameter (default value is 3) that specifies
    #              the size of the square kernel used for the median filtering.
    #              The kernel size determines the area around each pixel that will be
    #              considered when calculating the median value. It should be an odd
    #              integer (e.g., 3, 5, 7) to ensure a center pixel.
    # Note: You can assume the kernel_size is always an odd number.
    
    """TODO: Apply median filtering to a NumPy array of pixel values using a specified kernel size."""

    padded=np.pad(pixel_array,((1,1),(1,1)),mode='edge')
    output_arr=np.zeros_like(pixel_array)
    for i in range(len(padded)-kernel_size+1):
        for j in range(len(padded[i])-kernel_size+1):
            region=padded[i:i+kernel_size,j:j+kernel_size]
            m=np.median(region)
            output_arr[i][j]=m

    return output_arr