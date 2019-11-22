SATELLITE = "SATELLITE"
ROADMAP = "ROADMAP"
HYBRID = "HYBRID"
TERRAIN = "TERRAIN"

def option_entry(map_type):
    """
        Returns a string that represents the entry of mapOptions like:
        mapTypeId: google.maps.MapTypeId.HYBRID
    """
    return f"mapTypeId: google.maps.MapTypeId.{map_type}"
