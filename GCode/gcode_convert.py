'''
Functions to convert desired gantry movement into strings denoting G-code commands
'''

xy_speed = 1000 # mm/s, default speed: 1000
z_speed = 600   # mm/s , default speed: 600

def gcode_move_xy(coords, text_file):
    '''
    Generates G-code command to move toolhead to a coordinate.

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to coords.
    '''
    text_file.write(f"G1 X{coords[0]} Y{coords[1]} F{xy_speed*60}\n")

def gcode_move_z(z, text_file):
    '''
    Generates Gcode command to move toolhead to specified height, with z being
    zeroed at the base plate and the positive z direction being upwards.

    Args:
        coords: A 2-tuple with the (x,y) cartesian coordinate of the target location
        speed: An int denoting the desired speed speed of axis movement in mm/s
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to move to a specified height.
    '''
    text_file.write(f"G1 Z{z} F{z_speed * 60}\n")

def gcode_pump(state, text_file):
    # TODO: confirm this Gcode command
    '''
    Generates Gcode command to turn pump on and off. 

    Args:
        state: a string describing the desired state of the pump, either "OFF" or "ON"
        speed: An int denoting the desired speed speed of axis movement in mm/s
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to turn pump on/off.
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
    Generates Gcode command to open and close the solenoid connected to the pump.

    Args:
        state: a string describing the desired state of the pump, either "OPEN" or "CLOSE"
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to open/close the solenoid valve.
    '''

    if state == "OPEN":
        text_file.write("OPEN_VALVE\n")
    elif state == "CLOSE":
        text_file.write("CLOSE_VALVE\n")
    else:
        text_file.write("Error: Valve state invalid")

def gcode_delay(delay_time, text_file):
    '''
    Generate Gcode command to add a time-based delay.

    Args:
        delay_time: An integer denoting the amount of time to delay in ms
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command for a time-based delay.
    '''

    text_file.write(f"G4 P{delay_time} \n")

def gcode_probe(text_file):
    '''
    Generate Gcode command to probe tile to ensure contact with the nozzle.

    Args:
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    Returns a string with the Gcode command to probe tiles.
    '''

    text_file.write(f"probe_tile\n")

def gcode_home(text_file):
    '''
    Generate Gcode command to home toolhead

    Args:
        text_file: a string denoting the filepath of the .txt file with Gcode commands

    '''
    text_file.write("INITIALIZE \n")

def gcode_motors_off(text_file):
    '''
    Generate Gcode command to turn off motors

    Args:
        text_file: a string denoting the filepath of the .txt file with Gcode commands 

    '''
    text_file.write("M84 \n")

def gcode_abs_coords(text_file):
    '''
    Generate Gcode command to use absolute coordinates

    Args:
        text_file: a string denoting the filepath of the .txt file with Gcode commands 
        
    '''
    text_file.write("G90 \n")

def gcode_rel_coords(text_file):
    '''
    Generate Gcode command to use relative coordinates

    Args:
        text_file: a string denoting the filepath of the .txt file with Gcode commands 
        
    '''
    text_file.write("G91 \n")