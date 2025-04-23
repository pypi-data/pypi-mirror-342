# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Piper Cherokee
# Tutorial for CFD beginners or new-to-Luminary users walking through setting up an external aerodynamics simulation.
#
# Based on the UI tutorial: https://docs.luminarycloud.com/en/articles/10157837-piper-cherokee
#
# ## In this Tutorial
#
# The Piper PA-28 Cherokee is a small single-propeller aircraft intended for flight training and personal use. This tutorial will guide you through demonstrating and using Luminary Cloud's external aerodynamics solution.
#
# Follow the steps to upload a CAD file, generate a computational mesh, and analyze aerodynamic features.
#
# <img src="https://storage.googleapis.com/luminarycloud-learning/sample-projects/piper-cherokee/notebook-images/01-piper-cherokee-flow-vectors.png" width=600 />
#

# %% [markdown]
# ## Initialize the SDK
# A simple way to use the SDK is to create a .env file with your API key. Create a file named .env with one line similar to:
#
# ```LC_API_KEY=YOUR_API_KEY```
#
# You can generate an API key in the UI by navigating to My Account -> Profile in the left navigation menu under the heading "API Keys".

# %% [markdown]
# ### Set your API key in the environment
# The simplest way to use the SDK is to create an API key in the UI and assign it to the environment variable LC_API_KEY before running this notebook.
#
# Alternatively, you can use the python-dotenv python package (see https://pypi.org/project/python-dotenv/) and create a .env file with your API key specified as:
#
# `LC_API_KEY=MY_API_KEY`
#
# Note that if you do not set the API key, you will be asked to authenticate interactively when you make your first SDK request.

# %%
# Uncomment to use python-dotenv for loading LC_API_KEY into the environment from a .env file
# from dotenv import load_dotenv
# load_success=load_dotenv()

# %%
import luminarycloud as lc
import luminarycloud.vis as vis
from luminarycloud.geometry import Surface, Volume

import threading
import time
from datetime import datetime
from typing import Union, List, cast
from uuid import uuid4

import pandas as pd
import plotly.express as px
from PIL import Image

from IPython.display import display, update_display

# %% [markdown]
# ## Create a New Project
# To create a new project, use the lc.create_project(name=name, description=description) command.

# %%
project = lc.create_project(
    name="Piper Cherokee SDK Tutorial",
    description="This is a demo of the Luminary Cloud SDK with the Piper Cherokee",
)

# %% [markdown]
# You can now view the created project details.

# %%
{
    "id": project.id,
    "name": project.name,
    "description": project.description,
    "create_time": project.create_time.isoformat(),
    "update_time": project.update_time.isoformat(),
}

# %% [markdown]
# ## Upload the geometry (CAD)

# %% [markdown]
# Now upload the Piper Cherokee model to your project. To do this, use:
#
# `geometry = project.create_geometry(cad_file_path, name="CAD name", wait=True)`
#
# The `wait=True` parameter will wait until the geometry load is done before returning.
#

# %%
cad_file = "../testdata/piper-cherokee-tutorial-cad.x_t"

# %%
geometry = project.create_geometry(cad_file, name="Piper Cherokee Model", wait=True)

# %% [markdown]
# ## Identify farfield and plane surfaces
# Let's examine the geometry by getting its surfaces and volumes.

# %%
surfaces, volumes = geometry.list_entities()

# %% [markdown]
# We are interested in the surfaces representing the farfield and the plane.

# %% [markdown]
# ### Farfield surfaces
#
# In this model the farfield has an id of '0/bound/BC_14' so we will use this to distinguish the objects.

# %%
farfield_surface_id = "0/bound/BC_14"
farfield_surfaces = [surface for surface in surfaces if surface.id == farfield_surface_id]

# %% [markdown]
# ### Plane surfaces

# %%
plane_surfaces = [surface for surface in surfaces if surface.id != farfield_surface_id]

