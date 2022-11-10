#!/usr/bin/env python3

import sys
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

ip = sys.argv[1]                # 1 Arg = Target IP-Address
registry = int(sys.argv[2])     # 2 Arg = Registery from 0 to 16
value = int(sys.argv[3])        # 3 Arg = Value to write in registery 0 or 1
client = ModbusClient(ip, port=5020)
client.connect()
client.write_register(registry, value)
