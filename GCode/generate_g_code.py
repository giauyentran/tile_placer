from gcode_convert import *
import sys
import numpy
# from .image_processing.convert_image import image_to_array
from convert_image import image_to_array

bulk_of_path = R"/Users/giauyentran/tile_placer/Image Conversion/test_images"
# Insert the path of modules folder
sys.path.append(bulk_of_path)

# Gantry Geometry
work_offset = 98.5              # mm, unworkable area of grid for flipper
dist_between_tiles = 2          # mm
tile_width = 23                 # mm
flipper_drop_height = 100       # mm
tile_pickup_height = 6          # mm
flipper_pickup_height = 9       # mm
flipper_pickup_pos = (15.5,411) # mm
flipper_drop_pos = (flipper_pickup_pos[0], flipper_pickup_pos[1] + 38)       # mm
travel_height = 30              # mm

# Movement Parameters
default_speed = 200             # RPM 
image_dim = (18, 22)            # pixels
standard_delay = 100            # ms
suction_delay = 1000            # ms
flipper_delay = 400             # ms

# Image Naming Convention
image_paths = [bulk_of_path + r'\1.png', bulk_of_path + r'\2.png', bulk_of_path + r'\3.png',
               bulk_of_path + r'\4.png', bulk_of_path + r'\5.png', bulk_of_path + r'\6.png',
               bulk_of_path + r'\7.png']

delay_rate = 100
work_offset = 100
fast_speed = 12000

def get_coord(tile_index):
    '''
    Converts tile index to gantry coordinates.

    Args:
        tile_index

    Returns a 2-tuple with corresponding to (x,y) in the gantry space.
    '''
   
    t_x = tile_index[0]
    t_y = tile_index[1]

    x = (tile_width + dist_between_tiles) * t_x + work_offset
    y = (tile_width + dist_between_tiles) * t_y + 3

    return (x,y)

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

            # G-code command
            # Pick up tile from flipper
            gcode_move_z(travel_height, text_file)
            gcode_move_xy(flipper_pickup_pos, text_file)
            gcode_probe(text_file)
            gcode_move_z(flipper_pickup_height, text_file)
            gcode_delay(standard_delay, text_file)
            gcode_valve("OPEN", text_file)

            # Move to tile location
            gcode_move_z(travel_height, text_file)
            gcode_move_xy(coords, text_file)
            gcode_probe(text_file)
            gcode_move_z(tile_pickup_height, text_file)
            gcode_delay(standard_delay, text_file)
            gcode_valve("CLOSE", text_file)
            gcode_delay(standard_delay, text_file)
            gcode_move_z(travel_height, text_file)
            

def update_grid(previous_image, updated_image):
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

def generate_all_images(image_paths):
    '''
    Generate sequence of binary images from raw images.

    Args:
        TODO
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
    gcode_delay(standard_delay, text_file)
    text_file.write(f"G91\n") # converting to incremental - redefining origin
    text_file.write(f"G1 Z2\n") # moves it two up from where it is
    text_file.write(f"G90\n") # converts to absolute coords
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
    text_file.write(f"G91\n")  # converting to incremental - redefining origin
    text_file.write(f"G1 Z5 F1200\n")  # moves it two up from where it is
    text_file.write(f"G90\n")  # converts to absolute coords
    #gcode_delay(standard_delay, text_file)

    # place flipped tile
    text_file.write(f"; place flipped tile\n")
    gcode_move_z(travel_height, text_file)
    gcode_move_xy(tile_coords, text_file)
    gcode_move_z(tile_pickup_height, text_file)
    gcode_probe(text_file)

    # turn off vacuum pump
    #text_file.write(f"; pump off\n")
    #gcode_delay(standard_delay, text_file)
    gcode_valve("CLOSE", text_file)
    gcode_delay(standard_delay, text_file)

# Generate Gcode
text_file = open(r"gcode_commands.txt", "w")
text_file.write("INITIALIZE \n")
text_file.write("G90 \n")
text_file.write(f"G1 X0 F{fast_speed} \n")
gcode_pump("ON", text_file)
dino = image_to_array(r"/Users/giauyentran/tile_placer/Image Conversion/test_images/dino.png", (18, 22))
#place_empty_grid((22, 18), text_file)
white_grid = numpy.full((18, 22), 1)
#generate_all_images(image_paths)
update_grid(white_grid, dino)
text_file.close()

