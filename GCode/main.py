from movement import *
from gcode_convert import *
from parameters import *

# Generate Gcode
text_file = open(text_file_name, "w")

# Opening Tasks
gcode_home(text_file) # Home toolhead
gcode_abs_coords(text_file)        # Specify Absolute Coordinate System
gcode_pump("ON", text_file)      # Turn On Pump

# Main Script
# dino = image_to_array(r"C:\Users\jbrown\Documents\GitHub\tile_placer\Image Conversion\test_images\dino.png", (18, 24)) #Gia filepath
# dino = image_to_array(r"/Users/giauyentran/tile_placer/GCode/1722dino.png", image_dim) #Gia filepath
# place_empty_grid(image_dim, text_file)
white_grid = numpy.full(image_dim, 1)
black_grid = numpy.full(image_dim, 0)
# #generate_all_images(image_paths)
# update_grid(white_grid, dino)

image_list = ["1722dino.png","dino1.png", "dino2.png", "dino3.png", "dino4.png", "dino5.png", "dino6.png", "dino7.png", "dino8.png", 'dino9.png', 'dino10.png','dino11.png', 'dino12.png',\
            'dino13.png', 'dino14.png', 'dino15.png', 'dino16.png', 'dino17.png', 'dino18.png', 'dino19.png', 'dino20.png', 'dino21.png', 'dino22.png',\
                'dino23.png', 'dino24.png']
# image_list.insert(0, dino)
file_path = "/Users/giauyentran/Desktop/tile_placer/GCode/dino_animation/"
# initial_image = image_to_array()

dino1 = image_to_array('/Users/giauyentran/Desktop/tile_placer/GCode/dino_animation/dino1.png', image_dim)
dino2 = image_to_array('/Users/giauyentran/Desktop/tile_placer/GCode/dino_animation/dino2.png', image_dim)
update_grid(dino1, dino2, text_file)

# for index in range(0,len(image_list)-1):
#     current_image = f'{file_path}{image_list[index]}'
#     print(current_image)
#     next_image = f'{file_path}{image_list[index+1]}'
#     print(next_image)
#     prev_array = image_to_array(current_image, image_dim)
#     next_array = image_to_array(next_image, image_dim)
#     update_grid(prev_array, next_array)

# Closing Tasks
text_file.write("M84 \n")           # Turn off motors
gcode_pump('OFF', text_file) # Turn off pump
text_file.close()         

# convert .txt to .gcode
p = Path('gcode_commands.txt')
p = p.rename(f'gcode_commands_{random.randint(0, 10000)}.txt')
p.rename(p.with_suffix('.gcode'))