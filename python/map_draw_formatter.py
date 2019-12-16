"""
    map_draw_formatter.py
    Author: Hung Tran
    Purpose: Introduction to a file format to be parsed to draw the map.
    Parser included.

"""
import os
import lite_debug_printer
import statistics


if __name__ == "__main__":
    lite_debug_printer.DEBUG = True
    lite_debug_printer.TRACE = False

from lite_debug_printer import log_trace, log_debug
import gmplot_wrapper

COMMENT_CHAR = '~'
DEFAULT_EDGE_COLOR = "#000000"
DEFAULT_EDGE_ALPHA = 1.0
DEFAULT_EDGE_WIDTH = 1.0
DEFAULT_FACE_COLOR = "#000000"
DEFAULT_FACE_ALPHA = 0.3


ID = "id"
LAT = "lat"
LNG = "lng"
FACE_COLOR = "fc"
FACE_ALPHA = "fa"
EDGE_COLOR = "ec"
EDGE_ALPHA = "ea"
EDGE_WIDTH = "ew"


# ========================================== POLYGONS ==========================================


DEFAULT_ENTRY = {ID:"id", LAT:0.00, LNG:0.00, FACE_COLOR: DEFAULT_FACE_COLOR,
                 FACE_ALPHA: DEFAULT_FACE_ALPHA, EDGE_COLOR: DEFAULT_EDGE_COLOR,
                 EDGE_ALPHA: DEFAULT_EDGE_ALPHA, EDGE_WIDTH: DEFAULT_EDGE_WIDTH
                 }
ENTRY_AT = (ID, LAT, LNG, FACE_COLOR, FACE_ALPHA,\
            EDGE_COLOR, EDGE_ALPHA, EDGE_WIDTH)

D_LAT = 0
D_LNG = 1
D_KW_ARGS = 2
ENTRY_KW_START_POLYGONS = 3
#D_FC = 2
#D_FA = 3
#D_EC = 4
#D_EA = 5
#D_EW = 6


def assign_kw_args(kw, entry, entry_kw_start, ENTRY_AT):
    for i in range(entry_kw_start, len(ENTRY_AT)):
        kw[ENTRY_AT[i]] = entry[ENTRY_AT[i]]
    return kw

def parse_polygons(filename):
    """
        Parse from filename the declarations of polygons
        The format of filename should be:
        ID, lat, long, face_color, face_alpha, edge_color, edge_alpha, edge_width

        Ignores first line and any line that contains COMMENT_CHAR
        Return value:
            dict(id:string, [lats[], lngs[],{fc:=, fa:=, ec:=,ea:=,ew:=}])
    """
    last_entry = DEFAULT_ENTRY.copy()
    polygons = dict()
    with open(filename, 'r') as fobj:
        fobj.readline()   # skip the first line.
        for line in fobj:
            # parse only the non-comment string
            cmt_index = line.find(COMMENT_CHAR)
            if cmt_index != -1:
                line = line[0:cmt_index]
            # Strip out white lines and ""
            log_trace("Before strip: {}".format((line)))
            line = line.strip()
            line = line.strip("\"")
            log_trace("After strip: {}".format((line)))
            if len(line) < len("0,0,0"):
                # Does not have any good info
                continue
            # This entry defaults to be the last entry
            entry = last_entry.copy()
            # Split the values in line
            splited_words = line.split(',')
            for i in range(len(splited_words)):
                # Parse those values sequentially
                if splited_words[i] == "":
                    # Get the info from the last entry.
                    continue
                try:
                    entry[ENTRY_AT[i]] = float(splited_words[i]) if i != 0\
                        else (splited_words[i])  # ID is string
                except ValueError:
                    # Can't be expressed in floating point value
                    entry[ENTRY_AT[i]] = splited_words[i]
                log_trace("splited_word: {}, entry: {}".format(\
                    str(splited_words[i]), entry[ENTRY_AT[i]]))
            # entry is assigned
            poly_info = polygons.get(entry[ID])
            if poly_info is not None:
                # If ID already exists
                # append lats and lngs
                poly_info[D_LAT].append(entry[LAT])
                poly_info[D_LNG].append(entry[LNG])
            else:
                poly_info = [[entry[LAT]], [entry[LNG]], dict()]
                # Make it so that the entry[ID] points towards poly_info
                polygons[entry[ID]] = poly_info
            # Parse values by the most recent entry
            poly_info[D_KW_ARGS] = assign_kw_args(poly_info[D_KW_ARGS], entry,\
                                                  ENTRY_KW_START_POLYGONS,\
                                                  ENTRY_AT)
            last_entry = entry
    fobj.close()
    return polygons


