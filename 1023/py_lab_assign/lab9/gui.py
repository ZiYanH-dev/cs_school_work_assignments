import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
from lab9 import convert_to_grayscale, adjust_brightness, otsu_thresholding, median_filter

class OtsuApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing with Brightness Adjustment, Otsu's Thresholding and Median Filtering")

        # Frame for image selection
        self.selection_frame = tk.Frame(master)
        self.selection_frame.pack(pady=10)

        self.label = tk.Label(self.selection_frame, text="Select an image:")
        self.label.pack(side=tk.LEFT)

        self.select_button = tk.Button(self.selection_frame, text="Open Image", command=self.load_image)
        self.select_button.pack(side=tk.LEFT)

        # Frame for operation selection
        self.operation_frame = tk.Frame(master)
        self.operation_frame.pack(pady=10)

        self.operation_label = tk.Label(self.operation_frame, text="Select an operation:")
        self.operation_label.pack(side=tk.LEFT)

        self.brightness_button = tk.Button(self.operation_frame, text="Adjust Brightness", command=self.adjust_brightness)
        self.brightness_button.pack(side=tk.LEFT, padx=5)

        self.otsu_button = tk.Button(self.operation_frame, text="Apply Otsu's Thresholding", command=self.apply_otsu)
        self.otsu_button.pack(side=tk.LEFT, padx=5)

        self.median_button = tk.Button(self.operation_frame, text="Apply Median Filter", command=self.apply_median_filter)
        self.median_button.pack(side=tk.LEFT)

        # Frames for displaying images
        self.image_frame = tk.Frame(master)
        self.image_frame.pack(pady=10)

        self.original_frame = tk.Frame(self.image_frame)
        self.original_frame.grid(row=0, column=0, padx=10)

        self.binary_frame = tk.Frame(self.image_frame)
        self.binary_frame.grid(row=0, column=1, padx=10)

        # Labels for original and processed images
        self.original_label = tk.Label(self.original_frame, text="Original Image")
        self.original_label.pack()

        self.binary_label = tk.Label(self.binary_frame, text="Processed Image")
        self.binary_label.pack()

        # Canvases for displaying images
        self.original_canvas = tk.Canvas(self.original_frame, bg="white")
        self.original_canvas.pack()

        self.binary_canvas = tk.Canvas(self.binary_frame, bg="white")
        self.binary_canvas.pack()

        # Label for displaying the optimal threshold
        self.threshold_label = tk.Label(master, text="Optimal Threshold: N/A")
        self.threshold_label.pack(pady=5)

        self.image = None  # Store the original image
        self.gray_image = None  # Store the grayscale image

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", 
                                                filetypes=(("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),))
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.gray_image = convert_to_grayscale(self.image)  # Convert to grayscale
                self.show_image(self.gray_image, self.original_canvas)  # Display the grayscale image as original

                # Resize the processed image canvas to match the original image size
                self.binary_canvas.config(width=self.gray_image.width, height=self.gray_image.height)

                # Clear the processed image canvas
                self.binary_canvas.delete("all")
                self.threshold_label.config(text="Optimal Threshold: N/A")  # Reset threshold label
            except Exception as e:
                messagebox.showerror("Error", f"Could not open the image: {e}")

    def adjust_brightness(self):
        if self.gray_image:
            brightness_factor = simpledialog.askfloat("Brightness Adjustment", 
                                                        "Enter brightness adjustment factor (e.g., 1.2 for brighter, 0.8 for darker):", 
                                                        minvalue=0.0)
            if brightness_factor is not None:
                pixel_array = np.array(self.gray_image)  # Convert to a 2D NumPy array

                # Adjust brightness
                adjusted_pixel_array = adjust_brightness(pixel_array, brightness_factor)

                # Convert the adjusted image array back to a PIL Image for display
                adjusted_image = Image.fromarray(adjusted_pixel_array)
                self.show_image(adjusted_image, self.binary_canvas)  # Display the adjusted image
        else:
            messagebox.showerror("Error", "Please load an image first.")

    def apply_otsu(self):
        if self.gray_image:
            pixel_array = np.array(self.gray_image)  # Convert to a 2D NumPy array

            binary_image_array, threshold = otsu_thresholding(pixel_array)  # Pass the NumPy array

            # Convert the binary image array back to a PIL Image
            binary_image = Image.fromarray(binary_image_array)

            # Display the processed image
            self.show_image(binary_image, self.binary_canvas)

            # Update the threshold label
            self.threshold_label.config(text=f"Optimal Threshold: {threshold}")
            print(f"Otsu's Threshold: {threshold}")
        else:
            messagebox.showerror("Error", "Please load an image first.")

    def apply_median_filter(self):
        if self.gray_image:
            pixel_array = np.array(self.gray_image)  # Convert to a 2D NumPy array

            # Apply median filtering
            filtered_image_array = median_filter(pixel_array)  # Apply median filter with NumPy array

            # Convert the filtered image array back to a PIL Image for display
            filtered_image = Image.fromarray(filtered_image_array)
            self.show_image(filtered_image, self.binary_canvas)  # Display the filtered image
        else:
            messagebox.showerror("Error", "Please load an image first.")

    def show_image(self, image, canvas):
        # Resize image to fit in the canvas
        max_width = 400
        max_height = 400
        image.thumbnail((max_width, max_height))

        # Update canvas size based on image size
        canvas.config(width=image.width, height=image.height)

        image = ImageTk.PhotoImage(image)

        canvas.create_image(0, 0, anchor=tk.NW, image=image)
        canvas.image = image  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = OtsuApp(root)
    root.mainloop()