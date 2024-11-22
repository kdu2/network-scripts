import datetime
import os
import csv
from getpass import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)

'''
csv file must have these fields: ip,name,location,status
example:
ip,name,location,status
10.0.0.1,switch1,building1,online
'''

infilepath = str(input('Enter file path: ').strip() or 'switches.csv')
outfiledir = "c:/temp/cisco"
if os.path.exists(infilepath):
    devices = csv.DictReader(open(infilepath,"r"))
else:
    raise FileNotFoundError('The file does not exist')
    exit

username = str(input("Enter username: ") or "admin")
password = getpass("Enter password: ")

for device in devices:
    ipaddr = device["ip"].strip()
    switchname = device["name"]
    if device["status"] == "online" and device["location"] == "idf":
        ipaddr = device["ip"].strip()
        device = {
            "device_type": "cisco_ios",
            "host": ipaddr,
            "username": username,
            "password": password
        }
        print(f"Backing up config for {switchname}")
        try:
            net_connect = ConnectHandler(**device)
            output = net_connect.send_command('show run')
            time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            outfilepath = f"{outfiledir}/{switchname}/{switchname}_{time_now}.txt"
            if not os.path.exists(f"{outfiledir}/{switchname}"):
                os.mkdir(f"{outfiledir}/{switchname}")
            with open(outfilepath, "w") as f:
                f.write(output)
            net_connect.disconnect()
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            print(error)
    else:
        print(f"Switch {switchname} is offline")
