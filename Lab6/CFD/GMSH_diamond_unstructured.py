import gmsh
import sys

gmsh.initialize()
gmsh.model.add("DiamondAirfoil_Unstructured")

# ---------------------------------------------------------
# Parameters
# ---------------------------------------------------------
chord = 1.0
tc_ratio = 0.04
max_thickness = chord * tc_ratio

num_nodes_airfoil_edge = 200  # Nodes per airfoil edge
num_nodes_farfield_arc = 100  # Nodes per farfield quarter-arc (4 * 100 roughly = 400 nodes total)

farfield_radius = 80   
cx, cy = chord / 2.0, 0.0

# ---------------------------------------------------------
# 1. Create Geometry Points (Diamond Airfoil)
# ---------------------------------------------------------
# Diamond profile has 4 vertices
p_le  = gmsh.model.geo.addPoint(0.0, 0.0, 0)
p_top = gmsh.model.geo.addPoint(0.5, max_thickness / 2.0, 0)
p_te  = gmsh.model.geo.addPoint(1.0, 0.0, 0)
p_bot = gmsh.model.geo.addPoint(0.5, -max_thickness / 2.0, 0)

# ---------------------------------------------------------
# 2. Create Geometry Points (Farfield Boundary)
# ---------------------------------------------------------
p_center = gmsh.model.geo.addPoint(cx, cy, 0)
p_fe = gmsh.model.geo.addPoint(cx + farfield_radius, cy, 0) # Far East
p_fn = gmsh.model.geo.addPoint(cx, cy + farfield_radius, 0) # Far North
p_fw = gmsh.model.geo.addPoint(cx - farfield_radius, cy, 0) # Far West
p_fs = gmsh.model.geo.addPoint(cx, cy - farfield_radius, 0) # Far South

# ---------------------------------------------------------
# 3. Create Curves (Airfoil Edges)
# ---------------------------------------------------------
# Traced in a Clockwise (CW) direction for the inner hole
l_af_tl = gmsh.model.geo.addLine(p_le, p_top) # Top-Left edge
l_af_tr = gmsh.model.geo.addLine(p_top, p_te) # Top-Right edge
l_af_br = gmsh.model.geo.addLine(p_te, p_bot) # Bottom-Right edge
l_af_bl = gmsh.model.geo.addLine(p_bot, p_le) # Bottom-Left edge

# ---------------------------------------------------------
# 4. Create Curves (Farfield Quarter Arcs)
# ---------------------------------------------------------
# Traced in a Counter-Clockwise (CCW) direction for the outer boundary
arc_ne = gmsh.model.geo.addCircleArc(p_fe, p_center, p_fn)
arc_nw = gmsh.model.geo.addCircleArc(p_fn, p_center, p_fw)
arc_sw = gmsh.model.geo.addCircleArc(p_fw, p_center, p_fs)
arc_se = gmsh.model.geo.addCircleArc(p_fs, p_center, p_fe)

# ---------------------------------------------------------
# 5. Create Curve Loops and Surface
# ---------------------------------------------------------
cl_airfoil = gmsh.model.geo.addCurveLoop([l_af_tl, l_af_tr, l_af_br, l_af_bl])
cl_farfield = gmsh.model.geo.addCurveLoop([arc_ne, arc_nw, arc_sw, arc_se])

# The surface is bounded by the outer farfield loop, minus the inner airfoil hole
surf_domain = gmsh.model.geo.addPlaneSurface([cl_farfield, cl_airfoil])

# --- SYNCHRONIZE BEFORE APPLYING MESH CONSTRAINTS ---
gmsh.model.geo.synchronize()

# ---------------------------------------------------------
# 6. Define Mesh Node Constraints on Boundaries
# ---------------------------------------------------------
# Force 100 nodes onto each edge of the airfoil
for line in[l_af_tl, l_af_tr, l_af_br, l_af_bl]:
    gmsh.model.mesh.setTransfiniteCurve(line, num_nodes_airfoil_edge)

# Force 100 nodes onto each quarter-circle of the farfield (~400 total)
for arc in[arc_ne, arc_nw, arc_sw, arc_se]:
    gmsh.model.mesh.setTransfiniteCurve(arc, num_nodes_farfield_arc)

# Note: We purposely DO NOT use setTransfiniteSurface() or setRecombine().
# This allows the interior to be meshed freely with unstructured triangles.

# ---------------------------------------------------------
# 7. Physical Groups for the Solver
# ---------------------------------------------------------
gmsh.model.addPhysicalGroup(1,[l_af_tl, l_af_tr, l_af_br, l_af_bl], name="airfoil")
gmsh.model.addPhysicalGroup(1,[arc_ne, arc_nw, arc_sw, arc_se], name="farfield")
gmsh.model.addPhysicalGroup(2, [surf_domain], name="fluid_domain")

# ---------------------------------------------------------
# 8. Generate & Visualize
# ---------------------------------------------------------
# Use Frontal-Delaunay algorithm (good for smooth size transitions in 2D)
gmsh.option.setNumber("Mesh.Algorithm", 6) 
gmsh.option.setNumber("Mesh.Smoothing", 100)
gmsh.option.setNumber("Geometry.Points", 0)

gmsh.model.mesh.generate(2)

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()