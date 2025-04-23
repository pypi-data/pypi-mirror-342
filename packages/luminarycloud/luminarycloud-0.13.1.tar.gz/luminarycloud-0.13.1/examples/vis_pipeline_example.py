"""
This example demonstrates how to use the visualization pipeline to render a scene.
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

geom = proj.list_geometries()[0]
far_field_tag = geom.list_tags()[0]
print(far_field_tag)

simulation = proj.list_simulations()[0]
solution = simulation.list_solutions()[-1]

# Create a scene around the solution
scene = vis.Scene(solution)
print(scene.surface_ids())
scene.tag_visibility(far_field_tag.id, False)

# Add a slice
slice = vis.Slice("x-slice")
slice.plane.normal = [1, 0, 0]
slice.plane.origin = [4.08, 0, 0.52]

# Project the vectors onto the slice plane for downstream filters. This
# allows us to visualize the flow projected onto the slice plane.
slice.project_vectors = True
slice.display_attrs.field.quantity = vis.VisQuantity.VELOCITY
slice.display_attrs.field.component = vis.FieldComponent.MAGNITUDE
slice.display_attrs.visible = False
scene.add_filter(slice)

# Clip the volume so we don't see volume all the way out to the
# far field
clip = vis.BoxClip("clip")
clip.box.center = [3.55, 0.09, 0.52]
clip.box.lengths = [2, 12, 4]
clip.display_attrs.visible = False
clip.set_parent(slice)
scene.add_filter(clip)

# Add some vector glyphs on the slice
glyph = vis.FixedSizeVectorGlyphs("glyphs")
glyph.field.quantity = vis.VisQuantity.VELOCITY
glyph.sampling_rate = 100
glyph.size = 1.0
glyph.display_attrs.representation = vis.Representation.SURFACE
glyph.display_attrs.field.quantity = vis.VisQuantity.PRESSURE
glyph.set_parent(clip)
scene.add_filter(glyph)

# Setup the camera
camera = vis.DirectionalCamera()
camera.direction = vis.CameraDirection.X_NEGATIVE
scene.add_camera(camera)

# Setup global display attrs
scene.global_display_attrs.representation = vis.Representation.SURFACE
scene.global_display_attrs.visible = True

# The name and desciption are entered into the db.
render_ = scene.render_images(name="piper image", description="fun image of the piper.")

# The name and desciption are entered into the db.
render_output = scene.render_images(name="piper image", description="fun image of the piper.")
status = render_output.wait()
if status == RenderStatusType.COMPLETED:
    render_output.save_images("piper")
else:
    print("Rendering failed ", status)