# %% [markdown]
# ### Visualize the imported geometry
#
# We can visualize the geometry before proceeding.
#
# <img src="https://storage.googleapis.com/luminarycloud-learning/sample-projects/piper-cherokee/notebook-images/02-piper-cherokee-geometry.png" width=600 />

# %%
scene = vis.Scene(geometry)
# Hide the far field surface
scene.surface_visibility(farfield_surface_id, False)
scene.global_display_attrs.representation = vis.Representation.SURFACE_WITH_EDGES

camera = vis.LookAtCamera(
    look_at=[3.5, 0.0, 0.52],
    position=[-9.1, 12.6, 13.1],
    projection=vis.CameraProjection.PERSPECTIVE,
    width=2048,
    height=1024,
)
scene.add_camera(camera)

image_extract = scene.render_images(
    name="piper geometry", description="Piper geometry with the far field hidden."
)
image_extract.wait()

# Extract the BytesIO object from the first tuple in the list
image_buffer, label = image_extract.download_images()[0]
image = Image.open(image_buffer)
display(image)

# %% [markdown]
# ## Create tags

# %% [markdown]
# ### Create the far field and plane tags
# Create tags for the far field and plane based on the identified surfaces.

# %%
geometry.create_tag("Far-field", farfield_surfaces)
geometry.create_tag("Plane", plane_surfaces)

# %% [markdown]
# ### Create the fluid volume tag
# Create a new tag "Fluid Volume" from the one volume in the geometry. It must be passed as a list.

# %%
fluid_volume = volumes[0]
geometry.create_tag("Fluid Volume", [fluid_volume])

# %% [markdown]
# ## Load the geometry to setup
#
# This step is needed only if we want to see the model in the UI Setup screen.
# _NOTE: this operation is irreversible and deletes all the existing meshes and simulations in the project._

# %%
project.load_geometry_to_setup(geometry)

# %% [markdown]
# ## Generate Mesh
#
# Before running a simulation, we'll need to generate a computational mesh based on the geometry in the project
#
# First we'll set up the parameters that are used to generate the mesh. Normally, you'll want to iterate this process, starting with a coarser mesh and refining it as needed.
#
# We recommend starting coarser and refining because this will require fewer computational resources in total. In this tutorial, we'll go ahead and generate a fine mesh

# %% [markdown]
# ### Define model, volume, and boundary layer parameters
#
# Here we set the meshing parameters.

# %% [markdown]
# The model parameters are:
#
# - surfaces: plane_surfaces (which we created earlier)
# - curvature: 4 degrees
# - max_size: 0.05

# %%
model_meshing_params = lc.meshing.ModelMeshingParams(
    surfaces=plane_surfaces,
    curvature=4,
    max_size=0.05,
)

# %% [markdown]
# The boundary layer parameters are:
#
# - surfaces: plane_surfaces
# - n_layers: 20
# - initial_size: 0.00001
# - growth_rate: 1.2

# %%
boundary_layer_params = lc.meshing.BoundaryLayerParams(
    surfaces=plane_surfaces,
    n_layers=20,
    initial_size=0.00001,
    growth_rate=1.2,
)

# %% [markdown]
# ### Define sizing strategy
# Set the sizing strategy for the mesh. You can choose from the following:
#
# | Strategy    | Description               | Notes          |
# | :- | :- | :- |
# | lc.meshing.sizing_strategy.Minimal() | Minimal sizing strategy parameters. | If this is used, all other meshing parameters are ignored. |
# | lc.meshing.sizing_strategy.TargetCount(value) | Sizing strategy based on a target number of cells. | To reach a target number of cells, the edge length specifications will be proportionally scaled throughout the mesh. Requested boundary layer profiles will be maintained. |
# | lc.meshing.sizing_strategy.MaxCount(value)   | Sizing strategy based on a maximum number of cells. | If the mesh becomes larger than the max cell count, the mesh will be scaled. Requested boundary layer profiles will be maintained. |

