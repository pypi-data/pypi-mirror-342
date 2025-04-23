"""
This example demonstrates how to create output definitions for a simulation
"""

import luminarycloud as lc
from luminarycloud.enum import QuantityType, CalculationType
from sdk_util import get_client_for_env

# <internal>
# Please keep the <internal> tags because assistant will use it to filter out the internal code.
import urllib3

urllib3.disable_warnings()

# This points the client to main (Internal use only)
lc.set_default_client(get_client_for_env(env_name="main"))
# </internal>

project = lc.create_project(name="Outputs Test")
geometry = project.create_geometry(
    cad_file_path="/sdk/testdata/cube.cgns",  # Replace with your own file path
    wait=True,
)

# new project, so the only sim template is the default one
setup = project.list_simulation_templates()[0]

all_nodes = setup.list_output_definitions()
residuals = [n for n in all_nodes if isinstance(n, lc.outputs.ResidualOutputDefinition)]

# Disable the residual output definitions for the x, y, and z momentum quantities
for r in residuals:
    r.include[QuantityType.RESIDUAL_X_MOMENTUM] = False
    r.include[QuantityType.RESIDUAL_Y_MOMENTUM] = False
    r.include[QuantityType.RESIDUAL_Z_MOMENTUM] = False
    setup.update_output_definition(r.id, r)

# Create a output definition based on pressure difference
pressure_drop = setup.create_output_definition(
    lc.outputs.SurfaceAverageOutputDefinition(
        name="Pressure drop",
        quantity=QuantityType.PRESSURE,
        surfaces=["lcTag/tagContainer/tag/bottom"],
        out_surfaces=["lcTag/tagContainer/tag/top"],
        calc_type=CalculationType.DIFFERENCE,
        include=lc.outputs.OutputDefinitionInclusions(
            base_value=True,
            trailing_average=lc.outputs.TrailingAverageConfig(
                averaging_iterations=10,
            ),
            convergence_monitoring=lc.outputs.ConvergenceMonitoringConfig(
                averaging_iterations=10,
                iterations_to_consider=5,
            ),
        ),
    )
)

# Create a output definition based on lift force
force = setup.create_output_definition(
    lc.outputs.ForceOutputDefinition(
        name="Lift",
        quantity=QuantityType.LIFT,
        surfaces=["lcTag/tagContainer/tag/bottom"],
        calc_type=CalculationType.AGGREGATE,
        include=lc.outputs.OutputDefinitionInclusions(
            base_value=True,
            coefficient=True,
            trailing_average=lc.outputs.TrailingAverageConfig(
                averaging_iterations=10,
            ),
            convergence_monitoring=lc.outputs.ConvergenceMonitoringConfig(
                averaging_iterations=10,
                iterations_to_consider=5,
            ),
        ),
    )
)

# Here we try to set the quantity to PRESSURE, which is not a force quantity type.
try:
    force.include.coefficient = True
    force.quantity = QuantityType.PRESSURE
    # This will fail: "PRESSURE is not a force quantity type"
    setup.update_output_definition(force.id, force)
except Exception as e:
    print(e)

# Delete the pressure drop output definition
setup.delete_output_definition(pressure_drop.id)

# Get the general stopping conditions
setup.get_general_stopping_conditions()
setup.update_general_stopping_conditions(stop_on_any=True)

# Delete all stopping conditions
stopping_conditions = setup.list_stopping_conditions()
for sc in stopping_conditions:
    setup.delete_stopping_condition(sc.id)

# Create a LIFT force based stopping condition
lift_sc = setup.create_or_update_stopping_condition(
    output_definition_id=force.id,
    threshold=0.01,
    averaging_iterations=10,
    iterations_to_consider=5,
)

# Get the stopping condition and delete it
setup.get_stopping_condition(lift_sc.id)

setup.delete_stopping_condition(lift_sc.id)
