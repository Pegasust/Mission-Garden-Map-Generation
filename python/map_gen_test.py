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
Zoom: 19
"""

# =============================== Constant and helpers ===========================
OUTPUT_DIR = "D:\\_uofa_classworks\\arec\\map_generator\\maps\\"

LATITUDE = 32.213482
LONGITUDE = -110.986924
ZOOM = 19

def output_file(filename):
    """
        Returns a string that appends filename after OUTPUT_DIR
    """
    return OUTPUT_DIR + filename


import gmplot_wrapper


# =========================== WRAPPERS ===============================

def test():
    gmap = gmplot_wrapper.GoogleMapPlotter(LATITUDE, LONGITUDE, ZOOM)
    gmap.heatmap([32.213255], [-110.987159])
    gmap.draw(output_file("mission_garden.html"))
    gmap.map_type = gmplot_wrapper.map_types.SATELLITE
    gmap.draw(output_file("satellite_mg.html"))

test()
