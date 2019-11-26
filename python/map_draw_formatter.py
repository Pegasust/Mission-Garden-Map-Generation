"""
    map_draw_formatter.py
    Author: Hung Tran
    Purpose: Introduction to a file format to be parsed to draw the map.
    Parser included.

"""
import lite_debug_printer


if __name__ == "__main__":
    lite_debug_printer.DEBUG = True
    lite_debug_printer.TRACE = True

from lite_debug_printer import log_trace, log_debug

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

DEFAULT_ENTRY = {ID:"id", LAT:0.00, LNG:0.00, FACE_COLOR: DEFAULT_FACE_COLOR,
                 FACE_ALPHA: DEFAULT_FACE_ALPHA, EDGE_COLOR: DEFAULT_EDGE_COLOR,
                 EDGE_ALPHA: DEFAULT_EDGE_ALPHA, EDGE_WIDTH: DEFAULT_EDGE_WIDTH
                 }
ENTRY_AT = (ID, LAT, LNG, FACE_COLOR, FACE_ALPHA, EDGE_COLOR, EDGE_ALPHA, EDGE_WIDTH)

D_LAT = 0
D_LNG = 1
D_KW_ARGS = 2
ENTRY_KW_START = 3
#D_FC = 2
#D_FA = 3
#D_EC = 4
#D_EA = 5
#D_EW = 6

def assign_kw_args(kw, entry):
    for i in range(ENTRY_KW_START, len(ENTRY_AT)):
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
            cmt_index = line.find(COMMENT_CHAR)
            if cmt_index != -1:
                line = line[0:cmt_index]
            log_trace("Before strip: {}".format((line)))
            line = line.strip()
            log_trace("After strip: {}".format((line)))
            if len(line) < len("0,0,0"):
                # Does not have any good info
                continue
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
            #poly_info[D_FC] = entry[FACE_COLOR]
            #poly_info[D_FA] = entry[FACE_ALPHA]
            #poly_info[D_EC] = entry[EDGE_COLOR]
            #poly_info[D_EA] = entry[EDGE_ALPHA]
            #poly_info[D_EW] = entry[EDGE_WIDTH]
            poly_info[D_KW_ARGS] = assign_kw_args(poly_info[D_KW_ARGS], entry)
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

if __name__ == "__main__":
    print(polygon_dict_str(parse_polygons("../map_data/Spanish Crops - Sheet1.csv")))