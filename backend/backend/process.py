import sys
from PIL import Image
import numpy as np
from scipy.ndimage import convolve, label, find_objects
from pdf2image import convert_from_path, convert_from_bytes
from io import BytesIO


def pdf_to_nparray(pdf: bytes):
    return np.array(convert_from_bytes(pdf)[0].convert("L"))

def png_to_nparray(png: bytes):
    return np.array(Image.open(BytesIO(png)).convert("L"))

def create_simple_floorplan(
    img_array: np.ndarray, k, threshold, area_threshold, elongation_threshold
):
    # Create a normalized kernel of size k x k
    kernel = np.ones((k, k), dtype=np.float32) / (k * k)

    # Convolve the image with the kernel to compute the average grayness
    avg_array = convolve(img_array, kernel, mode="reflect")

    # Create the binary image based on the average grayness
    binary_array = np.where(avg_array > threshold, 255, 0).astype(np.uint8)

    # Invert the image: background should be 0, foreground (lines) should be 1
    binary_array = 1 - binary_array // 255

    # Label connected components
    labeled_array, _num_features = label(binary_array)

    # Initialize an output array
    output_array = np.zeros_like(binary_array)

    # Process each connected component
    slices = find_objects(labeled_array)
    for i, slice_ in enumerate(slices):
        component = labeled_array[slice_] == (i + 1)
        area = np.sum(component)

        # Compute elongation (aspect ratio)
        rows, cols = component.nonzero()
        if rows.size == 0 or cols.size == 0:
            continue  # Skip empty components

        height = rows.max() - rows.min() + 1
        width = cols.max() - cols.min() + 1
        elongation = (
            max(height, width) / min(height, width) if min(height, width) != 0 else 0
        )

        # Check area and elongation to decide if it's a line-like structure
        if area >= area_threshold or elongation >= elongation_threshold:
            output_array[slice_][component] = 1  # Keep the component

    # Convert output_array back to 0 and 255
    output_array = (1 - output_array) * 255  # Invert back to original color scheme
    output_floor = Image.fromarray(output_array.astype(np.uint8))
    output_floor.save('walls_.png')
    return output_array


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python script.py input.png [output.png] [threshold] [kernel_size] [area_threshold] [elongation_threshold]"
        )
        sys.exit(1)

    input_filename = sys.argv[1]

    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
    else:
        output_filename = "output.png"

    if len(sys.argv) >= 4:
        threshold = int(sys.argv[3])
    else:
        threshold = 127  # Default threshold

    if len(sys.argv) >= 5:
        k = int(sys.argv[4])
    else:
        k = 9  # Default kernel size

    if len(sys.argv) >= 6:
        area_threshold = int(sys.argv[5])
    else:
        area_threshold = 50  # Default area threshold

    if len(sys.argv) >= 7:
        elongation_threshold = float(sys.argv[6])
    else:
        elongation_threshold = 2.0  # Default elongation threshold

    print(area_threshold, elongation_threshold, k)

    # Read the image and convert it to grayscale
    img = convert_from_path(input_filename)[0].convert("L")  # L for grayscale
    # img = Image.open(input_filename).convert("L")  # 'L' mode for grayscale

    # Convert image to numpy array
    img_array = np.array(img).astype(np.float32)

    output_array = create_simple_floorplan(
        img_array, k, threshold, area_threshold, elongation_threshold
    )

    # Convert the output array back to an image and save it
    output_img = Image.fromarray(output_array.astype(np.uint8))
    output_img.save(output_filename)
    np.save(output_filename + ".npy", np.array(output_img))
    print(f"Processed image saved as {output_filename}")


def array_into_png(array: np.ndarray):
    bio = BytesIO()
    output_img = Image.fromarray(array.astype(np.uint8))
    output_img.save(bio, format="PNG")
    return bio.getvalue()
