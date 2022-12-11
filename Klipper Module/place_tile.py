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
    def __init__(self,config):
        self.printer = config.get_printer()
        # self.toolhead = self.printer.lookup_object("toolhead")
        self.phoming = self.printer.lookup_object("homing")
        gcode = self.printer.lookup_object("gcode")
        self.printer.register_event_handler("klipper:connect",
            self.handle_connect)
        gcode.register_command("AMOGUS", self.cmd_AMOGUS)

    def cmd_AMOGUS(self, gcmd):
        gcmd.respond_info("sus")
        self._detect_tile(self.z_endstop)

    def handle_connect(self):
        for endstop, name in self.query_endstops.endstops:
            if name == "z":
                self.z_endstops = EndstopWrapper(self.config, endstop)

    def _detect_tile(self, endstop):
        toolhead = self.printer.lookup_object("toolhead")
        toolhead_position = toolhead.get_position()
        self.phoming.probing_move(endstop, toolhead_position, 20)

def load_config(config):
    return PrinterPlaceProbe(config)
