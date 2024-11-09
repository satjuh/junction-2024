import sys
from PIL import Image
import numpy as np
from scipy.ndimage import convolve, label, find_objects
import cv2
from matplotlib import pyplot as plt


def find_largest_component(array):
    contours, _ = cv2.findContours(array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 3: Calculate the bounding box around all wall contours
    x, y, w, h = cv2.boundingRect(np.vstack(contours))

    # Crop the image to the bounding box area to focus only on the walls
    cropped = array[y : y + h, x : x + w]

    # Step 4: Use morphological closing to close gaps within the cropped walls
    kernel = np.ones((20, 20), np.uint8)
    closed = cv2.morphologyEx(cropped, cv2.MORPH_CLOSE, kernel)

    # Step 5: Detect and fill contours within the cropped region
    contours_cropped, _ = cv2.findContours(
        closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contour_filled = np.zeros_like(closed)
    cv2.drawContours(contour_filled, contours_cropped, -1, (255), thickness=cv2.FILLED)

    # Step 6: Flood fill the enclosed areas within the cropped bounding box
    flood_filled = contour_filled.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood_filled, mask, (0, 0), 255)  # start from outside point

    # Invert and combine flood-filled with original closed contours to fill inside regions
    flood_filled_inv = cv2.bitwise_not(flood_filled)
    final_cropped = cv2.bitwise_or(contour_filled, flood_filled_inv)

    # Step 7: Place the filled bounding box area back into the original image
    final_result = array.copy()
    final_result[y : y + h, x : x + w] = final_cropped

    # Display the result
    plt.figure(figsize=(12, 12))
    plt.subplot(1, 3, 1)
    plt.title("Cropped and Closed Boundaries")
    plt.imshow(closed, cmap="gray")
    plt.subplot(1, 3, 2)
    plt.title("Filled Enclosed Areas in Cropped Region")
    plt.imshow(final_cropped, cmap="gray")
    plt.subplot(1, 3, 3)
    plt.title("Final Result with Bounding Box Applied to Original Image")
    plt.imshow(final_result, cmap="gray")
    plt.show()
    return final_result


def connected_components(array, min_size=100_000):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        array, connectivity=8
    )

    cleaned_img = np.zeros_like(array)

    # Step 4: Filter components by size and keep only those above the threshold
    for i in range(1, num_labels):  # Start from 1 to skip the background
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            cleaned_img[labels == i] = 255

    # Invert the image back to original color scheme (lines black, background white)
    cleaned_img = cv2.bitwise_not(cleaned_img)
    print("Connected")
    return cleaned_img


def floor(array):
    filled = np.full_like(array, 255)
    contours, _ = cv2.findContours(
        255 - array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours:
        # Check if the contour is internal (exclude the external boundary)
        if (
            cv2.pointPolygonTest(contour, (0, 0), False) < 0
        ):  # External contours should be excluded
            cv2.drawContours(filled, [contour], -1, (0, 255, 0), thickness=-1)
            break
    return filled


def wall_detector(
    floor_plan: np.ndarray, threshold, k, area_threshold, elongation_threshold
):
    # Convert image to numpy array
    img_array = np.array(floor_plan).astype(np.float32)

    # Create a normalized kernel of size k x k
    kernel = np.ones((k, k), dtype=np.float32) / (k * k)

    # Convolve the image with the kernel to compute the average grayness
    avg_array = convolve(img_array, kernel, mode="reflect")

    # Create the binary image based on the average grayness
    binary_array = np.where(avg_array > threshold, 255, 0).astype(np.uint8)

    # Invert the image: background should be 0, foreground (lines) should be 1
    binary_array = 1 - binary_array // 255

    # Label connected components
    labeled_array, num_features = label(binary_array)

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
    output_array = (1 - output_array) * 255  # Invert back to original color scheme
    return output_array


def create_simple_floor(
    floor_plan: np.ndarray, k, threshold, area_threshold, elongation_threshold
):
    output_array = wall_detector(
        floor_plan, threshold, k, area_threshold, elongation_threshold
    )

    # Convert output_array back to 0 and 255
    floor_array = wall_detector(floor_plan, 190, 3, 1500, 20)

    filled_floor = floor(floor_array)
    # Convert the output array back to an image and save it
    output_floor = Image.fromarray(filled_floor.astype(np.uint8))
    return output_array
