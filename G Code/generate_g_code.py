storage_width = 10          # mm
dist_between_tiles = 5      # mm
tile_width = 23             # mm
flipper_drop_height = 96    # mm
tile_pickup_height = 2      # mm
flipper_pickup_height = 6  # mm
flipper_pickup_pos = (15,15)     # mm
flipper_drop_pos = (flipper_pickup_pos[0] + 45, flipper_pickup_pos[1])       # mm
travel_height = 30         # mm
default_speed = 200         # RPM 
vacuum_pin = 2


def get_coord(tile_pos):
    '''
    converts tile index to gantry coordinates
    '''
    t_x = tile_pos[0]
    t_y = tile_pos[1]
    x = (storage_width - (tile_width/2)) + (dist_between_tiles + tile_width)*t_x
    y = (storage_width - (tile_width/2)) + (dist_between_tiles + tile_width)*t_y

    return (x,y)

def place_empty_grid(image_array):
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
                flip_tile((r,c))
    pass

def flip_tile(tile_index):
    '''
    Move tile to flipper and place.
    '''

    coords = get_coord(tile_index)
    
    text_file.write(f"G1 Z{travel_height}\n")

    # move to get_coords(tile_index)
    text_file.write(f"G1 X{coords[0]} Y{coords[1]}\n")
    text_file.write(f"G1 Z{tile_pickup_height}\n")

    # turn on vacuum pump
    text_file.write(f"SET_PIN PIN = {vacuum_pin} VALUE = HIGH\n")

    # move to flipper @ flipper_drop_pos
    text_file.write(f"G1 Z{flipper_drop_height}\n")
    text_file.write(f"G1 X{flipper_drop_pos} Y{flipper_drop_pos}\n")

    # turn off vacuum pump
    text_file.write(f"SET_PIN PIN = {vacuum_pin} VALUE = LOW\n")

    # move to pickup @ flipper_pickup_pos
    text_file.write(f"G1 X{flipper_pickup_pos[0]} Y{flipper_pickup_pos[1]}\n")
    text_file.write(f"G1 Z{flipper_pickup_height}\n")

    # pick up tile (turn on vacuum pump)
    text_file.write(f"SET_PIN PIN = {vacuum_pin} VALUE = HIGH\n")

    # move to get_coords(tile_index)
    text_file.write(f"G1 Z{travel_height}\n")
    text_file.write(f"G1 X{coords[0]} Y{coords[1]}\n")
    text_file.write(f"G1 Z{tile_pickup_height}\n")

    # turn off vacuum pump
    text_file.write(f"SET_PIN PIN = {vacuum_pin} VALUE = LOW\n")
    

initial_image = [[0,0], [0,0]]
test_image = [[0,1],[1,0]]

text_file = open("G Code/gcode_commands.txt", "w")
place_empty_grid(initial_image)
update_grid(initial_image, test_image)
text_file.close()



