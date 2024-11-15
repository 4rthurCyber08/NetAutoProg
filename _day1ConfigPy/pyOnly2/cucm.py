import netmiko
from netmiko import ConnectHandler

monitorNumber = input(r'What is your monitor number?')
ephone1MAC = input(r'What is the MAC Address of ephone1 on port fa 0/5? Answer in xxxx.xxxx.xxxx format.')
ephone2MAC = input(r'What is the MAC Address of ephone2 on port fa 0/7? Answer in xxxx.xxxx.xxxx format.')

deviceInfo = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.100.8',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

config = [
    
]