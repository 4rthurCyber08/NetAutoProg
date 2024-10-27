import netmiko
import json
import pprint
import re
from netmiko import ConnectHandler

#prompt user for unique device info
mNum = input(r'What is your monitor number? ')
cucm_IP = input('What is your Call Manager\'s VLAN 1 IP ADDRESS? ')

#prompt and verify for a valid mac address
regex_mac = r"^[a-fA-F0-9]{4}\.[a-fA-F0-9]{4}\.[a-fA-F0-9]{4}$"

ephone_1_mac = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
mac_is_valid = bool(re.search(regex_mac, ephone_1_mac))

while mac_is_valid == False:
    print(r'INVALID MAC ADDRESS')
    print(r'Use the format: xxxx.xxxx.xxxx')
    ephone_1_mac = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
    mac_is_valid = bool(re.search(regex_mac, ephone_1_mac))
    
ephone_2_mac = input(r'What is the MAC ADDRESS of your ephone 2? (Use the format: xxxx.xxxx.xxxx): ')
mac_is_valid2 = bool(re.search(regex_mac, ephone_2_mac))

while mac_is_valid2 == False:
    print(r'INVALID MAC ADDRESS')
    print(r'Use the format: xxxx.xxxx.xxxx')
    ephone_1_mac = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
    mac_is_valid2 = bool(re.search(regex_mac, ephone_2_mac))

#read the device info of the call manager
with open('cucm_data_temp.json', 'r') as device:
    device_config = json.load(device)

    for mainkey in device_config:
        if mainkey != 'monitor_number':
            for subkey in device_config[mainkey]:
                #print(subkey)

                device_value = device_config[mainkey][subkey]
                #print(device_value)
                
                #match info based on the user's monitor number
                regex = r'{mNum}'
                matched = bool(re.search(regex, device_value))
                update_value = re.sub(regex, mNum, device_value)
                
                #update matched values based on user's monitor number
                if matched:
                    device_config[mainkey][subkey] = update_value
                    
#create/overwrite the call manager's info based on user's ip address ('my_cucm_data.json' will contain all YOUR call manager's data)
with open('my_cucm_data.json', 'w') as device:
    device_config['monitor_number'] = str(mNum)
    device_config['call_manager']['host'] = cucm_IP
    device_config['ephone_config']['mac_1'] = ephone_1_mac
    device_config['ephone_config']['mac_2'] = ephone_2_mac
    
    my_device_config = json.dumps(device_config, indent = 3)
    device.write(my_device_config)

data = device_config['device_data']
dhcp = device_config['dhcp_config']
analog = device_config['analog_config']
ephone = device_config['ephone_config']
eigrp = device_config['eigrp']
incall = device_config['in_calls']
outcall = device_config['out_calls']
ivrs = device_config['ivrs_config']

vlans_config = [
    #IP address
    f'hostname {data["hostname"]}',
    'interface vlan 10',
    'no shutdown',
    f'ip address {data["vl10"]}',
    f'description {data["description"]}',
    'exit',
    'interface vlan 100',
    'no shutdown',
    f'ip address {data["vl100"]}',
    f'description {data["description"]}',
    'exit',
  
    #Switchport VLANS
    'vlan 10',
    f'name {data["vl100_name"]}',
    'vlan 100',
    f'name {data["vl100_name"]}',
    'Interface fa 0/1/0',
    'switchport mode access',
    f'switchport {data["fa_010_access"]}',
    'interface fa 0/1/2',
    'switchport mode access',
    f'switchport {data["fa_012_access"]}',
    'interface fa 0/1/4',
    'switchport mode access',
    f'switchport {data["fa_014_n_015_access"]}',
    'Interface fa 0/1/5',
    'switchport mode access',
    f'switchport {data["fa_014_n_015_access"]}',
    'exit'
]

dhcp_config = [
    f'ip dhcp excluded-add {dhcp["exclude_ip"]}',
    
    f'ip dhcp pool {dhcp["pool_voice"]}',
    f'network {dhcp["network_voice"]}',
    f'default-router {dhcp["gateway_voice"]}',
    f'domain-name {dhcp["domain_voice"]}',
    'dns-server 8.8.8.8',
    f'option 150 ip {dhcp["option_150"]}',
    
    f'ip dhcp pool {dhcp["pool_voice"]}',
    f'network {dhcp["network_voice"]}',
    f'default-router {dhcp["gateway_voice"]}',
    f'domain-name {dhcp["domain_voice"]}',
    f'dns-server {dhcp["option_150"]}',
    'exit'
]

analog_config = [ 
    'dial-peer voice 1 pots',
    f'destination-pattern {analog["pots_1"]}',
    f'port {analog["pots_1_port"]}',
    'dial-peer voice 2 pots',
    f'destination-pattern {analog["pots_2"]}',
    f'port {analog["pots_1_port"]}',
    'exit'
]

