from __future__ import annotations
from arcgis.auth.tools import LazyLoader

arcgismapping = LazyLoader("arcgis.map")
features = LazyLoader("arcgis.features")
arcgis_layers = LazyLoader("arcgis.layers")
popups = LazyLoader("arcgis.map.popups")
renderers = LazyLoader("arcgis.map.renderers")
smart_mapping = LazyLoader("arcgis.map.smart_mapping")
forms = LazyLoader("arcgis.map.forms")
_models = LazyLoader("arcgis.map.dataclasses.models")


class GroupLayer:
    """
    The Group Layer class provides the ability to organize several sublayers into one
    common layer. Suppose there are several FeatureLayers that all represent
    water features in different dimensions.
    For example, wells (points), streams (lines), and lakes (polygons).
    The GroupLayer provides the functionality to treat them as one layer
    called "Water Features" even though they are stored as separate feature
    layers.


    .. note::
        This class should now be created by a user but rather accessed through
        indexing using the `layers` property on a Map instance.
    """

    def __init__(
        self,
        layer: _models.Layer,
        map: arcgismapping.Map | arcgismapping.Scene,
        parent: GroupLayer | arcgismapping.Map | arcgismapping.Scene,
    ) -> None:
        # Assign the layer dataclass passed in, this allows changes to be tracked
        self._layer: _models.Layer = layer

        # Store the parent: either the map or another group layer
        self._parent: GroupLayer | arcgismapping.Map | arcgismapping.Scene = parent

        # Assign webmap instance associated
        self._source: arcgismapping.Map | arcgismapping.Scene = map

        # Assign the spec and definition based on the type of widget
        if isinstance(map, arcgismapping.Map):
            self._is_map: bool = True
            self._definition: _models.Webmap = map._webmap
        elif isinstance(map, arcgismapping.Scene):
            self._is_map: bool = False
            self._definition: _models.Webscene = map._webscene
        else:
            raise ValueError("Invalid widget type")

    def __str__(self) -> str:
        return "Group Layer"

    def __repr__(self) -> str:
        return "Group Layer: " + self._layer.title

    @property
    def layers(self) -> list:
        """
        Get the list of layers in the group layer.
        """
        # List of layers in the group layer
        all_layers = []

        # Construct layer list
        # Step 1: Get the list of layers found in the dict
        layers: list = self._layer.dict()["layers"]
        for index, sub_layer in enumerate(layers):
            # Enumerate through each layer
            if sub_layer.get("layerType") in [
                "group",
                "GroupLayer",
            ]:
                # If the layer is an instance of group then create a new group layer
                # recursion
                new_layer = GroupLayer(
                    self._layer.layers[index], self._source, parent=self
                )
            else:
                # If the layer is a regular layer, infer the type
                new_layer = self._source._helper._infer_layer(sub_layer)
            # Add the layer to the list of layers
            all_layers.append(new_layer)
        return all_layers

    @property
    def title(self) -> str:
        """
        Get/Set the title of the group layer.
        """
        return self._layer.title

    @title.setter
    def title(self, value: str) -> None:
        """
        Set the title of the group layer.
        """
        self._layer.title = value
        if self._source.legend.enabled:
            # Update so it reflects in the legend and such widgets
            self._source._update_source()

    def popup(self, index: int) -> popups.PopupManager:
        """
        Get an instance of the PopupManager class for the layer specified. Specify the layer through it's
        position in the list of layers. The list of layers can be accessed with the `layers` property.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Required integer specifying the layer who's popup to get. Layer has to be
                                in list of layers of the Group Layer instance. You can get the list of layers
                                by calling the `layers` property on your Group Layer instance.
        ==================      =====================================================================
        """
        layer = self._layer.layers[index]
        if hasattr(layer, "popup_info"):
            return popups.PopupManager(layer=layer, source=self)
        else:
            raise ValueError("The layer type does not support popups.")

    def renderer(self, index: int) -> renderers.RendererManager:
        """
        Get an instance of the RendererManager class for the layer specified. Specify the layer through it's
        position in the list of layers. The list of layers can be accessed with the `layers` property.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Required integer specifying the layer who's renderer to get. Layer has to be
                                in list of layers of the Group Layer instance. You can get the list of layers
                                by calling the `layers` property on your Group Layer instance.
        ==================      =====================================================================
        """
        # Pass in the layer instance from the group layer
        return renderers.RendererManager(layer=self._layer.layers[index], source=self)

    def layer_visibility(self, index: int) -> arcgismapping.map_widget.LayerVisibility:
        """
        Get an instance of the LayerVisibility class for the layer specified. Specify the layer through it's
        position in the list of layers. The list of layers can be accessed with the `layers` property.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Required integer specifying the layer who's layer visibility to get. Layer has to be
                                in list of layers of the Group Layer instance. You can get the list of layers
                                by calling the `layers` property on your Group Layer instance.
        ==================      =====================================================================
        """
        # Pass in the layer instance from the group layer
        return arcgismapping.map_widget.LayerVisibility(self._layer.layers[index])

    def form(self, index: int) -> forms.FormInfo:
        """
        Get an instance of the FormInfo class for the layer specified. Specify the layer through it's
        position in the list of layers. The list of layers can be accessed with the `layers` property.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Required integer specifying the layer who's form to get. Layer has to be
                                in list of layers of the Group Layer instance. You can get the list of layers
                                by calling the `layers` property on your Group Layer instance.

                                Forms are only supported for Feature Layers, Tables, and Oriented Imagery Layers.
        ==================      =====================================================================

        :return: FormInfo dataclass for the layer specified.
        To see this dataclass, see the forms module where it is defined. You can also get the dataclass as a dict
        by calling the `dict` method on the dataclass.

        """
        # Pass in the layer instance from the group layer
        form_info = self._layer.layers[index].form_info
        if form_info is None:
            return None
        else:
            return forms.FormInfo(**form_info.dict())

    def update_layer(
        self,
        index,
        labeling_info=None,
        renderer=None,
        scale_symbols=None,
        transparency=None,
        options=None,
        form=None,
    ) -> None:
        """
        This method can be used to update certain properties found in a layer within a group layer in your map.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Optional integer specifying the index for the layer you want to update.
                                To see a list of layers use the layers property. This cannot be a group layer.
                                To update a layer in a GroupLayer, use the `update_layer` method in the group layer class.
        ------------------      ---------------------------------------------------------------------
        labeling_info           Optional list of dictionaries. Defines the properties used for labeling the layer.

                                Example of some properties:
                                labeling_info = [{
                                    "labelExpression": '[FAA_ID]',
                                    "maxScale": 0,
                                    "minScale": 10000,
                                    "symbol": <Symbol Dataclass>
                                    }
                                }]
        ------------------      ---------------------------------------------------------------------
        renderer                Optional dictionary representing the renderer properties for the layer
                                to be updated with.

                                Example:
                                renderer = SimpleRenderer(**{
                                    'type': 'simple',
                                    'symbol': {
                                        'type': 'esriPMS',
                                        'url': 'RedSphere.png',
                                        'imageData': '{data}',
                                        'contentType': 'image/png',
                                        'width': 15,
                                        'height': 15}
                                    })
        ------------------      ---------------------------------------------------------------------
        scale_symbols           Optional bool. Indicates whether symbols should stay the same size in
                                screen units as you zoom in. False means the symbols stay the same size
                                in screen units regardless of the map scale.
        ------------------      ---------------------------------------------------------------------
        transparency            Optional int. Value ranging between 0 (no transparency) to 100 (completely transparent).
        ------------------      ---------------------------------------------------------------------
        options                 Optional dictionary. Pass in key, value pairs that will edit the layer properties.
                                This is useful for updating the layer properties that are not exposed through
                                the other parameters. For example, you can update the layer title, opacity, or other
                                properties that are applicable for the type of layer.
        ------------------      ---------------------------------------------------------------------
        form                    Optional FormInfo Dataclass. See the forms module where all the dataclasses are defined.
                                You can get the current FormInfo by calling the `form` property and indicating the index
                                of the layer you want to get the form for.
                                Forms are only supported for Feature Layers, Tables, and Oriented Imagery Layers.
        ==================      =====================================================================
        """
        # Get layer from list (should not be pydantic)
        # We will edit pydantic layer after, this needs to be passed into method
        layer = self.layers[index]
        # Error check
        if isinstance(layer, GroupLayer):
            raise ValueError(
                "The layer cannot be of type Group Layer. Use the `update_layer` method found in the Group Layer class."
            )

        if not (
            isinstance(layer, features.FeatureCollection)
            or isinstance(layer, features.FeatureLayer)
            or isinstance(layer, arcgis_layers.GeoJSONLayer)
            or isinstance(layer, arcgis_layers.CSVLayer)
        ):
            raise ValueError(
                "Only Feature Collections, Feature Layers, GeoJSON Layers, and CSV Layers can be edited."
            )

        # Create drawing info dict
        drawing_info = {}

        if renderer:
            drawing_info["renderer"] = renderer
        if scale_symbols in [True, False]:
            drawing_info["scale_symbols"] = scale_symbols
        if labeling_info:
            drawing_info["labeling_info"] = labeling_info
        if transparency is not None:
            drawing_info["transparency"] = transparency

        # Create the layer definition
        if drawing_info:
            new_ld = self._source._helper._create_ld_dict(layer, drawing_info)

            # Assign the new layer definition to the pydantic layer
            self._layer.layers[index].layer_definition = new_ld

        if options is not None:
            # make the edits straight in the webmap definition
            layer = self._definition.operational_layers[index]
            # if an options dictionary was passed in, set the available attributes
            for key, value in options.items():
                # make sure key is in snake case
                key = "".join(
                    ["_" + c.lower() if c.isupper() else c for c in key]
                ).lstrip("_")
                if hasattr(layer, key):
                    setattr(layer, key, value)

        # Update the webmap dict on the widget so layer changes are reflected
        self._source._update_source()

        if form is not None:
            form_info = forms.FormInfo(**form.dict())
            # Update the form
            self._layer.layers[index].form_info = form_info

    def reposition(self, current_index: int, new_index: int) -> None:
        """
        Reposition a layer in the Group Layer's layers. You can do this by specifying the index of the current
        layer you want to move and what index it should be at.

        This method is useful if you have overlapping layers and you want to manage the order in which
        they are rendered on your map.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        current_index           Required int. The index of where the layer currently is in the list of layers.
                                You can see the list of layers by calling the `layers` property on your
                                Group Layer instance.
        ------------------      ---------------------------------------------------------------------
        new_index               Required int. The index you want to move the layer to.
        ==================      =====================================================================

        """
        # Insert back into the group layers at the new index
        self._layer.layers.insert(new_index, self._layer.layers.pop(current_index))
        self.layers.insert(new_index, self.layers.pop(current_index))

        # Update the webmap dict on the widget so layer changes are reflected
        self._source._update_source()

    def move(self, index: int, group: GroupLayer | None = None) -> None:
        """
        Move a layer from it's group into another GroupLayer or into 'No Group' which means it will be
        moved to the main Map's layers.

        You can use this method on a GroupLayer and the entire GroupLayer will be added to another group
        or be added to the main Map's layers.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Required int. The index of the layer you want to move. You can see the
                                list of layers by calling the `layers` property on your Group Layer instance.
        ------------------      ---------------------------------------------------------------------
        group                   Optional GroupLayer. The group layer you want to move the layer to.
                                If you want to move the layer to the main Map's layers, pass in None
        ==================      =====================================================================
        """
        # Get the layer from the list of layers
        layer = self.layers[index]

        # If the title is 'No Group' then we want to move the layer to the main map's layers
        if group is None:
            # Remove the layer from the group layer
            self._layer.layers.pop(index)
            # Add the layer to the main map's layers
            if isinstance(layer, GroupLayer):
                self._source.content.layers.append(layer)
                self._source._webmap.operational_layers.extend(layer._layer)
            else:
                self._source.content.add(layer)
        else:
            # Remove the layer from the group layer
            self._layer.layers.pop(index)
            # Add the layer to the group layer
            group.layers.append(layer)
            if isinstance(layer, GroupLayer):
                group._layer.layers.append(layer._layer)
            else:
                group._layer.layers.append(layer)

        # Update the webmap dict on the widget so layer changes are reflected
        self._source._update_source()

    def ungroup(self) -> None:
        """
        Ungroup a GroupLayer. This will send the layer to the parent's layers.
        If the parent is Map, then all the layers in the GroupLayer will be sent to the Map's layers and the GroupLayer removed.
        If the parent is another GroupLayer, then all the layers in the GroupLayer will be sent to the parent's layers and the GroupLayer removed.
        """
        # If the parent is a map, then we want to send the layers to the map's layers
        if isinstance(self._parent, arcgismapping.Map):
            # Remove the group layer from the map's layers
            self._source.content.layers.remove(self)
            self._source._webmap.operational_layers.remove(self._layer)
            # Add the layers to the map's layers
            self._source.content.layers.extend(self.layers)
            self._source._webmap.operational_layers.extend(
                [layer for layer in self._layer.layers]
            )
        else:
            # Remove the group layer from the parent's layers
            self._parent.layers.remove(self)
            self._parent._layer.layers.remove(self._layer)
            # Add the layers to the parent's layers
            self._parent.layers.extend(self.layers)
            self._parent._layer.layers.extend([layer for layer in self._layer.layers])

        # Update the webmap dict on the widget so layer changes are reflected
        self._source._update_source()

    def remove_layer(self, index: int) -> None:
        """
        Remove a layer from the Group Layer's layers. You can do this by specifying the index of the current
        layer you want to remove.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Required int. The index of the layer you want to remove.
                                You can see the list of layers by calling the `layers` property on your
                                Group Layer instance.
        ==================      =====================================================================

        """
        self._layer.layers.pop(index)
        self._source._update_source()
