import importlib.metadata

from .map_widget import (
    Map,
    MapContent,
    Bookmark,
    Bookmarks,
    Legend,
    LayerList,
    LayerVisibility,
    TimeSlider,
    BasemapManager,
)
from .scene_widget import Scene, SceneContent, Environment
from .group_layer import GroupLayer
from .smart_mapping import SmartMappingManager
from .offline_mapping import OfflineMapAreaManager
from . import popups, renderers, symbols, forms

__all__ = [
    "Map",
    "Scene",
    "popups",
    "renderers",
    "symbols",
    "forms",
    "OfflineMapAreaManager",
]
try:
    __version__ = importlib.metadata.version("arcgis-mapping")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
