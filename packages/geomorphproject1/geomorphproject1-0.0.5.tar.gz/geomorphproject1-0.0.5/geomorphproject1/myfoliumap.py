import folium


class Map(folium.Map):
    def __init__(self, center=(0, 0), zoom_start=2, **kwargs):
        super().__init__(location=center, zoom_start=zoom_start, **kwargs)
        folium.LayerControl().add_to(self)


# Instantiate and save the map
m = Map(center=(35.96, -83.92), zoom_start=10)
m.save("myfoliumap.html")
print("Map saved as myfoliumap.html")
