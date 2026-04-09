import gmsh
import sys
from pathlib import Path

# 1. Initialize Gmsh
gmsh.initialize(sys.argv)
gmsh.model.add("Euler_Mesh_OneraM6")

# Set the OpenCASCADE target unit to Meters
gmsh.option.setString("Geometry.OCCTargetUnit", "M")

# 2. Import the STEP file
script_dir = Path(__file__).resolve().parent
step_file = script_dir / "AileM6_with_sharp_TE.stp"
step_file = "Z:\AE462\AE462-git\Lab7\CFD\AileM6_with_sharp_TE.stp"
# if not step_file.exists():
#     print(f"Error: STEP file not found at {step_file}")
#     sys.exit(1)
try:
    v = gmsh.model.occ.importShapes(step_file)
except Exception as e:
    print(f"Error loading {step_file}. Make sure the file exists.")
    sys.exit(1)

# 3. Create the Far-field Bounding Box
# Since the wing root is at x,y,z = 0,0,0 and the wing extends in +y
# we start the box exactly at y=0 to create the symmetry plane.
# addBox(x, y, z, dx, dy, dz)
x_min, x_max = -20.0, 20.0  # Upstream and downstream limits
y_min, y_max = 0.0, 20.0    # Symmetry plane at 0, spanwise limit at 10
z_min, z_max = -20.0, 20.0  # Bottom and top limits

box_tag = gmsh.model.occ.addBox(x_min, y_min, z_min, 
                                x_max - x_min, 
                                y_max - y_min, 
                                z_max - z_min)
box = [(3, box_tag)]

# 4. Perform the Boolean Difference
# Subtract the wing volume from the bounding box
out, out_map = gmsh.model.occ.cut(box, v, removeObject=True, removeTool=True)

# Synchronize the OpenCASCADE CAD representation with the Gmsh model
gmsh.model.occ.synchronize()

# 5. Define Physical Groups for the CFD Solver
# 5a. Fluid Domain
fluid_volume_tags = [tag for (dim, tag) in out]
gmsh.model.addPhysicalGroup(3, fluid_volume_tags, name="Fluid_Domain")

# 5b. Automatically detect and assign Boundary Conditions based on geometry bounds
surfaces = gmsh.model.getEntities(2)

sym_tags =[]
farfield_tags = []
wing_tags =[]

tol = 1e-5  # Geometric tolerance for identifying surfaces

for dim, tag in surfaces:
    # Get the bounding box of each surface: (xmin, ymin, zmin, xmax, ymax, zmax)
    bbox = gmsh.model.getBoundingBox(dim, tag)
    
    # Check if the surface is purely on the symmetry plane (y=0)
    if abs(bbox[1]) < tol and abs(bbox[4]) < tol:
        sym_tags.append(tag)
        
    # Check if the surface is one of the outer far-field boundaries
    elif (abs(bbox[0] - x_min) < tol and abs(bbox[3] - x_min) < tol) or \
         (abs(bbox[0] - x_max) < tol and abs(bbox[3] - x_max) < tol) or \
         (abs(bbox[1] - y_max) < tol and abs(bbox[4] - y_max) < tol) or \
         (abs(bbox[2] - z_min) < tol and abs(bbox[5] - z_min) < tol) or \
         (abs(bbox[2] - z_max) < tol and abs(bbox[5] - z_max) < tol):
        farfield_tags.append(tag)
        
    # If it's not the symmetry plane and not the far-field, it must be the wing!
    else:
        wing_tags.append(tag)

# Create the surface physical groups
if sym_tags:
    gmsh.model.addPhysicalGroup(2, sym_tags, name="Symmetry")
if farfield_tags:
    gmsh.model.addPhysicalGroup(2, farfield_tags, name="Farfield")
if wing_tags:
    gmsh.model.addPhysicalGroup(2, wing_tags, name="Wing_Surface")

wing_surfaces = [(2, tag) for tag in wing_tags]
wing_points = gmsh.model.getBoundary(wing_surfaces, recursive=True)

# Force a specific element size purely on the wing geometry
gmsh.model.mesh.setSize(wing_points, 0.0005) 

# 6. Mesh Settings (Tuning for an Euler Mesh)

# 1. Measure the distance from the imported wing surfaces
gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumbers(1, "SurfacesList", wing_tags)

# 2. Force the baseline mesh size based on that distance
gmsh.model.mesh.field.add("Threshold", 2)
gmsh.model.mesh.field.setNumber(2, "IField", 1)      # Link to the distance field
gmsh.model.mesh.field.setNumber(2, "SizeMin", 0.01)  # General element size ON the flat parts of the wing
gmsh.model.mesh.field.setNumber(2, "SizeMax", 1.0)   # Element size in the far-field
gmsh.model.mesh.field.setNumber(2, "DistMin", 0.05)  # Keep elements small up to 0.05m away
gmsh.model.mesh.field.setNumber(2, "DistMax", 2.0)   # Gradually grow them until 2.0m away

# 3. Apply the field as the background mesh
gmsh.model.mesh.field.setAsBackgroundMesh(2)

# 4. Enable Curvature Adaptation (Extra refinement for TE/LE)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 1)    # Enable curvature adaptation
gmsh.option.setNumber("Mesh.MinimumElementsPerTwoPi", 50) # High resolution for leading/trailing edges
gmsh.option.setNumber("Mesh.MeshSizeMin", 0.001)          # Must be very low so curvature can shrink elements at the TE!
gmsh.option.setNumber("Mesh.MeshSizeMax", 2.0)

# Turn off point sizing so corner points don't override your fields/curvature
gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)

# Optimize the 3D tetrahedral mesh
gmsh.option.setNumber("Mesh.Optimize", 1)
gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)

# 7. Generate the Mesh
print("Generating 3D Mesh...")
gmsh.model.mesh.generate(3)

# 8. Export the Mesh
output_mesh = "euler_mesh_OneraM6.msh" 
gmsh.write(output_mesh)
print(f"Mesh successfully written to {output_mesh}")

# 9. Launch the GUI to inspect the result
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

# Finalize Gmsh to clear memory
gmsh.finalize()