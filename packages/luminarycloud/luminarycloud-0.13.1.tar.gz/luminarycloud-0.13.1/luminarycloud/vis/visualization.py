from .._proto.api.v0.luminarycloud.vis import vis_pb2
import luminarycloud._proto.api.v0.luminarycloud.common.common_pb2 as common_pb2
from .._client import get_default_client
from ..solution import Solution
from ..mesh import get_mesh_metadata, Mesh, get_mesh
from ..geometry import Geometry, get_geometry, Tag
from ..enum.vis_enums import *
from ..enum.quantity_type import QuantityType
from ..simulation import get_simulation
from .display import DisplayAttributes, ColorMap, Field, ColorMapAppearance
from .filters import Filter, PlaneClip, Slice, BoxClip, SurfaceStreamlines
from luminarycloud.types import Vector3, Vector3Like
from ..types.vector3 import _to_vector3
from .._helpers._get_project_id import _get_project_id
from ..exceptions import NotFoundError
from .interactive_scene import InteractiveScene
import io
import json
from luminarycloud._proto.client import simulation_pb2 as clientpb
from typing import List, Tuple, cast, Union, Dict
import requests
from time import time, sleep
import logging
import dataclasses as dc

logger = logging.getLogger(__name__)


def _is_valid_color(obj: common_pb2.Vector3) -> bool:
    return all(0 <= getattr(obj, attr) <= 1 for attr in ["x", "y", "z"])


@dc.dataclass
class DirectionalCamera:
    """
    Class defining a directional camera for visualization. Directional
    camera are oriented around the visible objects in the scene and will
    always face towards the scene.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name : str
        A user defined name for the camera.
    direction : CameraDirection
        The orientation of the camera. Default: X_POSITIVE
    projection : CameraProjection
        The type of projection used for the camera. Default: ORTHOGRAPHIC
    label: str
        A user defined label to help distinguish between multiple images.
        Default: ""
    width: int
        The width of the output image in pixels. Default: 1024
    height: int
        The height of the output image in pixels. Default: 1024
    """

    name: str = "default directional camera"
    direction: CameraDirection = CameraDirection.X_POSITIVE
    projection: CameraProjection = CameraProjection.ORTHOGRAPHIC
    label: str = ""
    width: int = 1024
    height: int = 1024


@dc.dataclass
class LookAtCamera:
    """
    Class defining a look at camera for visualization.  Unlike the directional
    camera which is placed relative to what is visisble, the the look at camera
    is an explict camera, meaning that we have to fully specify the parameters.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    look_at: Vector3
        The point the camera is looking at. Default (0,0,0)
    position: Vector3
        The position of the camera. Default (0,1,0)
    up: Vector3
        The up vector for the camera. Default (0,0,1)
    projection : CameraProjection
        The type of projection used for the camera. Default: ORTHOGRAPHIC
    label: str
        A user defined label to help distinguish between multiple images. Default: ""
    width: int
        The width of the output image in pixels. Default: 1024
    height: int
        The height of the output image in pixels. Default: 1024
    """

    look_at: Vector3Like = dc.field(default_factory=lambda: Vector3(x=0, y=0, z=0))
    position: Vector3Like = dc.field(default_factory=lambda: Vector3(x=0, y=1, z=0))
    up: Vector3Like = dc.field(default_factory=lambda: Vector3(x=0, y=0, z=1))
    projection: CameraProjection = CameraProjection.ORTHOGRAPHIC
    label: str = ""
    width: int = 1024
    height: int = 1024


