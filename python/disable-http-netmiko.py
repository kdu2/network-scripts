import os
import csv
from getpass import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

'''
csv file must have these fields: ip,name,location,status
example:
ip,name,location,status
10.0.0.1,switch1,building1,online
'''

infile = str(input('Enter filename: ').strip() or 'switches.csv')
filepath = "c:/temp/" + infile
if os.path.exists(filepath):
    devices = csv.DictReader(open(filepath,"r"))
else:
    raise FileNotFoundError('The file does not exist')
    exit

config_commands = [
    'no ip http server',
    'no ip http secure-server'
]

username = str(input('Enter username: ').strip() or 'admin')
password = getpass('Enter password: ')

for switch in devices:
    switchname = switch["name"]
    if switch["status"] != "offline":
        ipaddr = switch["ip"].strip()
        device = {
            "device_type": "cisco_ios",
            "host": ipaddr,
            "username": username,
            "password": password
        }
        print(f"Disabling http for {switchname}")
        try:
            net_connect = ConnectHandler(**device)
            output = net_connect.send_config_set(config_commands)
            net_connect.save_config()
            net_connect.disconnect()
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            print(error)
    else:
        print(f"Switch {switchname} is offline")
