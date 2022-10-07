#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

#####################################
# Code
#####################################
def get_ip():
    from netifaces import interfaces, ifaddresses, AF_INET
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        if ifaceName == "enp0s3":
            return ''.join(addresses)

client = ModbusClient(str(get_ip()), port=5020)

try:
    client.connect()
    while True:
        rq = client.write_register(0x10, 1) # Run Plant, Run!
        rq = client.write_register(0x1, 0) # Level Sensor
        rq = client.write_register(0x2, 1) # Limit Switch
        rq = client.write_register(0x3, 0) # Motor
        rq = client.write_register(0x4, 1) # Nozzle
except KeyboardInterrupt:
    client.close()
except ConnectionException:
    print("Unable to connect / Connection lost")
