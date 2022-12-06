from generate_g_code import get_coord, generate_g_code
from blah_path import GCodeCommand, GCodeDispatch
cmd = generate_g_code((50, 50))
send_cmd = GCodeCommand(cmd, )

# Define printer object
printer = Printer()

# Define GCodeDispatch Object
dispatch = GCodeDispatch(printer)

# Call process commands
dispatch._process_commands(self, commands, need_ack=True)
