import netmiko
from netmiko import ConnectHandler

monitorNumber = input(r'What is your monitor number? ')

deviceInfoBABA = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.1.4',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

deviceInfoCUCM = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.100.8',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

deviceInfoEDGE = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.' + monitorNumber + '.1',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

#connect to the specified device
accessCLI = ConnectHandler(**deviceInfoEDGE)

#send_command only allows show commands
sh_ip_int_br = accessCLI.send_command('sh ip int br')
print(sh_ip_int_br)

#disconnect from device
accessCLI.disconnect