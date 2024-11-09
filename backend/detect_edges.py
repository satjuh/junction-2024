import numpy as np
from pdf2image import convert_from_path
from joblib import Memory
import logging
import os
from skimage import io, color, filters, morphology, measure, draw, feature, morphology
from skimage.transform import probabilistic_hough_line

# Set up caching
location = "./cachedir"
mem = Memory(location, verbose=0)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define pdf2img as a standalone function
@mem.cache
def pdf2img(path):
    try:
        # Convert PDF to image
        img = convert_from_path(path)[0]
        logging.info("PDF converted to image.")
        return np.array(img)
    except Exception as e:
        logging.error(f"Error converting PDF to image: {e}")
        raise

class FloorPlanProcessor:
    def __init__(self, path, min_component_size=1000, cell_size=50, coverage_threshold=0.5):
        self.path = path
        self.min_component_size = min_component_size
        self.cell_size = cell_size
        self.coverage_threshold = coverage_threshold
        self.original_img = None
        self.processed_img = None
        self.grid_overlay = None

    def preprocess_image(self, img):
        try:
            # Convert to grayscale
            gray = color.rgb2gray(img)
            # Denoise using median filter
            gray = filters.median(gray)
            # Adaptive thresholding
            thresh = filters.threshold_local(gray, block_size=15, offset=3)
            binary = gray < thresh
            return binary.astype(np.uint8) * 255
        except Exception as e:
            logging.error(f"Error in preprocessing image: {e}")
            raise

    def detect_lines(self, img):
        try:
            # Use probabilistic Hough transform
            edges = feature.canny(img.astype(np.uint8))
            lines = probabilistic_hough_line(edges, threshold=10, line_length=5, line_gap=3)
            line_img = np.zeros_like(img)
            for line in lines:
                p0, p1 = line
                rr, cc = draw.line(p0[1], p0[0], p1[1], p1[0])
                line_img[rr, cc] = 255
            return line_img
        except Exception as e:
            logging.error(f"Error in line detection: {e}")
            raise

    def detect_contours(self, img):
        try:
            # Find contours
            contours = measure.find_contours(img, level=0.8)
            contour_img = np.zeros_like(img)
            for contour in contours:
                rr, cc = contour[:, 0].astype(int), contour[:, 1].astype(int)
                contour_img[rr, cc] = 255
            # Fill contours
            contour_img = morphology.binary_fill_holes(contour_img).astype(np.uint8) * 255
            return contour_img
        except Exception as e:
            logging.error(f"Error in contour detection: {e}")
            raise

    def connected_components(self, img):
        try:
            labels = measure.label(img, connectivity=2)
            props = measure.regionprops(labels)
            cleaned_img = np.zeros_like(img)
            for prop in props:
                if prop.area >= self.min_component_size:
                    cleaned_img[labels == prop.label] = 255
            return cleaned_img
        except Exception as e:
            logging.error(f"Error in connected components analysis: {e}")
            raise

    def apply_grid_analysis(self, img):
        try:
            h, w = img.shape
            grid_overlay = color.gray2rgb(img)
            coverage_threshold = int(self.cell_size * self.cell_size * self.coverage_threshold)

            # Optimize grid analysis using numpy slicing
            for y in range(0, h, self.cell_size):
                for x in range(0, w, self.cell_size):
                    cell = img[y:y + self.cell_size, x:x + self.cell_size]
                    white_pixels = np.count_nonzero(cell)
                    if white_pixels > coverage_threshold:
                        rr, cc = draw.rectangle_perimeter(start=(y, x), end=(y + self.cell_size - 1, x + self.cell_size - 1))
                        grid_overlay[rr, cc] = [0, 255, 0]  # Green color
            return grid_overlay
        except Exception as e:
            logging.error(f"Error in grid analysis: {e}")
            raise

    def process(self):
        try:
            # Step 1: Convert PDF to Image
            img = pdf2img(self.path)
            self.original_img = img.copy()

            # Step 2: Preprocess Image
            thresh = self.preprocess_image(img)
            io.imsave("./thresh.png", thresh, check_contrast=False)

            # Step 3: Morphological Operations
            kernel = morphology.square(3)

            # Apply binary closing in a loop to achieve the effect of multiple iterations
            morph = thresh
            for _ in range(2):  # Apply twice as per iterations=2
                morph = morphology.binary_closing(morph, footprint=kernel)

            # Convert the result to uint8 and save the image
            morph = morph.astype(np.uint8) * 255
            io.imsave("./morph.png", morph, check_contrast=False)

            # Step 4: Line Detection
            line_img = self.detect_lines(morph)
            io.imsave("./lines.png", line_img, check_contrast=False)

            # Step 5: Contour Detection
            contour_img = self.detect_contours(line_img)
            io.imsave("./contours.png", contour_img, check_contrast=False)

            # Step 6: Combine Results
            combined = np.bitwise_or(morph, contour_img)
            io.imsave("./combined.png", combined, check_contrast=False)

            # Step 7: Connected Components Analysis
            connected = self.connected_components(combined)
            io.imsave("./connected.png", connected, check_contrast=False)

            # Step 8: Grid Analysis
            self.grid_overlay = self.apply_grid_analysis(connected)
            io.imsave("./grid_overlay.png", self.grid_overlay, check_contrast=False)

            # Step 9: Overlay Results
            # Resize original image to match the grid overlay size
            original_resized = self.original_img
            if original_resized.shape[:2] != self.grid_overlay.shape[:2]:
                original_resized = resize(original_resized, self.grid_overlay.shape[:2], anti_aliasing=True)
                original_resized = (original_resized * 255).astype(np.uint8)
            overlay = (0.6 * original_resized + 0.4 * self.grid_overlay).astype(np.uint8)
            io.imsave("./final_with_grid.png", overlay, check_contrast=False)

            logging.info("Processing completed successfully.")
        except Exception as e:
            logging.error(f"Error in processing: {e}")
            raise

# Usage
if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("./output", exist_ok=True)
    os.chdir("./output")

    # Path to the provided floorplan PDF
    path = "/Users/haaparanta/Desktop/junction-2024/backend/numpy-to-glb/floor_1.pdf"  # Update this path to your PDF location

    # Initialize processor with desired parameters
    processor = FloorPlanProcessor(
        path=path,
        min_component_size=5000,   # Adjusted based on image resolution
        cell_size=100,             # Larger cell size for performance
        coverage_threshold=0.3     # Lower threshold for detection sensitivity
    )

    # Run processing
    processor.process()