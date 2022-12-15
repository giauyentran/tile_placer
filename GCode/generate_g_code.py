from gcode_convert import *
import sys
import numpy
#from image_processing.convert_image import image_to_array
from convert_image import image_to_array
from pathlib import Path
import random

bulk_of_path = R"C:\Users\jbrown\Documents\GitHub\tile_placer\Image Conversion\test_images"
# Insert the path of modules folder
sys.path.append(bulk_of_path)

# Gantry Geometry

work_offset = 40                # mm, unworkable area of grid for flipper
tile_gap = 4                    # mm, spacing between tiles
tile_width = 23                 # mm, length of square tile
tile_pickup_height = 9          # mm,
flipper_pickup_height = 12      # mm
flipper_pickup_pos = (15.5,409) # mm
flipper_drop_pos = \
    (flipper_pickup_pos[0], flipper_pickup_pos[1] + 29)       # mm
flipper_drop_height = 101       # mm
travel_height = 30              # mm, 
# maximum travel distance
x_max = 662                   # mm
y_max = 461                   # mm
z_max = 101                 #mm
image_dim = (17, 22)            # pixels

# Movement Parameters
standard_delay = 100            # ms
suction_delay = 1000            # ms
flipper_delay = 500             # ms

# TODO: What is this?
# Image Naming Convention
image_paths = [bulk_of_path + r'\1.png', bulk_of_path + r'\2.png', bulk_of_path + r'\3.png',
               bulk_of_path + r'\4.png', bulk_of_path + r'\5.png', bulk_of_path + r'\6.png',
               bulk_of_path + r'\7.png']

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
    text_file.write(f"G91\n")  # converting to incremental - redefining origin
    text_file.write(f"G1 Z5 F1200\n")  # moves it two up from where it is
    text_file.write(f"G90\n")  # converts to absolute coords
    # gcode_delay(standard_delay, text_file)

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
            text_file.write(f"G91\n")  # converting to incremental - redefining origin
            text_file.write(f"G1 Z5 F1200\n")  # moves it two up from where it is
            text_file.write(f"G90\n")  # converts to absolute coords
            # gcode_delay(standard_delay, text_file)

            # place flipped tile
            text_file.write(f"; place flipped tile\n")
            gcode_move_z(flipper_drop_height, text_file)
            gcode_move_xy(coords, text_file)
            gcode_move_z(tile_pickup_height, text_file)
            text_file.write("place_tile")

            gcode_valve("CLOSE", text_file)
            gcode_delay(standard_delay, text_file)

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
    
    
    # Move to corner after finished
    gcode_move_z(z_max, text_file)
    gcode_move_xy((x_max,y_max), text_file)
    gcode_delay(10000, text_file)

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
    text_file.write(f"G91\n")
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
    text_file.write("place_tile\n")
    gcode_valve("OPEN", text_file)

    # turn off vacuum pump
    #text_file.write(f"; pump off\n")
    #gcode_delay(standard_delay, text_file)
    gcode_valve("CLOSE", text_file)
    gcode_delay(standard_delay, text_file)

# # Generate Gcode
text_file = open(r"gcode_commands.txt", "w")

# Opening Tasks
text_file.write("INITIALIZE \n") # Home toolhead
text_file.write("G90 \n")        # Specify Absolute Coordinate System
gcode_pump("ON", text_file)      # Turn On Pump

# Main Script

# dino = image_to_array(r"C:\Users\jbrown\Documents\GitHub\tile_placer\Image Conversion\test_images\dino.png", (18, 24)) #Gia filepath
# dino = image_to_array(r"/Users/giauyentran/tile_placer/GCode/1722dino.png", image_dim) #Gia filepath
#place_empty_grid(image_dim, text_file)
white_grid = numpy.full(image_dim, 1)
black_grid = numpy.full(image_dim, 0)
# #generate_all_images(image_paths)
# update_grid(white_grid, dino)

image_list = ["1722dino.png","dino1.png", "dino2.png", "dino3.png", "dino4.png", "dino5.png", "dino6.png", "dino7.png", "dino8.png", 'dino9.png', 'dino10.png','dino11.png', 'dino12.png',\
            'dino13.png', 'dino14.png', 'dino15.png', 'dino16.png', 'dino17.png', 'dino18.png', 'dino19.png', 'dino20.png', 'dino21.png', 'dino22.png',\
                'dino23.png', 'dino24.png']
# image_list.insert(0, dino)
file_path = "/Users/giauyentran/tile_placer/GCode/dino_animation/"
# initial_image = image_to_array()

for index in range(21,len(image_list)-1):
    current_image = f'{file_path}{image_list[index]}'
    print(current_image)
    next_image = f'{file_path}{image_list[index+1]}'
    print(next_image)
    prev_array = image_to_array(current_image, image_dim)
    next_array = image_to_array(next_image, image_dim)
    update_grid(prev_array, next_array)

dino24 = image_to_array('/Users/giauyentran/tile_placer/GCode/dino_animation/dino24.png', image_dim)
dino1722 = image_to_array('/Users/giauyentran/tile_placer/GCode/dino_animation/1722dino.png', image_dim)
update_grid(dino24, dino1722)

for index in range(0,len(image_list)-1):
    current_image = f'{file_path}{image_list[index]}'
    print(current_image)
    next_image = f'{file_path}{image_list[index+1]}'
    print(next_image)
    prev_array = image_to_array(current_image, image_dim)
    next_array = image_to_array(next_image, image_dim)
    update_grid(prev_array, next_array)

# Closing Tasks
text_file.write("M84 \n")           # Turn off motors
gcode_pump('OFF', text_file) # Turn off pump
text_file.close()         

# convert .txt to .gcode
p = Path('gcode_commands.txt')
p = p.rename(f'gcode_commands_{random.randint(0, 10000)}.txt')
p.rename(p.with_suffix('.gcode'))