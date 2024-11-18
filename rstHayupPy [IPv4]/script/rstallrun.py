import netmiko
from netmiko import ConnectHandler
import json
import re
import pprint

#open json file containing all the authentication info for each device
#(with open defaults to read only "r")
with open('device_info_temp.json', 'r') as file:
    json_devices = json.load(file)

#write/create ("w") file "your_device_info.json" in the json folder
with open('your_device_info.json', 'w') as file:
    #variables for obtaining user's RSTallrun IP address
    user_rstallrun = ''
    ip_regex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    is_ip_valid = bool(re.search(ip_regex, user_rstallrun))

    #keep prompting the user for a valid ip address
    while is_ip_valid == False:
        if user_rstallrun == '':
            user_rstallrun = input('What is the ip address of your Clone of RSTallrun? ')
        
        else:
            user_rstallrun = input('INVALID IP ADDRESS: What is the ip address of your Clone of RSTallrun? ')
            
        is_ip_valid = bool(re.search(ip_regex, user_rstallrun))
        
    if is_ip_valid:
        #change the host address of every device in json_devices
        for i in json_devices:
            json_devices[i]["host"] = user_rstallrun
    
        #convert the python dictionary(json_devices) to a json string for writing prep
        new_device_info = json.dumps(json_devices, indent = 3)
    
        #write the json file with the user's rstallrun ip address
        file.write(new_device_info)
    
with open('pre_config.json') as file:
    json_configs = json.load(file)

#extract D1 and D2's device info
d1 = json_devices['d1_device']
d2 = json_devices['d2_device']
a1 = json_devices['a1_device']
a2 = json_devices['a2_device']
p1 = json_devices['p1_device']
p2 = json_devices['p2_device']
r4 = json_devices['r4_device']
r3 = json_devices['r3_device']
r2 = json_devices['r2_device']
r1 = json_devices['r1_device']
i4 = json_devices['i4_device']
i3 = json_devices['i3_device']
i2 = json_devices['i2_device']
i1 = json_devices['i1_device']

#extract device configs
dhcp = json_configs['dhcp_config']
ip = json_configs['i_protocol']
eigrp = json_configs['eigrp_config']
ospf = json_configs['ospf_config']
bgp = json_configs['bgp_config']
p2_config = json_configs['p2_config']
p1_config = json_configs['p1_config']
a2_config = json_configs['a2_config']
a1_config = json_configs['a1_config']
d2_config = json_configs['d2_config']
d1_config = json_configs['d1_config']
r4_config = json_configs['r4_config']
r3_config = json_configs['r3_config']
r2_config = json_configs['r2_config']
r1_config = json_configs['r1_config']
i1_config = json_configs['i1_config']
i2_config = json_configs['i2_config']
i3_config = json_configs['i3_config']
i4_config = json_configs['i4_config']

#commands to be pushed to cli
i1_commands = [
    f'Hostname {i1_config["hostname"]}',
    "interface loopback 0",
    f'ip address {i1_config["lo0"]} {ip["mask_32"]}',
    "exit",
    
    #bgp config
    f'router {bgp["as_45"]}',
    f'bgp router-id {i1_config["lo0"]}',
    "bgp log-negihbor-changes",
    f'{i1_config["neigh_45"]}',
    f'{i1_config["neigh_24"]}',
    f'{i1_config["neigh_208"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i1_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_45"]} mask {ip["mask_24"]}',
    f'network {bgp["net_24"]} mask {ip["mask_24"]}',
    f'network {bgp["net_208"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    "exit",
    
    #fake internet
    f'ip route {bgp["fake_net"]} 208.8.8.1',
    f'ip route {ip["def_route"]} null 0',
    "exit"
]

i2_commands = [
    f'hostname {i2_config["hostname"]}',
    "interface loopback 0",
    f'ip address {i2_config["lo0"]} {ip["mask_32"]}',
    "exit",
    
    #bgp config
    f'router {bgp["as_2"]}',
    f'bgp router-id {i2_config["lo0"]}',
    "bgp log-negihbor-changes",
    f'{i2_config["neigh_32"]}',
    f'{i2_config["neigh_25"]}',
    f'{i2_config["neigh_24"]}',
    f'{i2_config["neigh_207"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i2_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_32"]} mask {ip["mask_24"]}',
    f'network {bgp["net_25"]} mask {ip["mask_24"]}',
    f'network {bgp["net_24"]} mask {ip["mask_24"]}',
    f'network {bgp["net_207"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    "exit",
    
    #fake internet
    f'ip route {bgp["fake_net"]} 207.7.7.1',
    f'ip route {ip["def_route"]} null 0',
    "exit"
]

