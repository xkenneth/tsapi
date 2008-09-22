import sys

dev_name = sys.argv[1]

from tsapi import SuperSerial
from tsapi import commands
dev = SuperSerial.SuperSerial(dev_name)
dev.timeout = 2
print commands.get_tool_time(dev)



