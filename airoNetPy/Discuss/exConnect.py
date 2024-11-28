import netmiko
from netmiko import ConnectHandler



device_info = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.m.10.3',
    'port': 23,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

accessCLI = ConnectHandler(**device_info)
show_ip = accessCLI.send_command('sh ip int br')
print(show_ip)