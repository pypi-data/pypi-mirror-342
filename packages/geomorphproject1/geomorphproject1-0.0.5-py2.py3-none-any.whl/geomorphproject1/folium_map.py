import folium
import geopandas as gpd
from folium.raster_layers import TileLayer, ImageOverlay, VideoOverlay, WmsTileLayer


class CustomFoliumMap(folium.Map):
    """
    Interactive map using folium with support for basemaps, vector data,
    raster imagery, image/video overlays, and WMS layers.
    """

    def __init__(self, location=(20, 0), zoom_start=2, **kwargs):
        super().__init__(location=location, zoom_start=zoom_start, **kwargs)

    def add_basemap(self, tiles="OpenStreetMap", attr=None):
        folium.TileLayer(tiles=tiles, attr=attr or tiles).add_to(self)

    def add_layer_control(self):
        folium.LayerControl().add_to(self)

    def add_vector(self, filepath):
        gdf = gpd.read_file(filepath)
        folium.GeoJson(gdf, name="Vector Layer").add_to(self)

    def add_raster(self, url, name=None, colormap=None, opacity=1.0, attr=None):
        TileLayer(
            tiles=url,
            name=name or "Raster",
            opacity=opacity,
            attr=attr or "Attribution Required",
        ).add_to(self)

    def add_image(self, url, bounds, opacity=1.0):
        ImageOverlay(image=url, bounds=bounds, opacity=opacity, name="Image").add_to(
            self
        )

    def add_video(self, url, bounds, opacity=1.0):
        VideoOverlay(
            video_url=url, bounds=bounds, opacity=opacity, name="Video"
        ).add_to(self)

    def add_wms_layer(self, url, layers, name, format="image/png", transparent=True):
        WmsTileLayer(
            url=url, layers=layers, name=name, fmt=format, transparent=transparent
        ).add_to(self)