# %% [markdown]
# We will use a target number of 20 million cells.

# %%
target_count = 20_000_000
sizing_strategy = lc.meshing.sizing_strategy.TargetCount(target_count)

# %% [markdown]
# ### Set mesh parameters
#
# Now we set the meshing parameters based on the values we just set.
#
# Note that we have to specify the geometry ID shown earler, the sizing strategy, the model, volume, and boundary layer parameters, and the minimum and maximum size.

# %%
mesh_params = lc.meshing.MeshGenerationParams(
    geometry_id=geometry.id,
    sizing_strategy=sizing_strategy,
    model_meshing_params=[model_meshing_params],
    boundary_layer_params=[boundary_layer_params],
    min_size=0.005,
    max_size=50,
)

# %% [markdown]
# ### Create mesh
#
# Now we create the mesh. This may take several minutes depending on the number of volumes to create

# %%
# mesh = project.create_or_get_mesh(mesh_params, name="Piper Cherokee 20M mesh")

# %%
# Workaround for mesh timeout
mesh = None


def run_mesh_creation() -> None:
    global mesh
    mesh = project.create_or_get_mesh(mesh_params, name="Piper Cherokee 20M mesh")


thread = threading.Thread(target=run_mesh_creation)
thread.start()

# %%
elapsed_seconds = 0
wait_seconds = 30

current_time = datetime.now().isoformat()
display(
    f"{current_time}: elapsed: {elapsed_seconds//60:02d}:{elapsed_seconds%60:02d}",
    display_id="status_display",
)

while True:
    meshes = project.list_meshes()
    if len(meshes) > 0 and all(m.status.name == "COMPLETED" for m in meshes):
        update_display(
            f"{current_time}: elapsed: {elapsed_seconds//60:02d}:{elapsed_seconds%60:02d}; all meshes have been generated.",
            display_id="status_display",
        )
        break
    else:
        current_time = datetime.now().isoformat()
        update_display(
            f"{current_time}: elapsed: {elapsed_seconds//60:02d}:{elapsed_seconds%60:02d}; waiting...",
            display_id="status_display",
        )
        time.sleep(wait_seconds)
        elapsed_seconds += wait_seconds


# %% [markdown]
# We can see the mesh details after the mesh has been created.

# %%
mesh

# %% [markdown]
# We can also list all of the meshes in a project.

# %%
meshes = project.list_meshes()
meshes

# %% [markdown]
# ### Analyze the surface mesh
#
# We can visualize the surface mesh after it has been created.
#
# <img src="https://storage.googleapis.com/luminarycloud-learning/sample-projects/piper-cherokee/notebook-images/03-piper-cherokee-surface-mesh.png" width=600 />

# %%
# Check if mesh is None before passing to Scene constructor
scene = vis.Scene(mesh if mesh is not None else geometry)
# Hide the far field surface
scene.surface_visibility(farfield_surface_id, False)
scene.global_display_attrs.representation = vis.Representation.SURFACE_WITH_EDGES

camera = vis.LookAtCamera(
    look_at=[3.5, 0.0, 0.52],
    position=[3.5, 0, 12],
    up=[1, 0, 0],
    projection=vis.CameraProjection.PERSPECTIVE,
    width=4096,
    height=4096,
)
scene.add_camera(camera)

image_extract = scene.render_images(name="piper surface mesh", description="Piper surface mesh.")
image_extract.wait()

image_buffer, label = image_extract.download_images()[0]
image = Image.open(image_buffer)
display(image)


# %% [markdown]
# ### Analyze the volume mesh
#
# We can also visualize the volume mesh. We need to use a PlaneClip to see a cross-section.
#
# <img src="https://storage.googleapis.com/luminarycloud-learning/sample-projects/piper-cherokee/notebook-images/04-piper-cherokee-volume-mesh.png" width=600 />

