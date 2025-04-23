# Solution

A Solution represents the solution data for a specific iteration of a [`Simulation`](#luminarycloud.Simulation). Both surface and volume data are available for download.

## Downloading Surface Solutions

Surface solutions are returned as a gzipped tarball containing .vtu files. This is the case for both steady state and transient simulations.

See
[`download_surface_data`](#luminarycloud.Solution.download_surface_data)
for syntax and parameters.

## Downloading Volume Solutions

Volume solutions are returned for steady state simulations as a gzipped tarball containing .vtu files. You cannot download the volume solution from transient simulations.

See
[`download_volume_data`](#luminarycloud.Solution.download_volume_data)
for syntax and parameters.

:::{Tip}
Surface and volume solutions can be used with Paraview for visualization and
additional post-processing. See the [official Paraview
documentation](https://www.paraview.org/) for more information.
:::
