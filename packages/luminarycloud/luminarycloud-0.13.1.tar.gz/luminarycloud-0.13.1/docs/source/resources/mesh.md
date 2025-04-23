# Mesh

A `Mesh` represents the computational mesh. This could be an uploaded mesh file, a mesh generated from a [`Geometry`](./geometry.md), or a mesh adapted from a previous simulation. No matter the origin, you will need a mesh to run a [`Simulation`](./simulation.md).

## Uploading a Mesh

Once you've created a [`Project`](./project.md), you can upload a mesh file. Supported file formats are listed on the [learning site](https://docs.luminarycloud.com/en/articles/9275233-upload-a-mesh). See [`upload_mesh()`](#luminarycloud.Project.upload_mesh) for syntax and parameters.

You can use uploaded meshes to run simulations in the same project.

To see an example using the SDK, take a look at the corresponding section in our [end-to-end tutorial](../getting-started/first-simulation.md#upload-a-mesh).

## Generating a Mesh

To generate a mesh, you will need a [`Project`](./project.md) containing a [`Geometry`](./geometry.md). Click on the links for more info.

To set up the parameters for the mesh generation, you will need to create a [`MeshGenerationParams`](#luminarycloud.meshing.MeshGenerationParams) object.

```python3
from luminarycloud.meshing import MeshGenerationParams
from luminarycloud.meshing.sizing_strategy import MaxCount

mesh_generation_params = MeshGenerationParams(
    geometry_id=geometry.id,
    sizing_strategy=MaxCount(1000000),
)
```

At minimum, you will need to specify the two parameters set in the example above. The `geometry_id` parameter is the ID of the geometry to generate a mesh for. The `sizing_strategy` parameter can take one of three values: [`MinimalCount`](#luminarycloud.meshing.sizing_strategy.MinimalCount), [`TargetCount`](#luminarycloud.meshing.sizing_strategy.TargetCount), or [`MaxCount`](#luminarycloud.meshing.sizing_strategy.MaxCount). Click on the links for the full descriptions of each strategy.

Without specifying any additional parameters, the mesh generation will mesh all volumes in the geometry using default values. See [`MeshGenerationParams`](#luminarycloud.meshing.MeshGenerationParams) to learn more about the other parameters you can set.

Once you've set the parameters, you can generate a mesh by calling [`create_or_get_mesh()`](#luminarycloud.Project.create_or_get_mesh) with the mesh parameters on the project.

```python3
mesh = project.create_or_get_mesh(mesh_generation_params)
```

Before you can use the mesh in a simulation, you will need to wait for the mesh to finish processing. You can do this by calling [`wait()`](#luminarycloud.Mesh.wait) on the mesh, which will block the script from proceeding until the meshing is complete.

```python3
mesh.wait()
```