# %%
# Check if mesh is None before passing to Scene constructor
scene = vis.Scene(mesh if mesh is not None else geometry)
# Hide the far field surface
scene.surface_visibility(farfield_surface_id, False)
scene.global_display_attrs.representation = vis.Representation.SURFACE

camera = vis.LookAtCamera(
    look_at=[3.5, 0.0, 0.52],
    position=[3.5, -10.9, 0.5],
    projection=vis.CameraProjection.PERSPECTIVE,
    width=2048,
    height=1024,
)
scene.add_camera(camera)


# Add a clip to visualize the mesh cells.
clip = vis.PlaneClip("x-clip")
clip.plane.normal = [0, 1, 0]
clip.plane.origin = [3.55, 0, 0.52]
clip.display_attrs.representation = vis.Representation.SURFACE_WITH_EDGES
scene.add_filter(clip)

# Use a higher resolution to reduce line aliasing.
image_extract = scene.render_images(name="piper volume mesh", description="Piper volume mesh.")
image_extract.wait()

image_buffer, label = image_extract.download_images()[0]
image = Image.open(image_buffer)
display(image)

# %% [markdown]
# ## Set up physics
# First set the identifier for the physics and the type (Fluid).
#
# Set the initialization to FluidFarfieldValues.

# %%
from luminarycloud import EntityIdentifier

fluid_flow_physics = lc.params.simulation.Physics()

fluid_flow_physics.physics_identifier = EntityIdentifier(id=str(uuid4()), name="fluid_flow_physics")
fluid_flow_physics.fluid = lc.params.simulation.physics.Fluid()

fluid_flow_physics.fluid.initialization = (
    lc.params.simulation.physics.fluid.initialization.FluidFarfieldValues()
)

# %% [markdown]
# ### Set up material (air)

# %%

material_model = lc.params.simulation.material.fluid.material_model.IdealGas(
    molecular_weight=28.966,
    specific_heat_cp=1006.4,
)

thermal_conductivity_model = (
    lc.params.simulation.material.fluid.thermal_conductivity_model.PrescribedPrandtlNumber(
        prandtl_number=0.72,
    )
)

viscosity_model = lc.params.simulation.material.fluid.viscosity_model.Sutherland(
    reference_viscosity=1.716e-5,
    reference_temperature=264.37,
    sutherland_constant=110.56,
)

fluid_material = lc.params.simulation.material.MaterialFluid(
    reference_pressure=0,
    material_model=material_model,
    thermal_conductivity_model=thermal_conductivity_model,
    viscosity_model=viscosity_model,
)

air_material = lc.params.simulation.MaterialEntity(
    material_identifier=EntityIdentifier(id=str(uuid4()), name="air_fluid"),
    fluid=fluid_material,
)

# %% [markdown]
# ### Boundary conditions

# %% [markdown]
# #### Define wall boundary condition
#
# The wall boundary condition represents a solid, impermeable surface where the flow interacts with a physical object, such as an aircraft fuselage, a car body, or a pipe wall. The specific treatment of the boundary depends on whether the flow is no-slip (viscous flow) or slip (inviscid flow).
#
# For this simulation we set the wall boundary to the surfaces of the plane, and the momentum as no-slip.

# %%
# Create the wall boundary condition using the enum value
wall_bc = lc.params.simulation.physics.fluid.boundary_conditions.Wall(
    name="Wall",
    surfaces=[s.id for s in plane_surfaces],
    momentum=lc.params.simulation.physics.fluid.boundary_conditions.wall.momentum.NoSlip(),
)

