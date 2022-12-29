#!/usr/bin/env python3

import sys
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

ip = sys.argv[1]
client = ModbusClient(ip, port=5022)
client.connect()
while True:
  '''TODO'''
  client.write_register(1, 1)  # Open Feed Pump
  client.write_register(2, 0)  # Disable oil tank sensor
  client.write_register(3, 1)  # Open Outlet Vessel
  client.write_register(4, 0)  # Open Seperator Vessel Valve
  client.write_register(8, 1)  # Open Water Vessel Valve

