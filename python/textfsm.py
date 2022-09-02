from netmiko import ConnectHandler
from textfsm import TextFSM

UN = input("Enter username: ")
PW = getpass.getpass(prompt="Password: ")

with open ('Devices.txt') as Devices
    for IP in Devices:
        Device = {
            'device_type': 'cisco_ios',
            'ip' : IP
            'username': UN
            'password': PW
         }
         
         with ConnectHandler(**Device) as ssh_session:
             print ('Connecting to ' = IP)
             print('-'*79)
             output = net_connect.send_command('show int status',use_textfsm=True)
             print(output)
             print()
             print('-'*79)