# %% [markdown]
# #### Define far field boundary condition
#
# Your farfield boundary defines the atmospheric conditions in which your aircraft is flying. The farfield ensures that disturbances from the aircraft dissipate naturally, preventing artificial reflections. These values define the ambient conditions that your aircraft or object is moving through.
#
# `name="Farfield"`
#
# The name of the farfield boundary condition
#
# `surfaces=surface_ids`
#
# This is a list of the IDs for the surfaces that define the far field boundary.
#
# `mach_number=0.216`
#
# This defines a subsonic flow condition (about 73.4 m/s if the speed of sound is ~340 m/s).
#
# `pressure=70100`
#
# This is the static pressure at the farfield, which is lower than sea-level atmospheric pressure (suggesting a higher-altitude simulation).
#
# `temperature=288.15`
#
# This is 15°C, close to standard sea-level conditions in the International Standard Atmosphere (ISA).
#
#
#
# ##### Direction
#
# `direction_specification=FARFIELD_ANGLES`
#
# This means the flow direction is set using angles (instead of velocity components).
#
# ##### Angle of Attack:
# The flow is coming in at a slight upward angle (2° AoA), which is common for lift-producing wings.
#
# `angle_alpha = 2.0`
#
# This sets an angle of attack (AoA) of 2 degrees, meaning the airflow is slightly inclined relative to the aircraft.
#
# `angle_beta = 0.0`
#
# No sideslip angle, meaning the flow is aligned with the aircraft’s centerline in the lateral direction.
#

# %%
farfield_bc = lc.params.simulation.physics.fluid.boundary_conditions.Farfield(
    name="Farfield",
    surfaces=[farfield_surface_id],
    mach_number=0.216,
    pressure=70100,
    temperature=288.15,
    direction_specification=lc.params.enum.FarFieldFlowDirectionSpecification.FARFIELD_ANGLES,
    angle_alpha=2.0,
    angle_beta=0.0,
)

# %% [markdown]
# #### Set boundary conditions
#
# The boundary conditions includes the farfield and wall boundary conditions.

# %%
fluid_flow_physics.fluid.boundary_conditions = [farfield_bc, wall_bc]

# %% [markdown]
# ## Create simulation parameters

# %%
sim_params = lc.SimulationParam()
sim_params.assign_material(air_material, fluid_volume)
sim_params.assign_physics(fluid_flow_physics, fluid_volume)

# %% [markdown]
# ## Simulation

# %% [markdown]
# ### Create a simulation template
#
# We use a simulation template to hold the parameters for a simulation. In order to run the simulation, first create a simulation template based on the simulation parameters.

# %%
simulation_parameters = sim_params._to_proto()

# %%
simulation_template = project.create_simulation_template(
    name="piper simulation parameters",
    parameters=simulation_parameters,
)

# %% [markdown]
# ### Configure outputs

# %% [markdown]
# We output equation residuals and surface-integrated scalar outputs at every iteration, on all surfaces, volumes, monitor planes, and monitor points. This allows you to extract outputs after running a simulation without requiring you to re-run the simulation!
#
# However, if you’d like to define a stopping condition based on an output, you need to define a specific output first. Otherwise, declaring outputs up front is optional.

# %%
lift = simulation_template.create_output_definition(
    lc.outputs.ForceOutputDefinition(
        name="Lift",
        quantity=lc.enum.QuantityType.LIFT,
        surfaces=[s.id for s in plane_surfaces],
    )
)

# %%
drag = simulation_template.create_output_definition(
    lc.outputs.ForceOutputDefinition(
        name="Drag",
        quantity=lc.enum.QuantityType.DRAG,
        surfaces=[s.id for s in plane_surfaces],
    )
)

# %% [markdown]
# ### Set stopping conditions

# %% [markdown]
# Stopping Conditions are used to determine when a simulation exits and saves results. Here we set a stopping condition based on one of the custom outputs we just defined, and we'll stop the simulation after a maximum number of iterations even if the stopping condition is unmet.

# %%
simulation_template.create_or_update_stopping_condition(
    output_definition_id=lift.id,
    threshold=0.00_01,  # 0.01%
    start_at_iteration=500,
    averaging_iterations=10,
    iterations_to_consider=5,
)

# %%
simulation_template.update_general_stopping_conditions(max_iterations=2000)  # type: ignore

# %% [markdown]
# ### Run the simulation

