# Simulation

When you create a Simulation with the API, you can use it to retrieve global
residuals, solutions, and surface outputs. This is useful for analyzing the
results and creating residual plots.

## Creating and Running Simulations

To create and run a simulation, you need a mesh and a simulation template.

See the [`Mesh`](./mesh.md) section for more information on how to create a mesh.

The simplest way to create a simulation template is to use a settings file. You can download settings files from the Luminary Cloud web app. See the [learning site](https://docs.luminarycloud.com/en/articles/9363424-download-a-settings-file) for full instructions.

Once you have a settings file, you can create the template with the following code:

```python3
simulation_template = project.create_simulation_template(
  "my_sim_template",
  params_json_path="path/to/settings_file.json",
)
```

Once you have a simulation template, you can create a simulation with the following code:

```python3
simulation = project.create_simulation(
  mesh.id,
  "my_simulation",
  simulation_template.id,
)
```

See [`create_simulation`](#luminarycloud.project.Project.create_simulation) for
syntax and parameters.

:::{Note}
You can't create a new simulation using the same mesh and simulation settings as
a previously created simulation in the same project. This would result in a
duplicate, so the API prevents it from being created. Create a new project
first, then create a simulation with the same files.
:::

For example code, see the [Run a
Simulation section of the getting started guide](../getting-started/first-simulation.md#run-a-simulation).

## Downloading Global Residuals

Global residuals are available for both steady state and transient simulations
in CSV format. The CSV contains the values for every available residual type.
You can then use the data to generate residual plots and view the convergence
history.

For a transient simulation, you can download residuals for the latest iteration
of each time step.

See
[`download_global_residuals`](#luminarycloud.simulation.Simulation.download_global_residuals)
for syntax and parameters.

For example code, see the [Global
Residuals section of the getting started guide](../getting-started/first-simulation.md#global-residuals).

## Downloading Surface Outputs

Surface outputs are returned for both steady state and transient simulations in
CSV format. For a transient simulation, you can download surface outputs for the
latest iteration of each time step.

See
[`download_surface_output`](#luminarycloud.simulation.Simulation.download_surface_output)
for syntax and parameters.

For example code, see the [Output
Quantities section of the getting started guide](../getting-started/first-simulation.md#output-quantities).

## Getting Available Solutions

Solution data isn't usually outputted at every iteration. You can retrieve the
full list of available solutions by calling
[`list_solutions`](#luminarycloud.simulation.Simulation.list_solutions). More
solutions may become available as the simulation runs to completion.

See [](./solution.md) for more info.
