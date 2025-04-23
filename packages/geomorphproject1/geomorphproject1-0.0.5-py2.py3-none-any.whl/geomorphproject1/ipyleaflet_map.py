from ipyleaflet import (
    Map as LeafletMap,
    basemaps,
    LayersControl,
    GeoJSON,
    TileLayer,
    ImageOverlay,
    VideoOverlay,
    WMSLayer,
)
import geopandas as gpd
import json


class CustomLeafletMap(LeafletMap):
    """
    Interactive map using ipyleaflet with support for basemaps, vector data,
    raster imagery, image/video overlays, and WMS layers.
    """

    def __init__(self, center=(20, 0), zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_basemap(self, name="OpenStreetMap"):
        parts = name.split(".")
        result = basemaps
        for part in parts:
            result = result.get(part)
            if result is None:
                raise ValueError(f"Invalid basemap: {name}")
        self.add_layer(result)

    def add_layer_control(self):
        self.add_control(LayersControl())

    def add_vector(self, filepath):
        gdf = gpd.read_file(filepath)
        geo_json = json.loads(gdf.to_json())
        layer = GeoJSON(data=geo_json)
        self.add_layer(layer)

    def add_raster(self, url, name=None, colormap=None, opacity=1.0):
        """Add a raster tile layer (COG or XYZ)."""
        tile_layer = TileLayer(url=url, name=name or "Raster", opacity=opacity)
        self.add_layer(tile_layer)

    def add_image(self, url, bounds, opacity=1.0):
        """Add a static image overlay."""
        img_layer = ImageOverlay(url=url, bounds=bounds, opacity=opacity)
        self.add_layer(img_layer)

    def add_video(self, url, bounds, opacity=1.0):
        """Add a video overlay."""
        video_layer = VideoOverlay(url=url, bounds=bounds, opacity=opacity)
        self.add_layer(video_layer)

    def add_wms_layer(self, url, layers, name, format="image/png", transparent=True):
        """Add a WMS tile layer."""
        wms_layer = WMSLayer(
            url=url, layers=layers, name=name, format=format, transparent=transparent
        )
        self.add_layer(wms_layer)