class RenderOutput:
    """
    The render output represents the request to render images from a geometry, mesh or
    solution. The operation exectutes asyncronously, so the caller must check
    the status of the image extract. If the status is completed, then the
    resuling image is available for download.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    name: str
        The user provided name of the extract.
    description: str
        The user provided description of the extract.
    status: RenderStatusType
        The status of the extract (i.e., has it completed or not).
    _extract_id: str
        The unique indentifier of the extract.
    _project_id: str
        The project id associated with the extract.
    _deleted: bool
        Internal flag to track if the extract has been deleted.
    """

    def __init__(
        self, extract_id: str, project_id: str, name: str, desciption: str, status: RenderStatusType
    ):
        # TODO(matt): We could make all of these read only.
        self._extract_id: str = extract_id
        self._project_id: str = project_id
        self.status: RenderStatusType = status
        self.name: str = name
        self.description: str = desciption
        self._deleted = False

    def __repr__(self) -> str:
        return f"RenderOutput(Id: {self._extract_id} status: {self.status})"

    def refresh(self) -> "RenderOutput":
        """
        Refesh the status of the RenderOutput.

        Returns
        -------
        self
        """
        self._fail_if_deleted()
        render = get_render(self._project_id, self._extract_id)
        self.status = render.status
        return self

    def wait(
        self, interval_seconds: float = 5, timeout_seconds: float = float("inf")
    ) -> RenderStatusType:
        """
        Wait until the RenderOutput is completed or failed.

        Parameters
        ----------
        interval : float, optional
            Number of seconds between polls.
        timeout : float, optional
            Number of seconds before timeout.

        Returns
        -------
        RenderStatusType: Current status of the image extract.
        """
        self._fail_if_deleted()
        deadline = time() + timeout_seconds
        while True:
            self.refresh()

            if self.status in [
                RenderStatusType.COMPLETED,
                RenderStatusType.FAILED,
                RenderStatusType.INVALID,
            ]:
                return self.status
            if time() >= deadline:
                logger.error("`RenderOutput: wait ` timed out.")
                raise TimeoutError
            sleep(max(0, min(interval_seconds, deadline - time())))

    def download_images(self) -> List[Tuple[("io.BytesIO"), str]]:
        """
        Downloads the resulting jpeg images into binary buffers. This is useful
        for displaying images in notebooks.  If that status is not complete, an
        error will be raised.

        Returns:
            List[Tuple[io.BytesIO, str]]: a list of tuples containing the binary image
            data and the user provided image label (camera.label).

        .. warning:: This feature is experimental and may change or be removed in the future.

        """
        self._fail_if_deleted()
        self.refresh()
        if self.status != RenderStatusType.COMPLETED:
            raise Exception("download_image: status not complete.")
        req = vis_pb2.DownloadExtractRequest()
        req.extract_id = self._extract_id
        req.project_id = self._project_id
        res: vis_pb2.DownloadExtractResponse = get_default_client().DownloadExtract(req)

        buffers: List[Tuple["io.BytesIO", str]] = []
        assert len(res.files) == len(res.labels)
        for output, label in zip(res.files, res.labels):
            buffer = io.BytesIO()
            if output.signed_url:
                response = requests.get(output.signed_url, stream=True)
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=8192):
                    buffer.write(chunk)
            elif output.full_contents:
                buffer.write(output.full_contents)
            else:
                raise Exception("download_image respose contains no data.")
            # Reset buffer position to the beginning for reading
            buffer.seek(0)
            buffers.append((buffer, label))
        return buffers

    def save_images(self, file_prefix: str, write_labels: bool = False) -> None:
        """
        A helper for downloading and save resulting images to the file system. If that status is not
        complete, an error will be raised. Images will be of the form {file_prefix}_{index}.jpg.
        Optionally, a file will be written containing a list of file names and image labels. Labels
        are an optional field in the camera (camera.label).

        .. warning:: This feature is experimental and may change or be removed in the future.

        Parameters
        ----------
        file_prefix: str, required
            The file prefix to save the image. A image index and  '.jpg' will be
            appended to the file names.
        write_labels: bool, optional
            Write a json file containing a list of image file names and labels,
            if True. The resulting json file is named '{file_prefix}.json' Default: False
        """
        if not file_prefix:
            raise ValueError("file_prefix must be non-empty")

        images = self.download_images()
        names_labels: List[Tuple[str, str]] = []
        # TODO(matt): need a better way to name these, ie, a label
        counter = 0
        for image in images:
            output_file = f"{file_prefix}_{counter}.jpg"
            with open(output_file, "wb") as file:
                file.write(image[0].getvalue())
            counter = counter + 1
            names_labels.append((output_file, image[1]))
        if write_labels:
            with open(f"{file_prefix}.json", "w") as json_file:
                json.dump(names_labels, json_file, indent=2)

    def _fail_if_deleted(self) -> None:
        if self._deleted:
            raise ValueError("RenderOutput has been deleted.")

    def delete(self) -> None:
        """Delete the image."""
        self._fail_if_deleted()
        req = vis_pb2.DeleteExtractRequest()
        req.extract_id = self._extract_id
        req.project_id = self._project_id
        get_default_client().DeleteExtract(req)
        self._deleted = True


