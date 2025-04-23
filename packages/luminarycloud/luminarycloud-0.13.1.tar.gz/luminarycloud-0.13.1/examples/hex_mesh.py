"""
This example demonstrates how to create a hex-dominant mesh.
Note: it only works with STL files.
"""

import luminarycloud as lc
import luminarycloud._proto.base.base_pb2 as basepb
import luminarycloud._proto.cad.shape_pb2 as shapepb
from luminarycloud._proto.hexmesh import hexmesh_pb2 as hexmeshpb

# <internal>
# This points the client to main (Internal use only)
# Please keep the <internal> tags because assistant will use it to filter out the internal code.
lc.set_default_client(
    lc.Client(
        target="apis,aom.int.luminarycloud.com",
        domain="luminarycloud-dev.us.auth0.com",
        client_id="mbM8OSEk5ShoU5iKfzUxSinKluPlxGQ9",
        audience="https://api-dev.luminarycloud.com",
    )
)
# </internal>

project = lc.create_project(name="Test")
print(f"Project ID: {project.id}")
params = hexmeshpb.HexMeshSpec(
    name="test hex mesh",
    background_mesh=hexmeshpb.BackgroundMesh(
        n_x=20,
        n_y=20,
        n_z=20,
        cube=shapepb.Cube(
            min=basepb.Vector3(x=1, y=1, z=1),
            max=basepb.Vector3(x=10, y=10, z=10),
        ),
    ),
    refinement_regions=[
        hexmeshpb.RefinementRegionParams(
            name="box",
            id="box",
            cube=shapepb.Cube(
                min=basepb.Vector3(x=1, y=1, z=1),
                max=basepb.Vector3(x=2, y=2, z=2),
            ),
            refinement_spec=hexmeshpb.RefinementSpec(
                refinement_levels=[hexmeshpb.RefinementLevel(distance=0, level=2)]
            ),
        )
    ],
    shm_config=hexmeshpb.OpenfoamMeshShmConfig(
        feature_edges=hexmeshpb.FeatureEdges(
            feature_angle=150,
            refinement_spec=hexmeshpb.RefinementSpec(
                refinement_levels=[hexmeshpb.RefinementLevel(distance=0, level=2)]
            ),
        ),
        castellated_mesh_controls=hexmeshpb.CastellatedMeshControls(
            location_in_mesh=basepb.Vector3(x=1, y=1, z=1),
            refinement_surfaces=hexmeshpb.RefinementSurfaces(
                input_file_refinement_min_level=3, input_file_refinement_max_level=3
            ),
        ),
    ),
)
mesh = project.create_hex_mesh(
    file_path="/sdk/testdata/cube.stl",
    params=params,
)
print(f"Mesh ID: {mesh.id}")
mesh.wait()
print("Mesh is ready")
