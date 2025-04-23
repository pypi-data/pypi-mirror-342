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

print(lc.list_projects())

project = None
for proj in lc.list_projects():
    if "motorbike" == proj.name:
        project = proj
        break

if not project:
    print("Project not found.")
    exit(0)

simulation = project.list_simulations()[0]
solution = simulation.list_solutions()[-1]
print(solution)

scene = vis.Scene(solution)
print(scene.surface_ids())
camera = vis.LookAtCamera()
camera.look_at = [0.67, -0.229, 0.714]
camera.position = [0.67, -3.229, 0.714]
print(camera)

camera.projection = vis.CameraProjection.PERSPECTIVE
scene.add_camera(camera)

scene.hide_far_field()

scene.global_display_attrs.field.component = vis.FieldComponent.X
scene.global_display_attrs.field.quantity = vis.VisQuantity.PRESSURE
scene.global_display_attrs.representation = vis.Representation.SURFACE
scene.global_display_attrs.visible = True

clip = vis.PlaneClip("cut the mesh in half")
clip.plane.normal = [0.0, 1.0, 0.0]
clip.plane.origin = [0.72, 0.008, 0.67]
clip.display_attrs.field.quantity = vis.VisQuantity.PRESSURE
clip.display_attrs.representation = vis.Representation.SURFACE_WITH_EDGES
print(clip)
scene.add_filter(clip)

render_outputs = scene.render_images(name="motorbike clip", description="A clip of the bike")

status = render_outputs.wait()
if status == RenderStatusType.COMPLETED:
    render_outputs.save_images("motorbike")
else:
    print("Image extract failed ", status)

renders = vis.list_renders(solution)
print(f"Num images {len(renders)}")
for render in renders:
    print(render)