i3_commands = [
    f'hostname {i3_config["hostname"]}',
    "interface loopback 0",
    f'ip address {i3_config["lo0"]} {ip["mask_32"]}',
    "exit",
    
    #bgp config
    f'router {bgp["as_3"]}',
    f'bgp router-id {i3_config["lo0"]}',
    "bgp log-negihbor-changes",
    f'{i3_config["neigh_35"]}',
    f'{i3_config["neigh_32"]}',
    f'{i3_config["neigh_209"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i3_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_35"]} mask {ip["mask_24"]}',
    f'network {bgp["net_32"]} mask {ip["mask_24"]}',
    f'network {bgp["net_209"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    "exit",
    
    #fake internet
    f'ip route {bgp["fake_net"]} 207.9.9.1',
    f'ip route {ip["def_route"]} null 0',
    "exit"
]

i4_commands = [
    f'hostname {i4_config["hostname"]}',
    "interface loopback 0",
    f'ip address {i4_config["lo0"]} {ip["mask_32"]}',
    "exit",
    
    #bgp config
    f'router {bgp["as_45"]}',
    f'bgp router-id {i4_config["lo0"]}',
    "bgp log-negihbor-changes",
    f'{i4_config["neigh_35"]}',
    f'{i4_config["neigh_25"]}',
    f'{i4_config["neigh_45"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i4_config["google"]} mask {ip["mask_32"]}',
    f'network {i4_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_35"]} mask {ip["mask_24"]}',
    f'network {bgp["net_25"]} mask {ip["mask_24"]}',
    f'network {bgp["net_45"]} mask {ip["mask_24"]}',
    "exit",
    
    #fake google
    "interface loopback 5",
    f'ip address {i4_config["google"]} {ip["mask_32"]}',
    f'description Google',
    "exit",
    "exit"
]

r1_commands = [
    f'hostname {r1_config["hostname"]}',
    
    "interface loopback 5",
    f'ip address {r1_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    "exit",
    
    #ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r1_config["lo5"]}',
    f'network {ospf["net_1_0"]}',
    f'network {r1_config["lo5"]} 0.0.0.0 area 12',
    f'{ospf["redis_bgp"]}',
    "exit",
    
    #bgp config
    f'router {bgp["as_1"]}',
    f'bgp router-id {r1_config["lo5"]}',
    "bgp log-neighbor-changes",
    f'{r1_config["neigh_209"]}',
    f'{r1_config["neigh_207"]}',
    f'{r1_config["neigh_208"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {r1_config["lo5"]} mask {ip["mask_32"]}',
    f'network {bgp["net_209"]} mask {ip["mask_24"]}',
    f'network {bgp["net_207"]} mask {ip["mask_24"]}',
    f'network {bgp["net_208"]} mask {ip["mask_24"]}',
    f'network {bgp["net_10"]} mask {ip["mask_30"]}',
    "exit",
    "exit"
]

r2_commands = [
    f'hostname {r2_config["hostname"]}',
    
    "interface loopback 5",
    f'ip address {r2_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    #ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r2_config["lo5"]}',
    f'network {ospf["net_1_4"]}',
    f'network {ospf["net_1_0"]}',
    f'network {r2_config["lo5"]} 0.0.0.0 area 0',
    "exit",
    "exit"
]

