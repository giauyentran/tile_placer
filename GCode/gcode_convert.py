"""
TODO: Docstring
"""

def gcode_move_xy(coords, text_file):
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''
    text_file.write(f"G1 X{coords[0]} Y{coords[1]}\n")

def gcode_move_z(z, text_file):
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''
    text_file.write(f"G1 Z{z}\n")

def gcode_move_xy(coords, text_file):
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''
    text_file.write(f"G1 X{coords[0]} Y{coords[1]}\n")

def gcode_pump(state, text_file):
    # TODO: confirm this Gcode command
    '''
    Generated Gcode command to move toolhead to location 

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        state: a string describing the desired state of the pump, either "OFF" or "ON"
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''

    if state == "OFF":
        text_file.write("TURN_OFF_PUMP\n")
    elif state == "ON":
        text_file.write("TURN_ON_PUMP\n")
    else:
        text_file.write("Error: Pump state invalid")

def gcode_valve(state, text_file):
    # TODO: confirm this Gcode command
    '''
    Generated Gcode command to move toolhead to location

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        state: a string describing the desired state of the pump, either "OFF" or "ON"
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''

    if state == "OPEN":
        text_file.write("OPEN_VALVE\n")
    elif state == "CLOSE":
        text_file.write("CLOSE_VALVE\n")
    else:
        text_file.write("Error: Valve state invalid")

def gcode_delay(delay_time, text_file):
    '''
    Generate Gcode command to delay

    Args:
        delay_time: An integer denoting the amount of time to delay in ms
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''

    text_file.write(f"G4 P{delay_time} \n")

def gcode_probe(text_file):
    '''
    Generate Gcode command to delay

    Args:
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to check that tile is in contact with nozzle.
    '''

    text_file.write(f"probe_tile \n")