def polygon_dict_str(polygons):
    s = "{\n"
    for key,value in polygons.items():
        s+=str(key)+": "
        s+=str(value)+",\n\n"
    s+="}"
    return s







# ================================================= CIRCLES ========================================

RADIUS = "radius"
DEFAULT_RADIUS = 3

DEFAULT_ENTRY_CIRCLES = {ID:"id", LAT:0.00, LNG:0.00, RADIUS: DEFAULT_RADIUS,
                         FACE_COLOR: DEFAULT_FACE_COLOR,
                         FACE_ALPHA: DEFAULT_FACE_ALPHA,
                         EDGE_COLOR: DEFAULT_EDGE_COLOR,
                         EDGE_ALPHA: DEFAULT_EDGE_ALPHA,
                         EDGE_WIDTH: DEFAULT_EDGE_WIDTH
                         }
ENTRY_AT_CIRCLES = (ID, LAT, LNG, RADIUS, FACE_COLOR,\
                    FACE_ALPHA, EDGE_COLOR, EDGE_ALPHA, EDGE_WIDTH)
D_RADIUS = 2
ENTRY_KW_START_CIRCLES = 4
D_KW_ARGS_CIRC = 3

def parse_circles(filename):
    """
        Parse from filename the declarations of circles
        The format of filename should be:
        ID, lat, long, radius, face_color, face_alpha, edge_color, edge_alpha, edge_width

        Ignores first line and any line that contains COMMENT_CHAR
        Return value:
            dict(id:string, [lats, lngs, radius, {fc:=, fa:=, ec:=,ea:=,ew:=}])
    """
    last_entry = DEFAULT_ENTRY_CIRCLES.copy()
    circs = dict()
    with open(filename, 'r') as fobj:
        for line in fobj:
            # parse only the non-comment string
            cmt_index = line.find(COMMENT_CHAR)
            if cmt_index != -1:
                line = line[0:cmt_index]
            # Strip out white lines, '"' and ""
            log_trace("Before strip: {}".format((line)))
            line = line.strip()
            line = line.strip("\"")
            log_trace("After strip: {}".format((line)))
            if len(line) < len("a,0,0,"):
                # Does not have any good info
                continue
            # This entry defaults to be the last entry
            entry = last_entry.copy()
            # Split the values in line
            splited_words = line.split(',')
            for i in range(len(splited_words)):
                # Parse those values sequentially
                if splited_words[i] == "":
                    # Info remains as the last entry
                    continue
                try:
                    entry[ENTRY_AT_CIRCLES[i]] = float(splited_words[i]) if i != 0\
                        else (splited_words[i])  # Parse ID as string
                except ValueError:
                    # Parse info as string if it can't be expressed as float
                    entry[ENTRY_AT_CIRCLES[i]] = splited_words[i]
                log_trace("splited_word: {}, entry: {}".format(\
                    str(splited_words[i]), entry[ENTRY_AT_CIRCLES[i]]))
            # entry is assigned
            circ_info = [entry[LAT], entry[LNG], entry[RADIUS], dict()]
            # Make it so that the entry[ID] points towards circ_info
            circs[entry[ID]] = circ_info
            # Parse values by the most recent entry
            circ_info[D_KW_ARGS_CIRC] = assign_kw_args(circ_info[D_KW_ARGS_CIRC],\
                                                       entry,\
                                                       ENTRY_KW_START_CIRCLES,\
                                                       ENTRY_AT_CIRCLES)
            last_entry = entry
    fobj.close()
    return circs

