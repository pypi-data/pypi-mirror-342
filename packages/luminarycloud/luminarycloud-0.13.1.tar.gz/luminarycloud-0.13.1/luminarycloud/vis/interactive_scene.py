from .display import DisplayAttributes
from .filters import SurfaceStreamlines, Filter
from .._client import get_default_client
from ..enum.vis_enums import EntityType
from typing import TYPE_CHECKING, cast

from .._proto.api.v0.luminarycloud.vis import vis_pb2

if TYPE_CHECKING:
    from .visualization import Scene, LookAtCamera

try:
    import luminarycloud_jupyter as lcj
except ImportError:
    lcj = None


class InteractiveScene:
    """
    The InteractiveScene acts as the bridge between the the Scene and
    the Jupyter widget, handling checking if we have the widget package
    before passing calls to the widget to handle it being an optional
    dependency
    """

    # Using the type causes a circular import error, not sure on best way to resolve.
    # I do want to keep this in a separate file
    def __init__(self, scene: "Scene") -> None:
        if not lcj:
            raise ImportError("InteractiveScene requires luminarycloud[jupyter] to be installed")
        self.widget = lcj.LCVisWidget()
        self.set_scene(scene)

    def _ipython_display_(self) -> None:
        """
        When the InteractiveScene is shown in Jupyter we show the underlying widget
        to run the widget's frontend code
        """
        self.widget._ipython_display_()

    def set_scene(self, scene: "Scene") -> None:
        # Display the initial scene we've been given
        # Submit request for the render data URLs we need
        req = vis_pb2.GetRenderDataUrlsRequest()
        req.project_id = scene._project_id
        if scene._entity_type == EntityType.SIMULATION:
            req.entity.simulation.id = scene._solution.simulation_id
            req.entity.simulation.solution_id = scene._solution.id
        elif scene._entity_type == EntityType.MESH:
            req.entity.mesh.id = scene._mesh.id
        elif scene._entity_type == EntityType.GEOMETRY:
            req.entity.geometry.id = scene._geometry.id
        else:
            # Should never hit b/c the Scene would have complained already
            raise TypeError(
                f"Expected Solution, Mesh or Geometry in Scene, got {scene._entity_type}"
            )

        # Validate filter connections and filter params.
        # we don't care about validating anything else that the Scene checks in _create_request
        # for now. We could unify this code more later.
        scene._validate_filter_connections()
        for filter in scene._filters:
            if isinstance(filter, SurfaceStreamlines):
                # Validate surfaces names
                streamlines = cast(SurfaceStreamlines, filter)
                bad_ids = scene._validate_surfaces_and_tags(streamlines._surface_names)
                if len(bad_ids) != 0:
                    raise ValueError(f"SurfaceStreamlines has invalid surfaces: {bad_ids}")

            if isinstance(filter, Filter):
                vis_filter: vis_pb2.Filter = filter._to_proto()
                req.filters.append(vis_filter)
            else:
                raise TypeError(f"Expected 'filter', got {type(filter).__name__}")
            if filter.get_parent_id():
                req.filter_connections[filter.get_parent_id()].children_id.append(filter.id)

        # TODO: would be nice to show execution progress of the workspace here,
        # some inline progress bar in the notebook
        resp = get_default_client().GetRenderDataUrls(req)

        # TODO: would be nice to print/report some download progress info
        # This can be done on the app frontend side now that the download
        # is moved there.
        self.widget.set_workspace_state(scene, resp)

    def set_surface_visibility(self, surface_id: str, visible: bool) -> None:
        self.widget.set_surface_visibility(surface_id, visible)

    def set_surface_color(self, surface_id: str, color: list[float]) -> None:
        self.widget.set_surface_color(surface_id, color)

    def set_display_attributes(self, object_id: str, attrs: DisplayAttributes) -> None:
        self.widget.set_display_attributes(object_id, attrs)

    def reset_camera(self) -> None:
        self.widget.reset_camera()

    def get_camera(self) -> "LookAtCamera":
        # Import here to avoid circular import issue
        from .visualization import LookAtCamera

        camera = LookAtCamera()
        camera.position = self.widget.camera_position
        camera.look_at = self.widget.camera_look_at
        camera.up = self.widget.camera_up
        return camera
