'''
Functions to control the om
'''

from parameters import *
from gcode_convert import *
import convert_image

def get_coord(tile_index):
    '''
    Converts tile index to gantry coordinates.

    Args:
        tile_index

    Returns a 2-tuple with corresponding to (x,y) in the gantry space.
    '''
   
    t_x = tile_index[0]
    t_y = tile_index[1]

    x = (tile_width + tile_gap) * t_x + work_offset
    y = (tile_width + tile_gap) * t_y

    return (x,y)

def place_tile_legacy(tile_coordinates, text_file):
    '''
    TODO: determine how to do this

    Places an empty grid, the starting "image".

    Args:
        image_array: a 2D binary array with each value representing a pixel
    '''

    c = tile_coordinates[0]
    r = tile_coordinates[1]
    tile_index = (c + 1, r + 1)
    coords = get_coord(tile_index)

    # GCode command
    # pick up tile from flipper
    gcode_move_z(travel_height, text_file)
    text_file.write(f"; pick up tile from flipper\n")
    gcode_delay(flipper_delay, text_file)
    gcode_move_xy(flipper_pickup_pos, text_file)
    gcode_valve("OPEN", text_file)
    gcode_move_z(flipper_pickup_height, text_file)
    text_file.write("place_tile")
    gcode_delay(standard_delay, text_file)
    gcode_incr_coords(text_file)    # converting to incremental - redefining origin
    gcode_move_z(5, text_file)      # moves it two up from where it is
    gcode_abs_coords(text_file)     # converts to absolute coords

    # place flipped tile
    text_file.write(f"; place flipped tile\n")
    gcode_move_z(travel_height, text_file)
    gcode_move_xy(coords, text_file)
    gcode_move_z(tile_pickup_height, text_file)
    text_file.write("place_tile")

    gcode_valve("CLOSE", text_file)
    gcode_delay(standard_delay, text_file)

def place_empty_grid(image_dimensions, text_file):
    '''
    TODO: determine how to do this

    Places an empty grid, the starting "image".

    Args:
        image_dimensions: a 2-tuple representing the (height, width) of the
            image in pixels
        image_array: a 2D binary array with each value representing a pixel
    '''

    for r in range(image_dimensions[0]):
        for c in range(image_dimensions[1]):
            tile_index = (c+1, r+1)
            coords = get_coord(tile_index)

            # pick up tile from flipper
            gcode_move_z(flipper_drop_height, text_file)
            text_file.write(f"; pick up tile from flipper\n")
            gcode_delay(flipper_delay, text_file)
            gcode_move_xy(flipper_pickup_pos, text_file)
            gcode_valve("OPEN", text_file)
            gcode_move_z(flipper_pickup_height, text_file)
            text_file.write("place_tile")
            gcode_delay(standard_delay, text_file)
            gcode_incr_coords(text_file)  # converting to incremental - redefining origin
            gcode_move_z(5, text_file)    # moves it two up from where it is
            gcode_abs_coords(text_file)   # converts to absolute coords

            # place flipped tile
            text_file.write(f"; place flipped tile\n")
            gcode_move_z(flipper_drop_height, text_file)
            gcode_move_xy(coords, text_file)
            gcode_move_z(tile_pickup_height, text_file)
            text_file.write("place_tile")

            gcode_valve("CLOSE", text_file)
            gcode_delay(standard_delay, text_file)

def update_grid(previous_image, updated_image, text_file):
    '''
    Change image displayed on grid

    Args:
        previous_image: a 2D binary array representing the image to be replaced
        updated_image: a 2D binary array representing the image to be plotted
    '''

    for r in range(image_dim[0]):
        for c in range(image_dim[1]):
            if previous_image[r][c] != updated_image[r][c]:
                flip_tile((c+1, r+1), text_file)
    
    
    # Move to corner after finished
    gcode_move_z(z_max, text_file)
    gcode_move_xy((x_max,y_max), text_file)
    gcode_delay(10000, text_file)

def generate_all_images(image_paths):
    '''
    Generate sequence of binary images from raw images.

    Args:
        image_paths: a list of strings, with each string denoting the filepaths
            of the images to plot
    '''
    for i in range(1, len(image_paths)):
        img1_arr = convert_image.image_to_array(image_paths[i-1])
        print(f"img {i-1} against img {i}")
        img2_arr = convert_image.image_to_array(image_paths[i])
        update_grid(img1_arr, img2_arr)

def flip_tile(tile_index, text_file):
    '''
    Generate Gcode to flip tile and place.

    Args:
        tile_index: the position of the tile in the grid, with the lower left corner starting at (1,1)
        text_file: a string denoting the filepath of the .txt file with Gcode commands
    '''

    text_file.write(f"G1 Z{travel_height}\n")
    tile_coords = get_coord(tile_index)

    # pick up tile to flip
    text_file.write(f"; pick up tile\n")
    gcode_move_z(travel_height, text_file)
    gcode_move_xy(tile_coords, text_file)
    gcode_valve("OPEN", text_file)
    gcode_move_z(tile_pickup_height, text_file)
    gcode_probe(text_file)
    gcode_incr_coords(text_file)
    gcode_delay(standard_delay, text_file)
    gcode_incr_coords(text_file)  # converting to incremental - redefining origin
    gcode_move_z(2, text_file)    # moves it two up from where it is
    gcode_abs_coords(text_file)   # converts to absolute coords
    gcode_move_z(travel_height, text_file)

    # drop tile into flipper
    text_file.write(f"; drop tile into flipper\n")
    gcode_move_z(flipper_drop_height, text_file)
    gcode_move_xy(flipper_drop_pos, text_file)
    gcode_delay(standard_delay, text_file)
    gcode_valve("CLOSE", text_file)
    gcode_delay(standard_delay, text_file)
    gcode_valve("OPEN", text_file)

    # pick up tile from flipper
    text_file.write(f"; pick up tile from flipper\n")
    gcode_delay(flipper_delay, text_file)
    gcode_move_xy(flipper_pickup_pos, text_file)
    gcode_move_z(flipper_pickup_height, text_file)
    gcode_probe(text_file)
    gcode_delay(standard_delay, text_file)
    gcode_incr_coords(text_file)  # converting to incremental - redefining origin
    gcode_move_z(5, text_file)    # moves it two up from where it is
    gcode_abs_coords(text_file)   # converts to absolute coords
    #gcode_delay(standard_delay, text_file)

    # place flipped tile
    text_file.write(f"; place flipped tile\n")
    gcode_move_z(travel_height, text_file)
    gcode_move_xy(tile_coords, text_file)
    gcode_move_z(tile_pickup_height, text_file)
    text_file.write("place_tile\n")
    gcode_valve("OPEN", text_file)

    # turn off vacuum pump
    #text_file.write(f"; pump off\n")
    #gcode_delay(standard_delay, text_file)
    gcode_valve("CLOSE", text_file)
    gcode_delay(standard_delay, text_file)