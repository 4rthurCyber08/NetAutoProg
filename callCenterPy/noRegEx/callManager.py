import netmiko
import json
from netmiko import ConnectHandler

#prompt user for unique device info
mNum = input(r'What is your monitor number? ')
cucm_IP = input('What is your Call Manager\'s VLAN 1 IP ADDRESS? ')
ephone_1 = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
ephone_2 = input(r'What is the MAC ADDRESS of your ephone 2? (Use the format: xxxx.xxxx.xxxx): ')

#read cucm_info_temp.json
with open('cucm_info_temp.json', 'r') as device:
    device_info = json.load(device)

#create/overwrite my_cucm.json
with open('my_cucm.json', 'w') as device:
    for i in device_info:
        device_info[i]['host'] = cucm_IP

cucm_config = [
    #Switchport VLANS
    'vlan 10',
    'name wirelessVLAN',
    'vlan 100',
    'name callCenterVLAN',
    'Int Fa 0/1/2',
    'switchport mode access',
    'switchport access vlan 10',
    'Int Fa 0/1/4',
    'switchport mode access',
    'switchport access vlan 100',
    'Int Fa 0/1/5',
    'switchport mode access',
    'switchport access vlan 100',
    'Int Fa 0/1/0',
    'switchport mode access',
    'switchport access vlan 1',
    
    #DHCP
    f'ip dhcp excluded-add 10.{mNum}.100.1 10.{mNum}.100.150',
    
    f'ip dhcp pool CallCenterPOOL-{mNum}',
    f'network 10.{mNum}.100.0 255.255.255.0',
    f'default-router 10.{mNum}.100.4',
    f'domain-name CallCenter{mNum}.com',
    'dns-server 8.8.8.8',
    f'option 150 ip 10.{mNum}.100.4',
    
    f'ip dhcp pool WirelessPOOL-{mNum}',
    f'network 10.{mNum}.10.0 255.255.255.0',
    f'default-router 10.{mNum}.10.1',
    f'domain-name Wireless{mNum}.com',
    f'dns-server 10.{mNum}.1.10',
    
    #Analog Phones
    f'dial-peer voice 1 pots',
    f'destination-pattern {mNum}00',
    'port 0/0/0',
    'dial-peer voice 2 pots',
    f'destination-pattern {mNum}01',
    'port 0/0/1'
]

tele_config = [
    
    'no telephony-service',
    'telephony-service',
    'no auto assign',
    'no auto-reg-ephone',
    'max-ephones 12',
    'max-dn 48',
    f'ip source-address 10.{mNum}.100.4 port 2000',
    'create cnf-files',
    'ephone-dn 1',
    f'number {mNum}11',
    'ephone-dn 2',
    f'number {mNum}22',
    'ephone-dn 3',
    f'number {mNum}33',
    'ephone-dn 4',
    f'number {mNum}44',
    'ephone-dn 5',
    f'number {mNum}55',
    'ephone-dn 6',
    f'number {mNum}66',
    'ephone-dn 7',
    f'number {mNum}77',
    'ephone-dn 8',
    f'number {mNum}88',
    'ephone-dn 9',
    f'number {mNum}68',
    'ephone-dn 10',
    f'number {mNum}23',
    'Ephone 1',
    f'Mac-address {ephone_1}',
    'type 8945',
    'button 1:1 2:3 3:2 4:4',
    'restart',
    'exit',
    'Ephone 2',
    f'Mac-address {ephone_2}',
    'type 8945',
    'button 1:8 2:7 3:3 4:5',
    'restart',
    'exit'
]

config_more = [
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
    
    'int fa 0/0',
    'no shut',
    f'ip add 200.0.0.{mNum} 255.255.255.0',
    'router eigrp 100',
    'network 10.0.0.0',
    'network 200.0.0.0',
    'exit',
    
    'voice service voip',
    'ip address trusted list',
    'ipv4 0.0.0.0 0.0.0.0',

    'dial-peer voice 12 Voip',
    'destination-pattern 12..',
    'session target ipv4:10.12.100.4',
    'codec g711ULAW',
    'dial-peer voice 21 Voip',
    'destination-pattern 21..',
    'session target ipv4:10.21.100.4',
    'codec g711ULAW',
    'dial-peer voice 22 Voip',
    'destination-pattern 22..',
    'session target ipv4:10.22.100.4',
    'codec g711ULAW',
    'dial-peer voice 31 Voip',
    'destination-pattern 31..',
    'session target ipv4:10.31.100.4',
    'codec g711ULAW',
    'dial-peer voice 32 Voip',
    'destination-pattern 32..',
    'session target ipv4:10.32.100.4',
    'codec g711ULAW'
]

ivrs = [
    r'dial-peer voice 69 voip',
    r'service rivanaa out-bound',
    f'destination-pattern {mNum}69',
    f'session target ipv4:10.{mNum}.100.4',
    f'incoming called-number {mNum}69',
    r'dtmf-relay h245-alphanumeric',
    'codec g711ulaw',
    'no vad',

    'telephony-service',
    r'moh "flash:/en_bacd_music_on_hold.au"',

    'application',
    r'service rivanaa flash:app-b-acd-aa-3.0.0.2.tcl',
    'paramspace english index 1',
    'param number-of-hunt-grps 2',
    'param dial-by-extension-option 8',
    'param handoff-string rivanaa',
    'param welcome-prompt flash:en_bacd_welcome.au',
    'paramspace english language en',
    'param call-retry-timer 15',
    'param service-name rivanqueue',
    'paramspace english location flash:',
    'param second-greeting-time 60',
    'param max-time-vm-retry 2',
    'param voice-mail 1234',
    'param max-time-call-retry 700',
    f'param aa-pilot {mNum}69',
    r'service rivanqueue flash:app-b-acd-3.0.0.2.tcl',
    'param queue-len 15',
    f'param aa-hunt1 {mNum}00',
    f'param aa-hunt2 {mNum}01',
    f'param aa-hunt3 {mNum}33',
    f'param aa-hunt4 {mNum}77',
    'param queue-manager-debugs 1',
    'param number-of-hunt-grps 4 '
]

#iptest = accessCli.send_command("sh ip int br")
accessCli = ConnectHandler(**device_info['CUCM'])
#accessCli.enable()
output1 = accessCli.send_config_set(cucm_config)
print("Configuring Analog Phones")
for i in range(5):
    prog = str(i + 1)
    output2 = accessCli.send_config_set(tele_config)
    print('Configuring telephony ' + prog + '/5')

#INCOMING AND OUTGOING   
output3 = accessCli.send_config_set(config_more)
print("Configuring Incoming and outgoing calls")

#IVRS
output4 = accessCli.send_config_set(ivrs)
print("Configuring IVRS")

output2 = accessCli.send_config_set(tele_config)

print(output1)
print(output2)
print(output3)
print(output4)

accessCli.disconnect


