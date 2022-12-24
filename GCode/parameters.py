# Gantry Geometry
work_offset = 40                # mm, unworkable width of grid due to flipper
tile_gap = 4                    # mm, spacing between tiles
tile_width = 23                 # mm, length of square tile
tile_pickup_height = 9          # mm,
flipper_pickup_height = 12      # mm
flipper_pickup_pos = (15.5,409) # mm
flipper_drop_pos = \
    (flipper_pickup_pos[0], flipper_pickup_pos[1] + 29)       # mm
flipper_drop_height = 101       # mm
travel_height = 30              # mm, 
x_max = 662                     # mm
y_max = 461                     # mm
z_max = 101                     # mm
image_dim = (17, 22)            # pixels

# Movement Parameters
standard_delay = 100            # ms
suction_delay = 1000            # ms
flipper_delay = 500             # ms
xy_speed = 1000                 # mm/s, default speed: 1000
z_speed = 600                   # mm/s , default speed: 600


text_file_name = "gcode_commands.txt"

# bulk_of_path = R"C:\Users\jbrown\Documents\GitHub\tile_placer\Image Conversion\test_images"
# # Insert the path of modules folder
# sys.path.append(bulk_of_path)