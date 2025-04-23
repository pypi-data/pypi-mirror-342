from ipyleaflet import Map as LeafletMap, basemaps, LayersControl, GeoJSON
import geopandas as gpd
import json


class CustomLeafletMap(LeafletMap):
    """
    Interactive map using ipyleaflet with basemap, vector, and layer control.
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