tele_config = [
    'no telephony-service',
    'telephony-service',
    'no auto assign',
    'no auto-reg-ephone',
    'max-ephones 12',
    'max-dn 48',
    f'ip source-address {ephone["source_address"]}',
    'create cnf-files',
    'ephone-dn 1',
    f'number {ephone["dn_1"]}',
    'ephone-dn 2',
    f'number {ephone["dn_2"]}',
    'ephone-dn 3',
    f'number {ephone["dn_3"]}',
    'ephone-dn 4',
    f'number {ephone["dn_4"]}',
    'ephone-dn 5',
    f'number {ephone["dn_5"]}',
    'ephone-dn 6',
    f'number {ephone["dn_6"]}',
    'ephone-dn 7',
    f'number {ephone["dn_7"]}',
    'ephone-dn 8',
    f'number {ephone["dn_8"]}',
    'ephone-dn 9',
    f'number {ephone["dn_9"]}',
    'ephone-dn 10',
    f'number {ephone["dn_10"]}',
    'Ephone 1',
    f'Mac-address {ephone["mac_1"]}',
    f'type {ephone["model"]}',
    f'button {ephone["btn_1"]}',
    'restart',
    'exit',
    'Ephone 2',
    f'Mac-address {ephone["mac_2"]}',
    f'type {ephone["model"]}',
    f'button {ephone["btn_2"]}',
    'restart',
    'exit'
]

video_call_config = [
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

routing_config = [
    'int fa 0/0',
    'no shut',
    f'ip add {eigrp["fa_00_ip"]}',
    f'router {eigrp["as_number"]}',
    f'network {eigrp["net_10"]}',
    f'network {eigrp["net_200"]}',
    'exit',
]

incoming_calls_config = [
    'voice service voip',
    'ip address trusted list',
    f'ipv4 {incall["ipv4"]}'
]

#outgoing calls
callers = f'{outcall["monitors_occupied"]}'
list_of_callers = callers.split(",")
outgoing_calls_config = []
for i in list_of_callers:
    out_per_user = [
        f'dial-peer voice {i} Voip',
        f'destination-pattern {i}..',
        f'session target ipv4:10.{i}.100.4',
        f'codec g711ULAW',
        'exit'
    ]
    outgoing_calls_config.append(out_per_user)

ivrs_config = [
    r'dial-peer voice 69 voip',
    r'service rivanaa out-bound',
    f'destination-pattern {ivrs["dial_number"]}',
    f'session target ipv4:{ivrs["session_ipv4"]}',
    f'incoming called-number {ivrs["dial_number"]}',
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
    f'param aa-pilot {ivrs["dial_number"]}',
    r'service rivanqueue flash:app-b-acd-3.0.0.2.tcl',
    'param queue-len 15',
    f'param aa-hunt1 {ivrs["hunt_1"]}',
    f'param aa-hunt2 {ivrs["hunt_2"]}',
    f'param aa-hunt3 {ivrs["hunt_3"]}',
    f'param aa-hunt4 {ivrs["hunt_4"]}',
    'param queue-manager-debugs 1',
    'param number-of-hunt-grps 4 '
]

restart_ephones = [
    'ephone 1',
    'restart',
    'exit',
    'ephone 2',
    'restart',
    'exit'
]

print(r"(my_cucm_data.json) Your Call Manager's info:")
pprint.pp(device_config)

#connect and apply configurations to device
access_cli = ConnectHandler(**device_config["call_manager"])

#for telnet only
#accessCli.enable()

access_cli.send_config_set(vlans_config)
print("Configuring IPs and VLANs..")

access_cli.send_config_set(dhcp_config)
print("Configuring DHCP Server..")

access_cli.send_config_set(analog_config)
print("Configuring Analog Phones..")

for i in range(1, 4):
    progress = 'Configuring Ephones ' + str(i) + ' /3'
    access_cli.send_config_set(tele_config)
    print(progress)

access_cli.send_config_set(routing_config)
print("Configuring EIGRP..")

access_cli.send_config_set(video_call_config)
print("Enabling Video Calls..")

access_cli.send_config_set(incoming_calls_config)
print("Allowing Incoming Calls..")

for i in outgoing_calls_config:
    access_cli.send_config_set(i)
    print('Allowing Outgoing Calls..')

access_cli.send_config_set(ivrs_config)
print("Applying Voice Response for " + mNum + "69..")

access_cli.send_config_set(restart_ephones)
print("Restarting ephones..")


#iptest = accessCli.send_command("sh ip int br")
#print(iptest)

access_cli.disconnect


