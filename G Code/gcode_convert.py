
def gcode_move_xy(coords):
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location

    Returns a string with the Gcode command to move to coords.
    '''
    print(f"G1 X{coords[0]} Y{coords[1]}\n")

def gcode_move_z(z):
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location

    Returns a string with the Gcode command to move to coords.
    '''
    return(f"G1 Z{z}\n")

def gcode_move_xy(coords):
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location

    Returns a string with the Gcode command to move to coords.
    '''
    return(f"G1 X{coords[0]} Y{coords[1]}\n")

def gcode_pump(vacuum_pin, state):
    # TODO: confirm this Gcode command
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location

    Returns a string with the Gcode command to move to coords.
    '''

    if state == "LOW":
        return(f"SET_PIN PIN = {vacuum_pin} VALUE = LOW\n")
    elif state == "HIGH":
        return(f"SET_PIN PIN = {vacuum_pin} VALUE = HIGH\n")
    else:
        return("Error: Pump state value invalid")