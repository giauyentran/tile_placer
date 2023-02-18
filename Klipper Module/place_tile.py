# Global variables
PLACEMENT_SPEED = 100.
TILE_THICKENESS_THRESHOLD = 2.
TILE_THICKNESS_TOLERANCE = 1.
FLIPPER_PICKUP_POSITION = (15.5,409.) # Final, testing with MK3 build area
XY_TRAVEL = 600
Z_TRAVEL = 400

# Pin definitions
# SOLENOID_PIN = "PA14" # Final, testing with MK3 fan pin :P

class EndstopWrapper:
    def __init__(self, config, endstop):
        self.mcu_endstop = endstop
        # Wrappers
        self.get_mcu = self.mcu_endstop.get_mcu
        self.add_stepper = self.mcu_endstop.add_stepper
        self.get_steppers = self.mcu_endstop.get_steppers
        self.home_start = self.mcu_endstop.home_start
        self.home_wait = self.mcu_endstop.home_wait
        self.query_endstop = self.mcu_endstop.query_endstop

class PrinterPlaceProbe:
    def __init__(self, config):
        self.config = config
        self.printer = config.get_printer()
        self.pins = self.printer.lookup_object("pins")
        #self.pins.reset_pin_sharing("SOLENOID_PIN") # Need initially, not sure how long this is persistent
        #self.solenoid = self.pins.setup_pin("pwm", SOLENOID_PIN)
        self.position_min = config.getfloat("position_min", None)
        self.gcode = self.printer.lookup_object("gcode")
        self.query_endstops = self.printer.load_object(config,
            'query_endstops')
        self.printer.register_event_handler("klippy:connect",
            self.handle_connect)
        self.gcode.register_command("PROBE_TILE", self.cmd_PROBE_TILE)
        self.gcode.register_command("PLACE_TILE", self.cmd_PLACE_TILE)

    def cmd_PROBE_TILE(self, gcmd):
        self._detect_tile(self.z_endstop)

    def cmd_PLACE_TILE(self, gcmd):
        self.PLACE_TILE()

    def PLACE_TILE(self):
        # Move Z to placement location, until z max limit switch is pressed
        z_position = self._detect_tile(self.z_endstop)
        if z_position < TILE_THICKENESS_THRESHOLD:
            if self._confirm_missing_tile(z_position):
                self._retry_tile_pickup()

    def handle_connect(self):
        for endstop, name in self.query_endstops.endstops:
            if name == "z":
                self.z_endstop = EndstopWrapper(self.config, endstop)

    def _detect_tile(self, endstop):
        toolhead = self.printer.lookup_object("toolhead")
        toolhead_position = toolhead.get_position()
        toolhead_position[2] = 0.0 #self.position_min
        phoming = self.printer.lookup_object("homing")
        current_position = phoming.probing_move(endstop, toolhead_position, PLACEMENT_SPEED)
        self.gcode.respond_info("Z at %.6f" % (current_position[2]))
        return current_position[2]

    def _confirm_missing_tile(z_position, self):
        toolhead = self.printer.lookup_object("toolhead")
        toolhead_position = toolhead.get_position()
        if toolhead_position[1] < 225:
            check_move = 25
        else:
            check_move = -25
        tile_position = (toolhead_position[0], toolhead_position[1])
        toolhead.manual_move([None, None, 20], Z_TRAVEL) # Move Z up to 20mm
        toolhead.manual_move([None, toolhead_position[1] + check_move, None], XY_TRAVEL) # Move to tile above or below
        z_position_other_tile = self._detect_tile(self.z_endstop)
        if abs(z_position_other_tile - z_position) > TILE_THICKNESS_TOLERANCE:
            return False
        else:
            return True

    def _retry_tile_pickup(self):
        toolhead = self.printer.lookup_object("toolhead")
        toolhead_position = toolhead.get_position()
        tile_position = (toolhead_position[0], toolhead_position[1])
        toolhead.manual_move([None, None, 101], Z_TRAVEL) # Move Z up to 101mm
        toolhead.manual_move([FLIPPER_PICKUP_POSITION[0], FLIPPER_PICKUP_POSITION[1], None], XY_TRAVEL) # Move to flipper pick up location
        toolhead.manual_move([None, None, 15], Z_TRAVEL) # Move Z above pickup location, prep for probe
        self._detect_tile(self.z_endstop) # Attempt tile pickup
        toolhead.manual_move([None, None, 30], Z_TRAVEL) # Move Z up to 30mm
        toolhead.manual_move([tile_position[0], tile_position[1], None], XY_TRAVEL) # Move to tile placement location
        self.PLACE_TILE()
        pass

def load_config(config):
    return PrinterPlaceProbe(config)
