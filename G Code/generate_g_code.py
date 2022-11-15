storage_width = 10 # mm
dist_between_tiles = 5 # mm
tile_width = 23 # mm
flipper_drop_height = 15 # mm
tile_pickup_height = 0 # mm
flipper_pickup_height = 5 # mm
flipper_drop_pos = () # cartesian coords
flipper_pickup_pos = () # cartesian coords
default_height = 10 # mm
default_speed = 200 # RPM 

def get_coord(tile_pos):
    t_x = tile_pos[0]
    t_y = tile_pos[1]
    x = (storage_width - (tile_width/2)) + (dist_between_tiles + tile_width)*t_x
    y = (storage_width - (tile_width/2)) + (dist_between_tiles + tile_width)*t_y

    return (x,y)

def generate_g_code(coords):
    return f"G1 {coords[0]} {coords[1]} {default_height} {0} {default_speed}"