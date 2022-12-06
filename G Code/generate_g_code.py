from gcode_convert import *
# from convert_image import * #TODO: import

storage_width = 100          # mm
dist_between_tiles = 5      # mm
tile_width = 75             # mm
flipper_drop_height = 96    # mm
tile_pickup_height = 2      # mm
flipper_pickup_height = 6  # mm
flipper_pickup_pos = (60,150)     # mm
flipper_drop_pos = (flipper_pickup_pos[0] - 45, flipper_pickup_pos[1])       # mm
travel_height = 30         # mm
default_speed = 200         # RPM 
vacuum_pin = 2
image_dimensions = [18, 24]


def get_coord(tile_index):
    '''
    converts tile index to gantry coordinates

    Args:
        tile_index
    '''
    t_x = tile_index[0]
    t_y = tile_index[1]
    x = (storage_width - (tile_width/2)) + (dist_between_tiles + tile_width)*t_x
    y = (storage_width - (tile_width/2)) + (dist_between_tiles + tile_width)*t_y

    return (x,y)

def place_empty_grid(image_array, text_file):
    '''
    iterates through image and returns a coordinate
    '''
    
    for r in range(len(image_array)):
        for c in range(len(image_array[r])):
            tile_index = (r+1,c+1)
            coords = get_coord(tile_index)

            # G Code command
            text_file.write(f"G1 Z{travel_height}\n")
            text_file.write(f"G1 X{coords[0]} Y{coords[1]}\n")

    pass
            

def update_grid(previous_image, updated_image):
    '''
    Change image displayed on grid
    '''
    for r in range(len(previous_image)):
        for c in range(len(previous_image[r])):
            if previous_image[r][c] != updated_image[r][c]:
                flip_tile((r+1,c+1), text_file)
    pass

def flip_tile(tile_index, text_file):
    '''
    Generate Gcode to flip tile and place.

    Args:
        tile_index: the position of the tile in the grid, with the lower left corner starting at (1,1)
        text_file: a string denoting the filepath of the .txt file with Gcode commands
    '''
    
    text_file.write(f"G1 Z{travel_height}\n")
    tile_coords = get_coord(tile_index)

    # pick up to tile to flip
    text_file.write(gcode_move_xy(tile_coords))
    text_file.write(gcode_move_z(tile_pickup_height))
    text_file.write(gcode_pump(vacuum_pin, "HIGH"))

    # drop tile into flipper
    text_file.write(gcode_move_z(flipper_drop_height))
    text_file.write(gcode_move_xy(flipper_drop_pos))
    text_file.write(gcode_pump(vacuum_pin, "LOW"))

    # pick up tile
    text_file.write(gcode_move_xy(flipper_pickup_pos))
    text_file.write(gcode_move_z(flipper_pickup_height))
    text_file.write(gcode_pump(vacuum_pin, "HIGH"))

    # place flipped tile
    text_file.write(gcode_move_z(travel_height))
    text_file.write(gcode_move_xy(tile_coords))
    text_file.write(gcode_move_z(tile_pickup_height))

    # turn off vacuum pump
    text_file.write(gcode_pump(vacuum_pin, "LOW"))

initial_image = [([0]*image_dimensions[1]) for i in range(image_dimensions[0])]
print(initial_image)
test_image = convert_image()

text_file = open("G Code/gcode_commands.txt", "w")
place_empty_grid(initial_image, text_file)
update_grid(initial_image, test_image)
text_file.close()
