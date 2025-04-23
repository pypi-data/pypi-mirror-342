"""
This example demonstrates how to copy a geometry.
"""

import luminarycloud as lc
from sdk_util import get_client_for_env
from time import time

GEOMETRY_ID = None

# <internal>
# This points the client to main (Internal use only)
# Please keep the <internal> tags because assistant will use it to filter out the internal code.
lc.set_default_client(get_client_for_env(env_name="main"))
# </internal>

print("Creating project...")
project = lc.create_project(name="test2")
print(f"Project created: {project.id}")

print("Uploading geometry...")
geometry = project.create_geometry(
    cad_file_path="/sdk/testdata/box-sphere.sab",
    wait=True,
)
print(f"Geometry created: {geometry.id}")

print("Adding farfield...")
geometry.add_farfield(
    lc.params.geometry.Sphere(
        center=lc.types.Vector3(0, 0.5, 0),
        radius=10,
    )
)

print("Copying geometry...")
start_time = time()
copied_geometry = geometry.copy(name="copy")
print(f"Copied geometry: {copied_geometry.id}")
print(f"Time taken: {time() - start_time}")

print("Loading geometry to setup...")
project.load_geometry_to_setup(copied_geometry)
