import logging
import numpy as np
import trimesh
from skimage import filters, measure
from shapely.geometry import Polygon
from trimesh.creation import extrude_polygon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def image_data_to_glb(
    wall_data,
    floor_ceiling_data,
    output_filename,
    wall_height=5.0,
    floor_height=0.1,
    ceiling_height=0.1,
    buffer_distance=0.1,
    walls=True,
    floor=True,
    ceiling=True
):
    """
    Extrude detected contours from image data and export as a GLB file.

    Parameters:
        wall_data (np.ndarray): 2D array where non-zero pixels indicate wall boundaries.
        floor_ceiling_data (np.ndarray): 2D array where non-zero pixels indicate floor/ceiling.
        output_filename (str): The path for the output GLB file.
        wall_height (float): The extrusion height for walls.
        floor_height (float): The extrusion height for the floor.
        ceiling_height (float): The extrusion height for the ceiling.
        buffer_distance (float): The buffer distance for lines.
        walls (bool): Whether to create walls.
        floor (bool): Whether to create a floor.
        ceiling (bool): Whether to create a ceiling.
    """
    try:
        meshes = []

        # Process walls if enabled
        if walls:
            logger.info("Processing walls")
            edges = filters.sobel(wall_data)
            contours = measure.find_contours(edges, level=0.1)

            for contour in contours:
                polygon = Polygon(contour)
                if polygon.is_valid:
                    mesh = extrude_polygon(polygon, height=wall_height)
                    meshes.append(mesh)
                else:
                    logger.warning("Invalid wall polygon detected, skipping")

        # Process floor if enabled
        if floor:
            logger.info("Processing floor")
            contours = measure.find_contours(floor_ceiling_data, level=0.1)

            for contour in contours:
                polygon = Polygon(contour)
                if polygon.is_valid:
                    # Extrude the floor at the specified height
                    mesh = extrude_polygon(polygon, height=floor_height)
                    meshes.append(mesh)
                else:
                    logger.warning("Invalid floor polygon detected, skipping")

        # Process ceiling if enabled
        if ceiling:
            logger.info("Processing ceiling")
            contours = measure.find_contours(floor_ceiling_data, level=0.1)

            for contour in contours:
                polygon = Polygon(contour)
                if polygon.is_valid:
                    # Extrude the ceiling and shift it vertically
                    ceiling_mesh = extrude_polygon(polygon, height=ceiling_height)
                    ceiling_mesh.apply_translation([0, 0, wall_height])  # Shift to ceiling height
                    meshes.append(ceiling_mesh)
                else:
                    logger.warning("Invalid ceiling polygon detected, skipping")

        # Combine all meshes into a single mesh
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
    # Load the wall and floor-ceiling data
    wall_data = np.load('walls.npy')
    floor_ceiling_data = np.load('floor-ceiling.npy')
    
    # Set booleans for the structures to be created
    walls = False
    floor = True
    ceiling = True
    
    # Run the extrusion and export process
    image_data_to_glb(
        wall_data=wall_data,
        floor_ceiling_data=floor_ceiling_data,
        output_filename='test-numpy-6.glb',
        wall_height=50.0,
        floor_height=0.5,
        ceiling_height=0.5,
        buffer_distance=0.1,
        walls=walls,
        floor=floor,
        ceiling=ceiling
    )