import netmiko
from netmiko import ConnectHandler
import json

deviceInfo = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.61.10.3',
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

deviceConfig = [
    'hostname art-61',
    'dot11 ssid hiFromArt-61',
    'authentication open',
    'authentication key-management wpa',
    'wpa-psk ascii C1sc0123',
    'guest-mode',
    'Default Int Dot11Radio 0',
    'Int Dot11Radio 0',
    'channel 9',
    'no shut',
    'encryption mode ciphers tkip',
    'ssid hiFromArt-61',
    'exit',
]

#with open('---wireless1.json') as file:
#    data = json.load(file)



accessAutoAP = ConnectHandler(**deviceInfo)
accessAutoAP.enable()
accessAutoAP.send_config_set(deviceConfig)

accessAutoAP.disconnect
