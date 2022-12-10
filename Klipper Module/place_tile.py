class PrinterPlaceProbe:
    def __init__(self,config):
        self.printer = config.get_printer()
        gcode = self.printer.lookup_object("gcode")
        gcode.register_command("AMOGUS", self.cmd_AMOGUS)
    def cmd_AMOGUS(self, gcmd):
        gcmd.respond_info("sus")

def load_config(config):
    return PrinterPlaceProbe(config)

# May need later
# def get_status(self, eventtime):
#     return {'last_query': self.last_state,
#         'last_z_offset': self.last_z_offset}

# def get_status(self, eventtime):
#     return {'value': self.last_value}