class Scene:
    """
    The scene class is the base for any visualization. The scene is constructed
    with what "entity" you want to visualize: a solution, a mesh, or
    a geometry.

    Global display attributes: The global display attributes control the default
    appearance of all the surfaces (i.e. boundaries). Attributes include visibitiy,
    what fields are displayed on the surfaces (if applicable), and representation
    (e.g., surface, surface with edges, ...).

    Individual surface visibilities can be overidden to hide/show specific surfaces.
    Additionally, if the scene is constructed around a simulation, a helper method is
    provided to automatically hide surfaces associated with far fields.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    global_display_attrs : DisplayAttributes
        These attributes apply to all the surfaces in the
        geometry/mesh/solution. Individual surface visibilities can be
        overridden with the 'surface_visibility' function.
    triad_visible: bool
        This value controls whether the triad is visible or not in the rendered
        images.  Default: True
    background_color: Vector3Like
        This value controls then scene background color. These are rgb values in
        the range [0,1] for each component.  Default: [0,0,0]
    axes_grid_visible: bool
        This values controls whether the axes grid is visible or not in the
        rendered images. Default: False
    auto_color_map_annotations: bool
        This values controls whether we automatically generate color map
        annotations for all fields used in global and filter display attributes.
        When False, only color maps explicitly added by the user appear in the
        images. Default: True
    """

    def __init__(self, entity: Geometry | Mesh | Solution):
        self.triad_visible: bool = True
        self.axes_grid_visible: bool = True
        self.background_color: Vector3 = Vector3(x=0, y=0, z=0)
        self.auto_color_map_annotations = True
        # Global display attrs
        self.global_display_attrs = DisplayAttributes()
        self._filters: List[Filter] = []
        self._color_maps: List[ColorMap] = []
        self._cameras: List[DirectionalCamera | LookAtCamera] = []
        self._entity_type: EntityType = EntityType.SIMULATION
        # Meshes that are directly uploaded will not have tags.
        self._has_tags: bool = True

        # Interactive scene if we're in Jupyter and displaying it
        self._interactive_scene: InteractiveScene | None = None

        # Find out what we are working on.
        if isinstance(entity, Solution):
            self._solution: Solution = entity
            self._entity_type = EntityType.SIMULATION
        elif isinstance(entity, Mesh):
            self._mesh: Mesh = entity
            self._entity_type = EntityType.MESH
        elif isinstance(entity, Geometry):
            self._geometry: Geometry = entity
            self._entity_type = EntityType.GEOMETRY
        else:
            raise TypeError(f"Expected Solution, Mesh or Geometry, got {type(entity).__name__}")

        project_id = _get_project_id(entity)
        if not project_id:
            raise ValueError("Unable to get project id from entity")

        self._project_id = project_id

        # A list containing visibility overrides. Can contain both surface ids and tag ids.
        self._surface_visibilities: dict[str, bool] = {}

        # Find all the surfaces from the metadata.
        mesh_meta = None
        # Trace each entity all the way back to the geometry so we
        # can accesss the tags.
        geom: Geometry | None = None
        if self._entity_type == EntityType.SIMULATION:
            simulation = get_simulation(self._solution.simulation_id)
            mesh_meta = get_mesh_metadata(simulation.mesh_id)
            mesh = get_mesh(simulation.mesh_id)
            try:
                geom = mesh.geometry_version().geometry()
            except NotFoundError:
                self._has_tags = False
            except Exception as e:
                raise ValueError("An unknow error occurred retrieving tags")
        elif self._entity_type == EntityType.MESH:
            mesh_meta = get_mesh_metadata(self._mesh.id)
            try:
                geom = get_geometry(self._mesh.geometry_version().geometry_id)
            except NotFoundError:
                self._has_tags = False
            except Exception as e:
                raise ValueError("An unknow error occurred retrieving tags")
        else:
            geom = self._geometry

        self._surface_ids: List[str] = []
        if mesh_meta:
            for zone in mesh_meta.zones:
                for bound in zone.boundaries:
                    self._surface_ids.append(bound.name)
        else:
            surface_list = self._geometry.list_entities()[0]
            for surface in surface_list:
                self._surface_ids.append(surface.id)

        self._tag_ids: List[str] = []
        if geom and self._has_tags:
            tags = geom.list_tags()
            for tag in tags:
                self._tag_ids.append(tag.id)

        self._far_field_boundary_ids: List[str] = []

        # Find all the far field surfaces if we can get the params.
        if self._entity_type == EntityType.SIMULATION:
            params = simulation.get_parameters()
            for physics in params.physics:
                if physics.fluid:
                    for bc in physics.fluid.boundary_conditions_fluid:
                        if bc.physical_boundary == clientpb.PhysicalBoundary.FARFIELD:
                            for bc_surface in bc.surfaces:
                                self._far_field_boundary_ids.append(bc_surface)

    def hide_far_field(self) -> None:
        """
        Hide all far fields surfaces based on simulation parameters. Will work
        if the entity is a simulation.
        """

        for boundary_id in self._far_field_boundary_ids:
            self.surface_visibility(boundary_id, False)

    def surface_ids(self) -> List[str]:
        """Get a list of all the surface ids associated with the mesh."""
        return self._surface_ids

    def tag_ids(self) -> List[str]:
        """Get a list of all the tag ids associated with the entity."""
        return self._tag_ids

    def surface_visibility(self, surface_id: str, visible: bool) -> None:
        """
        Explicitly override the the visibility of a surface by id.  When
        caclulating final visibilities, we first apply overrides to the global
        display attributes using tags, then surface ids.
        """
        if not surface_id in self._surface_ids:
            raise ValueError(f"Id {id} not a boundary id")
        self._surface_visibilities[surface_id] = visible

        if self._interactive_scene:
            self._interactive_scene.set_surface_visibility(surface_id, visible)

    def tag_visibility(self, tag_id: str, visible: bool) -> None:
        """
        Explicitly override the the visibility based on tag id.  When
        caclulating final visibilities, we first apply overrides to the global
        display attributes using tags, then surface ids.
        """
        if not self._has_tags:
            raise ValueError(f"The scene entity does not have tags.")
        if not tag_id in self._tag_ids:
            raise ValueError(f"Id {tag_id} not a known tag id {self._tag_ids}")
        self._surface_visibilities[tag_id] = visible

    def add_filter(self, filter: Filter) -> None:
        """
        Add a filter to the scene. Filters not currently supported with geometries and will
        raise an error if added.
        """
        if not isinstance(filter, Filter):
            raise TypeError(f"Expected 'Filter', got {type(filter).__name__}")
        if self._entity_type == EntityType.GEOMETRY:
            raise ValueError("Filters with geometries are not currently supported.")
        elif self._entity_type == EntityType.MESH and not isinstance(
            filter, (BoxClip, PlaneClip, Slice)
        ):
            raise ValueError("Only 'BoxClip', 'PlaneClip', and 'Slice' are supported with meshes.")
        self._filters.append(filter)

    def add_color_map(self, color_map: ColorMap) -> None:
        """
        Add a color map to the scene. If a color map with the field
        already exists, it will be overwritten.
        """
        if not isinstance(color_map, ColorMap):
            raise TypeError(f"Expected 'ColorMap', got {type(filter).__name__}")

        # We can only have one color map per field, so check.
        found = False
        for cmap in self._color_maps:
            if cmap.field == color_map.field:
                found = True
                cmap = color_map
                logger.warning("Color map for field already exists. Overwriting.")

        if not found:
            self._color_maps.append(color_map)

    def add_camera(self, camera: DirectionalCamera | LookAtCamera) -> None:
        """
        Add a camera to the scene. Each camera added produces an image.
        """
        if not isinstance(camera, (DirectionalCamera, LookAtCamera)):
            raise TypeError(
                f"Expected 'DirectionalCamera or LookAtCamera, got {type(camera).__name__}"
            )
        self._cameras.append(camera)

    def _validate_surfaces_and_tags(self, ids: List[str]) -> List[str]:
        """
        Validate a list of ids as either tags or ids. Returns a list of invalid ids. If the
        length of the list is zero, the input list is valid.
        """
        bad_ids: List[str] = []
        for id in ids:
            if id in self._tag_ids:
                continue
            if id not in self._surface_ids:
                bad_ids.append(id)
        return bad_ids

    def _validate_filter_connections(self) -> None:
        """
        Validate that the filters have valid connections.
        """
        filter_ids: List[str] = []
        for filter in self._filters:
            filter_ids.append(filter.id)

        for filter in self._filters:
            parent_id = filter.get_parent_id()
            if not parent_id:
                # Using the root when we have an empty string
                continue
            if parent_id not in filter_ids:
                raise ValueError(f"Filter {filter.id} parent {parent_id} not present in filters")

    def _create_request(self, name: str, description: str) -> vis_pb2.CreateExtractRequest:
        req = vis_pb2.CreateExtractRequest()
        if len(self._cameras) == 0:
            raise ValueError("Error: at least one camera required for rendering")

        for camera in self._cameras:
            out_camera = vis_pb2.Camera()
            out_camera.projection = camera.projection.value
            if isinstance(camera, LookAtCamera):
                lookat = cast(LookAtCamera, camera)
                out_camera.look_at.position.CopyFrom(_to_vector3(lookat.position)._to_proto())
                out_camera.look_at.up.CopyFrom(_to_vector3(lookat.up)._to_proto())
                out_camera.look_at.look_at.CopyFrom(_to_vector3(lookat.look_at)._to_proto())
            elif isinstance(camera, DirectionalCamera):
                out_camera.direction = camera.direction.value
            else:
                raise TypeError(f"Internal error: expected 'camera', got {type(camera).__name__}")

            static = vis_pb2.AnimationSettingsStatic()
            static.camera.CopyFrom(out_camera)
            static.label = camera.label
            static.resolution.width = camera.width
            static.resolution.height = camera.height
            req.spec.animation_properties.statics.items.append(static)

        req.spec.global_display_attributes.visible = self.global_display_attrs.visible
        req.spec.global_display_attributes.representation = (
            self.global_display_attrs.representation.value
        )
        req.spec.global_display_attributes.field.component = (
            self.global_display_attrs.field.component.value
        )
        req.spec.global_display_attributes.field.quantity_typ = (
            self.global_display_attrs.field.quantity.value
        )

        for id, visible in self._surface_visibilities.items():
            attrs = vis_pb2.DisplayAttributes()
            attrs.visible = visible
            attrs.field.component = vis_pb2.Field.COMPONENT_X
            attrs.field.quantity_typ = quantitypb.INVALID_QUANTITY_TYPE
            req.spec.display_attributes[id].CopyFrom(attrs)

        self._validate_filter_connections()
        cmap_fields: Dict[Field, bool] = {}
        for filter in self._filters:
            if isinstance(filter, SurfaceStreamlines):
                # Validate surfaces names
                streamlines = cast(SurfaceStreamlines, filter)
                bad_ids = self._validate_surfaces_and_tags(streamlines._surface_names)
                if len(bad_ids) != 0:
                    raise ValueError(f"SurfaceStreamlines has invalid surfaces: {bad_ids}")

            if isinstance(filter, Filter):
                vis_filter: vis_pb2.Filter = filter._to_proto()
                req.spec.filters.append(vis_filter)
                req.spec.display_attributes[filter.id].CopyFrom(filter.display_attrs._to_proto())
            else:
                raise TypeError(f"Expected 'filter', got {type(filter).__name__}")
            if filter.get_parent_id():
                req.spec.filter_connections[filter.get_parent_id()].children_id.append(filter.id)
            if (
                self.auto_color_map_annotations
                and filter.display_attrs.field.quantity != VisQuantity.NONE
                and filter.display_attrs.visible
            ):
                cmap_fields[filter.display_attrs.field] = True

        for cmap in self._color_maps:
            if self.auto_color_map_annotations and not cmap.appearance:
                # Defer color map processing to the auto color annotation.
                continue
            color_map: vis_pb2.ColorMap = cmap._to_proto()
            req.spec.color_maps.append(color_map)

        # Add the automated color maps if enabled. If we don't specify them
        # in the proto, the annotations will not appear in the image.
        if self.auto_color_map_annotations:
            auto_cmaps: List[ColorMap] = []
            for field in cmap_fields:
                found = False
                # Make sure we don't have an explicit color map for this field.
                for cmap in self._color_maps:
                    if field == cmap.field:
                        found = True
                if not found:
                    default_cmap = ColorMap()
                    default_cmap.field = field
                    default_cmap.appearance = ColorMapAppearance()
                    auto_cmaps.append(default_cmap)
            for cmap in self._color_maps:
                if not cmap.appearance:
                    # Include any color maps with no appearance set. We skipped
                    # processing them above
                    cmap.appearance = ColorMapAppearance()
                    auto_cmaps.append(cmap)
            if len(auto_cmaps) != 0:
                # These are all default contructed, so they all have the same dimentions.
                # All the coordinates are in normalized device space.
                assert auto_cmaps[0].appearance != None
                width = auto_cmaps[0].appearance.width
                height = auto_cmaps[0].appearance.height
                x_padding = 0.05
                y_padding = 0.05
                # Placing them on the right side.
                lower_left_x = 1.0 - width - x_padding
                lower_left_y = 1.0 - height - y_padding
                for cmap in auto_cmaps:
                    assert cmap.appearance != None
                    cmap.appearance.lower_left_x = lower_left_x
                    cmap.appearance.lower_left_y = lower_left_y
                    lower_left_y = lower_left_y - height - y_padding
                    if lower_left_y < 0:
                        lower_left_y = 0
                    color_map_proto: vis_pb2.ColorMap = cmap._to_proto()
                    req.spec.color_maps.append(color_map_proto)

        if not isinstance(self.triad_visible, bool):
            raise TypeError(f"Expected 'bool', got {type(self.triad_visible).__name__}")
        req.spec.triad_properties.visible = self.triad_visible

        if not isinstance(self.axes_grid_visible, bool):
            raise TypeError(f"Expected 'bool', got {type(self.axes_grid_visible).__name__}")
        req.spec.axes_grid_properties.visible = self.axes_grid_visible

        bg_color = _to_vector3(self.background_color)._to_proto()
        if not _is_valid_color(bg_color):
            raise ValueError(f"Background color is not in the range [0,1]: {bg_color}")
        req.spec.background_properties.color.r = bg_color.x
        req.spec.background_properties.color.g = bg_color.y
        req.spec.background_properties.color.b = bg_color.z
        req.spec.background_properties.color.a = 1

        req.project_id = self._project_id
        if self._entity_type == EntityType.SIMULATION:
            req.spec.entity_type.simulation.id = self._solution.simulation_id
            req.spec.entity_type.simulation.solution_id = self._solution.id
        elif self._entity_type == EntityType.MESH:
            req.spec.entity_type.mesh.id = self._mesh.id
        elif self._entity_type == EntityType.GEOMETRY:
            req.spec.entity_type.geometry.id = self._geometry.id
        else:
            raise ValueError(f"Unknown entity type: '{self._entity_type}' ")
        req.spec.name = name
        req.spec.description = description
        return req

    def render_images(self, name: str, description: str) -> RenderOutput:
        """
        Create a request to render a images of the scene using the scene's cameras.

        Parameters
        ----------
        name : str
            A short name for the the renders.
        description : str
           A longer description of the scene and renderings.
        """
        req: vis_pb2.CreateExtractRequest = self._create_request(name=name, description=description)
        res: vis_pb2.CreateExtractResponse = get_default_client().CreateExtract(req)
        logger.info("Successfully submitted 'render_images' request")
        return RenderOutput(
            extract_id=res.extract.extract_id,
            project_id=self._project_id,
            name=name,
            desciption=description,
            status=RenderStatusType(res.extract.status),
        )

    def interact(self) -> InteractiveScene:
        """
        Start an interactive display of the scene, when running inside LuminaryCloud's
        AI Notebook environment or Jupyter Lab. The returned object must be displayed
        in the notebook to display the interactive visualization. This requires that
        the luminarycloud package was installed with the optional jupyter feature.
        """
        self._interactive_scene = InteractiveScene(self)
        return self._interactive_scene