# %%
# Check if mesh is None before accessing its id attribute
simulation = project.create_simulation(
    mesh.id if mesh is not None else meshes[0].id,
    name="Piper simulation",
    simulation_template_id=simulation_template.id,
    batch_processing=False,
)
simulation

# %% [markdown]
# Note that the status is **SIMULATION_STATUS_ACTIVE** (**ACTIVE**) while running. We must wait for the simulation to finish.

# %%
# Wait for simulation
# We are getting the simulation status using project.list_simulations()[0].status.name; this will be replaced by a function
done = False
spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
display(f"Status: {simulation.status.name}⠏", display_id="status_display")
i = 0
while not done:
    sim_status = project.list_simulations()[0].status.name
    if sim_status != "ACTIVE":
        update_display(f"Status: {sim_status}", display_id="status_display")
        done = True
        break
    i += 1
    update_display(f"Status: {sim_status}{spinner[i % len(spinner)]}", display_id="status_display")
    time.sleep(0.5)

# %% [markdown]
# ## Plot residuals
#
# Now we can download the residuals as CSV and plot them.

# %%
with simulation.download_global_residuals() as stream:
    # since this is a steady state simulation, we can drop these columns
    residuals_df = pd.read_csv(stream, index_col="Iteration index").drop(
        ["Time step", "Physical time"], axis=1
    )
residuals_df

# %%
# We want to plot all residuals on a log scale (residuals are typically shown this way)
# 'Spalart-Allmaras Variable' is also available for plotting
fig = px.line(
    residuals_df,
    x=residuals_df.index,
    y=["X-Momentum Residual", "Y-Momentum Residual", "Z-Momentum Residual", "Energy Residual"],
    title="Residuals vs Iteration",
    template="plotly_white",
    log_y=True,
)  # Using log scale for y-axis since these are residuals

fig.update_layout(
    xaxis_title="Iteration",
    yaxis_title="Residual Value",
    width=1000,
    height=600,
    showlegend=True,
    legend_title="Residual Type",
    legend=dict(
        orientation="h",  # horizontal orientation
        yanchor="bottom",
        y=-0.2,  # position below the plot
        xanchor="center",
        x=0.5,  # centered horizontally
    ),
)

# Optional: Update line styles for better visibility
fig.update_traces(mode="lines")

fig.show()

# %%
# Check if mesh is None before accessing its id attribute
mesh_metadata = lc.get_mesh_metadata(mesh.id if mesh is not None else meshes[0].id)
target_boundaries = ["0/bound/BC_1"]

# %%
from luminarycloud.enum import ReferenceValuesType
from luminarycloud.reference_values import ReferenceValues
from luminarycloud.enum import QuantityType, CalculationType, SimulationStatus, ReferenceValuesType

ref_vals = ReferenceValues(
    reference_value_type=ReferenceValuesType.PRESCRIBE_VALUES,
    area_ref=10.0,
    length_ref=10.0,
    p_ref=101325.0,
    t_ref=273.15,
    v_ref=265.05709547039106,
)

# see documentation for more details about optional parameters
with simulation.download_surface_output(
    QuantityType.LIFT,
    target_boundaries,
    reference_values=ref_vals,
    frame_id="body_frame_id",
) as stream:
    # since this is a steady state simulation, we can drop "Time step" and "Physical time"
    lift_df = pd.read_csv(stream, index_col="Iteration index").drop(
        ["Time step", "Physical time"], axis=1
    )
    # rename lift column
    lift_df = lift_df.rename(columns={"Lift - 0/bound/BC_1": "lift"})

# %%
lift_df

# %%
fig = px.line(lift_df, y="lift", title="Lift vs Iteration", template="plotly_white")

fig.update_layout(xaxis_title="Iteration", yaxis_title="Lift", width=800, height=500)

fig.show()

