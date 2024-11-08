import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import ImageFilter, Image
from pdf2image import convert_from_path


def pdf2img(path):
    img = convert_from_path(path)[0]
    img = img.filter(ImageFilter.MedianFilter(5))
    img = img.filter(ImageFilter.GaussianBlur(5))
    img = img.filter(ImageFilter.ModeFilter(5))
    print("PDF converted")
    return np.array(img)


def connected_components(array):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        array, connectivity=8
    )

    cleaned_img = np.zeros_like(array)

    # Define the minimum size of components to keep (e.g., 50 pixels)
    min_size = 10000

    # Step 4: Filter components by size and keep only those above the threshold
    for i in range(1, num_labels):  # Start from 1 to skip the background
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            cleaned_img[labels == i] = 255

    # Invert the image back to original color scheme (lines black, background white)
    cleaned_img = cv2.bitwise_not(cleaned_img)
    print("Connected")
    return cleaned_img


def floor_plan(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 0, 150)
    blurred = cv2.GaussianBlur(edges, (25, 25), 0)
    walls = connected_components(blurred)
    walls = cv2.Canny(walls, 0, 150)
    return walls


def plotting(img):
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.show()
    np.save("./clean_np.npy", img, allow_pickle=True)
    # Save the cleaned image
    cv2.imwrite("./cleaned_image.png", img)


path = "./floor_1.pdf"
img = pdf2img(path)
cleaned = floor_plan(img)
plotting(cleaned)
