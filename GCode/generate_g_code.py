from image_processing import convert_image
from gcode_convert import *
import sys
bulk_of_path = R"C:\Users\jbrown\Documents\GitHub\tile_placer\Image Conversion\test_images"
# Insert the path of modules folder
sys.path.append(bulk_of_path)

storage_width = 100          # mm
dist_between_tiles = 5      # mm
tile_width = 25             # mm
flipper_drop_height = 96    # mm
tile_pickup_height = 3.4      # mm
flipper_pickup_height = 6  # mm
flipper_pickup_pos = (17,408)     # mm
flipper_drop_pos = (flipper_pickup_pos[0], flipper_pickup_pos[1]+35)       # mm
travel_height = 30         # mm
default_speed = 200         # RPM 
image_dimensions = [18, 24]
image_paths = [bulk_of_path + r'\1.png', bulk_of_path + r'\2.png', bulk_of_path + r'\3.png',
               bulk_of_path + r'\4.png', bulk_of_path + r'\5.png', bulk_of_path + r'\6.png',
               bulk_of_path + r'\7.png']
delay_rate = 100
work_offset = 100
def get_coord(tile_index):
    '''
    Converts tile index to gantry coordinates.

    Args:
        tile_index

    Returns a 2-tuple with corresponding to (x,y) in the gantry space.
    '''
    t_x = tile_index[0]
    t_y = tile_index[1]
    x = 25*t_x + work_offset
    y = 25*t_y

    return (x,y)

def place_empty_grid(image_dimensions, text_file):
    '''
    TODO: determine how to do this

    Places an empty grid, the starting "image".

    Args:
        image_array: a 2D binary array with each value representing a pixel
    '''
    
    for r in range(6, 10):
        for c in range(image_dimensions[0]):
            tile_index = (c+1, r+1)
            coords = get_coord(tile_index)
            print(f"r: {r} c: {c} coords: {coords}")

            # GCode command
            text_file.write(gcode_move_z(travel_height))
            text_file.write(gcode_move_xy(flipper_pickup_pos))
            text_file.write("probe_tile\n")
            text_file.write(gcode_move_z(flipper_pickup_height))
            text_file.write(gcode_valve("OPEN"))
            text_file.write(gcode_move_z(travel_height))
            text_file.write(f"G1 X{coords[0]} Y{coords[1]}\n")
            text_file.write("probe_tile\n")
            text_file.write(gcode_move_z(tile_pickup_height))
            text_file.write(gcode_valve("CLOSE"))
            text_file.write(gcode_move_z(travel_height))
    pass
            

def update_grid(previous_image, updated_image):
    '''
    Change image displayed on grid

    Args:
        previous_image: a 2D binary array representing the image to be replaced
        updated_image: a 2D binary array representing the image to be plotted
    '''
    for r in range(len(previous_image)):
        for c in range(len(previous_image[r])):
            if previous_image[r][c] != updated_image[r][c]:
                print(f"Found a difference")
                flip_tile((c+1, r+1), text_file)

def generate_all_images(image_paths):
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

    # pick up to tile to flip
    text_file.write(gcode_pump("ON"))
    text_file.write(gcode_valve("OPEN"))
    text_file.write(gcode_move_xy(tile_coords))
    text_file.write("probe_tile\n")
    text_file.write(gcode_move_z(tile_pickup_height))

    # drop tile into flipper
    text_file.write(gcode_move_z(flipper_drop_height))
    text_file.write(gcode_move_xy(flipper_drop_pos))
    text_file.write("probe_tile\n")
    text_file.write(gcode_valve("CLOSE"))
    text_file.write(f"G4 P{400} \n")
    text_file.write(gcode_valve("OPEN"))

    # pick up tile
    text_file.write(gcode_move_xy(flipper_pickup_pos))
    text_file.write("probe_tile\n")
    text_file.write(gcode_move_z(flipper_pickup_height))

    # place flipped tile
    text_file.write(gcode_move_z(travel_height))
    text_file.write(gcode_move_xy(tile_coords))
    text_file.write("probe_tile\n")
    text_file.write(gcode_move_z(tile_pickup_height))

    # turn off vacuum pump
    text_file.write(gcode_valve("CLOSE"))
    text_file.write(f"G4 P{delay_rate} \n")

initial_image = [([0]*5) for i in range(5)]
#initial_image = [[0,0],[0,0]]
test_image = [[0,1,1,1,0],[1,1,0,0,0], [1,1,0,0,0], [1,1,1,1,0], [0,1,0,1,0]]
# test_image = convert_image()


# Generate Gcode
text_file = open(r"gcode_commands.txt", "w")
text_file.write("INITIALIZE \n")
text_file.write("G90 \n")
text_file.write("G1 X0 F6000 \n")
text_file.write(gcode_pump("ON"))
place_empty_grid((24, 1), text_file)
#generate_all_images(image_paths)
#update_grid(initial_image, test_image)
text_file.close()
#print(get_coord((20, 15)))
