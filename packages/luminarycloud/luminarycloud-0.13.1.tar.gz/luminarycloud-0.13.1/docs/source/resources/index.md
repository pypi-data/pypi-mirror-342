# Core Resources

The Luminary Cloud API consists of operations for creating, reading, and
modifying objects in the Luminary Cloud platform. We call these objects "resources."
The core resources are listed below.

```{eval-rst}
.. toctree::
  :glob:
  :maxdepth: 1

  project
  geometry
  mesh
  simulation
  solution
```

These operations are available through the SDK as methods related to the
corresponding resource classes. For example, the `Simulation` resource has
these basic "CRUD" methods:

- Create: [`create_simulation() -> Simulation`](#luminarycloud.Project.create_simulation)
- Read: [`get_simulation() -> Simulation`](#luminarycloud.get_simulation)
- Update: [`Simulation:update()`](#luminarycloud.Simulation.update)
- Delete: [`Simulation:delete()`](#luminarycloud.Simulation.delete)

Some resources may support slightly more advanced or more specific operations
than these generic CRUD methods. For example, `Geometry` has a
[`Geometry:add_farfield()`](#luminarycloud.Geometry.add_farfield) method that
adds a farfield volume to the geometry.

## Resource IDs

Each resource you create in the API will have a globally unique ID. The IDs are
strings of the format: `<prefix>-<unique id>`, where `prefix` varies based on the
resource type.  Some example resource IDs are shown in the table below.

| Resource Type | Example ID                                           |
| ------------- | ---------------------------------------------------- |
| Project       | p-dyd4voqsbm62m4nt6ychnrib4e01x5nq7k6tzn2f64cillg14b |
| Mesh          | mesh-0d570a5a-169f-4c6f-b851-6283bcbf0e37            |
| Simulation    | sim-a8f0b812-9a5e-4fe7-ab72-4787476cd662             |

There are two primary ways to access resources you have previously created:
`get` APIs and `list` APIs.

If you already have the ID of the resource you'd like to access, you can simply
use the `get` API corresponding to the resource type, for example:

```py
import luminarycloud as lc

my_project = lc.get_project("p-dyd4voqsbm62m4nt6ychnrib4e01x5nq7k6tzn2f64cillg14b")
my_sim = lc.get_simulation("sim-a8f0b812-9a5e-4fe7-ab72-4787476cd662")
```

If you don't have a resource ID, you can use `list` APIs to find what you need:

```py
import luminarycloud as lc

all_projects = lc.list_projects()
for p in projects:
  # print out the project info to help us find the one we want
  print(p.id, p.name, p.description)

# let's pick the first project
my_project = all_projects[0]

# list all meshes that are available in this project
meshes_in_my_project = my_project.list_meshes()
```

<!--
## Other Resources

TODO: add details about other resources like Operation and Upload once they've
been released in the API
-->
