# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
import luminarycloud as lc
from luminarycloud._proto.base import base_pb2 as basepb
from luminarycloud._proto.output import output_pb2 as outputpb
from luminarycloud._proto.frontend.output import output_pb2 as feoutputpb
from luminarycloud._proto.quantity import quantity_pb2 as quantitypb


def test_surface_average_output_definition() -> None:
    outdef = lc.outputs.SurfaceAverageOutputDefinition(
        id="great-outdef",
        name="Velocity drop",
        quantity=lc.enum.QuantityType.VELOCITY,
        vector_component=lc.enum.Vector3Component.Z,
        surfaces=["lcTag/tagContainer/tag/bottom"],
        out_surfaces=["lcTag/tagContainer/tag/top"],
        calc_type=lc.enum.CalculationType.DIFFERENCE,
        reference_frame_id="great-frame",
        include=lc.outputs.OutputDefinitionInclusions(
            base_value=True,
            trailing_average=lc.outputs.TrailingAverageConfig(
                averaging_iterations=10,
            ),
            convergence_monitoring=lc.outputs.ConvergenceMonitoringConfig(
                averaging_iterations=15,
                iterations_to_consider=5,
            ),
        ),
    )

    proto = feoutputpb.OutputNode(
        id="great-outdef",
        name="Velocity drop",
        in_surfaces=["lcTag/tagContainer/tag/bottom"],
        out_surfaces=["lcTag/tagContainer/tag/top"],
        calc_type=feoutputpb.CalculationType.CALCULATION_DIFFERENCE,
        frame_id="great-frame",
        surface_average=feoutputpb.SurfaceAverageNode(
            quantity_type=quantitypb.QuantityType.VELOCITY,
            vector_component=basepb.VECTOR_3_COMPONENT_Z,
            props=outputpb.SurfaceAverageProperties(
                averaging_type=outputpb.SPACE_AREA_AVERAGING,
            ),
        ),
        trail_avg_iters=10,
        average_iters=15,
        analysis_iters=5,
        include={
            feoutputpb.OUTPUT_INCLUDE_BASE: True,
            feoutputpb.OUTPUT_INCLUDE_TIME_AVERAGE: True,
            feoutputpb.OUTPUT_INCLUDE_MAX_DEV: True,
        },
    )

    assert outdef._to_proto() == proto
    assert lc.outputs.SurfaceAverageOutputDefinition._from_proto(proto) == outdef


def test_residual_output_definition() -> None:
    outdef = lc.outputs.ResidualOutputDefinition(
        id="great-'zids",
        name="Rizziduals",
        include={
            lc.enum.QuantityType.RESIDUAL_DENSITY: True,
            lc.enum.QuantityType.RESIDUAL_X_MOMENTUM: False,
            lc.enum.QuantityType.RESIDUAL_Y_MOMENTUM: True,
            lc.enum.QuantityType.RESIDUAL_Z_MOMENTUM: False,
            lc.enum.QuantityType.RESIDUAL_ENERGY: True,
            lc.enum.QuantityType.RESIDUAL_SA_VARIABLE: False,
            lc.enum.QuantityType.RESIDUAL_TKE: True,
            lc.enum.QuantityType.RESIDUAL_OMEGA: False,
            lc.enum.QuantityType.RESIDUAL_GAMMA: True,
            lc.enum.QuantityType.RESIDUAL_RE_THETA: False,
            lc.enum.QuantityType.RESIDUAL_N_TILDE: True,
        },
        residual_type=lc.enum.ResidualType.MAX,
        physics_id="great-physics-really-great",
    )

    proto = feoutputpb.OutputNode(
        id="great-'zids",
        name="Rizziduals",
        residual=feoutputpb.ResidualNode(
            props=outputpb.ResidualProperties(
                type=outputpb.RESIDUAL_MAX,
            ),
            res_enabled={
                quantitypb.RESIDUAL_DENSITY: True,
                quantitypb.RESIDUAL_X_MOMENTUM: False,
                quantitypb.RESIDUAL_Y_MOMENTUM: True,
                quantitypb.RESIDUAL_Z_MOMENTUM: False,
                quantitypb.RESIDUAL_ENERGY: True,
                quantitypb.RESIDUAL_SA_VARIABLE: False,
                quantitypb.RESIDUAL_TKE: True,
                quantitypb.RESIDUAL_OMEGA: False,
                quantitypb.RESIDUAL_GAMMA: True,
                quantitypb.RESIDUAL_RE_THETA: False,
                quantitypb.RESIDUAL_N_TILDE: True,
            },
            physics_id="great-physics-really-great",
        ),
    )

    assert outdef._to_proto() == proto
    assert lc.outputs.ResidualOutputDefinition._from_proto(proto) == outdef