# %%
# see documentation for more details about optional parameters
with simulation.download_surface_output(
    QuantityType.DRAG,
    target_boundaries,
    reference_values=ref_vals,
    frame_id="body_frame_id",
) as stream:
    # since this is a steady state simulation, we can drop "Time step" and "Physical time"
    drag_df = pd.read_csv(stream, index_col="Iteration index").drop(
        ["Time step", "Physical time"], axis=1
    )
    # rename drag column
    drag_df = drag_df.rename(columns={"Drag - 0/bound/BC_1": "drag"})

# %%
drag_df

# %%
fig = px.line(drag_df, y="drag", title="Drag vs Iteration", template="plotly_white")

fig.update_layout(xaxis_title="Iteration", yaxis_title="Drag", width=800, height=500)

fig.show()

# %% [markdown]
# ### Visualizing flow movement
#
# One of the powerful abilities of computational fluid dynamics is that it can allow us to visualize the usually invisible movement of a fluid past an object. This understanding can be critical in improving the designs of vehicles and aircraft.
#
# <img src="https://storage.googleapis.com/luminarycloud-learning/sample-projects/piper-cherokee/notebook-images/05-piper-cherokee-flow-slice.png" width=600 />

# %%

# Pick the last iteration
solution = simulation.list_solutions()[-1]
scene = vis.Scene(solution)

# Hide the far field surface
scene.hide_far_field()
scene.global_display_attrs.representation = vis.Representation.SURFACE
scene.global_display_attrs.field.quantity = vis.VisQuantity.NONE

camera = vis.LookAtCamera(
    look_at=[4.0, 0.0, 0.0],
    position=[-4.0, -7.0, 7.0],
    projection=vis.CameraProjection.PERSPECTIVE,
    width=2048,
    height=1024,
)
scene.add_camera(camera)

# Add a slice to visualize the volume solution.
slice = vis.Slice("x-slice")
slice.plane.normal = [0, 1, 0]
slice.plane.origin = [3.55, 0, 0.52]
slice.display_attrs.representation = vis.Representation.SURFACE
slice.display_attrs.field.quantity = vis.VisQuantity.VELOCITY
slice.display_attrs.field.component = vis.FieldComponent.MAGNITUDE
scene.add_filter(slice)

# Use a higher resolution to reduce line aliasing.
image_extract = scene.render_images(
    name="piper volume solution", description="Piper volume solution visualization."
)
image_extract.wait()

image_buffer, label = image_extract.download_images()[0]
image = Image.open(image_buffer)
display(image)


# %% [markdown]
# We can also visualize the velocity vectors.
#
# <img src="https://storage.googleapis.com/luminarycloud-learning/sample-projects/piper-cherokee/notebook-images/06-piper-cherokee-flow-vectors.png" width=600 />
#

# %%
scene = vis.Scene(solution)
# Hide the far field surface
scene.hide_far_field()
scene.global_display_attrs.representation = vis.Representation.SURFACE
scene.global_display_attrs.field.quantity = vis.VisQuantity.NONE

camera = vis.LookAtCamera(
    look_at=[4.0, 0.0, 0.0],
    position=[-4.0, -7.0, 7.0],
    projection=vis.CameraProjection.PERSPECTIVE,
    width=2048,
    height=1024,
)
scene.add_camera(camera)

# Add a slice to visualize the volume solution.
glyph = vis.FixedSizeVectorGlyphs("glyphs")
glyph.field.quantity = vis.VisQuantity.VELOCITY
glyph.sampling_rate = 1000
glyph.size = 0.2
glyph.display_attrs.representation = vis.Representation.SURFACE
glyph.display_attrs.field.quantity = vis.VisQuantity.VELOCITY
glyph.display_attrs.field.component = vis.FieldComponent.MAGNITUDE
scene.add_filter(glyph)

# Use a higher resolution to reduce line aliasing.
image_extract = scene.render_images(
    name="piper volume solution", description="Piper volume solution visualization."
)
image_extract.wait()

image_buffer, label = image_extract.download_images()[0]
image = Image.open(image_buffer)
display(image)
