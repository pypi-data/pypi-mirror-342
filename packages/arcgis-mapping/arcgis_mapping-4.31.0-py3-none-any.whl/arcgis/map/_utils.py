from __future__ import annotations
import logging
from arcgis.auth.tools import LazyLoader
import copy
from traitlets import link
from typing import Optional, Union, Any
import base64
from functools import cached_property


# Import methods from modules
auth = LazyLoader("arcgis.auth._auth._schain")
arcgis = LazyLoader("arcgis")
arcgismapping = LazyLoader("arcgis.map")
basemapdef = LazyLoader("arcgis.map.definitions._basemap_definitions")
basemapdef3d = LazyLoader("arcgis.map.definitions._3d_basemap_definitions")
rm = LazyLoader("arcgis.map.definitions._renderer_metaclass")
env = LazyLoader("arcgis.env")
features = LazyLoader("arcgis.features")
json = LazyLoader("json")
arcgis_layers = LazyLoader("arcgis.layers")
pd = LazyLoader("pandas")
geocoding = LazyLoader("arcgis.geocoding")
realtime = LazyLoader("arcgis.realtime")
raster = LazyLoader("arcgis.raster")
uuid = LazyLoader("uuid")
_gis_mod = LazyLoader("arcgis.gis")
os = LazyLoader("os")
arcgis_utils = LazyLoader("arcgis._impl.common._utils")
arcgis_cm = LazyLoader("arcgis._impl._content_manager")
geoprocessing = LazyLoader("arcgis.geoprocessing")
urllib = LazyLoader("urllib")
_models = LazyLoader("arcgis.map.dataclasses.models")
_model_enums = LazyLoader("arcgis.map.dataclasses.enums")


