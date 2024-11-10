# Flippity BIM Bop

**Introduction**  
*Flippity BIM Bop* generates 3D models from building floor blueprints, providing a practical and user-friendly way to visualize and plan for equipment placement, such as elevators. This tool is designed to bridge the gap for buildings lacking digital BIMs, enabling faster, smarter planning and modernization.

**Impact on the World**  
This project empowers end users to easily create 3D models of buildings, helping streamline processes like quoting, maintenance planning, and people flow simulation. By simplifying 3D model generation, *Flippity BIM Bop* aims to drive more efficient workflows in industries such as real estate, construction, and urban planning.

**How It Works**

- **Frontend**: The frontend is built with SvelteKit (version 5) and three.js. TypeScript and styled with Tailwind. It provides:
  - A viewer for existing models.
  - Tools to add and adjust elevator placements on different floors, including the ability to move them.
  - Floor-by-floor viewing capability.
  - An interface to upload new floorplan images and receive a .glb format 3D model.
  - VR viewing, allowing users to navigate inside the model and adjust elevator placements.

- **Backend**: The backend processes floorplans by:
  - Reading blueprints layer-by-layer.
  - Simplifying each floor using edge and contour detection algorithms to create 2D masks.
  - Scaling and extruding these masks to appropriate dimensions, creating a full 3D model.
  - Returning the generated .glb model to the frontend, which assembles it for visualization.

In practice, the backend simplifies blueprints into 2D layers, scales them for real-world accuracy, and extrudes them into a cohesive 3D model for interactive use.


![Sequence Diagram](https://github.com/satjuh/junction-2024/blob/docs/docs/sequence.png?raw=true)

---

### Future Plans

- **Automatic Scale Detection**: Enhance models by automatically detecting scale from common blueprint fixtures (e.g., stoves).
- **Texture Mapping**: Apply textures from street maps to create realistic models.
- **Sensor Fusion**: Integrate data from LIDAR and other sensors to add detail and accuracy.
- **Data Input Flexibility**: Support diverse input sources, such as satellite imagery.
- **Cost and Usage Simulation**: Implement cost analysis and simulate elevator usage based on historical data.
