import logging
import numpy as np
import cv2
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
    ceiling=True,
    scaling_factor=1.0,
    scaling_method="contour",  # 'contour' or 'resize'
    contour_filter=0.0,
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
        scaling_factor (float): Factor to scale pixel coordinates to meters.
        scaling_method (str): Method to apply scaling ('contour' or 'resize').
        contour_filter (float): Minimum contour area to keep (in meters squared).
    """
    try:
        # Apply scaling using the 'resize' method if selected
        if scaling_method == "resize":
            logger.info("Resizing image data using cv2")
            # Calculate the new dimensions
            new_size = (
                int(wall_data.shape[1] * scaling_factor),
                int(wall_data.shape[0] * scaling_factor),
            )
            # Resize wall_data and floor_ceiling_data
            wall_data = cv2.resize(wall_data, new_size, interpolation=cv2.INTER_NEAREST)
            floor_ceiling_data = cv2.resize(
                floor_ceiling_data, new_size, interpolation=cv2.INTER_NEAREST
            )
            # Set scaling_factor to 1 since we've resized the images
            scaling_factor = 1.0
            wall_height *= 10
            contour_filter *= 100
            logger.info(f"Image data resized to {new_size}")
        elif scaling_method != "contour":
            logger.warning(
                "Invalid scaling_method provided. Using default 'contour' method."
            )

        meshes = []

        # Function to process contours and apply the contour filter
        def process_contours(data, height, shift=0.0):
            contours = measure.find_contours(data, level=0.1)
            for contour in contours:
                if scaling_method == "contour":
                    scaled_contour = contour * scaling_factor
                else:
                    scaled_contour = contour

                polygon = Polygon(scaled_contour)
                if polygon.is_valid:
                    # Filter out small contours based on area
                    if polygon.area < contour_filter:
                        logger.info(
                            f"Skipping small contour with area {polygon.area:.2f} m²"
                        )
                        continue

                    # Optionally apply buffer to the polygon
                    if buffer_distance > 0:
                        polygon = polygon.buffer(buffer_distance)

                    # Extrude and optionally translate the mesh
                    mesh = extrude_polygon(polygon, height=height)
                    if shift > 0:
                        mesh.apply_translation(
                            [0, 0, shift]
                        )  # Shift mesh vertically if needed
                    meshes.append(mesh)
                else:
                    logger.warning("Invalid polygon detected, skipping")

        # Process walls if enabled
        if walls:
            logger.info("Processing walls")
            edges = filters.sobel(wall_data)
            process_contours(edges, wall_height)

        # Process floor if enabled
        if floor:
            logger.info("Processing floor")
            process_contours(floor_ceiling_data, floor_height)

        # Process ceiling if enabled
        if ceiling:
            logger.info("Processing ceiling")
            process_contours(floor_ceiling_data, ceiling_height, shift=wall_height)

        # Combine all meshes into a single mesh
        if meshes:
            logger.info("Combining meshes")
            combined_mesh = trimesh.util.concatenate(meshes)

            # Export the combined mesh to a GLB file
            logger.info(f"Exporting combined mesh to: {output_filename}")
            combined_mesh.export(output_filename)

            logger.info("Extrusion and export completed successfully")
        else:
            logger.warning(
                "No meshes were created. Check your input data and parameters."
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    # Load the wall and floor-ceiling data
    wall_data = np.load("output.png.npy")
    floor_ceiling_data = np.load("floor-ceiling.npy")

    # Set booleans for the structures to be created
    walls = True
    floor = False
    ceiling = False

    # Calculate scaling factor based on provided equivalence
    pixel_to_meter = 0.07  # 14 pixels correspond to 0.1 meters

    # Choose scaling method: 'contour' or 'resize'
    scaling_method = "resize"  # or 'resize'

    # Run the extrusion and export process
    image_data_to_glb(
        wall_data=wall_data,
        floor_ceiling_data=floor_ceiling_data,
        output_filename="test-13.glb",
        wall_height=2.5,  # Set realistic wall height in meters
        floor_height=0.1,
        ceiling_height=0.1,
        buffer_distance=0.1,
        walls=walls,
        floor=floor,
        ceiling=ceiling,
        scaling_factor=pixel_to_meter,  # Pass the scaling factor
        scaling_method=scaling_method,  # Choose the scaling method
        contour_filter=1.0,  # Filter out small contours
    )
