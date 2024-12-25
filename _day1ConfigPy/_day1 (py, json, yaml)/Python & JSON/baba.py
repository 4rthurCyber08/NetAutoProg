import netmiko
from netmiko import ConnectHandler
import json
import pprint

# prompt user for info
user_m = input('What is your monitor number? ')
cam6_mac = input('''
What is the MAC address of the device on fa0/6?
Enter in period separated format ( xxxx.xxxx.xxxx )
''')
cam8_mac = input('''
What is the MAC address of the device on fa0/8?
Enter in period separated format ( xxxx.xxxx.xxxx )
''')

# 3 Steps (WRITE, CONNECT, PUSH)

# WRITE - device info and commands
# read the json file
with open('baba-configs.json') as file:
    # convert json data to usable python data
    json_configs = json.load(file)

# update the key[ip] for connection
json_configs['device_info']['ip'] = f'10.{user_m}.1.4'

# parse data
# ConnectHandler arguments to establish SSH connection to device
device_info = json_configs['device_info']

# configurations for commands
ips = json_configs['ips']
svi = ips['svi']
cam = ips['cam_ip']
dhcp = json_configs['dhcp']
pool = dhcp['pool']
v_names = json_configs['switchport']['vlan_names']
access_port = json_configs['switchport']['access']
voice_port = json_configs['switchport']['voice']
ospf = json_configs['ospf']


# Commands are separated per variable for more user readability
ip_commands = [
    # console access
    'line cons 0',
    f'password {ips["password"]}',
    'login',
    f'exec-timeout {ips["no_timeout"]}',
    'exit',
    
    # interface IPs
    'int vlan 10',
    'no shut',
    f'ip add 10.{user_m}.{svi["v10"]} {ips["mask_24"]}',
    f'desc mgmtWifi{ips["via_py"]}',
    'exit',
    'int vlan 50',
    'no shut',
    f'ip add 10.{user_m}.{svi["v50"]} {ips["mask_24"]}',
    f'desc mgmtCCTV{ips["via_py"]}',
    'exit',
]

dhcp_commands = [
    # exclude ips
    f'ip dhcp excluded-add 10.{user_m}.1.{dhcp["save_first"]} 10.{user_m}.1.{dhcp["save_last"]}',
    f'ip dhcp excluded-add 10.{user_m}.10.{dhcp["save_first"]} 10.{user_m}.10.{dhcp["save_last"]}',
    f'ip dhcp excluded-add 10.{user_m}.50.{dhcp["save_first"]} 10.{user_m}.50.{dhcp["save_last"]}',
    f'ip dhcp excluded-add 10.{user_m}.100.{dhcp["save_first"]} 10.{user_m}.100.{dhcp["save_last"]}',
    
    # dhcp pool
    f'ip dhcp pool {pool[0]['pool_name']}',
    f'network 10.{user_m}.1.0 {ips["mask_24"]}',
    f'default-router 10.{user_m}.{svi["v1"]}',
    f'domain-name {pool[0]['domain']}',
    f'dns-server 10.{user_m}.{dhcp["dns"]}',
    'exit',

    f'ip dhcp pool {pool[1]['pool_name']}',
    f'network 10.{user_m}.10.0 {ips["mask_24"]}',
    f'default-router 10.{user_m}.{svi["v10"]}',
    f'domain-name {pool[1]['domain']}',
    f'dns-server 10.{user_m}.{dhcp["dns"]}',
    'exit',

    f'ip dhcp pool {pool[2]['pool_name']}',
    f'network 10.{user_m}.50.0 {ips["mask_24"]}',
    f'default-router 10.{user_m}.{svi["v50"]}',
    f'domain-name {pool[2]['domain']}',
    f'dns-server 10.{user_m}.{dhcp["dns"]}',
    'exit',

    f'ip dhcp pool {pool[3]['pool_name']}',
    f'network 10.{user_m}.100.0 {ips["mask_24"]}',
    f'default-router 10.{user_m}.{svi["v100"]}',
    f'domain-name {pool[3]['domain']}',
    f'dns-server 10.{user_m}.{dhcp["dns"]}',
    f'option 150 ip 10.{user_m}.{dhcp["150_ip"]}',
    'exit'
]

switchport_commands = [
    # create vlans
    'vlan 1',
    f'name {v_names[0]}',
    'exit',
    'vlan 10',
    f'name {v_names[1]}',
    'exit',
    'vlan 50',
    f'name {v_names[2]}',
    'exit',
    
    # access/voice port
    'int fa 0/2',
    'switchport mode access',
    f'switchport {access_port["fa0/2"]}',
    'exit',
    'int fa 0/4',
    'switchport mode access',
    f'switchport {access_port["fa0/4"]}',
    'exit',
    'int fa 0/6',
    'switchport mode access',
    f'switchport {access_port["fa0/6"]}',
    'exit',
    'int fa 0/8',
    'switchport mode access',
    f'switchport {access_port["fa0/8"]}',
    'exit',
    'int fa 0/5',
    'switchport mode access',
    f'switchport {voice_port["fa0/5"]}',
    f'switchport {access_port["fa0/5"]}',
    'mls qos trust device cisco-phone',
    'exit',
    'int fa 0/7',
    'switchport mode access',
    f'switchport {voice_port["fa0/7"]}',
    f'switchport {access_port["fa0/7"]}',
    'mls qos trust device cisco-phone',
    'exit'
]

reserve_commands = [
    # reserve ips
    f'ip dhcp pool {pool[4]['pool_name']}',
    f'host 10.{user_m}.{cam[0]} {ips["mask_24"]}',
    f'client-identifier {cam6_mac}',
    'exit',
    f'ip dhcp pool {pool[5]['pool_name']}',
    f'host 10.{user_m}.{cam[1]} {ips["mask_24"]}',
    f'client-identifier {cam8_mac}',
    'exit'
]

ospf_commands = [
    # dynamic routing
    f'router ospf {ospf["process"]}',
    f'router-id 10.{user_m}.{user_m}.4',
    f'network 10.{user_m}.0.0 {ips["wild_16"]} {ospf["area"]}',
    'exit',
    'int gi 0/1',
    'ip ospf network point-to-point',
    'exit'
]


# CONNECT - to the device
# Establish connection and access cli
accessCLI = ConnectHandler(**device_info)

# PUSH - commands to the device
order_of_config = ['IP addresses', 'DHCP', 'Switchport', 'Reserved IPs', 'OSPF Routing']

for config in order_of_config:
    # inform user what is currently being configured
    print('~'*15 + f'\nConfiguring {config}...')
    
    if config == 'IP addresses':
        accessCLI.send_config_set(ip_commands)
    elif config == 'DHCP':
        accessCLI.send_config_set(dhcp_commands)
    elif config == 'Switchport':
        accessCLI.send_config_set(switchport_commands)
    elif config == 'Reserved IPs':
        accessCLI.send_config_set(reserve_commands)
    else:
        accessCLI.send_config_set(ospf_commands)
        
    print('Configuration Successful!!!\n')


#pprint.pp(reserve_commands, indent=4)