# ================================================= main ====================================================

CIRC_EXT = ".circles"
POLYGONS_EXT = ".polygons"

LATITUDE = 32.213482
LONGITUDE = -110.987034
ZOOM = 20

def assign_gmap(gmap, circles, polygons, make_id_points = True):
    log_trace("================== ASSIGN_GMAP() =======================")
    for polygons_dict in polygons:
        for polyname, poly in polygons_dict.items():
            log_trace(poly)
            gmap.polygon(poly[D_LAT], poly[D_LNG], **poly[D_KW_ARGS])
            if make_id_points:
                # Marker is in the position of the mean of lats and longs
                marker_lat = statistics.mean(poly[D_LAT])
                marker_long = statistics.mean(poly[D_LNG])
                log_debug("Marker: lat: {}, lng:  {}, title: {}".format(marker_lat,\
                                                                        marker_long,\
                                                                        polyname))
                gmap.marker(lat=marker_lat,lng=marker_long,title=polyname)
    for circs_dict in circles:
        for circ_name, circs in circs_dict.items():
            log_trace(circs)
            gmap.circle(circs[D_LAT], circs[D_LNG], circs[D_RADIUS], **circs[D_KW_ARGS_CIRC])
            if make_id_points:
                gmap.marker(lat=circs[D_LAT],lng=circs[D_LNG],title=circ_name)
                log_debug("Marker: lat: {}, lng:  {}, title: {}".format(circs[D_LAT],\
                                                                        circs[D_LNG],\
                                                                        circ_name))                

def parse(directory = "../map_data/", out_dir = "../maps/", api = ''):
    if directory == "":
        directory = "./"
    map_data = dict()
    circles_set = set()
    polygons_set = set()
    # circles_set contains .circles.csv files
    # polygons_set contains other .csv files.
    # map_data contains: {filename_without_ext, [paths]}
    for file in os.listdir(directory):
        name_last_index = file.find(".csv")
        if name_last_index == -1:
            continue
        log_debug("Found {}".format(file))
        circ_index = file.find(CIRC_EXT)
        if circ_index != -1:
            # file contains .circles
            circles_set.add(file)
            name_last_index = min(name_last_index,circ_index)
        else:
            # default to be polygons
            polygons_set.add(file)
            poly_index = file.find(POLYGONS_EXT)
            if poly_index != -1:
                name_last_index = min(name_last_index, poly_index)
        name = file[:name_last_index]
        map_info = map_data.get(name)
        if map_info is None:
            map_info = []
        map_info.append(file)
        log_debug("map_data[{}] = {}".format(name, map_info))
        map_data[name] = map_info
    log_debug("circles_set = {}".format(circles_set))
    log_debug("polygons_set = {}".format(polygons_set))
    # map_data, circles_set, polygons_set are assigned
    for map_name, map_paths in map_data.items():
        log_debug("map_name = {}".format(map_name))
        gmap = gmplot_wrapper.GoogleMapPlotter(LATITUDE, LONGITUDE, ZOOM, api)
        polygons = []
        circles = []
        for path in map_paths:
            parse_path = directory + path
            print("Parsing {}".format(parse_path))
            if path in polygons_set:
                polygons.append(parse_polygons(parse_path))
            elif path in circles_set:
                circles.append(parse_circles(parse_path))
        # polygons and circles are assigned
        log_debug("polies: {}".format(polygons))
        log_debug("circs: {}".format(circles))

        # Do normal type map
        output_filename = map_name + ".html"
        assign_gmap(gmap, circles, polygons)
        gmap.draw(out_dir+output_filename)
        
        # Do satellite type map
        output_filename = "satellite_"+map_name + ".html"
        gmap = gmplot_wrapper.GoogleMapPlotter(LATITUDE, LONGITUDE, ZOOM, api)
        gmap.map_type = gmplot_wrapper.map_types.SATELLITE
        assign_gmap(gmap, circles, polygons)
        gmap.draw(out_dir+output_filename)
    print("Parse complete.")
        

if __name__ == "__main__":
    parse()
