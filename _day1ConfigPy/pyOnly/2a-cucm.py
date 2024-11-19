import netmiko
from netmiko import ConnectHandler

#prompt users for info
monitorNumber = input(r'What is your monitor number? ')
ephone1MAC = input(r'What is the MAC Address of ephone1 on port fa 0/5? Answer in xxxx.xxxx.xxxx format. ')
ephone2MAC = input(r'What is the MAC Address of ephone2 on port fa 0/7? Answer in xxxx.xxxx.xxxx format. ')

deviceInfo = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.100.8',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

#set console access
configConsole = [
    'line cons 0',
    'password pass',
    'login',
    'exec-timeout 0 0',
    'exit'
]

#configure analog phones
configAnalog = [
    'dial-peer voice 1 pots',
    f'destination-pattern {monitorNumber}00',
    'port 0/0/0',
    'dial-peer voice 2 pots',
    f'destination-pattern {monitorNumber}01',
    'port 0/0/1',
    'dial-peer voice 3 pots',
    f'destination-pattern {monitorNumber}02',
    'port 0/0/2',
    'dial-peer voice 4 pots',
    f'destination-pattern {monitorNumber}03',
    'port 0/0/3',
    'exit'
]

#configure Telephony
configEphone = [
    'no telephony-service',
    'telephony-service',
    'no auto assign',
    'no auto-reg-ephone',
    'max-ephones 5',
    'max-dn 20',
    f'ip source-address 10.{monitorNumber}.100.8 port 2000',
    'create cnf-files',
    'ephone-dn 1',
    f'number {monitorNumber}11',
    'ephone-dn 2',
    f'number {monitorNumber}22',
    'ephone-dn 3',
    f'number {monitorNumber}33',
    'ephone-dn 4',
    f'number {monitorNumber}44',
    'ephone-dn 5',
    f'number {monitorNumber}55',
    'ephone-dn 6',
    f'number {monitorNumber}66',
    'ephone-dn 7',
    f'number {monitorNumber}77',
    'ephone-dn 8',
    f'number {monitorNumber}88',
    'ephone 1',
    f'mac-address {ephone1MAC}',
    'type 8945',
    'button 1:1 2:2 3:3 4:4',
    'restart',
    'ephone 2',
    f'mac-address {ephone2MAC}',
    'type 8945',
    'button 1:5 2:6 3:7 4:8',
    'restart',
    'end'
]

#activate video calls
configVideo = [
    'ephone 1',
    'video',
    'voice service voip',
    'h323',
    'call start slow',
    'ephone 2',
    'video',
    'voice service voip',
    'h323',
    'call start slow',
    'exit'
]

#allow incoming calls
configIncoming = [
    'voice service voip',
    'ip address trusted list',
    'ipv4 0.0.0.0 0.0.0.0',
    'exit'
]

#allow outgoing calls
configOutgoing = [
    'dial-peer voice 11 Voip',
    'destination-pattern 11..',
    'session target ipv4:10.11.100.8',
    'codec g711ULAW',
    'dial-peer voice 12 Voip',
    'destination-pattern 12..',
    'session target ipv4:10.12.100.8',
    'codec g711ULAW',
    'dial-peer voice 21 Voip',
    'destination-pattern 21..',
    'session target ipv4:10.21.100.8',
    'codec g711ULAW',
    'dial-peer voice 22 Voip',
    'destination-pattern 22..',
    'session target ipv4:10.22.100.8',
    'codec g711ULAW',
    'dial-peer voice 31 Voip',
    'destination-pattern 31..',
    'session target ipv4:10.31.100.8',
    'codec g711ULAW',
    'dial-peer voice 32 Voip',
    'destination-pattern 32..',
    'session target ipv4:10.32.100.8',
    'codec g711ULAW',
    'dial-peer voice 41 Voip',
    'destination-pattern 41..',
    'session target ipv4:10.41.100.8',
    'codec g711ULAW',
    'dial-peer voice 42 Voip',
    'destination-pattern 42..',
    'session target ipv4:10.42.100.8',
    'codec g711ULAW',
    'dial-peer voice 51 Voip',
    'destination-pattern 51..',
    'session target ipv4:10.51.100.8',
    'codec g711ULAW',
    'dial-peer voice 52 Voip',
    'destination-pattern 52..',
    'session target ipv4:10.52.100.8',
    'codec g711ULAW',
    'dial-peer voice 61 Voip',
    'destination-pattern 61..',
    'session target ipv4:10.61.100.8',
    'codec g711ULAW',
    'dial-peer voice 62 Voip',
    'destination-pattern 62..',
    'session target ipv4:10.62.100.8',
    'codec g711ULAW',
    'dial-peer voice 71 Voip',
    'destination-pattern 71..',
    'session target ipv4:10.71.100.8',
    'codec g711ULAW',
    'dial-peer voice 72 Voip',
    'destination-pattern 72..',
    'session target ipv4:10.72.100.8',
    'codec g711ULAW',
    'exit'
]

#Use only if routing will use OSPF
configOSPF = [
    'router ospf 1',
    f'router-id 10.{monitorNumber}.100.8',
    f'network 10.{monitorNumber}.100.0 0.0.0.255 area 0',
    'exit'
]

#connect to the specified device   
accessCLI = ConnectHandler(**deviceInfo)

#sh_ip_int_br = accessCLI.send_command('sh ip int br')
#print(sh_ip_int_br)

#apply configurations
print(r'Configuring Console Connection...')
accessCLI.send_config_set(configConsole)
print(r'...Success!' + '\n')

print(r'Configuring Analog Phones...')
accessCLI.send_config_set(configAnalog)
print(r'...Success!' + '\n')

#apply ephone numbers twice 
#IF numbers don't appear just run the script twice.
for i in range(1,3):
    print(r'Configuring Ephones ' + str(i) + r'/2')
    accessCLI.send_config_set(configEphone)
print(r'...Success!' + '\n')

print(r'Configuring Video Calls...')
accessCLI.send_config_set(configVideo)
print(r'...Success!' + '\n')

print(r'Allowing Incoming Calls...')
accessCLI.send_config_set(configIncoming)
print(r'...Success!' + '\n')

print(r'Allowing Outgoing Calls...')
accessCLI.send_config_set(configOutgoing)
print(r'...Success!' + '\n')

print(r'Configurations Successful!!!')

showRun = accessCLI.send_command('sh run')

#disconnect from device
accessCLI.disconnect

input(r'Press Enter to close terminal. [A "_2-callManager-shrun.txt" will be created containing show run output for the device]')

#create a text file for show run command
with open(r'_2-callManager-shrun.txt', 'w') as file:
    file.write(showRun)
    
