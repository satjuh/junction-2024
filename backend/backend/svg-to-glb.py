import logging
import trimesh
from shapely.geometry import Polygon, LineString
from trimesh.creation import extrude_polygon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def svg_to_glb(
    svg_filename,
    output_filename,
    height=5.0,
    buffer_distance=0.1
):
    """
    Extrude paths from an SVG file and export as a GLB file.

    Parameters:
        svg_filename (str): The path to the input SVG file.
        output_filename (str): The path for the output GLB file.
        height (float): The extrusion height.
        buffer_distance (float): The buffer distance for lines.
    """
    try:
        # Load the SVG file as a Path2D object
        logger.info(f"Loading SVG file: {svg_filename}")
        svg_path = trimesh.load_path(svg_filename)

        # Initialize a list to hold the extruded meshes
        meshes = []

        # Iterate over each path in the SVG
        for entity in svg_path.entities:
            # Get the points defining the entity
            indices = entity.points
            points = svg_path.vertices[indices]

            # Check if the entity is a closed loop (Polygon) or a line (LineString)
            if entity.closed:
                logger.debug("Processing closed entity as Polygon")
                # Create a Shapely Polygon
                polygon = Polygon(points)
                # Extrude the polygon up by the specified height
                mesh = extrude_polygon(polygon, height=height)
                meshes.append(mesh)
            else:
                logger.debug("Processing open entity as LineString")
                # Create a Shapely LineString
                line = LineString(points)
                # Buffer the line to create a thin polygon for extrusion
                buffered_line = line.buffer(buffer_distance)
                # Extrude the buffered line
                mesh = extrude_polygon(buffered_line, height=height)
                meshes.append(mesh)

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
    svg_to_glb(
        svg_filename='test.svg',
        output_filename='test.glb',
        height=5.0,
        buffer_distance=0.1
    )