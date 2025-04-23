"""
This example demonstrates how to use the visualization pipeline for a completed simulation.
"""

import luminarycloud as lc
import luminarycloud.vis as vis
from luminarycloud.vis import RenderStatusType

# <internal>
# This points the client to main (Internal use only)
# Please keep the <internal> tags because assistant will use it to filter out the internal code.
lc.set_default_client(
    lc.Client(
        target="apis.main.int.luminarycloud.com",
        domain="luminarycloud-dev.us.auth0.com",
        client_id="mbM8OSEk5ShoU5iKfzUxSinKluPlxGQ9",
        audience="https://api-dev.luminarycloud.com",
    )
)
# </internal>

# Find the piper project
proj = None
for project in lc.list_projects():
    if "Piper Cherokee SDK" in project.name:
        proj = project
        break
if not proj:
    print("Can't find the project.")
    exit(1)
print(proj)

simulation = proj.list_simulations()[0]
solution = simulation.list_solutions()[-1]
print(solution)
print(vis.list_quantities(solution))
# Create a scene around the solution
scene = vis.Scene(solution)
print(scene.surface_ids())

camera = vis.LookAtCamera()
camera.look_at = [3.85, -0.5, 0]
camera.position = [3.85, -10.5, 0]
camera.up = [0, 0, 1]
scene.add_camera(camera)

# Setup global display attrs
scene.global_display_attrs.field.component = vis.FieldComponent.X
scene.global_display_attrs.field.quantity = vis.VisQuantity.PRESSURE
scene.global_display_attrs.representation = vis.Representation.SURFACE
scene.global_display_attrs.visible = True
scene.hide_far_field()
# Hide the triad in this scene
scene.triad_visible = False


rake = vis.RakeStreamlines("z_curves")
rake.n_streamlines = 10
rake.max_length = 10
rake.start = [1.89, -3.3, -0.88]
rake.end = [1.89, -3.3, 0.52]
rake.field.quantity = vis.VisQuantity.VELOCITY
rake.display_attrs.field.quantity = vis.VisQuantity.VELOCITY
scene.add_filter(rake)

# Add a slice
slice = vis.Slice("x-slice")
slice.plane.normal = [0, 1, 0]
slice.plane.origin = [3.55, 0, 0.52]
slice.display_attrs.field.quantity = vis.VisQuantity.VELOCITY
slice.display_attrs.field.component = vis.FieldComponent.MAGNITUDE
scene.add_filter(slice)

# Add some vector glyphs
glyph = vis.FixedSizeVectorGlyphs("glyphs")
glyph.field.quantity = vis.VisQuantity.VELOCITY
glyph.sampling_rate = 5000
glyph.size = 0.2
glyph.display_attrs.representation = vis.Representation.SURFACE
glyph.display_attrs.field.quantity = vis.VisQuantity.VELOCITY
glyph.display_attrs.field.component = vis.FieldComponent.MAGNITUDE
scene.add_filter(glyph)

# Add a threshold
threshold = vis.Threshold("threshold")
threshold.field.quantity = vis.VisQuantity.ABSOLUTE_PRESSURE
threshold.min_value = 70617
threshold.max_value = 72652
threshold.display_attrs.representation = vis.Representation.SURFACE
scene.add_filter(threshold)

# Add a contour
isosurface = vis.Isosurface("contour")
isosurface.field.quantity = vis.VisQuantity.ABSOLUTE_PRESSURE
isosurface.isovalues.append(70000)
isosurface.display_attrs.representation = vis.Representation.SURFACE
isosurface.display_attrs.field.quantity = vis.VisQuantity.NONE
scene.add_filter(isosurface)

cmap = vis.ColorMap()
cmap.preset = vis.ColorMapPreset.WAVE
cmap.field = slice.display_attrs.field
cmap.data_range.min_value = 38.0
cmap.data_range.max_value = 82.0
scene.add_color_map(cmap)

# The name and desciption are entered into the db.
render_output = scene.render_images(name="piper image", description="fun image of the piper.")
status = render_output.wait()
if status == RenderStatusType.COMPLETED:
    render_output.save_images("piper")
else:
    print("Rendering failed ", status)