class _HelperMethods:
    """
    The Helper Methods class defines the methods that are used in both the Map and Scene classes. This facilitates
    upkeep since many similarities can be found and we store them in one place.

    The class is instantiated with either an instance of Map or Scene and the spec used depends on this.
    Not all layers are in the webmap spec and vise versa. So it is up to the documentation in the respective classes
    to clearly state what layers can and cannot be added. This is an example of a minor difference but there are others as well.

    When making edits, consult the documentation for each method found in each widget class as well as their respective specs.

    There are four main properties on the class that are used throughout the methods:
    - spec: The spec used to validate depends on the widget type. This is either the webmap spec or the webscene spec.
    - _source: The class instance which is either Map or Scene. This is important to grab methods and properties from there such as layers, extent, gis, etc.
    - pydantic_class: This represents the pydantic dataclass we are manipulating throughout each property and method. This can be found in the Map class as _webmap and in the Scene class as _webscene.
    - is_map: A boolean to determine if the widget is a Map or Scene. This is used to determine which spec to use and some other minor differences.
    """

    def __init__(self, widget: arcgismapping.Map | arcgismapping.Scene) -> None:
        # Map and Scene will be referred to as widget since they share commonality of being DOMWidgets.
        self._source: arcgismapping.Map | arcgismapping.Scene = widget

        # The spec used to validate depends on the widget type
        if isinstance(widget, arcgismapping.Map):
            self.is_map = True
        elif isinstance(widget, arcgismapping.Scene):
            self.is_map = False
        else:
            raise ValueError("Invalid widget type")

    ############################## Map and Scene Setup Methods ##############################
    def _set_widget_definition(self, definition):
        """
        This is a method to avoid circular reference. Once the definition has been created in the widget, this
        method is called and the definition is assigned. This method is called in the widget constructors.

        This represents the pydantic dataclass we are manipulating throughout each property and method.
        For a Map it is the pydantic Webmap class and for a Scene it is the pydantic Webscene class, each found
        in their respective spec files.

        In the map this property is called `_webmap` and in the scene it is called `_webscene`.
        """
        self.pydantic_class: _models.Webmap | _models.Webscene = definition

    def _setup_gis_properties(self, gis):
        if gis is None:
            # If no active gis then login as anonymous user
            gis: _gis_mod.GIS = (
                env.active_gis if env.active_gis else _gis_mod.GIS(set_active=False)
            )
        # gis property on the widget
        self._source._gis: _gis_mod.GIS = gis

        # Determine if tokenBased or anonymous, used for typescript side
        if hasattr(gis.session.auth, "token") and gis._session.auth.token:
            self._source._portal_token = str(gis._session.auth.token)
            self._source._auth_mode = "tokenBased"
        elif isinstance(
            gis._session.auth,
            (auth._MultiAuth, auth.SupportMultiAuth),
        ) and hasattr(self._source._gis._session.auth, "authentication_modes"):
            tokens = [
                auth.token
                for auth in gis._session.auth.authentication_modes
                if hasattr(auth, "token")
            ]
            if tokens:
                self._source._portal_token = str(tokens[0])
                self._source._auth_mode = "tokenBased"
            else:
                self._source._auth_mode = "anonymous"
        else:
            self._source._auth_mode = "anonymous"

        # Set the properties that aren't dependent on auth mode
        self._source._portal_rest_url = self._get_portal_url()
        self._source._username = str(gis._username)
        self._source._proxy_rule = self._get_proxy_rule()

        self._check_js_cdn_variable()

    def _check_js_cdn_variable(self):
        """
        Check if the JS API CDN variable is set and if not, set it.
        """
        # Look if env variable is set
        self._source.js_api_path = os.getenv("JSAPI_CDN", "")

    def _get_portal_url(self):
        """
        Get the portal url to be used.
        """
        try:
            # public rest url
            return self._source._gis._public_rest_url
        except Exception:
            pass
        # gis url
        return self._source._gis.url

    def _get_proxy_rule(self):
        """
        Get the proxy configuration to be used.
        """
        return self._source._gis.session.proxies or {}

    def _setup_location_properties(self, location, geocoder):
        """
        Set up the widget properties to be used.
        """
        if location:
            # If user gave location, set camera based on location
            self._geocode_location(location, geocoder)
        else:
            # check if initial state is defined
            target_geom = (
                self.pydantic_class.initial_state.viewpoint.target_geometry
                if self.pydantic_class.initial_state
                else None
            )

            # Set extent based on org settings or default
            # target geom might only be spatial reference and nothing else
            if target_geom and target_geom.xmin is not None:
                if (
                    not hasattr(target_geom, "spatial_reference")
                    or target_geom.spatial_reference.wkid is None
                ):
                    # If no spatial reference, set it
                    target_geom.spatial_reference = _models.SpatialReference(
                        **{
                            "latestWkid": 3857,
                            "wkid": 102100,
                        }
                    )
                # set extent based on target geometry. Must be dictionary.
                self._source.extent = target_geom.dict()
            elif "defaultExtent" in self._source._gis.org_settings:
                # If no viewpoint, then see if default in org settings
                org_extent = self._source._gis.org_settings["defaultExtent"]
                if "spatialReference" not in org_extent:
                    org_extent["spatialReference"] = {
                        "latestWkid": 3857,
                        "wkid": 102100,
                    }
                self._source.extent = org_extent
            else:
                # Last resort
                self._source.extent = {
                    "spatialReference": {"latestWkid": 3857, "wkid": 102100},
                    "xmin": -13034068.816148141,
                    "ymin": 4021158.323305902,
                    "xmax": -13014692.029477874,
                    "ymax": 4036445.728962917,
                }

        self._fix_webmap_initial_state()

    def _geocode_location(self, location, geocoder):
        """
        If a location was given, geocode and find the correct points to set
        """
        if isinstance(location, str):
            # get the geocoder(s)
            geocoders = (
                [geocoder]
                if geocoder and isinstance(geocoder, geocoding.Geocoder)
                else geocoding.get_geocoders(self._source._gis)
            )

            # geocode
            for geocoder in geocoders:
                locations = geocoding.geocode(
                    location,
                    out_sr=102100,
                    max_locations=1,
                    geocoder=geocoder,
                )
                if locations:
                    # set properties based on location
                    loc = locations[0]
                    self._source.center = [
                        loc["location"]["y"],
                        loc["location"]["x"],
                    ]
                    extent = loc["extent"] if "extent" in loc else None
                    if extent and "spatialReference" not in extent:
                        extent["spatialReference"] = {
                            "latestWkid": 3857,
                            "wkid": 102100,
                        }
                    self._source.extent = extent
                    break

    def _fix_webmap_initial_state(self):
        """
        Fix the initial state of the webmap if it is None.
        """
        # reference _webmap or _webscene initial state class
        initial_state = self.pydantic_class.initial_state
        if (
            not initial_state
            or not initial_state.viewpoint.target_geometry
            or initial_state.viewpoint.target_geometry.xmin is None
        ):
            if self.is_map:
                viewpoint = _models.MapViewpoint(
                    rotation=0, targetGeometry=self._source.extent
                )
                if not initial_state:
                    # create the initial state class
                    self.pydantic_class.initial_state = _models.MapInitialState(
                        viewpoint=viewpoint
                    )
                else:
                    # set target geometry extent to the extent of the map
                    self.pydantic_class.initial_state.viewpoint.target_geometry = (
                        _models.Extent(**self._source.extent)
                    )
            else:
                # Create camera dataclass for scene
                camera = _models.Camera(
                    tilt=0.0,
                    position={
                        "spatialReference": {
                            "latestWkid": 3857,
                            "wkid": 102100,
                        },
                        "x": (self._source.extent["xmin"] + self._source.extent["xmax"])
                        / 2,
                        "y": (self._source.extent["ymin"] + self._source.extent["ymax"])
                        / 2,
                        "z": 3000000,
                    },
                    heading=0.0,
                )
                # set on traitlet
                self._source.camera = camera.dict()
                # set on _webscene dataclass
                self.pydantic_class.initial_state.viewpoint = _models.SceneViewpoint(
                    camera=camera
                )

    ############################## MapContent Methods ##############################
    @property
    def _tables(self):
        """
        A list of tables that can be found on the scene.
        """
        tables = []
        # Get the tables from the dataclass
        map_tables = self.pydantic_class.tables or []
        # Create Table objects
        for table in map_tables:
            t = features.Table(table.url)
            tables.append(t)
        return tables

    @property
    def _layers(self):
        """
        A list of layers that can be found on the scene. This is called when
        the Webscene is initialized if pre-existing layers are in the Webscene.
        After that the layers will be added and removed from the `layers` property.
        """
        layers = []
        operational_layers = self.pydantic_class.operational_layers or []
        for index, layer in enumerate(operational_layers):
            # index needed when dealing with group layers
            l = self._infer_layer(layer, index)
            if l:
                layers.append(l)
        return layers

    def _infer_layer(self, layer, index=None):
        """
        Infer the layer instance to be created and added to the list.
        """

        # layer mapping for group layer creation
        layer_type_mapping = {
            "GroupLayer": lambda *args, **kwargs: arcgismapping.GroupLayer(
                self.pydantic_class.operational_layers[index],
                self._source,
                self._source,
            ),
        }

        # define the needed variables
        layer_instance = None
        layer = layer.dict() if not isinstance(layer, dict) else layer

        layer_type = layer.get("layerType")
        layer_url = layer.get("url")
        item_id = layer.get("itemId")

        if layer_type == "GroupLayer":
            # Group Layers
            layer_class = layer_type_mapping.get(layer_type, _gis_mod.Layer)
            return layer_class(layer_url, gis=self._source._gis)

        if layer_url:
            return arcgis_layers.Service(layer_url, server=self._source._gis)
        if item_id:
            try:
                item_url = self._source._gis.content.get(item_id).url
                return arcgis_layers.Service(item_url, server=self._source._gis)
            except Exception as e:
                try:
                    item = self._source._gis.content.get(item_id)
                    if item is None:
                        raise ValueError(f"Item with id {item_id} not found.")
                except Exception as e:
                    raise Exception(f"Error: {e}")
                raise Exception(f"Error: {e}")

        return layer_instance

    def _get_layer_definition(self, layer):
        """
        Method that determines where the layer definition will come from.
        This definition gets returned for further editing.
        """
        if self.is_map and isinstance(layer, _models.FeatureCollection):
            # Get the layer definition from pydantic feature collection properties
            return layer.layers[0].layer_definition

        if isinstance(layer, features.FeatureLayer) and layer.properties.get(
            "serviceItemId"
        ):
            item = self._source._gis.content.get(layer.properties["serviceItemId"])
            item_data = None
            if item:
                item_data = item.get_data()
            if item_data and "layers" in item_data:
                for l in item_data["layers"]:
                    # Hierarchy states that service layer definition will go above layer properties layer definition.
                    # Find the layer definition that matches the id for the layer we are adding.
                    if l["id"] == layer.properties["id"] and "layerDefinition" in l:
                        layer_def = (
                            copy.deepcopy(dict(layer.properties)) | l["layerDefinition"]
                        )
                        break
                else:
                    # If specific layer was not defined, use layer properties
                    layer_def = copy.deepcopy(dict(layer.properties))
            else:
                # If no definition in service, use layer properties
                layer_def = copy.deepcopy(dict(layer.properties))

            # Edit renderer for feature layer
            # There is a hierarchy of where the renderer comes from (if provided by user, edited later in code)
            drawing_info = (
                layer_def["drawingInfo"] if "drawingInfo" in layer_def else {}
            )
            if drawing_info != {} and "renderer" in drawing_info:
                # above we checked for service vs layer. But now we need to make sure the layer didn't have a different
                # renderer than it's own properties. Set in the layer visualization tab.
                if layer.renderer != drawing_info["renderer"]:
                    layer_def["drawingInfo"]["renderer"] = dict(layer.renderer)
        else:
            if "layerDefinition" in layer.properties:
                layer_def = dict(layer.properties["layerDefinition"])
            else:
                layer_def = dict(layer.properties)

        return layer_def

    def _fix_fields_type(self, layer_def):
        field_types = {
            "blob": "esriFieldTypeBlob",
            "date": "esriFieldTypeDate",
            "double": "esriFieldTypeDouble",
            "geometry": "esriFieldTypeGeometry",
            "global_id": "esriFieldTypeGlobalID",
            "guid": "esriFieldTypeGUID",
            "integer": "esriFieldTypeInteger",
            "oid": "esriFieldTypeOID",
            "raster": "esriFieldTypeRaster",
            "single": "esriFieldTypeSingle",
            "small_integer": "esriFieldTypeSmallInteger",
            "string": "esriFieldTypeString",
            "xml": "esriFieldTypeXML",
            "esriFieldTypeBigInteger": "esriFieldTypeDouble",
            "esriFieldTypeDateOnly": "esriFieldTypeDate",
            "esriFieldTypeTimeOnly": "esriFieldTypeString",
            "esriFieldTimestampOffset": "esriFieldTypeString",
        }
        for field in layer_def["fields"]:
            field["type"] = field_types.get(field["type"], field["type"])
        return layer_def

    def _create_ld_dict(self, layer, drawing_info):
        """
        Create the layer definition for the layer.
        This method is being applied to: Feature Collection, Feature Layer, CSV Layer, and GeoJSON Layer.

        This is a rare case where we use a dictionary rather than the dataclass. This is because the layer definition
        dataclass is very rigid depending on the layer type and we need to be able to edit it in a more flexible way.
        It will become a dataclass when passed into the layer dataclasses when added to map.

        :return: layer_definition dict
        """
        # Get the original layer definition
        layer_def = self._get_layer_definition(layer)

        # For certain workflows (draw) we are given a dataclass, make it a dict
        if isinstance(layer_def, _models.LayerDefinition):
            layer_def = layer_def.dict()
        # If layer definition has a layerDefinition property, merge it with the layer definition
        # one big happy layer definition
        if "layerDefinition" in layer_def:
            layer_def.update(layer_def["layerDefinition"])

        # This is a webmap spec necessity
        if "type" not in layer_def or layer_def["type"] not in [
            "Feature Layer",
            "Table",
        ]:
            layer_def["type"] = "Feature Layer"

        # Field types need to be corrected in some cases
        if "fields" in layer_def:
            layer_def = self._fix_fields_type(layer_def)

        # If htmlPopupType is null change to correct None type
        if (
            "htmlPopupType" in layer_def
            and layer_def["htmlPopupType"] == "esriServerHTMLPopupTypeNull"
        ):
            layer_def["htmlPopupType"] = "esriServerHTMLPopupTypeNone"

        # Needed if id is not an integer. For example with geojson layers
        if "id" in layer_def and not isinstance(layer_def["id"], int):
            del layer_def["id"]

        if drawing_info:
            if isinstance(drawing_info, dict):
                if "renderer" in drawing_info:
                    if drawing_info["renderer"] is not None:
                        if not isinstance(drawing_info["renderer"], dict):
                            # make renderer dataclass into dict.
                            # seems like extra step but we renamed some dataclasses for users
                            # this will normalize the names
                            drawing_info["renderer"] = drawing_info["renderer"].dict()

                        # Create renderer dataclass from spec
                        drawing_info["renderer"] = rm.FactoryWorker(
                            renderer_type=drawing_info["renderer"]["type"],
                            renderer=drawing_info["renderer"],
                        )

                # drawing info spelled differently in webmap and webscene
                if "drawingInfo" in layer_def:
                    layer_def["drawingInfo"] = layer_def["drawingInfo"] | drawing_info
                elif "drawing_info" in layer_def:
                    layer_def["drawingInfo"] = layer_def["drawing_info"] | drawing_info
                    del layer_def["drawing_info"]
                else:
                    layer_def["drawingInfo"] = drawing_info

        # Handle time info for certain layers
        if (
            self.is_map
            and "timeInfo" in layer_def
            and layer_def["timeInfo"] is not None
        ):
            if "timeIntervalUnits" in layer_def["timeInfo"]:
                try:
                    layer_def["timeInfo"]["timeIntervalUnits"] = (
                        _model_enums.TimeIntervalUnits(
                            layer_def["timeInfo"]["timeIntervalUnits"]
                        )
                    )
                except Exception:
                    layer_def["timeInfo"][
                        "timeIntervalUnits"
                    ] = _model_enums.TimeIntervalUnits.esri_time_units_unknown

        # Handle capabilities for certain layers
        if "capabilities" in layer_def and isinstance(layer_def["capabilities"], list):
            layer_def["capabilities"] = ",".join(layer_def["capabilities"])

        # Return LayerDefinition Dataclass for further use
        return layer_def

    def _create_popup_dataclass(self, layer, popup_info):
        """
        This method will create the popup info with user input as well as existing info in
        either the item data or the layer properties.

        What is important to know:
            - It is ok if this returns None or empty dict (unlike _create_ld_dict)

        :return: PopupInfo Dataclass or None
        """
        # Get the original popup info
        if self.is_map and isinstance(layer, _models.FeatureCollection):
            orig_popup_info = layer.layers[0].popup_info or {}
        else:
            props = dict(layer.properties)
            orig_popup_info = props.get("popupInfo", {})

            # If the layer is a feature layer, we need to get the popup info from the item data
            if isinstance(layer, features.FeatureLayer) and layer.properties.get(
                "serviceItemId"
            ):
                item = self._source._gis.content.get(layer.properties["serviceItemId"])
                item_data: dict | None = None
                if item:
                    item_data = item.get_data()
                if item_data and "layers" in item_data:
                    for l in item_data["layers"]:
                        if l["id"] == layer.properties["id"] and "popupInfo" in l:
                            orig_popup_info = l["popupInfo"]
                            break

        # Create pydantic popup info
        if not isinstance(popup_info, dict):
            popup_info = popup_info.dict() if popup_info else {}
        popup_info = orig_popup_info | popup_info if popup_info else orig_popup_info

        if popup_info is not None and popup_info != {}:
            return _models.PopupInfo(**popup_info)
        else:
            return None

    def _normalize_feature_collection(self, fc):
        # Ensure consistent format
        if "featureSet" in fc.properties:
            fc.properties = {
                "layers": [
                    {
                        "featureSet": fc.properties["featureSet"],
                        "layerDefinition": fc.properties["layerDefinition"],
                    }
                ]
            }
        else:
            fc.properties = dict(fc.properties)
        return fc

    def _create_layer_from_feature_collection(
        self, fc, drawing_info, popup_info, index
    ):
        """
        This methods goes through the steps of taking a feature collection and creating
        a layer that will be added to the map.

        What is important to know:
            - Feature Collections have various schemas depending on what they were created from
            - We need to create a feature layer out of the feature collection
            - Feature Collection will be added to the `layers` property.

        """
        fc = self._normalize_feature_collection(fc)

        # Set the title
        title = fc.properties["layers"][0]["layerDefinition"].get(
            "name", uuid.uuid4().hex[0:7]
        )

        # Add as a feature collection to the list of layers
        self._source.content.layers.append(fc)

        # Create pydantic feature collection and layer definition
        layers = fc.properties["layers"]

        # need to add a screening for fields of type 'esriFieldTypeBigInteger', 'esriFieldTypeDateOnly', 'esriFieldTypeTimeOnly', and 'esriFieldTimestampOffset'
        for layer in layers:
            layer_def = layer["layerDefinition"]
            layer_def_fixed = self._fix_fields_type(layer_def)
            layer["layerDefinition"] = layer_def_fixed

        fc = _models.FeatureCollection(layers=layers)
        ld = self._create_ld_dict(fc, drawing_info)
        popup_info = self._create_popup_dataclass(fc, popup_info)

        # Create pydantic Feature Layer with the feature collection and layer definition
        geometry_mapping = {
            "esriGeometryPoint": "point",
            "esriGeometryMultipoint": "multipoint",
            "esriGeometryPolyline": "polyline",
            "esriGeometryPolygon": "polygon",
        }
        sr: dict = {
            "latestWkid": 3857,
            "wkid": 102100,
        }  # sets default SpatialReference
        for layer in fc.layers:
            if (
                hasattr(layer, "layer_definition")
                and hasattr(layer.layer_definition, "spatial_reference")
                and not getattr(layer.layer_definition, "spatial_reference", None)
                is None
            ):
                sr: dict = layer.layer_definition.spatial_reference.model_dump(
                    mode="python",
                    include=None,
                    exclude=None,
                    by_alias=True,
                    exclude_unset=False,
                    exclude_defaults=False,
                    exclude_none=True,
                    round_trip=False,
                    warnings=True,
                )
        return _models.FeatureLayer(
            featureCollection=fc,
            layerDefinition=ld,
            popupInfo=popup_info,
            title=title,
            id=uuid.uuid4().hex[0:12],
            geometryType=geometry_mapping[ld.get("geometry_type", "esriGeometryPoint")],
            fields=ld.get("fields", []),
            objectIdField=ld.get("object_id_field"),
            spatialReference=sr,
            source=fc.layers[0].feature_set.features,
        )

    def _get_rendering_rule(self, layer):
        """
        Get the rendering rule for the layer. This is used for imagery layers.
        """
        _lyr = layer._lyr_json
        if "options" in _lyr:
            lyr_options = json.loads(_lyr["options"])
            if "imageServiceParameters" in lyr_options:
                if "renderingRule" in lyr_options["imageServiceParameters"]:
                    if lyr_options["imageServiceParameters"]["renderingRule"] == {}:
                        return None
                    rr = lyr_options["imageServiceParameters"]["renderingRule"]
                    if "function" in rr:
                        ## if it is a Raster function template (case from RFT class), then we need to set the RFT as a value for the rasterFunctionDefinition key
                        rr = {"rasterFunctionDefinition": rr}
                    return rr

        return None

    def _get_mosaic_rule(self, layer):
        """
        Get the mosaic rule for the layer. This is used for imagery layers.
        """
        _lyr = layer._lyr_json
        if "options" in _lyr:
            lyr_options = json.loads(_lyr["options"])
            if "imageServiceParameters" in lyr_options:
                if "mosaicRule" in lyr_options["imageServiceParameters"]:
                    if lyr_options["imageServiceParameters"]["mosaicRule"] == {}:
                        return None
                    return lyr_options["imageServiceParameters"]["mosaicRule"]

        return None

    def _get_datastore_raster(self, layer):
        _lyr = layer._lyr_json
        if "options" in _lyr:
            lyr_options = json.loads(_lyr["options"])
            if "imageServiceParameters" in lyr_options:
                if "raster" in lyr_options["imageServiceParameters"]:
                    ras = lyr_options["imageServiceParameters"]["raster"]
                    if isinstance(ras, dict):
                        # if the layer is a tiles only service or if allow raster function is set to False but allow analysis is true, the if a raster function is applied then the input will be a dictionary which needs to be base 64 encoded
                        import base64

                        encoded_dict = str(ras).encode("utf-8")
                        ras = base64.b64encode(encoded_dict)
                    return ras
        return None

    def _get_base64_data_url(self, layer):
        img = layer.export_image(
            size=[400, 400], export_format="PNG", bbox=layer.extent
        )
        base64_data = base64.b64encode(img.data).decode("utf-8")
        return f"data:image/png;base64,{base64_data}"

    def _add_local_raster(self, layer, options):
        # trigger the traitlet to update the JS code
        opacity = 1
        if "opacity" in options.keys():
            opacity = options["opacity"]

        self._source._local_image_data = {
            "image": self._get_base64_data_url(layer),
            "extent": layer.extent,
            "opacity": opacity,
        }
        return None

    def _create_layer_from_item(
        self, layer, drawing_info=None, popup_info=None, options=None
    ):
        """
        This method goes through the steps of taking an existing layer or item from a user's
        portal and adding it to the map either as a single layer or as a Group Layer.

        What is important to know:
            - Per the JS API, when an item with multiple layers is added, its layers automatically become a Group Layer on the map
        """
        if not options:
            options = {}
        if isinstance(layer, raster.Raster):
            if isinstance(layer._engine_obj, raster._ImageServerRaster):
                layer = layer._engine_obj

        if isinstance(layer, (_gis_mod.Item, list)):
            # Map Service Items will have layers stored within and we do not add one by one
            if isinstance(layer, _gis_mod.Item) and layer.type == "Map Service":
                options["itemId"] = layer.id
                # layer.url will represent the service as a whole and not the individual layers url
                # so either Item or instance of MapImageLayer
                all_layers = [arcgis_layers.Service(layer.url)]
            elif isinstance(layer, _gis_mod.Item):
                all_layers = []
                options["itemId"] = layer.id
                if hasattr(layer, "layers") and layer.layers:
                    for l in layer.layers:
                        all_layers.append(l)
                if hasattr(layer, "tables") and layer.tables:
                    if len(all_layers) > 0:
                        # If there are already layers we cannot add tables. Group Layer does not support tables.
                        raise ValueError(
                            "Cannot add a group layer with tables to the map. Please add the layers individually or as a list to the add method."
                        )
                    for t in layer.tables:
                        all_layers.append(t)
            else:
                all_layers = layer

            if len(all_layers) == 1:
                return self._create_layer_from_item(
                    all_layers[0], drawing_info, popup_info, options
                )
            else:
                layers = [
                    self._create_layer_from_item(l, drawing_info, popup_info, options)
                    for l in all_layers
                ]
                title = (
                    layer.title if isinstance(layer, _gis_mod.Item) else "Group Layer"
                )
                return _models.GroupLayer(layers=layers, title=title)

        # extract properties
        properties = dict(layer.properties)

        # Extract the item id
        # Item id is important because rendering and popup information can be stored at this level.
        # Especially, but not only, with living atlas layers.
        item_id = properties.get(
            "serviceItemId", properties.get("id", options.get("itemId"))
        )

        # Need individual ids for each layer added, this is important for finding layers when using the JS API
        properties["id"] = uuid.uuid4().hex[0:12]

        ### Private URL Section Start
        # Do not need to check if gis is online, if _use_private_url_only is False, (Check layer types)
        if not self._source._gis._is_agol and self._source._gis._use_private_url_only:
            if isinstance(layer, arcgis_layers.MapImageLayer):
                layer_url = layer._url
            else:
                layer_url = self._private_to_public_url(layer)
        else:
            layer_url = layer._url
        ### Private URL Section End

        if (
            isinstance(layer, features.FeatureLayer)
            and properties["type"] == "Catalog Layer"
        ):
            ld = self._create_ld_dict(layer, drawing_info)
            return _models.CatalogLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                itemId=item_id,
                title=properties["name"],
            )
        elif (
            isinstance(layer, features.FeatureLayer)
            and not isinstance(layer, features.Table)
            or isinstance(layer, arcgis_layers.MapFeatureLayer)
        ):
            if self.is_map or drawing_info:
                ld = self._create_ld_dict(layer, drawing_info)
            else:
                # If not a map, we need to get the layer definition from the item data. Scene Viewer will take care of this.
                ld = None
            popup = self._create_popup_dataclass(layer, popup_info)
            return _models.FeatureLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
                title=properties["name"],
            )
        elif isinstance(layer, arcgis_layers.VectorTileLayer):
            style_url = f"{layer_url}/resources/styles/root.json"
            return _models.VectorTileLayer(
                **properties,
                itemId=item_id,
                title=properties["name"],
                styleUrl=style_url,
                isReference=False,
            )
        elif isinstance(layer, features.Table):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            return _models.Table(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
                title=properties["name"],
            )
        elif isinstance(layer, realtime.StreamLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            return _models.StreamLayer(
                **properties,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
            )
        elif isinstance(layer, arcgis_layers.CSVLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            properties.pop("layerDefinition", None)
            return _models.CSVLayer(
                **properties,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
            )
        elif isinstance(layer, arcgis_layers.KMLLayer):
            return _models.KMLLayer(
                **properties,
                itemId=item_id,
            )
        elif isinstance(layer, arcgis_layers.WMSLayer):
            return _models.WMSLayer(
                **layer._operational_layer_json,
            )
        elif isinstance(layer, arcgis_layers.WMTSLayer):
            if options and "layer" in options:
                lyr_json = layer.operational_layer_json(options["layer"])
            else:
                lyr_json = layer._operational_layer_json

            info = lyr_json.get("wmtsInfo", {})
            # Get title and layer identifier
            layer_identifier = info["layerIdentifier"]
            title = (
                lyr_json["title"]["#text"]
                if isinstance(lyr_json["title"], dict)
                else layer_identifier
            )
            wmts_info = _models.WebMapTileServiceInfo(
                url=info["url"],
                layer_identifier=layer_identifier,
                tile_matrix_set=info["tileMatrixSet"][0],
            )
            # create tile info dataclass
            tile_info = lyr_json.get("tileInfo", {})
            tile_info["spatialReference"] = {"wkid": layer._spatial_reference}

            return _models.WebTiledLayer(
                **properties,
                item_id=layer._id,
                title=title,
                wmts_info=wmts_info,
                copyright=layer._copyright,
                max_scale=layer._max_scale,
                min_scale=layer._min_scale,
                opacity=layer._opacity,
                template_url=lyr_json.get("templateUrl"),
                full_extent=lyr_json.get("fullExtent"),
                tile_info=_models.TileInfo(**tile_info),
            )
        elif isinstance(layer, arcgis_layers.GeoRSSLayer):
            return _models.GeoRSSLayer(
                **properties,
                itemId=item_id,
            )
        elif isinstance(layer, arcgis_layers.GeoJSONLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            return _models.GeoJSONLayer(
                **properties,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
            )
        elif isinstance(layer, features.layer.OrientedImageryLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            return _models.OrientedImageryLayer(
                **properties,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
            )
        elif isinstance(layer, arcgis_layers.OGCFeatureService) or isinstance(
            layer, arcgis_layers.OGCCollection
        ):
            if isinstance(layer, arcgis_layers.OGCFeatureService):
                url = layer_url
                # Add the first collection found
                layer = [coll for coll in layer.collections][0]
            else:
                # This is the collections url, need to get the FeatureServer url
                coll_url = layer_url
                # Find the index of "/collections/..." in the URL
                index = coll_url.rfind("/collections/")

                # Remove "/collections/" and everything after it
                url = coll_url[:index]

            # create layer definition and popup info from the collection as a pydantic feature collection
            sedf = layer.query("1=1").spatial
            fs = sedf.to_featureset()
            fc = features.FeatureCollection.from_featureset(fs)
            fc = _models.FeatureCollection(layers=fc.layer["layers"])

            ld = self._create_ld_dict(fc, drawing_info)
            popup = self._create_popup_dataclass(fc, popup_info)

            return _models.OGCFeatureLayer(
                url=url,
                collectionId=layer.properties["id"],
                title=layer.properties["title"],
                layerDefinition=ld,
                popupInfo=popup,
            )
        elif (
            isinstance(layer, arcgis_layers.MapServiceLayer)
            or isinstance(layer, arcgis_layers.MapImageLayer)
            or isinstance(layer, arcgis_layers.MapRasterLayer)
        ):
            try:
                if (
                    layer.container is not None
                    and "TilesOnly"
                    in layer.container.properties.get("capabilities", [])
                ):
                    layer_type = _models.TiledMapServiceLayer
                else:
                    layer_type = _models.MapServiceLayer
            except Exception:
                layer_type = (
                    _models.TiledMapServiceLayer
                    if "TilesOnly" in layer.properties.get("capabilities", [])
                    else _models.MapServiceLayer
                )

            name = properties.get("name", properties.get("mapName", "Map Service"))
            return layer_type(
                **properties,
                url=layer_url,
                itemId=item_id,
                title=name,
            )
        elif isinstance(layer, arcgis_layers.MapRasterLayer):
            return _models.TiledMapServiceLayer(
                **properties,
                url=layer_url,
                itemId=item_id,
                title=properties["name"],
            )
        elif isinstance(layer, raster.ImageryLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            rr = self._get_rendering_rule(layer)
            mr = self._get_mosaic_rule(layer)
            # for datastore raster, the datastore path has to be passed as value to the Raster parameter to the raster rendering service
            datastore_raster = self._get_datastore_raster(layer)
            custom_params = None
            if datastore_raster:
                custom_params = {"Raster": datastore_raster}
            layer_type = (
                _models.TiledImageServiceLayer
                if layer.tiles_only
                else _models.ImageServiceLayer
            )
            return layer_type(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
                title=properties["name"],
                noData=0,
                rendering_rule=rr,
                mosaic_rule=mr,
                custom_parameters=custom_params,
            )
        elif isinstance(layer, raster.Raster):
            if isinstance(layer._engine_obj, raster._ArcpyRaster):
                return self._add_local_raster(layer, options)
            else:
                ld = self._create_ld_dict(layer, drawing_info)
                popup = self._create_popup_dataclass(layer, popup_info)
                rr = self._get_rendering_rule(layer)
                mr = self._get_mosaic_rule(layer)
                return _models.ImageServiceLayer(
                    **properties,
                    url=layer.catalog_path,
                    layerDefinition=ld,
                    popupInfo=popup,
                    itemId=item_id,
                    title=layer.name,
                    noData=0,
                    rendering_rule=rr,
                    mosaic_rule=mr,
                )
        elif isinstance(layer, arcgis_layers.BuildingLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            sublayers = properties.get("layers", [])
            title = properties.get(
                "name", properties.get("serviceName", "Building Layer")
            )
            return _models.BuildingSceneLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                itemId=item_id,
                sublayers=sublayers,
                title=title,
            )
        elif isinstance(layer, arcgis_layers.PointCloudLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            popup = self._create_popup_dataclass(layer, popup_info)
            title = properties.get(
                "name", properties.get("serviceName", "Point Cloud Layer")
            )
            return _models.PointCloudLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
                title=title,
            )
        elif (
            isinstance(layer, arcgis_layers.SceneLayer)
            or isinstance(layer, arcgis_layers.Object3DLayer)
            or isinstance(layer, arcgis_layers.Point3DLayer)
        ):
            ld = self._create_ld_dict(layer, drawing_info)
            properties["popupInfo"] = self._create_popup_dataclass(layer, popup_info)
            title = properties.get("name", properties.get("serviceName", "Scene Layer"))
            try:
                del properties["layerType"]
            except KeyError:
                pass
            return _models.SceneLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                itemId=item_id,
                title=title,
            )
        elif isinstance(layer, arcgis_layers.IntegratedMeshLayer):
            ld = self._create_ld_dict(layer, drawing_info)
            title = properties.get(
                "name", properties.get("serviceName", "Integrated Mesh Layer")
            )
            return _models.IntegratedMeshLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                itemId=item_id,
                title=title,
            )
        elif isinstance(layer, arcgis_layers.VoxelLayer):
            ld_pre = self._create_ld_dict(layer, drawing_info)
            ld = _models.VoxelLayerDefinition(**ld_pre)
            popup = self._create_popup_dataclass(layer, popup_info)
            title = properties.get("name", properties.get("serviceName", "Voxel Layer"))
            return _models.VoxelLayer(
                **properties,
                url=layer_url,
                layerDefinition=ld,
                popupInfo=popup,
                itemId=item_id,
                title=title,
            )
        else:
            raise ValueError("Layer type not supported or incorrectly formatted.")

    def update_layer(
        self,
        index=None,
        labeling_info=None,
        renderer=None,
        scale_symbols=None,
        transparency=None,
        options=None,
        form=None,
        **kwargs,
    ):
        """
        This method can be used to update certain properties on a layer that is in your scene.
        """
        # was this method called from the group layer class?
        group_layer = kwargs.pop("group_layer", False)

        if not group_layer:
            if index is None:
                raise ValueError("Must specify index parameter.")

            # Get layer from list (should not be pydantic)
            # We will edit pydantic layer after, this needs to be passed into method
            layer = self._source.content.layers[index]
            # Error check
            if isinstance(layer, arcgismapping.GroupLayer):
                raise ValueError(
                    "The layer cannot be of type Group Layer. Use the `update_layer` method found in the Group Layer class."
                )
        if not options and not (
            isinstance(layer, features.FeatureCollection)
            or isinstance(layer, features.FeatureLayer)
            or isinstance(layer, arcgis_layers.GeoJSONLayer)
            or isinstance(layer, arcgis_layers.CSVLayer)
        ):
            raise ValueError(
                "Only Feature Collections, Feature Layers, GeoJSON Layers, and CSV Layers can have their drawing info edited."
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
            new_ld = self._create_ld_dict(layer, drawing_info)

            # Assign the new layer definition
            self.pydantic_class.operational_layers[index].layer_definition = new_ld

        if options is not None:
            # make the edits straight in the webmap definition
            layer = self.pydantic_class.operational_layers[index]
            # if an options dictionary was passed in, set the available attributes
            for key, value in options.items():
                # make sure key is in snake case
                key = "".join(
                    ["_" + c.lower() if c.isupper() else c for c in key]
                ).lstrip("_")
                if hasattr(layer, key):
                    setattr(layer, key, value)

        if form is not None:
            # Assign the new FormInfo
            form_info = _models.FormInfo(**form.dict())
            self.pydantic_class.operational_layers[index].form_info = form_info

    def remove_layer(self, index: int | None = None):
        """
        Remove a layer from the scene either by specifying the index or passing in the layer dictionary.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Optional integer specifying the index for the layer you want to remove.
                                To see a list of layers use the layers property.
        ==================      =====================================================================
        """
        if index is None:
            raise ValueError(
                "Must specify index parameter. You can see a list of all your layers by calling the `layers` property."
            )

        # Remove from pydantic dataclass
        try:
            del self.pydantic_class.operational_layers[index]
        except Exception:
            logging.error("Layer index not found.")
            return
        # Remove from layers property
        del self._source.content.layers[index]

    def remove_all(self):
        """
        Remove all layers and tables from the map.
        """
        # Remove from pydantic dataclass
        # check that the operational layers and tables exist
        if hasattr(self.pydantic_class, "operational_layers") and isinstance(
            self.pydantic_class.operational_layers, (list, tuple)
        ):
            self.pydantic_class.operational_layers.clear()
        if hasattr(self.pydantic_class, "tables") and isinstance(
            self.pydantic_class.tables, (list, tuple)
        ):
            self.pydantic_class.tables.clear()
        # Remove from properties
        self._source.content.layers.clear()
        self._source.content.tables.clear()

    def remove_table(self, index: int | None = None):
        """
        Remove a table from the map either by specifying the index or passing in the table object.

        ==================      =====================================================================
        **Parameter**           **Description**
        ------------------      ---------------------------------------------------------------------
        index                   Optional integer specifying the index for the table you want to remove.
                                To see a list of tables use the `tables` property.
        ==================      =====================================================================
        """
        if index is None:
            raise ValueError(
                "You must provide a table index. See your map's tables by calling the `tables` property."
            )

        # Remove from pydantic dataclass
        del self.pydantic_class.tables[index]
        # Remove from tables property
        del self._source.content.tables[index]

    ###################### Map and Scene Methods ######################

    def _save(
        self,
        item_properties: dict[str, Any],
        thumbnail: Optional[str] = None,
        metadata: Optional[str] = None,
        owner: Optional[str] = None,
        folder: Optional[str] = None,
    ):
        # Check a user is logged in
        if not self._source._gis.users.me:
            raise RuntimeError("You must be logged in to save a webmap or webscene.")

        # check item props are there
        if (
            "title" not in item_properties
            or "snippet" not in item_properties
            or "tags" not in item_properties
        ):
            raise RuntimeError(
                "title, snippet and tags are required in item_properties dictionary"
            )

        # fix the tags to be a string of comma separated values
        if isinstance(item_properties["tags"], list):
            item_properties["tags"] = ",".join(item_properties["tags"])

        # make sure authoring app and version are correct
        self.pydantic_class.authoring_app = "ArcGIS Python API"
        self.pydantic_class.authoring_app_version = arcgis.__version__

        if self.is_map:
            # Refresh to make sure all changes are in the webmap_dict
            # We exclude none values when saving to avoid saving unneccessary properties
            self._source._update_source()
            # Add to item properties
            item_properties["type"] = "Web Map"

            # check extent spatial reference
            self._check_extent_sr()

            # Set the extent to the current map extent
            item_properties["extent"] = self._source.extent

            # Update the initial state so that the mapviewer has the correct extent to render
            self._source._webmap_dict["initialState"]["viewpoint"][
                "targetGeometry"
            ] = self._source.extent
            self._source._webmap_dict["initialState"]["viewpoint"]["targetGeometry"][
                "spatialReference"
            ] = self._source._webmap_dict["spatialReference"]

            item_properties["text"] = json.dumps(
                self._source._webmap_dict, default=arcgis_utils._date_handler
            )
        else:
            item_properties["type"] = "Web Scene"
            # Set to current camera view if applicable
            self.pydantic_class.initial_state.viewpoint.camera = (
                _models.Camera(**self._source.camera)
                if self._source.camera
                else _models.Camera(
                    **{
                        "position": {
                            "spatialReference": {
                                "latestWkid": 3857,
                                "wkid": 102100,
                            },
                            "x": -0.00044117777277823567,
                            "y": -42336.301402091056,
                            "z": 20266096.34006851,
                        },
                        "heading": 1.7075472925031877e-06,
                        "tilt": 0.11968932646564065,
                    }
                )
            )
            # Refresh to make sure all changes are in the webscene_dict
            self._source._update_source()
            # Add to item properties

        if "typeKeywords" not in item_properties:
            item_properties["typeKeywords"] = self._eval_type_keywords()

        # Add as a new item to the portal
        # if the folder is a string, it will either get or create it
        # otherwise get the root folder
        if isinstance(folder, str):
            folder = self._source._gis.content.folders._get_or_create(folder, owner)
        elif folder is None:
            folder = self._source._gis.content.folders.get()  # root folder
        elif not isinstance(folder, arcgis_cm.Folder):
            raise ValueError("Folder must be a Folder object.")

        item_properties["thumbnail"] = thumbnail
        item_properties["metadata"] = metadata

        # add in folder class
        future_item = folder.add(
            item_properties,
            text=(self.pydantic_class.dict()),
        )
        new_item = future_item.result()

        # set to item property
        self._source.item = new_item

        return new_item

    def _update(
        self,
        item_properties: Optional[dict[str, Any]] = None,
        thumbnail: Optional[str] = None,
        metadata: Optional[str] = None,
    ):
        if self._source.item is not None:
            self.pydantic_class.authoring_app = "ArcGIS Python API"
            self.pydantic_class.authoring_app_version = arcgis.__version__
            self._source._update_source()

            if item_properties is None:
                item_properties = {}
            elif "tags" in item_properties and isinstance(
                item_properties["tags"], list
            ):
                item_properties["tags"] = ",".join(item_properties["tags"])

            if self.is_map:
                # Make sure all changes are in webmapdict
                # Set exclude none to True to avoid saving unnecessary parameters

                # Check the extent spatial reference of the map
                self._check_extent_sr()

                # Update the initial state so that the mapviewer has the correct extent to render
                self.pydantic_class.initial_state.viewpoint.target_geometry = (
                    _models.Extent(**self._source.extent)
                )

                item_properties["extent"] = self._source.extent

            item_properties["text"] = json.dumps(
                self.pydantic_class.dict(),
                default=arcgis_utils._date_handler,
            )
            if "typeKeywords" not in item_properties:
                item_properties["typeKeywords"] = self._eval_type_keywords()
            if "type" in item_properties:
                item_properties.pop("type")  # type should not be changed.
            return self._source.item.update(
                item_properties=item_properties,
                thumbnail=thumbnail,
                metadata=metadata,
            )
        else:
            raise RuntimeError(
                "Item object missing, you should use `save()` method if you are creating a "
                "new web map item"
            )

    def _check_extent_sr(self):
        """
        Check the extent spatial reference and make sure it matches that of the map before saving and updating.
        This method is important when a user has set the extent and the map is not rendered. When a
        map is rendered, the extent is automatically updated to match the spatial reference of the map.
        """
        if self._source.extent is not None:
            if (
                self._source.extent["spatialReference"]
                != self.pydantic_class.spatial_reference
            ):
                self._source.extent = self._reproject_extent(
                    [self._source.extent],
                    self.pydantic_class.spatial_reference.dict(),
                )

    def _eval_type_keywords(self):
        # Get type keywords from item if any
        type_keywords = (
            set(self._source.item.typeKeywords) if self._source.item else set([])
        )
        # Check if offline disabled
        if "OfflineDisabled" not in type_keywords:
            if self._source.content.layers and self._is_offline_capable_map():
                type_keywords.add("Offline")
            else:
                type_keywords.discard("Offline")
        # Check if collector disabled
        if "CollectorDisabled" not in type_keywords:
            if self._source.content.layers and self._is_collector_ready_map():
                type_keywords.add("Collector")
                type_keywords.add("Data Editing")
            else:
                type_keywords.discard("Collector")
                type_keywords.discard("Data Editing")
        # Return the list of keywords
        return list(type_keywords)

    def _is_offline_capable_map(self):
        # Check that feature services are sync-enabled and tiled layers are exportable
        try:
            for layer in self.pydantic_class.operational_layers:
                layer_object = arcgis.gis.Layer(url=layer.url, gis=self._source._gis)
                if "ArcGISFeatureLayer" in layer.layer_type:
                    if "Sync" not in layer_object.properties.capabilities:
                        return False
                elif (
                    "VectorTileLayer" in layer.layer_type
                    or "ArcGISMapServiceLayer" in layer.layer_type
                    or "ArcGISImageServiceLayer" in layer.layer_type
                ):
                    if not self._is_exportable(layer_object):
                        return False
                else:
                    return False
            return True
        except Exception:
            return False

    def _is_exportable(self, layer):
        # heck SRs are equivalent and exportTilesAllowed is set to true or AGOl-hosted esri basemaps
        if (
            self._get_layer_wkid(layer)
            == self.pydantic_class.dict()["spatialReference"]["wkid"]
        ) and (
            layer.properties["exportTilesAllowed"]
            or "services.arcgisonline.com" in layer.url
            or "server.arcgisonline.com" in layer.url
        ):
            return True
        else:
            return False

    def _get_layer_wkid(self, layer):
        # spatialReference can either be set at the root level or within initialExtent
        if "spatialReference" in layer.properties:
            return layer.properties["spatialReference"]["wkid"]
        elif "initialExtent" in layer.properties:
            return layer.properties["initialExtent"]["spatialReference"]["wkid"]
        else:
            raise ValueError("No wkid found")

    def _is_collector_ready_map(self):
        # check that one layer is an editable feature service
        for layer in self._source.content.layers:
            try:
                layer_object = arcgis.gis.Layer(url=layer.url, gis=self._source._gis)
                if "ArcGISFeatureLayer" in layer.type:
                    if any(
                        capability in layer_object.properties.capabilities
                        for capability in [
                            "Create",
                            "Update",
                            "Delete",
                            "Editing",
                        ]
                    ):
                        return True
            except Exception:
                # Not every layer in self.layers has a URL (local featurelayer, SEDF, etc.)
                continue
        return False

    def _zoom_to_layer(self, item):
        # Get the target extent from the item passed in
        target_extent = self._get_extent(item)

        # Get the widget's spatial reference so we can project the extent
        target_sr = self.pydantic_class.spatial_reference.dict()

        # Transform target extent if needed
        if isinstance(target_extent, list):
            target_extent = self._flatten_list(target_extent)
            if len(target_extent) > 1:
                target_extent = self._get_master_extent(target_extent, target_sr)
            else:
                target_extent = target_extent[0]

        # Check if need to re-project
        if not (target_extent["spatialReference"] == target_sr):
            target_extent = self._reproject_extent(target_extent, target_sr)

        # Sometimes setting extent will not work for the same target extent if we do it multiple times, doing this fixes that issue.
        # self._source.extent = self._source.extent
        self._source.extent = target_extent

    def _get_extent(self, item):
        if isinstance(item, raster.Raster):
            if isinstance(item._engine_obj, raster._ImageServerRaster):
                item = item._engine_obj
            elif isinstance(item._engine_obj, raster._ArcpyRaster):
                return dict(item.extent)
        if isinstance(item, _gis_mod.Item):
            return list(map(self._get_extent, item.layers))
        elif isinstance(item, list):
            return list(map(self._get_extent, item))
        elif isinstance(item, pd.DataFrame):
            return self._get_extent_of_dataframe(item)
        elif isinstance(item, features.FeatureSet):
            return self._get_extent(item.sdf)
        elif isinstance(item, features.FeatureCollection):
            props = dict(item.properties)
            return props.get("layerDefinition", {}).get("extent")
        elif isinstance(item, _gis_mod.Layer):
            try:
                if "extent" in item.properties:
                    return dict(item.properties.extent)
                elif "fullExtent" in item.properties:
                    return dict(item.properties["fullExtent"])
                elif "initialExtent" in item.properties:
                    return dict(item.properties["initialExtent"])
            except Exception:
                ext = item.extent
                return {
                    "spatialReference": {"wkid": 4326, "latestWkid": 4326},
                    "xmin": ext[0][1],
                    "ymin": ext[0][0],
                    "xmax": ext[1][1],
                    "ymax": ext[1][0],
                }
        else:
            raise Exception("Could not infer layer type")

    def _flatten_list(self, *unpacked_list):
        return_list = []
        for x in unpacked_list:
            if isinstance(x, (list, tuple)):
                return_list.extend(self._flatten_list(*x))
            else:
                return_list.append(x)
        return return_list

    def _get_extent_of_dataframe(self, sdf):
        if hasattr(sdf, "spatial"):
            sdf_ext = sdf.spatial.full_extent
            return {
                "spatialReference": sdf.spatial.sr,
                "xmin": sdf_ext[0],
                "ymin": sdf_ext[1],
                "xmax": sdf_ext[2],
                "ymax": sdf_ext[3],
            }
        else:
            raise Exception(
                "Could not add get extent of DataFrame it is not a spatially enabled DataFrame."
            )

    def _get_master_extent(self, list_of_extents, target_sr=None):
        if target_sr is None:
            target_sr = {"wkid": 102100, "latestWkid": 3857}
        # Check if any extent is different from one another
        varying_spatial_reference = False
        for extent in list_of_extents:
            if not target_sr == extent["spatialReference"]:
                varying_spatial_reference = True
        if varying_spatial_reference:
            list_of_extents = self._reproject_extent(list_of_extents, target_sr)

        # Calculate master_extent
        master_extent = list_of_extents[0]
        for extent in list_of_extents:
            master_extent["xmin"] = min(master_extent["xmin"], extent["xmin"])
            master_extent["ymin"] = min(master_extent["ymin"], extent["ymin"])
            master_extent["xmax"] = max(master_extent["xmax"], extent["xmax"])
            master_extent["ymax"] = max(master_extent["ymax"], extent["ymax"])
        return master_extent

    def _reproject_extent(
        self, extents, target_sr={"wkid": 102100, "latestWkid": 3857}
    ):
        """Reproject Extent

        ==================      ====================================================================
        **Parameter**           **Description**
        ------------------      --------------------------------------------------------------------
        extents                 Extent or list of extents you want to project.
        ------------------      --------------------------------------------------------------------
        target_sr               The target Spatial Reference you want to get your extent in.
                                default is {'wkid': 102100, 'latestWkid': 3857}
        ==================      ====================================================================

        """
        if not isinstance(extents, list):
            extents = [extents]

        extents_to_reproject = {}
        for i, extent in enumerate(extents):
            if not extent["spatialReference"] == target_sr:
                in_sr_str = str(extent["spatialReference"])
                if in_sr_str not in extents_to_reproject:
                    extents_to_reproject[in_sr_str] = {}
                    extents_to_reproject[in_sr_str]["spatialReference"] = extent[
                        "spatialReference"
                    ]
                    extents_to_reproject[in_sr_str]["extents"] = []
                    extents_to_reproject[in_sr_str]["indexes"] = []
                extents_to_reproject[in_sr_str]["extents"].extend(
                    [
                        {"x": extent["xmin"], "y": extent["ymin"]},
                        {"x": extent["xmax"], "y": extent["ymax"]},
                    ]
                )
                extents_to_reproject[in_sr_str]["indexes"].append(i)

        for in_sr_str in extents_to_reproject:  # Re-project now
            reprojected_extents = arcgis.geometry.project(
                extents_to_reproject[in_sr_str]["extents"],
                in_sr=extents_to_reproject[in_sr_str]["spatialReference"],
                out_sr=target_sr,
                gis=self._source._gis,
            )
            for i in range(0, len(reprojected_extents), 2):
                source_idx = extents_to_reproject[in_sr_str]["indexes"][int(i / 2)]
                extents[source_idx] = {
                    "xmin": reprojected_extents[i]["x"],
                    "ymin": reprojected_extents[i]["y"],
                    "xmax": reprojected_extents[i + 1]["x"],
                    "ymax": reprojected_extents[i + 1]["y"],
                    "spatialReference": target_sr,
                }

        if len(extents) == 1:
            return extents[0]
        return extents

    def _sync_navigation(self, mapview):
        """
        The ``sync_navigation`` method synchronizes the navigation from one rendered Map/Scene to
        another rendered Map/Scene instance so panning/zooming/navigating in one will update the other.

        .. note::
            Users can sync more than two instances together by passing in a list of Map/Scene instances to
            sync. The syncing will be remembered

        ==================      ===================================================================
        **Parameter**           **Description**
        ------------------      -------------------------------------------------------------------
        mapview                 Either a single Map/Scene instance, or a list of ``Map`` or ``Scene``
                                instances to synchronize to.
        ==================      ===================================================================

        """
        if isinstance(mapview, list):
            # append the current Map/Scene to the list so it gets linked as well
            mapview.append(self._source)
            # Iterate through if list of maps and link all of them
            for i in range(len(mapview) - 1):
                for j in range(i + 1, len(mapview)):
                    # Extent is linked to zoom and scale on js side so we only need to link this.
                    l = link((mapview[i], "extent"), (mapview[j], "extent"))
                    # Keep track of links for each mapview
                    mapview[i]._linked_maps.append(l)
                    mapview[j]._linked_maps.append(l)
        elif self.is_map and isinstance(mapview, arcgismapping.Map):
            l = link((self._source, "extent"), (mapview, "extent"))
            self._source._linked_maps.append(l)
            mapview._linked_maps.append(l)
        elif self.is_map is False and isinstance(mapview, arcgismapping.Scene):
            l = link((self._source, "extent"), (mapview, "extent"))
            self._source._linked_maps.append(l)
            mapview._linked_maps.append(l)
        else:
            raise ValueError(
                "Please provide a valid list of Map instances or a single Map instance to link to the current Map."
            )

    def _unsync_navigation(self, mapview=None):
        """
        The ``unsync_navigation`` method unsynchronizes connections made to other rendered Map/Scene instances
        made via the sync_navigation method.

        ==================     ===================================================================
        **Parameter**           **Description**
        ------------------     -------------------------------------------------------------------
        mapview                Optional, either a single `Map` or `Scene` instance, or a list of
                               `Map` or `Scene` instances to unsynchronize. If not specified, will
                               unsynchronize all synced `Map` or `Scene` instances.
        ==================     ===================================================================
        """
        # Unlink all
        if mapview is None:
            for link_obj in self._source._linked_maps:
                link_obj.unlink()
                # clear list of links for source and target
                link_obj.source[0]._linked_maps.clear()
                link_obj.target[0]._linked_maps.clear()
                return

        if self.is_map:
            # Unlink some
            if isinstance(mapview, arcgismapping.Map):
                # Make a list since the logic will be the same as list
                mapview = [mapview]
        else:
            # Unlink some
            if isinstance(mapview, arcgismapping.Scene):
                # Make a list since the logic will be the same as list
                mapview = [mapview]

        if isinstance(mapview, list):
            # Iterate through if list of maps and link all of them
            for widget in mapview:
                # We want to unlink the list of widgets from this one
                widgets = [self._source, widget]
                for link_obj in self._source._linked_maps:
                    source_widget = link_obj.source[0]
                    target_widget = link_obj.target[0]

                    if source_widget in widgets and target_widget in widgets:
                        link_obj.unlink()
                        source_widget._linked_maps.remove(link_obj)
                        target_widget._linked_maps.remove(link_obj)

    def _export_to_html(
        self,
        path_to_file,
        title=None,
    ):
        """
        The ``export_to_html`` method takes the current state of the rendered map and exports it to a
        standalone HTML file that can be viewed in any web browser.

        By default, only publicly viewable layers will be visible in any
        exported html map. Specify ``credentials_prompt=True`` to have a user
        be prompted for their credentials when opening the HTML page to view
        private content.

        .. warning::
            Follow best security practices when sharing any HTML page that
            prompts a user for a password.

        .. note::
            You cannot successfully authenticate if you open the HTML page in a
            browser locally like file://path/to/file.html. The credentials
            prompt will only properly function if served over a HTTP/HTTPS
            server.

        ==================     ====================================================================
        **Parameter**           **Description**
        ------------------     --------------------------------------------------------------------
        path_to_file           Required string. The path to save the HTML file on disk.
        ------------------     --------------------------------------------------------------------
        title                  Optional string. The HTML title tag used for the HTML file.
        ==================     ====================================================================
        """
        js_api_path = self._source.js_api_path or "https://js.arcgis.com/4.30/"
        html_template = """
        <html>
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no" />
                <title>{title}</title>

                <style>
                    html,
                    body,
                    #viewDiv {{
                        padding: 0;
                        margin: 0;
                        height: 100%;
                        width: 100%;
                    }}
                </style>

                <link rel="stylesheet" href="{js_api_path}esri/themes/light/main.css">
                <script src="{js_api_path}"></script>

                <script>
                    require(["esri/config", "esri/WebMap", "esri/views/MapView"], function(esriConfig, WebMap, MapView) {{


                        const map = WebMap.fromJSON({state});

                        const view = new MapView({{
                            map: map,
                            extent: {extent},
                            container: "viewDiv"
                        }});

                    }});
                </script>
            </head>
            <body>
                <div id="viewDiv"></div>
            </body>
        </html>
        """
        # Title
        if title is None:
            title = "Exported ArcGIS Map from Python API"

        # WebMap state to export
        state = json.dumps(self.pydantic_class.dict())
        extent = json.dumps(self._source.extent)

        # Create template
        rendered_template = html_template.format(
            title=title,
            js_api_path=js_api_path,
            state=state,
            extent=extent,
        )

        # Write to file
        with open(path_to_file, "w") as fp:
            fp.write(rendered_template)

        return True

    def _print(
        self,
        file_format: str,
        extent: dict[str, Any],
        dpi: int = 92,
        output_dimensions: tuple[float] = (500, 500),
        scale: Optional[float] = None,
        rotation: Optional[float] = None,
        spatial_reference: Optional[dict[str, Any]] = None,
        layout_template: str = "MAP_ONLY",
        time_extent: Optional[Union[tuple[int], list[int]]] = None,
        layout_options: Optional[dict[str, Any]] = None,
    ):
        # compose map options
        map_options: dict = {
            "extent": extent,
            "scale": scale,
            "rotation": rotation,
            "spatialReference": spatial_reference,
            "time": time_extent,
        }

        # compose export options
        export_options: dict = {"dpi": dpi, "outputSize": output_dimensions}

        map_dict: dict = self.pydantic_class.dict()
        # compose combined JSON
        print_options: dict = {
            "mapOptions": map_options,
            "operationalLayers": map_dict["operationalLayers"],
            "baseMap": map_dict["baseMap"],
            "exportOptions": export_options,
        }

        # add token parameter to the operational layers if token present
        if self._source._gis._session.auth.token is not None:
            for i in range(len(print_options["operationalLayers"])):
                print_options["operationalLayers"][i][
                    "token"
                ] = self._source._gis._session.auth.token

        if layout_options:
            print_options["layoutOptions"] = layout_options

        # execute printing, result is a DataFile
        result = self._export_map(
            web_map_as_json=print_options,
            format=file_format,
            layout_template=layout_template,
            gis=self._source._gis,
        )

        # process output
        return result.url

    def _export_map(
        self,
        web_map_as_json: Optional[dict] = None,
        format: str = """PDF""",
        layout_template: str = """MAP_ONLY""",
        gis=None,
        **kwargs,
    ):
        """
        The ``export_map`` function takes the state of the :class:`~arcgis.map.Map` object (for example, included services, layer visibility
        settings, client-side graphics, and so forth) and returns either (a) a page layout or
        (b) a map without page surrounds of the specified area of interest in raster or vector format.
        The input for this function is a piece of text in JavaScript object notation (JSON) format describing the layers,
        graphics, and other settings in the web map. The JSON must be structured according to the Map specification
        in the ArcGIS Help.
        .. note::
            The ``export_map`` tool is shipped with ArcGIS Server to support web services for printing, including the
            pre-configured service named ``PrintingTools``.
        ==================     ====================================================================
        **Parameter**           **Description**
        ------------------     --------------------------------------------------------------------
        web_map_as_json        Web Map JSON along with export options. See the
                            `Export Web Map Specifications <https://developers.arcgis.com/rest/services-reference/exportwebmap-specification.htm>`_
                            for more information on structuring this JSON.
        ------------------     --------------------------------------------------------------------
        format                 Format (str). Optional parameter.  The format in which the map image
                            for printing will be delivered. The following strings are accepted:
                            For example:
                                    PNG8
                            Choice list:
                                    ['PDF', 'PNG32', 'PNG8', 'JPG', 'GIF', 'EPS', 'SVG', 'SVGZ']
        ------------------     --------------------------------------------------------------------
        layout_template        Layout Template (str). Optional parameter.  Either a name of a
                            template from the list or the keyword MAP_ONLY. When MAP_ONLY is chosen
                            or an empty string is passed in, the output map does not contain any
                            page layout surroundings.
                            For example - title, legends, scale bar, and so forth
                            Choice list:
                                | ['A3 Landscape', 'A3 Portrait',
                                | 'A4 Landscape', 'A4 Portrait', 'Letter ANSI A Landscape',
                                | 'Letter ANSI A Portrait', 'Tabloid ANSI B Landscape',
                                | 'Tabloid ANSI B Portrait', 'MAP_ONLY'].
                            You can get the layouts configured with your GIS by calling the :meth:`get_layout_templates <arcgis.mapping.get_layout_templates>` function
        ------------------     --------------------------------------------------------------------
        gis                    The :class:`~arcgis.gis.GIS` to use for printing. Optional
                            parameter. When not specified, the active GIS will be used.
        ==================     ====================================================================
        Returns:
            A dictionary with URL to download the output file.
        """

        verbose = kwargs.pop("verbose", False)

        if gis is None:
            gis = arcgis.env.active_gis
        params = {
            "web_map_as_json": web_map_as_json,
            "format": format,
            "layout_template": layout_template,
            "gis": gis,
            "future": False,
        }
        params.update(kwargs)

        url = os.path.dirname(gis.properties.helperServices.printTask.url)
        tbx = geoprocessing.import_toolbox(url, gis=gis, verbose=verbose)
        basename = os.path.basename(gis.properties.helperServices.printTask.url)
        basename = geoprocessing._tool._camelCase_to_underscore(
            urllib.parse.unquote_plus(urllib.parse.unquote(basename))
        )

        fn = getattr(tbx, basename)
        return fn(**params)

    def _layer_info(self):
        """
        Return a table with three columns. One with the layer index, one with the layer title, and one with the class instance of the layer.

        :return: A pandas DataFrame with the layer information.
        """
        layers = self._source.content.layers
        layer_info = []
        for i, layer in enumerate(layers):
            title = self.pydantic_class.operational_layers[
                i
            ].title  # title is in the properties unlike with the python classes
            layer_info.append([i, title, layer])
        return pd.DataFrame(
            layer_info, columns=["Layer Index", "Layer Title", "Layer Class"]
        )

    def _table_info(self):
        """
        Return a table with three columns. One with the table index, one with the table title, and one with the class instance of the table.

        :return: A pandas DataFrame with the table information.
        """
        tables = self._source.content.tables
        table_info = []
        for i, table in enumerate(tables):
            title = self.pydantic_class.tables[
                i
            ].title  # title is in the properties unlike with the python classes
            table_info.append([i, title, table])
        return pd.DataFrame(
            table_info, columns=["Table Index", "Table Title", "Table Class"]
        )

    def _get_layer(self, title, is_table=False):
        """
        Get the layer object by title.

        :param title: The title of the layer.
        :return: The layer object.
        """
        # use the pydantic class operational layers to get the layer index since title is in every layer property
        if is_table:
            tables = self.pydantic_class.tables
            for i, table in enumerate(tables):
                if table.title == title:
                    return self._source.content.tables[i]
        layers = self.pydantic_class.operational_layers
        for i, layer in enumerate(layers):
            if layer.title == title:
                return self._source.content.layers[i]

    def _js_requirement(self):
        return "This version of arcgis-mapping requires the ArcGIS Maps SDK for JavaScript version 4.30. You can download it from https://developers.arcgis.com/javascript/latest/downloads/ ."

    ############################################## Basemap Methods ##############################################
    @property
    def basemaps(self):
        # List of basemaps from the basemap def file
        return list(basemapdef.basemap_dict.keys())

    @property
    def basemaps3d(self):
        # List of basemaps from the basemap def file
        return list(basemapdef3d.basemap_dict.keys())

    @property
    def basemap(self):
        # Current basemap in the widget
        # Set exclude none to True to avoid returning unnecessary properties
        return self.pydantic_class.base_map.dict()

    def _move_to_basemap(self, index: int):
        # Types accepted as basemap
        layer_types = [
            "ArcGISTiledMapServiceLayer",
            "ArcGISImageServiceLayer",
            "ArcGISImageServiceVectorLayer",
            "ArcGISMapServiceLayer",
            "ArcGISTiledImageServiceLayer",
            "VectorTileLayer",
            "WMS",
            "WebTiledLayer",
        ]

        # Get the pydantic layer
        layer = self.pydantic_class.operational_layers[index]
        # Check the type
        if layer.layer_type in layer_types:
            # Store initial states
            initial_operational_layers = list(self.pydantic_class.operational_layers)
            initial_base_map_layers = list(self.pydantic_class.base_map.base_map_layers)
            initial_widget_layers = list(self._source.content.layers)

            try:
                # Add to basemap layers
                self.pydantic_class.base_map.base_map_layers.append(layer)
                # Remove from operational layers
                del self.pydantic_class.operational_layers[index]
                # Remove from layers property
                del self._source.content.layers[index]
            except Exception as e:
                # Revert to initial state
                self.pydantic_class.operational_layers = initial_operational_layers
                self.pydantic_class.base_map.base_map_layers = initial_base_map_layers
                self._source.content.layers = initial_widget_layers

                # Raise the exception again to notify the caller
                raise e
        else:
            raise ValueError(
                "This layer type cannot be added as a basemap. See method description to know what layer types can be moved to basemap."
            )

    def _move_from_basemap(self, index: int):
        try:
            # Store initial states
            initial_base_map_layers = list(self.pydantic_class.base_map.base_map_layers)
            initial_operational_layers = list(self.pydantic_class.operational_layers)
            initial_widget_layers = list(self._source.content.layers)

            if len(initial_base_map_layers) == 1:
                raise ValueError(
                    "You only have one basemap layer present. You cannot remove the layer since you must always have at least one layer."
                )
            # Get the layer from basemap layers
            layer = self.pydantic_class.base_map.base_map_layers[index]
            # Add to the pydantic dataclass
            self.pydantic_class.operational_layers.append(layer)
            # Add to the layers property
            self._source.content.layers.append(self._infer_layer(layer))
            # Remove from the basemap layers
            del self.pydantic_class.base_map.base_map_layers[index]
            first_layer = self.pydantic_class.base_map.base_map_layers[
                0
            ]  # need extra line incase fails
            self._check_layer_sr(first_layer)
        except Exception as e:
            # Revert to initial state
            self.pydantic_class.base_map.base_map_layers = initial_base_map_layers
            self.pydantic_class.operational_layers = initial_operational_layers
            self._source.content.layers = initial_widget_layers

            # Raise the exception again to notify the caller
            raise e

    def _basemap_title_format(self, title):
        return title.replace("-", " ").replace("_", " ")

    def _set_basemap_title(self, title: str):
        """
        Set the basemap title.

        =====================       ===================================================================
        **Parameter**                **Definition**
        ---------------------       -------------------------------------------------------------------
        title                       Required string. The title to set for the basemap.
        =====================       ===================================================================
        """
        title = self._basemap_title_format(title)
        self.pydantic_class.base_map.title = title

    def _remove_basemap_layer(self, index: int):
        if len(self.pydantic_class.base_map.base_map_layers) > 1:
            if index == 0:
                # If removing first basemap layer, need to check the spatial reference of new first layer
                # We know there has to be at least one layer following since cannot delete all basemap layers
                self._check_layer_sr(self.pydantic_class.base_map.base_map_layers[1])
            # Remove the basemap layer at the specific layer
            del self.pydantic_class.base_map.base_map_layers[index]
            # Refresh the basemap property
            self._source._update_source()
        else:
            raise ValueError(
                "You only have one basemap layer present. You cannot remove the layer since you must always have at least one layer."
            )

    def _set_basemap_from_service(self, basemap):
        if "id" not in basemap:
            raise ValueError(
                "The basemap dictionary must contain an 'id' key specifying the basemap style path. (i.e. 'arcgis/streets')"
            )

        # Set the basemap in the rendered map, does not work if map is not rendered
        self._source._basemap = {
            "style": {
                "id": basemap["id"],
                "language": basemap.get("language", "en"),
                "places": basemap.get("places", "none"),
                "worldview": basemap.get("worldview", "none"),
            }
        }
        # The python basemap gets updated in an observe call on the main Map class

    def _set_basemap_from_definition(self, basemap):
        """Set basemap from the hardcoded basemap definitions in the basemapdef file or the basemap gallery."""
        # set basemap_dict
        basemap_dict = None
        # reset the spatial reference if it was changed for other basemap
        if self.pydantic_class.spatial_reference.wkid != 102100:
            self.pydantic_class.spatial_reference = _models.SpatialReference(
                wkid=102100
            )
        if basemap in self.basemaps:
            basemap_dict = {
                "baseMapLayers": basemapdef.basemap_dict[basemap],
                "title": self._basemap_title_format(basemap.title()),
            }
        elif basemap in self.basemaps3d:
            # Only on webscene
            basemap_dict = {
                "baseMapLayers": basemapdef3d.basemap_dict[basemap],
                "title": self._basemap_title_format(basemap.title()),
            }
        elif basemap in self.basemap_gallery:
            # Pass in a dictionary representation of basemap to widget
            basemap_dict = self._get_basemap_from_gallery(basemap)
            self._check_layer_sr(basemap_dict)
        if not basemap_dict:
            raise ValueError(
                "Basemap not found. Please check the basemap name and try again."
            )
        return basemap_dict

    def _set_basemap_from_map_scene_item(self, basemap):
        self._check_layer_sr(basemap)
        # Set the basemap to an existing widget's basemap
        # Pass in a dictionary representation of basemap to widget
        orig_dict = basemap.get_data()
        # Check spatial reference
        return orig_dict["baseMap"]

    def _set_basemap_from_item(self, basemap):
        if isinstance(basemap, _gis_mod.Item):
            basemap = basemap.layers[0]
        # Add the layer to the widget and then move it to basemap
        self._source.content.add(basemap, index=0)
        try:
            # Since we set the index when adding, we know which layer it is to move
            self._move_to_basemap(0)
        except Exception as e:
            # Maybe the layer type was not correct or there was another error.
            # Remove the layer and return exception
            # We added at index 0 so ok to say it is there
            self._source.content.remove(index=0)
            raise e
        # Remove the old basemap layer(s).
        # Replacing old layers entirely so need to remove all except one we just added.
        while len(self.pydantic_class.base_map.base_map_layers) != 1:
            # Layers keep moving forward.
            # We know recent one was added at end so keep removing first until only recent one left.
            self._remove_basemap_layer(index=0)
        # Finally update the basemap title
        self._set_basemap_title(self.pydantic_class.base_map.base_map_layers[0].title)

    def _get_basemap_from_gallery(self, basemap_name):
        """Get the basemap from the basemap gallery."""
        basemap_gallery = self._basemap_gallery_dict()
        # The key in the dictionary is the title of the basemap, the value is the basemap definition we need
        return basemap_gallery.get(basemap_name)

    def _basemap_gallery_dict(self):
        basemap_gallery = self._source.basemap._basemap_gallery

        if len(basemap_gallery) <= 1:
            # If the only loaded basemap_gallery is 'default', load the rest
            basemap_group_query = self._source._gis.properties[
                "basemapGalleryGroupQuery"
            ]
            basemap_groups = self._source._gis.groups.search(
                basemap_group_query, outside_org=True
            )

            if len(basemap_groups) == 1:
                # Get the basemaps from the group
                for basemap in basemap_groups[0].content():
                    if basemap.type.lower() in ["web map", "web scene"]:
                        item_data = basemap.get_data()
                        basemap_title = basemap.title.lower().replace(" ", "_")
                        basemap_gallery[basemap_title] = item_data["baseMap"]
        return basemap_gallery

    @cached_property
    def basemap_gallery(self):
        """
        The ``basemap_gallery`` property allows for viewing of your portal's custom basemap group.

        :returns: list of basemap names
        """
        basemap_gallery = self._basemap_gallery_dict()
        return list(basemap_gallery.keys())

    def _check_layer_sr(self, service):
        """
        Find the spatial reference being used by the widget and the first basemap layer and make sure they match.
        Otherwise throw an error.

        This method is used when switching the basemap to a new basemap. This can occur when a user sets
        the basemap using the `basemap` property or when they remove the first basemap layer using the
        `remove_basemap_layer` method.

        What can be checked here:
        - Existing Web Map Item that is being used to set basemap
        - Existing Web Scene Item that is being used to set basemap
        - Pydantic classes when a user is removing the first basemap layer and we must check the next in line is compatible
        - Layer coming from the arcgis Item class's `layers` property.
        - Dictionary of basemap from basemap file or gallery basemaps
        """
        # Get the spatial reference from the widget
        map_sr = self.pydantic_class.spatial_reference.wkid

        # Determine spatial reference of the service
        layer_sr = self._get_service_spatial_reference(service)

        # Check if spatial references match
        if layer_sr and map_sr != layer_sr:
            # Update widget's spatial reference and log a warning
            self.pydantic_class.spatial_reference = _models.SpatialReference(
                wkid=layer_sr
            )
            self._check_extent_sr()
            # self._source._update_source()
            logging.warning(
                "The layer's spatial reference does not match that of the webmap or webscene. "
                "The spatial reference of the webmap/webscene will be updated but this might "
                "affect the rendering of layers."
            )

    def _get_service_spatial_reference(self, service):
        """
        Get the spatial reference of the service. In cases where the service is a dictionary, find the corresponding service.
        If the spatial reference cannot be easily found through one of these workflows, skip and we leave map as-is. Normal services
        will have a spatial reference in their properties.
        """
        layer_sr = None
        if isinstance(service, dict) and not isinstance(service, _gis_mod.Item):
            # If the service is a dictionary, it is either a basemap from the basemap file or a gallery basemap, find corresponding service
            base_map_layers = service.get("baseMapLayers", [])
            if not base_map_layers:
                return
            base_map_layer = base_map_layers[0]
            if "itemId" in base_map_layer:
                service = self._source._gis.content.get(base_map_layer["itemId"])
                try:
                    service = service.layers[0]
                except Exception as e:
                    return
            elif "url" in base_map_layer:
                service = arcgis_layers.Service(base_map_layer["url"])
            else:
                return
            return self._check_layer_sr(service)
        if isinstance(service, _models.WMSLayer):
            layer_sr = service.spatial_references[0]
        elif isinstance(service, _models.VectorTileLayer):
            layer_sr = (
                (service.full_extent.dict().get("spatialReference", {}).get("wkid"))
                if hasattr(service, "full_extent") and service.full_extent
                else None
            )
        elif isinstance(service, _models.WebTiledLayer):
            layer_sr = service.tile_info.spatial_reference.wkid
        elif isinstance(
            service,
            (
                _gis_mod.Item,
                _models.TiledMapServiceLayer,
            ),
        ):
            if isinstance(service, _gis_mod.Item):
                service = (
                    service.get_data().get("baseMap", {}).get("baseMapLayers", [])[0]
                )

            # Check if we can get the item id from the service
            if "itemId" in service:
                item_id = service.get("itemId")
            elif hasattr(service, "item_id"):
                item_id = service.item_id
            else:
                item_id = None
            if item_id:
                service = self._source._gis.content.get(item_id)
                try:
                    if service.type == "Map Service":
                        # Map services need to be treated differently
                        service = arcgis_layers.Service(service.url)
                    else:
                        # get spatial reference from the first layer
                        service = service.layers[0]
                except:
                    return
            elif "url" in service or hasattr(service, "url"):
                # Next try with url
                service = (
                    arcgis_layers.Service(service["url"])
                    if "url" in service
                    else arcgis_layers.Service(service.url)
                )
            return self._check_layer_sr(service)
        else:
            if "spatialReference" in service.properties:
                layer_sr = service.properties["spatialReference"]
            elif (
                "extent" in service.properties
                and "spatialReference" in service.properties["extent"]
            ):
                layer_sr = service.properties["extent"]["spatialReference"]
            elif (
                "fullExtent" in service.properties
                and "spatialReference" in service.properties["fullExtent"]
            ):
                layer_sr = service.properties["fullExtent"]["spatialReference"]
            elif (
                "tileInfo" in service.properties
                and "spatialReference" in service.properties
            ):
                layer_sr = service.properties["tileInfo"]["spatialReference"]
            else:
                # Could not find a spatial reference. Taking a chance.
                return

        if isinstance(layer_sr, dict):
            layer_sr = layer_sr["wkid"]
        elif isinstance(layer_sr, str):
            layer_sr = int(layer_sr)
        elif layer_sr and not isinstance(layer_sr, int):
            # property map
            layer_sr = dict(layer_sr)["wkid"]

        return layer_sr

    def _private_to_public_url(self, layer) -> str:
        """
        In certain cases urls set on Feature Layer and other services are private urls.
        Need to find the service's public url through the Item class and create public url.
        """
        # On the source._gis, there is a property called: _use_private_url_only. This is checked as a precursor to this method call.
        # If this property is True, then the Layers being read in are using a private url, we need to find the public url and return it

        # We will write each service out first and then combine later
        # Feature Layer, MapFeatureLayer, MapRasterLayer, Table, TiledImageryLayer, ElevationLayer:
        # If serviceItemId is present, we can find the service url through the Item class
        # Caveat: If layer is coming from another gis instance, we cannot find the service url
        if layer.properties.get("serviceItemId"):
            layer_idx = os.path.basename(layer.url)
            service_item = self._source._gis.content.get(
                layer.properties["serviceItemId"]
            )
            if service_item:
                return service_item.url + "/" + layer_idx
        # Scene Layers and Vector Tile Layer
        if hasattr(layer, "_parent_url"):
            if isinstance(layer, _models.VectorTileLayer):
                return layer._parent_url
            # 3D Layers need to add /layers/<their idx> to the url if they came from Item class
            return layer._parent_url + "/layers/" + os.path.basename(layer.url)
        # default
        return layer.url
