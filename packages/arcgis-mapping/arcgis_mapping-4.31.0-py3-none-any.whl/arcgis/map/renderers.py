import json
import time
from arcgis.map import smart_mapping
from arcgis.map.dataclasses.models.renderers import (
    ColorRamp,
    AuthoringInfoVisualVariable,
    AuthoringInfoStatistics,
    AuthoringInfoClassBreakInfo,
    AuthoringInfoField,
    AuthoringInfo,
    HeatmapColorStop,
    LegendOptions,
    ColorStop,
    ColorInfoVisualVariable,
    RotationInfoVisualVariable,
    SizeStop,
    Size,
    SizeInfoVisualVariable,
    TransparencyStop,
    TransparencyInfoVisualVariable,
    UniqueValueInfo,
    AttributeColorInfo,
    HeatmapRenderer,
    UniqueValueClass,
    UniqueValueGroup,
    UniqueValueRenderer,
    ClassBreakInfo,
    SimpleRenderer,
    DotDensityRenderer,
    StretchRenderer,
    FlowRenderer,
    PredominanceRenderer,
    ClassBreaksRenderer,
    ExpressionInfo,
    DictionaryRenderer,
    OthersThresholdColorInfo,
    PieChartRenderer,
    VectorFieldRenderer,
    TemporalRenderer,
    ColormapInfo,
    RasterShadedReliefRenderer,
    RasterColorMapRenderer,
    ColorClassBreakInfo,
    ColorModulationInfo,
    RendererLegendOptions,
    PointCloudFixedSizeAlgorithm,
    PointCloudSplatAlgorithm,
    PointCloudClassBreaksRenderer,
    PointCloudRGBRenderer,
    PointCloudStretchRenderer,
    ColorUniqueValueInfo,
    PointCloudUniqueValueRenderer,
)

from arcgis.map.dataclasses.enums.renderers import (
    RampAlgorithm,
    ColorRampType,
    HillshadeType,
    ScalingType,
    RatioStyle,
    ValueRepresentation,
    FieldTransformType,
    Axis,
    LengthUnit,
    Theme,
    VisualVariableType,
    TimeUnits,
    UnivariateSymbolStyle,
    StandardDeviationInterval,
    Focus,
    FlowTheme,
    ClassificationMethod,
    RendererType,
    UnivariateTheme,
    LegendOrder,
    StretchType,
    TrailCap,
    FlowRepresentation,
    NormalizationType,
    InputOutputUnit,
    VectorFieldStyle,
)

__all__ = [
    "ColorRamp",
    "AuthoringInfoVisualVariable",
    "AuthoringInfoStatistics",
    "AuthoringInfoClassBreakInfo",
    "AuthoringInfoField",
    "AuthoringInfo",
    "HeatmapColorStop",
    "LegendOptions",
    "ColorStop",
    "ColorInfoVisualVariable",
    "RotationInfoVisualVariable",
    "SizeStop",
    "Size",
    "SizeInfoVisualVariable",
    "TransparencyStop",
    "TransparencyInfoVisualVariable",
    "UniqueValueInfo",
    "AttributeColorInfo",
    "HeatmapRenderer",
    "UniqueValueClass",
    "UniqueValueGroup",
    "UniqueValueRenderer",
    "ClassBreakInfo",
    "SimpleRenderer",
    "DotDensityRenderer",
    "StretchRenderer",
    "FlowRenderer",
    "PredominanceRenderer",
    "ClassBreaksRenderer",
    "ExpressionInfo",
    "DictionaryRenderer",
    "OthersThresholdColorInfo",
    "PieChartRenderer",
    "VectorFieldRenderer",
    "TemporalRenderer",
    "ColormapInfo",
    "RasterShadedReliefRenderer",
    "RasterColorMapRenderer",
    "ColorClassBreakInfo",
    "ColorModulationInfo",
    "RendererLegendOptions",
    "PointCloudFixedSizeAlgorithm",
    "PointCloudSplatAlgorithm",
    "PointCloudClassBreaksRenderer",
    "PointCloudRGBRenderer",
    "PointCloudStretchRenderer",
    "ColorUniqueValueInfo",
    "PointCloudUniqueValueRenderer",
    "RampAlgorithm",
    "ColorRampType",
    "HillshadeType",
    "ScalingType",
    "RatioStyle",
    "ValueRepresentation",
    "FieldTransformType",
    "Axis",
    "LengthUnit",
    "Theme",
    "VisualVariableType",
    "TimeUnits",
    "UnivariateSymbolStyle",
    "StandardDeviationInterval",
    "Focus",
    "FlowTheme",
    "ClassificationMethod",
    "RendererType",
    "UnivariateTheme",
    "LegendOrder",
    "StretchType",
    "TrailCap",
    "FlowRepresentation",
    "NormalizationType",
    "InputOutputUnit",
    "VectorFieldStyle",
]


