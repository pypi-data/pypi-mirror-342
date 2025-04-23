# Geometry

A `Geometry` represents a 3D CAD model. You can import a geometry by uploading a CAD file, and you can modify existing geometries using boolean operations and transformations. This is useful when you want to run a large number of simulations with different geometric variants.

The sections below describe some of the most common operations you can perform on a `Geometry`. The full reference for the class can be found [here](#luminarycloud.Geometry).

## Creating a Geometry

To create a geometry, you must first create a project to contain it. See [Creating a Project](./project.md#creating-a-project) for more info.

Once you've created a project, you can create a geometry by uploading a CAD file.

```python3
my_geometry = project.upload_geometry(
  "path/to/cad/file.stp",
  scaling=1.0,
  wait=True,
)
```

The only required parameter is the path to the CAD file.

The `scaling` parameter is optional and defaults to 1.0. If your geometry is in a different unit system, you can use this parameter to scale it to the desired unit system.

The `wait` parameter is also optional and defaults to `False`. If `wait` is `True`, the method will block until the geometry is fully uploaded and ready to use. It's recommended to set this to `True` when you're first getting started with the SDK, but you can set it to `False` to achieve higher throughput when setting up a large number of simulations in parallel.

See [`upload_geometry()`](#luminarycloud.project.Project.upload_geometry) for the full syntax and parameters.

## Modifying a Geometry

Once you've created a geometry, you can modify it.

The recommended way to do this is by using `select_volumes()`. Once you've selected the volumes you want, you can apply the desired set of boolean operations and transformations on them. If an operation creates or destroys a volume, the selection is updated to reflect that.

For example, suppose you have a geometry that contains a model of a car, and you want to convert this into a wind tunnel volume that surrounds the car.

To start, we can select all the volumes in the car, then shrink wrap them into a single volume.

```python3
_, all_volumes = my_geometry.list_entities()

car = my_geometry.select_volumes(all_volumes)
car.shrinkwrap(min_resolution=0.01, max_resolution=0.04)
```

The `shrinkwrap()` operation replaces the car volumes with a single volume that is the shrink wrapped version of the car, which is guaranteed to be watertight. The volume selection is updated so that instead of containing the car volumes, it now contains the shrink wrapped volume.

Next, we can add a wind tunnel volume around the car.

```python3
windtunnel = geometry.select_volumes([])
windtunnel.import_cad(windtunnel_filepath)
```

Here, we've started with an empty selection, then imported a second CAD file to create a wind tunnel volume. The selection is updated to include the newly created wind tunnel volume.

Finally, we can subtract the car volume from the wind tunnel volume, and tag the resulting volume as "windtunnel". Notice that we can use `car.volumes()` to get the shrink wrapped car volume from before.

```python3
windtunnel.subtract(car.volumes())
windtunnel.tag("windtunnel")
```

You can find the full reference of supported operations [`here`](#luminarycloud.volume_selection.VolumeSelection).
