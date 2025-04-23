# Project

Projects are containers for everything related to running and analyzing a simulation, including geometries, meshes, and solutions. This is where you should start when using the API.

The sections below describe some of the most common operations you can perform on a `Project`. The full reference for the class can be found [here](#luminarycloud.Project).

## Creating a Project

When you create a project, you must specify a name. The name does not need to be unique. You can also specify a description, but this is optional. See [`create_project()`](#luminarycloud.create_project) for syntax and parameters.

After you create a project, you can update the name and/or the description, create a simulation, upload a mesh, and more.

To see an example using the SDK, take a look at the corresponding section in our [end-to-end tutorial](../getting-started/first-simulation.md#creating-a-project).

## Creating a Mesh

Once you've created a project, you can create a mesh. You can either upload a mesh file or generate a mesh yourself from a [`Geometry`](./geometry.md).

See the [`Mesh`](./mesh.md) section for more information.