r3_commands = [
    f'hostname {r3_config["hostname"]}',
    
    "interface loopback 5",
    f'ip address {r3_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    #ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r3_config["lo5"]}',
    f'network {ospf["net_1_8"]}',
    f'network {ospf["net_1_4"]}',
    f'network {r3_config["lo5"]} 0.0.0.0 area 0',
    "exit",
    "exit"
]
r4_commands = [
    f'hostname {r4_config["hostname"]}',
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {r4_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    #eigrp config
    f'router eigrp {eigrp["as100"]}',
    f'eigrp router-id {r4_config["lo5"]}',
    "no auto-summary",
    f'network {eigrp["net_4_4"]}',
    f'network {eigrp["net_4_8"]}',
    f'network {r4_config["lo5"]} 0.0.0.0',
    f'{eigrp["redis_ospf_1"]}',
    "exit",
    
    #ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r4_config["lo5"]}',
    f'network {ospf["net_1_8"]}',
    f'network {r4_config["lo5"]} 0.0.0.0 area 34',
    f'{ospf["redis_eigrp_100"]}',
    "exit",
    "exit"
]

d1_commands = [
    f'hostname {d1_config["hostname"]}',
    "interface ethernet 1/0",
    "switchport mode acccess",
    "switchport access vlan 200",
    "exit",
    
    #dhcp config
    f'ip dhcp excluded-address {d1_config["excip_01"]}',
    f'ip dhcp excluded-address {d1_config["excip_02"]}',
    f'ip dhcp pool {d1_config["dhcp_pool"]}',
    f'network {dhcp["net_v10"]} {ip["mask_24"]}',
    f'default-router {d1_config["gateway"]}',
    "exit",
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {d1_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    #eigrp config
    f'router {eigrp["named-eigrp"]}',
    f'address-family ipv4 unicast autonomous-system {eigrp["as100"]}',
    f'eigrp router-id {d1_config["lo5"]}',
    f'network {eigrp["net_4_4"]}',
    f'network {eigrp["net_1_0"]}',
    f'network {eigrp["net_2_0"]}',
    f'network {eigrp["net_v200"]}',
    f'network {d1_config["lo5"]} 0.0.0.0',
    "exit",
    "exit",
    "exit"
]

d2_commands = [
    f'hostname {d2_config["hostname"]}',
    "interface ethernet 1/0",
    "switchport mode access",
    "switchport access vlan 20",
    "exit",
    
    #dhcp config
    f'ip dhcp excluded-address {d2_config["excip_01"]}',
    f'ip dhcp excluded-address {d2_config["excip_02"]}',
    f'ip dhcp pool {d2_config["dhcp_pool"]}',
    f'network {dhcp["net_v10"]} {ip["mask_24"]}',
    f'default-router {d2_config["gateway"]}',
    "exit",
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {d2_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    #eigrp config
    f'router {eigrp["named-eigrp"]}',
    f'address-family ipv4 unicast autonomous-system {eigrp["as100"]}',
    f'eigrp router-id {d2_config["lo5"]}',
    f'network {eigrp["net_4_8"]}',
    f'network {eigrp["net_1_0"]}',
    f'network {eigrp["net_2_0"]}',
    f'network {eigrp["net_v200"]}',
    f'network {d2_config["lo5"]} 0.0.0.0',
    "exit",
    "exit",
    "exit"
]

a1_commands = [
    f'hostname {a1_config["hostname"]}',
    "interface ethernet 0/0",
    "switchport mode access",
    "switchport access vlan 10",
    "exit",
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {a1_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    f'ip route {ip["def_route"]} {ip["def_129"]} 1',
    f'ip route {ip["def_route"]} {ip["def_130"]} 2',
    "exit"
]

a2_commands = [
    f'hostname {a2_config["hostname"]}',
    "interface ethernet 1/0",
    "switchport mode access",
    "switchport access vlan 10",
    "exit",
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {a2_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    f'ip route {ip["def_route"]} {ip["def_130"]} 1',
    f'ip route {ip["def_route"]} {ip["def_129"]} 2',
    "exit"
]

p1_commands = [
    f'hostname {p1_config["hostname"]}',
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {p1_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    
    f'ip route {ip["def_route"]} {ip["def_1_1"]} 1',
    f'ip route {ip["def_route"]} {ip["def_1_2"]} 2',
    "interface ethernet 0/0",
    "ip add dhcp",
    "exit"
]

p2_commands = [
    f'hostname {p2_config["hostname"]}',
    
    #just an indication that it was configured through python
    "interface loopback 5",
    f'ip address {p2_config["lo5"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    f'ip route {ip["def_route"]} {ip["def_1_2"]} 1',
    f'ip route {ip["def_route"]} {ip["def_1_1"]} 2',
    "interface ethernet 1/0",
    "ip add dhcp",
    "exit"
]

#preview what commands would look like on cli
#pprint.pp(d1_commands)

#sequence of configuring the devices
#Configure ISPs First so that pinging 8.8.8.8 will be faster
seq_of_Config = ['ISP4', 'ISP3', 'ISP2', 'ISP1', 'R1', 'D1', 'D2', 'A1', 'A2', 'P1', 'P2', 'R3', 'R2', 'R4', 'END']

#for loop to configure each device
for device in seq_of_Config:    
    if device == 'D1':
        d1_cli = ConnectHandler(**d1)
        d1_cli.enable()
        d1_cli.send_config_set(d1_commands)
        
        show_run_d1 = d1_cli.send_command('sh run')
        d1_cli.disconnect
    elif device == 'D2':
        d2_cli = ConnectHandler(**d2)
        d2_cli.enable()
        d2_cli.send_config_set(d2_commands)
        
        show_run_d2 = d2_cli.send_command('sh run')
        d2_cli.disconnect
    elif device == 'A1':
        a1_cli = ConnectHandler(**a1)
        a1_cli.enable()
        a1_cli.send_config_set(a1_commands)
        
        show_run_a1 = a1_cli.send_command('sh run')
        a1_cli.disconnect
    elif device == 'A2':
        a2_cli = ConnectHandler(**a2)
        a2_cli.enable()
        a2_cli.send_config_set(a2_commands)
        
        show_run_a2 = a2_cli.send_command('sh run')
        a2_cli.disconnect
    elif device == 'P1':
        p1_cli = ConnectHandler(**p1)
        p1_cli.enable()
        p1_cli.send_config_set(p1_commands)
        
        show_run_p1 = p1_cli.send_command('sh run')
        p1_cli.disconnect
    elif device == 'P2':
        p2_cli = ConnectHandler(**p2)
        p2_cli.enable()
        p2_cli.send_config_set(p2_commands)
        
        show_run_p2 = p2_cli.send_command('sh run')
        p2_cli.disconnect
    elif device == 'R3':
        r3_cli = ConnectHandler(**r3)
        r3_cli.enable()
        r3_cli.send_config_set(r3_commands)
        
        show_run_r3 = r3_cli.send_command('sh run')
        r3_cli.disconnect
    elif device == 'R2':
        r2_cli = ConnectHandler(**r2)
        r2_cli.enable()
        r2_cli.send_config_set(r2_commands)
        
        show_run_r2 = r2_cli.send_command('sh run')
        r2_cli.disconnect
    elif device == 'R4':
        r4_cli = ConnectHandler(**r4)
        r4_cli.enable()
        r4_cli.send_config_set(r4_commands)
        
        show_run_r4 = r4_cli.send_command('sh run')
        r4_cli.disconnect
    elif device == 'ISP4': 
        i4_cli = ConnectHandler(**i4)
        i4_cli.enable()
        i4_cli.send_config_set(i4_commands)
        
        show_run_i4 = i4_cli.send_command('sh run')
        i4_cli.disconnect 
    elif device == 'ISP3': 
        i3_cli = ConnectHandler(**i3)
        i3_cli.enable()
        i3_cli.send_config_set(i3_commands)
        
        show_run_i3 = i3_cli.send_command('sh run')
        i3_cli.disconnect 
    elif device == 'ISP2': 
        i2_cli = ConnectHandler(**i2)
        i2_cli.enable()
        i2_cli.send_config_set(i2_commands)
        
        show_run_i2 = i2_cli.send_command('sh run')
        i2_cli.disconnect 
    elif device == 'ISP1': 
        i1_cli = ConnectHandler(**i1)
        i1_cli.enable()
        i1_cli.send_config_set(i1_commands)
        
        show_run_i1 = i1_cli.send_command('sh run')
        i1_cli.disconnect 
    elif device == 'R1': 
        r1_cli = ConnectHandler(**r1)
        r1_cli.enable()
        r1_cli.send_config_set(r1_commands)
        show_run_r1 = r1_cli.send_command('sh run')
        r1_cli.disconnect
    
    if device != 'END':
        print('Configuring ' + device)
    else:
        print('Configuration Complete for : Clone of RSTallrun [' + json_devices['p1_device']['host'] + ']')
        print(r'Please wait for BGP to build routes before pinging 8.8.8.8')
        input(r'Press Enter to close terminal. [A "show_run.txt" will be created containing show run output for all devices.]')

#create a file for show run output of all devices
with open('show_run.txt', 'w') as file:
    file.write(
        '===================================================================== \n\n'
        + '@P1 \n\n' +
        show_run_p1
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@P2 \n\n' +
        show_run_p2
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@A1 \n\n' +
        show_run_a1
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@A2 \n\n' +
        show_run_a2
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@D1 \n\n' +
        show_run_d1
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@D2 \n\n' +
        show_run_d2
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@R4 \n\n' +
        show_run_r4
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@R3 \n\n' +
        show_run_r3
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@R2 \n\n' +
        show_run_r2
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@R1 \n\n' +
        show_run_r1
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@I1 \n\n' +
        show_run_i1
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@I2 \n\n' +
        show_run_i2
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@I3 \n\n' +
        show_run_i3
        + '\n\n\n' +
        '===================================================================== \n\n'
        + '@I4 \n\n' +
        show_run_i4
    )
    
#test to see if connection is established by outputing "sh ip int br" command
#sh_ip_int_br = d1_cli.send_command("sh ip int br")
#print(sh_ip_int_br)