def get_render(project_id: str, extract_id: str) -> RenderOutput:
    """
    Get a previously created set of render outputs by project and extract id.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Parameters
    ----------
    project_id : str
        The project id to of the extract.
    extract_id: str
        The id to of the extract.

    """
    req = vis_pb2.GetExtractRequest()
    req.extract_id = extract_id
    req.project_id = project_id
    res: vis_pb2.GetExtractResponse = get_default_client().GetExtract(req)
    output = RenderOutput(
        extract_id=extract_id,
        project_id=project_id,
        name=res.extract.name,
        desciption=res.extract.description,
        status=RenderStatusType(res.extract.status),
    )
    return output


def list_quantities(solution: Solution) -> List[VisQuantity]:
    """
    List the quantity types, including derived quantities, that are available in
    a solution.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Parameters
    ----------
    solution: Solution
        The the solution object to query.

    """
    if not isinstance(solution, Solution):
        raise TypeError(f"Expected 'Solution', got {type(solution).__name__}")
    sim = get_simulation(solution.simulation_id)
    req = vis_pb2.ListSolutionFieldsRequest()
    req.simulation.id = solution.simulation_id
    req.simulation.solution_id = solution.id
    req.project_id = sim.project_id
    res: vis_pb2.ListSolutionFieldsReply = get_default_client().ListSolutionFields(req)
    result: List[VisQuantity] = []
    for q in res.quantities:
        # This will cause a crash if its not in the list. There are a lot of quantities
        # that are not in the list.
        result.append(VisQuantity(q))
    return result


