import logging
import numpy as np
import trimesh
from skimage import filters, measure
from shapely.geometry import Polygon
from trimesh.creation import extrude_polygon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def image_data_to_glb(
    data,
    output_filename,
    height=5.0,
    buffer_distance=0.1
):
    """
    Extrude detected contours from image data and export as a GLB file.

    Parameters:
        data (np.ndarray): 2D array of image data where non-zero pixels indicate boundaries.
        output_filename (str): The path for the output GLB file.
        height (float): The extrusion height.
        buffer_distance (float): The buffer distance for lines.
    """
    try:
        # Step 1: Apply edge detection to highlight lines/boundaries
        logger.info("Applying edge detection")
        edges = filters.sobel(data)

        # Step 2: Find contours of the detected edges, representing potential line paths
        logger.info("Finding contours")
        contours = measure.find_contours(edges, level=0.1)

        # Initialize a list to hold the extruded meshes
        meshes = []

        # Step 3: Process each contour to create an extruded 3D shape
        for contour in contours:
            # Convert contour points to a polygon and extrude
            polygon = Polygon(contour)
            if polygon.is_valid:
                logger.info("Extruding a polygon")
                mesh = extrude_polygon(polygon, height=height)
                meshes.append(mesh)
            else:
                logger.warning("Invalid polygon detected, skipping")

        # Step 4: Combine all meshes into a single mesh
        logger.info("Combining meshes")
        combined_mesh = trimesh.util.concatenate(meshes)

        # Export the combined mesh to a GLB file
        logger.info(f"Exporting combined mesh to: {output_filename}")
        combined_mesh.export(output_filename)

        logger.info("Extrusion and export completed successfully")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Load the image data file
    walls = np.load('walls.npy')
    floor_ceiling = np.load('floor-ceiling.npy')
    
    walls = True
    floor = True
    ceiling = False
    
    # Run the extrusion and export process
    image_data_to_glb(
        data=walls,
        output_filename='test-numpy-3.glb',
        height=50.0,
        buffer_distance=0.1
    )