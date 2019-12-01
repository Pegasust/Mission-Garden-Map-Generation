"""
    map_gen.py
    Author: Hung Tran
    Purpose: Draw a map or maps of Mission Garden.

    Since there is no API key, the map will turn out to be
    a bit weird, I'm sorry, I tried my best to find a
    non-costly solution.
"""


"""
INFO:
Lat: 32.213482
Lon: -110.986924
Zoom: 20
"""

# =============================== Constant and helpers ===========================
OUTPUT_DIR = "D:\\_uofa_classworks\\arec\\map_generator\\maps\\"

LATITUDE = 32.213482
LONGITUDE = -110.987034
ZOOM = 20

def output_file(filename):
    """
        Returns a string that appends filename after OUTPUT_DIR
    """
    return OUTPUT_DIR + filename


import gmplot_wrapper
from map_draw_formatter import *

# =========================== WRAPPERS ===============================

def test():
    gmap = gmplot_wrapper.GoogleMapPlotter(LATITUDE, LONGITUDE, ZOOM)
    # gmap.heatmap([32.213255], [-110.987159])
    polygons = parse_polygons("../map_data/Spanish Crops - Drawing Data.csv")
    for poly in polygons.values():
        print(poly)
        gmap.polygon(poly[0], poly[1], **poly[2])
    gmap.draw(output_file("mission_garden.html"))
    gmap.map_type = gmplot_wrapper.map_types.SATELLITE    
    for poly in polygons.values():
        print(poly)
        gmap.polygon(poly[0], poly[1], **poly[2])
    gmap.draw(output_file("satellite_mg.html"))

test()
