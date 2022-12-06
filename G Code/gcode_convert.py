
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

def gcode_pump(state):
    # TODO: confirm this Gcode command
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        state: a string describing the desired state of the pump, either "OFF" or "ON"

    Returns a string with the Gcode command to move to coords.
    '''

    if state == "OFF":
        return("TURN_OFF_PUMP\n")
    elif state == "ON":
        return("TURN_ON_PUMP\n")
    else:
        return("Error: Pump state invalid")