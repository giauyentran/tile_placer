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
        self.position_min = config.getfloat('position_min', None)
        self.gcode = self.printer.lookup_object("gcode")
        self.query_endstops = self.printer.load_object(config,
            'query_endstops')
        self.printer.register_event_handler("klippy:connect",
            self.handle_connect)
        self.gcode.register_command("PROBE_TILE", self.cmd_PROBE_TILE)

    def cmd_PROBE_TILE(self, gcmd):
        self._detect_tile(self.z_endstop)

    def handle_connect(self):
        for endstop, name in self.query_endstops.endstops:
            if name == "z":
                self.z_endstop = EndstopWrapper(self.config, endstop)

    def _detect_tile(self, endstop):
        toolhead = self.printer.lookup_object("toolhead")
        toolhead_position = toolhead.get_position()
        toolhead_position[2] = 0.0 #self.position_min
        phoming = self.printer.lookup_object("homing")
        current_position = phoming.probing_move(endstop, toolhead_position, 100)
        self.gcode.respond_info("sus")
        # self.gcode.respond_info("probe at %.3f,%.3f is z=%.6f"
        #         % (current_position[0], current_position[1], current_position[2]))

def load_config(config):
    return PrinterPlaceProbe(config)
