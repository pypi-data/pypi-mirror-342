"""
This example demonstrates how to use the wrap feature when creating a mesh.
This uses an approximation of the surfaces to mesh.
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

if GEOMETRY_ID:
    geometry = lc.get_geometry(GEOMETRY_ID)
    project = geometry.project()
else:
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

    print("Loading geometry to setup...")
    project.load_geometry_to_setup(geometry)

tags = geometry.list_tags()
farfield_surfaces = next(t.surfaces for t in tags if t.name == "Farfield")
model_surfaces = next(t.surfaces for t in tags if t.name != "Farfield")

print("Creating mesh...")
start = time()
mesh = project.create_or_get_mesh(
    lc.meshing.MeshGenerationParams(
        geometry_id=geometry.id,
        # minimal mode is not ignored, and uses a relatively small estimate for the global min size.
        # This results in a likely larger than desired mesh size.
        sizing_strategy=lc.meshing.sizing_strategy.MaxCount(0),  # should be ignored
        min_size=0.1,
        max_size=0.5,
        model_meshing_params=[
            lc.meshing.ModelMeshingParams(
                surfaces=model_surfaces,
                max_size=0.2,
                curvature=8,
            )
        ],
        boundary_layer_params=[
            lc.meshing.BoundaryLayerParams(
                surfaces=model_surfaces,
                n_layers=10,
                initial_size=1e-3,
                growth_rate=1.2,
            )
        ],
        use_wrap=True,
    ),
    name="wrap",
)
print(f"Mesh created in {time() - start} seconds")
print(f"Mesh created: {mesh.id}")