def list_renders(entity: Geometry | Mesh | Solution) -> List[RenderOutput]:
    """
    Lists all previously created renders associated with a project and an entity.

    .. warning:: This feature is experimental and may change or be removed in the future.

    Parameters
    ----------
    project_id : str
        The project id to query.
    entity : Geometry | Mesh | Solution
        Specifies what types of rendering extracts to list(e.g., geometry, mesh or solution).

    """

    # Find out what we are working on.
    entity_type: EntityType = EntityType.GEOMETRY
    if isinstance(entity, Solution):
        entity_type = EntityType.SIMULATION
    elif isinstance(entity, Mesh):
        entity_type = EntityType.MESH
    elif isinstance(entity, Geometry):
        entity_type = EntityType.GEOMETRY
    else:
        raise TypeError(f"Expected Solution, Mesh or Geometry, got {type(entity).__name__}")

    project_id = _get_project_id(entity)
    if not project_id:
        raise ValueError("Unable to get project id from entity")

    req = vis_pb2.ListExtractsRequest()
    req.project_id = project_id

    if entity_type == EntityType.SIMULATION:
        # Make the linter happy
        sim_entity = cast(Solution, entity)
        req.entity.simulation.id = sim_entity.simulation_id
        req.entity.simulation.solution_id = sim_entity.id
    elif entity_type == EntityType.MESH:
        req.entity.mesh.id = entity.id
    elif entity_type == EntityType.GEOMETRY:
        req.entity.geometry.id = entity.id
    else:
        raise ValueError(f"Unknown entity type: '{entity_type}' ")

    res: vis_pb2.ListExtractsResponse = get_default_client().ListExtracts(req)

    results: List[RenderOutput] = []
    for extract in res.extracts:
        result = RenderOutput(
            extract_id=extract.extract_id,
            project_id=extract.project_id,
            name=extract.name,
            desciption=extract.description,
            status=RenderStatusType(extract.status),
        )

        # TODO(matt): the List extracts request is giving us nil for the status.
        # This need to be fixed on the backend, but manually refreshing works for now.
        result.refresh()
        results.append(result)

    return results
