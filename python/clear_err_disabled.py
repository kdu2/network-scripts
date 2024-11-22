from netmiko import ConnectHandler
from textfsm import TextFSM
import getpass

UN = input("Enter username: ")
PW = getpass.getpass(prompt="Password: ")

with open ('Devices.txt') as routers:
    for IP in routers:
        Router = {
            'device_type': 'cisco_ios',
            'ip' : IP,
            'username': UN,
            'password': PW
        }

    with ConnectHandler(**Router) as netconnect:
        print('-'*79)
        output = netconnect.send_command('show int status',use_textfsm=True)
        for i in output:
             if i["status"] == "err-disabled":
                config_set = ['interface ' + i["port"], 'shutdown', 'do clear port-sec all', 'no shut']
                x = netconnect.send_config_set(config_set)
        print(output)
        print()
        print('-'*79)

