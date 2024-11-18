import json
import netmiko
from netmiko import ConnectHandler

#read json file containing aironet settings
with open('autoAP.json', 'r') as file:
    deviceData = json.load(file)

#parse info from json file
aironet = deviceData['aironetInfo']
apConfig = deviceData['aironetConfig']

deviceConfig = [
    f'hostname {apConfig["hostname"]}',
    f'dot11 ssid {apConfig["ssid"]}',
    f'authentication {apConfig["authentication"]}',
    f'authentication key-management {apConfig["key-man"]}',
    f'wpa-psk ascii {apConfig["wifi-pass"]}',
    'guest-mode',
    'Default Int Dot11Radio 0',
    'Int Dot11Radio 0',
    f'channel {apConfig["channel"]}',
    'no shut',
    f'encryption mode ciphers {apConfig["encr-mod"]}',
    f'ssid {apConfig["ssid"]}',
    'exit',
]

#connect to the device
accessAutoAP = ConnectHandler(**aironet)

#use enable command to enter privilege exec mode
accessAutoAP.enable()

#push configurations through global configuration mode
accessAutoAP.send_config_set(deviceConfig)

#close connection
accessAutoAP.disconnect