class RendererManager:
    """
    A class that defines the renderer found on a layer.
    Through this class you can edit the renderer and get information on it.


    .. note::
        This class should not be created by a user but rather called through the `renderer` method on
        a MapContent or GroupLayer instance.
    """

    def __init__(self, **kwargs) -> None:
        # The pydantic layer, this hooks it to the main webmap and tracks changes made
        self._layer = kwargs.pop("layer")
        self._source = kwargs.pop("source")

    def __str__(self) -> str:
        return "Renderer for: " + self._layer.title

    def __repr__(self) -> str:
        return "Renderer for: " + self._layer.title

    @property
    def renderer(
        self,
    ) -> (
        SimpleRenderer
        | HeatmapRenderer
        | PredominanceRenderer
        | DotDensityRenderer
        | FlowRenderer
        | ClassBreaksRenderer
        | DictionaryRenderer
        | PieChartRenderer
        | VectorFieldRenderer
    ):
        """
        Get an instance of the Renderer dataclass found in the layer.
        :return: Renderer dataclass for the layer specified.
        """
        # Return initialized instance of the class
        # Must pass in pydantic class to edit
        renderer = self._layer.layer_definition.drawing_info.renderer

        # pass the renderer through our renderer classes so there are no inconsistencies
        rtype = renderer["type"] if isinstance(renderer, dict) else renderer.type
        renderer_class_mapping = {
            "simple": SimpleRenderer,
            "heatmap": HeatmapRenderer,
            "uniqueValue": PredominanceRenderer,
            "dotDensity": DotDensityRenderer,
            "flowRenderer": FlowRenderer,
            "classBreaks": ClassBreaksRenderer,
            "dictionary": DictionaryRenderer,
            "pieChart": PieChartRenderer,
            "vectorField": VectorFieldRenderer,
        }
        if rtype in renderer_class_mapping:
            # if came from smart_mapping it is a dict else dataclass
            if not isinstance(renderer, dict):
                renderer = renderer.dict()
            return renderer_class_mapping[rtype](**renderer)
        else:
            return renderer

    @renderer.setter
    def renderer(self, new_renderer):
        """
        Set the renderer for the layer.
        :param renderer: The renderer to set for the layer.
        :return: None
        """
        rtype = new_renderer.type

        # Turn it into the corresponding spec class
        if rtype == "simple":
            new_renderer = SimpleRenderer(**new_renderer.dict())
        elif rtype == "heatmap":
            new_renderer = HeatmapRenderer(**new_renderer.dict())
        elif rtype == "uniqueValue":
            new_renderer = PredominanceRenderer(**new_renderer.dict())
        elif rtype == "dotDensity":
            new_renderer = DotDensityRenderer(**new_renderer.dict())
        elif rtype == "flowRenderer":
            new_renderer = FlowRenderer(**new_renderer.dict())
        elif rtype == "classBreaks":
            new_renderer = ClassBreaksRenderer(**new_renderer.dict())
        elif rtype == "dictionary":
            new_renderer = DictionaryRenderer(**new_renderer.dict())
        elif rtype == "pieChart":
            new_renderer = PieChartRenderer(**new_renderer.dict())
        elif rtype == "vectorField":
            new_renderer = VectorFieldRenderer(**new_renderer.dict())
        else:
            raise ValueError("The renderer type provided is not supported.")
        # Set the renderer
        self._layer.layer_definition.drawing_info.renderer = new_renderer
        # Update the webmap to reflect the changes
        self._source._update_source()

    def smart_mapping(self) -> smart_mapping.SmartMappingManager:
        """
        Returns a SmartMappingManager object that can be used to create
        smart mapping visualizations.

        .. note::
            Requires the Map to be rendered in a Jupyter environment.
        """
        return smart_mapping.SmartMappingManager(source=self._source, layer=self._layer)

    def to_template(self) -> bool:
        """
        This method will take the current renderer and save it as an item resource on the Item.
        This will allow the renderer to be used in other web maps and applications. You can also
        share the renderer with other users. Use the Item's Resource Manager to export the renderer
        to a file.

        :return: name of the resource that was added to the resources
        """
        if hasattr(self._source, "item") and self._source.item is not None:
            # Save the renderer dictionary to a json file, add to resources
            resource_manager = self._source.item.resources

            # Get the renderer dictionary and dump to json
            # Add new resource_name with time in milliseconds
            resource_name = (
                self.renderer.type
                + "_renderer_"
                + str(int(time.time() * 1000))
                + ".json"
            )
            json_str = json.dumps(self.renderer.dict(), ensure_ascii=False)

            # Add the json to the resources
            resource_manager.add(
                file_name=resource_name, text=json_str, access="inherit"
            )
            return resource_name
        else:
            # Check that item is not None, else tell user to save map/scene
            raise ValueError(
                "The Map or Scene must be saved as an item before the renderer can be saved as a template."
            )

    def from_template(self, template: str) -> bool:
        """
        This method will take a template and apply it to the current layer.
        The template should be a file that was exported from another layer using the to_template method.
        """
        # First check that template is a json file
        if template.endswith(".json"):
            # Read the file
            with open(template, "r") as f:
                data = json.load(f)

            # Pass the renderer into a dataclass depending on type
            if data["type"] == "simple":
                self.renderer = SimpleRenderer(**data)
            elif data["type"] == "heatmap":
                self.renderer = HeatmapRenderer(**data)
            elif data["type"] == "uniqueValue":
                self.renderer = PredominanceRenderer(**data)
            elif data["type"] == "dotDensity":
                self.renderer = DotDensityRenderer(**data)
            elif data["type"] == "flowRenderer":
                self.renderer = FlowRenderer(**data)
            elif data["type"] == "classBreaks":
                self.renderer = ClassBreaksRenderer(**data)
            elif data["type"] == "dictionary":
                self.renderer = DictionaryRenderer(**data)
            elif data["type"] == "pieChart":
                self.renderer = PieChartRenderer(**data)
            elif data["type"] == "vectorField":
                self.renderer = VectorFieldRenderer(**data)
            else:
                raise ValueError("The renderer type provided is not supported.")
        else:
            raise ValueError("The template must be a json file.")
        return self.renderer
