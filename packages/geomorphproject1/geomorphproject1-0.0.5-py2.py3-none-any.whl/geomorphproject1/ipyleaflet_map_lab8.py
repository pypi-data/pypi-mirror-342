# geomorphproject1/ipyleaflet_map_lab8.py
# -------------------------------------------------
# This module defines CustomLeafletMap specifically for Lab 8.
# It provides UI widgets: a dropdown to switch basemaps and a toggle button.

from ipyleaflet import Map, basemaps, LayersControl, WidgetControl
from ipywidgets import Dropdown, Button


class CustomLeafletMap(Map):
    """
    Interactive map with UI widgets for switching basemaps using a dropdown,
    and a toggle button to hide the dropdown. Lab 8 specific.
    """

    def __init__(self, center=(20, 0), zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
        self._dropdown_widget = None
        self._close_button = None
        self.add_control(LayersControl())

    def add_basemap(self, name="OpenStreetMap"):
        self.clear_layers()
        selected = name.split(".")
        tile = basemaps
        for part in selected:
            tile = getattr(tile, part) if hasattr(tile, part) else tile[part]
        self.add_layer(tile)

    def add_basemap_dropdown(self, position="topright"):
        """
        Adds an interactive dropdown menu to switch basemaps.

        Params:
            position (str): Position of the dropdown on the map.

        Returns:
            None
        """
        dropdown = Dropdown(
            options=[
                "OpenStreetMap",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "CartoDB.DarkMatter",
            ],
            value="OpenStreetMap",
            description="Basemap:",
        )

        def on_change(change):
            if change["name"] == "value":
                self.add_basemap(change["new"])

        dropdown.observe(on_change)
        self._dropdown_widget = WidgetControl(widget=dropdown, position=position)
        self.add_control(self._dropdown_widget)

    def add_dropdown_toggle_button(self, position="topright"):
        """
        Adds a button to hide the basemap dropdown.

        Params:
            position (str): Position of the button on the map.

        Returns:
            None
        """
        button = Button(description="Hide Dropdown", layout={"width": "150px"})

        def on_click(b):
            if self._dropdown_widget:
                self.remove_control(self._dropdown_widget)
                self._dropdown_widget = None

        button.on_click(on_click)
        self._close_button = WidgetControl(widget=button, position=position)
        self.add_control(self._close_button)
