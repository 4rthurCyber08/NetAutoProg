import json
import re
import os
import netmiko
from netmiko import ConnectHandler

class ConnectCisco:
    '''
    A class used to login to a device.
    
    To be invoked by class:ConfigureDevice and return as
    a telnet connection, accessing the cli of the device.
    
    '''
    
    def __init__(self, device_info):
        self.device_info = device_info
        
    def login(self):
        self.access_cli = netmiko.ConnectHandler(**self.device_info)
        
        return self.access_cli

class SetDeviceInfo:
    '''
    A class to determine the port number of a device.
    
    To be invoked by class:ConfigureDevice and return as a dictionary, 
    containing all device info for ConnectHandler.
    '''
    
    def __init__(self, device, device_info):
        self.device = device
        self.device_info = device_info
    
    def getPort(self):
        #determine port number
        if self.device == 'p1':
            self.device_info['port'] = 2001
        elif self.device == 'p2':
            self.device_info['port'] = 2002
        elif self.device == 'a1':
            self.device_info['port'] = 2003
        elif self.device == 'a2':
            self.device_info['port'] = 2004
        elif self.device == 's1':
            self.device_info['port'] = 2005
        elif self.device == 'd1':
            self.device_info['port'] = 2006
        elif self.device == 'd2':
            self.device_info['port'] = 2007
        elif self.device == 's2':
            self.device_info['port'] = 2008
        elif self.device == 'r4':
            self.device_info['port'] = 2009
        elif self.device == 'r3':
            self.device_info['port'] = 2010
        elif self.device == 'r2':
            self.device_info['port'] = 2011
        elif self.device == 'r1':
            self.device_info['port'] = 2012
        elif self.device == 'i3':
            self.device_info['port'] = 2013
        elif self.device == 'i2':
            self.device_info['port'] = 2014
        elif self.device == 'i1':
            self.device_info['port'] = 2015
        elif self.device == 'i4':
            self.device_info['port'] = 2016
        
        return self.device_info
    
    def getUserIP(self):
        self.user_host_ip = promptUserIP()
        self.device_info['host'] = self.user_host_ip
        
        return self.device_info

class ConfigureDevice:
    '''A class used to push commands to a device.'''
    
    def __init__(self, device, device_info):
        self.device_info = SetDeviceInfo(device, device_info).getPort()
        
        if 'host' not in self.device_info:
            self.device_info = SetDeviceInfo(device, self.device_info).getUserIP()
            
        self.access_cli = ConnectCisco(self.device_info).login()
    
    def show(self, show_command='sh ip int br'):
        '''Send show commands to a device. Default= show ip interface brief.'''
        
        self.show_run = self.access_cli.send_command(show_command)
        
        return self.show_run
    
    def push(self, config = 'do sh ip int br', return_show_run = False):
        ''' 
        Send configurations in global configuration mode (config)# to device. 
        
        Will return a text wrapper of the last few configurations applied
        to the device.
        
        Optional - return a show run command if return_show_run = True
        
        '''
        
        self.access_cli.enable()
        self.send_config = self.access_cli.send_config_set(config)
        
        if return_show_run:
            self.show_run = self.access_cli.send_command('show run')
            
            return self.show_run
        else:
            return self.send_config

def promptUserIP(force_change_ip=False):
    '''Prompt the user for their rstallrun ip address.'''
    
    if os.path.exists('saved_ip.json') == False or force_change_ip == True:
        # if the user's host ip is not saved, prompt the user
        user_rst_host_ip = ''
        ip_regex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        is_ip_valid = bool(re.search(ip_regex, user_rst_host_ip))
        
        while is_ip_valid == False:
            if user_rst_host_ip == '':
                user_rst_host_ip = input('\n What is the ip address of your Clone of RSTallrun? ')
            else:
                user_rst_host_ip = input('INVALID IP ADDRESS: What is the ip address of your Clone of RSTallrun? ')
            is_ip_valid = bool(re.search(ip_regex, user_rst_host_ip))
        
        return user_rst_host_ip
    
    else:
        # otherwise, read the saved file
        with open('saved_ip.json') as file:
            user_rst_host_ip = json.load(file)
            
        # prompt user if they need to change ip
        do_change_ip = promptChangeIP(user_rst_host_ip['host'])
        if do_change_ip:
            user_rst_host_ip = promptUserIP(True)
            device_info['host'] = user_rst_host_ip
            saveUserIP()
            
            return user_rst_host_ip
        else:
            return user_rst_host_ip['host']

def saveUserIP():
    '''Save user input information in a json file.'''
    
    with open('saved_ip.json', 'w') as file:
        user_ip = {
            'host': device_info['host']
        }
        user_ip_json = json.dumps(user_ip, indent=2)
        file.write(user_ip_json)

def promptChangeIP(saved_ip):
    '''A function to prompt the user if they want to change the already existing ip in the record.'''
    
    regexYesNo = r'^\s*[Y,y][E,e][S,s]\s*$|^\s*[N,n][O,o]\s*$|^\s*[Y,y][E,e]\s*$|^\s*[0,1]\s*$|^\s*[y,n,Y,N]\s*$'
    regexYes = r'^\s*[Y,y][E,e][S,s]\s*$|^\s*[1]\s*$|^\s*[Y,y][E,e]\s*$|^\s*[y,Y]\s*$'
    output = input(
        '\n' +
        'There is an existing record of your host ip: ' + saved_ip 
        + '\n\n' +
        r'Would you like to change it? (yes/no) '
    )
    isValidFormat = bool(re.search(regexYesNo, output))
    while isValidFormat == False:
        output = input(
            'There is an existing record of your host ip: ' + saved_ip 
            + '\n\n' +
            r'!!!INVALID INPUT!!!'
            + '\n\n' +
            r'Would you like to change it? (yes/no) '
        )
        isValidFormat = bool(re.search(regexYesNo, output))
    do_change_ip = bool(re.search(regexYes, output))
    
    return do_change_ip

# read device json file
with open('device_info.json') as file:
    device_data = json.load(file)

# parse device information for ConnectHandler arguments
device_info = device_data['device_info']

# parse device configs
dhcp = device_data['dhcp_config']
ip = device_data['i_protocol']
eigrp = device_data['eigrp_config']
ospf = device_data['ospf_config']
bgp = device_data['bgp_config']
p2_config = device_data['p2_config']
p1_config = device_data['p1_config']
a2_config = device_data['a2_config']
a1_config = device_data['a1_config']
d2_config = device_data['d2_config']
d1_config = device_data['d1_config']
s1_config = device_data['s1_config']
s2_config = device_data['s2_config']
r4_config = device_data['r4_config']
r3_config = device_data['r3_config']
r2_config = device_data['r2_config']
r1_config = device_data['r1_config']
i1_config = device_data['i1_config']
i2_config = device_data['i2_config']
i3_config = device_data['i3_config']
i4_config = device_data['i4_config']

# commands list
# commands to be pushed to cli
i1_commands = [
    f'Hostname {i1_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i1_config["r_id"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_45"]}',
    f'bgp router-id {i1_config["r_id"]}',
    'bgp log-negihbor-changes',
    f'{i1_config["neigh_45"]}',
    f'{i1_config["neigh_24"]}',
    f'{i1_config["neigh_208"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i1_config["r_id"]} mask {ip["mask_32"]}',
    f'network {bgp["net_45"]} mask {ip["mask_24"]}',
    f'network {bgp["net_24"]} mask {ip["mask_24"]}',
    f'network {bgp["net_208"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    'exit',
    'exit',
    
    # fake internet
    f'ip route {bgp["fake_net"]} 208.8.8.1',
    f'ip route {ip["def_route"]} null 0',
    
    # --ipv6
    'ipv6 unicast-routing',
    
	'interface ethernet 1/2',
	'ipv6 add b:1:4:b::4/64',
    'exit',
    
	'interface ethernet 1/1',
	'ipv6 add b:2:1:b::4/64',
    'exit',
    
	'interface ethernet 1/3',
	'ipv6 add b:1:11:b::4/64',
	'exit',
 
    'interface loopback 1',
    'ipv6 add b44::1/128',
    'exit',
    
    'router bgp 45',
    'neigh b:1:4:b::5 remote-as 45',
    'neigh b:2:1:b::2 remote-as 2',
    'neigh b:1:11:b::1 remote-as 1',
    'address-family ipv6',
    'neigh b:1:4:b::5 activate',
    'neigh b:2:1:b::2 activate',
    'neigh b:1:11:b::1 activate',
    'network b:1:4:b::/64',
    'network b:2:1:b::/64',
    'network b:1:11:b::/64',
    'network b44::1/128',
    'exit',
    'exit'
]

i2_commands = [
    f'hostname {i2_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i2_config["r_id"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_2"]}',
    f'bgp router-id {i2_config["r_id"]}',
    'bgp log-negihbor-changes',
    f'{i2_config["neigh_32"]}',
    f'{i2_config["neigh_25"]}',
    f'{i2_config["neigh_24"]}',
    f'{i2_config["neigh_207"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i2_config["r_id"]} mask {ip["mask_32"]}',
    f'network {bgp["net_32"]} mask {ip["mask_24"]}',
    f'network {bgp["net_25"]} mask {ip["mask_24"]}',
    f'network {bgp["net_24"]} mask {ip["mask_24"]}',
    f'network {bgp["net_207"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    'exit',
    'exit',
    
    # fake internet
    f'ip route {bgp["fake_net"]} 207.7.7.1',
    f'ip route {ip["def_route"]} null 0',
    
    # --ipv6
    'ipv6 unicast-routing',
    
	'interface ethernet 0/2',
	'ipv6 add b:2:4:b::2/64',
	'exit',
 
	'interface ethernet 1/1',
	'ipv6 add b:2:1:b::2/64',
	'exit',
 
	'interface ethernet 1/3',
	'ipv6 add b:1:22:b::2/64',
	'exit',
 
	'interface ethernet 1/2',
	'ipv6 add b:1:2:b::2/64',
	'exit',
 
    'interface loopback 2',
    'ipv6 add b22::1/128',
    'exit',
    
    'router bgp 2',
    'neigh b:2:1:b::4 remote-as 45',
    'neigh b:2:4:b::5 remote-as 45',
    'neigh b:1:2:b::3 remote-as 3',
    'neigh b:1:22:b::1 remote-as 1',
    'address-family ipv6',
    'neigh b:2:4:b::5 activate',
    'neigh b:2:1:b::4 activate',
    'neigh b:1:2:b::3 activate',
    'neigh b:1:22:b::1 activate',
    'network b:2:4:b::/64',
    'network b:1:2:b::/64',
    'network b:2:1:b::/64',
    'network b:1:22:b::/64',
    'network b22::1/128',
    'exit',
    'exit'
]

i3_commands = [
    f'hostname {i3_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i3_config["r_id"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_3"]}',
    f'bgp router-id {i3_config["r_id"]}',
    'bgp log-negihbor-changes',
    f'{i3_config["neigh_35"]}',
    f'{i3_config["neigh_32"]}',
    f'{i3_config["neigh_209"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i3_config["r_id"]} mask {ip["mask_32"]}',
    f'network {bgp["net_35"]} mask {ip["mask_24"]}',
    f'network {bgp["net_32"]} mask {ip["mask_24"]}',
    f'network {bgp["net_209"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    'exit',
    'exit',
    
    # fake internet
    f'ip route {bgp["fake_net"]} 207.9.9.1',
    f'ip route {ip["def_route"]} null 0',
    
    # --ipv6
    'ipv6 unicast-routing',
    
	'interface ethernet 1/1',
	'ipv6 add b:3:4:b::3/64',
	'exit',
 
    'interface ethernet 1/2',
	'ipv6 add b:1:2:b::3/64',
	'exit',
 
	'interface ethernet 1/3',
	'ipv6 add b:1:33:b::3/64',
	'exit',

    'interface loopback 3',
    'ipv6 add b33::1/128',
    'exit',
    
    'router bgp 3',
    'neigh b:3:4:b::5 remote-as 45',
    'neigh b:1:2:b::2 remote-as 2',
    'neigh b:1:33:b::1 remote-as 1',
    'address-family ipv6',
    'neigh b:3:4:b::5 activate',
    'neigh b:1:2:b::2 activate',
    'neigh b:1:33:b::1 activate',
    'network b:3:4:b::/64',
    'network b:1:2:b::/64',
    'network b:1:33:b::/64',
    'network b33::1/128',
    'exit',
    'exit'
]

i4_commands = [
    f'hostname {i4_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i4_config["r_id"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_45"]}',
    f'bgp router-id {i4_config["r_id"]}',
    'bgp log-negihbor-changes',
    f'{i4_config["neigh_35"]}',
    f'{i4_config["neigh_25"]}',
    f'{i4_config["neigh_45"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {i4_config["google"]} mask {ip["mask_32"]}',
    f'network {i4_config["r_id"]} mask {ip["mask_32"]}',
    f'network {bgp["net_35"]} mask {ip["mask_24"]}',
    f'network {bgp["net_25"]} mask {ip["mask_24"]}',
    f'network {bgp["net_45"]} mask {ip["mask_24"]}',
    'exit',
    'exit',
    
    # fake google
    'interface loopback 8',
    f'ip address {i4_config["google"]} {ip["mask_32"]}',
    f'description Google',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
    'interface loopback 8',
    'ipv6 add 2001:4860:4860::8888/128',
    'exit',
    
    'interface ethernet 0/1',
    'ipv6 add b:1:4:b::5/64',
    'exit',
    
    'interface ethernet 0/2',
    'ipv6 add b:2:4:b::5/64',
    'exit',
    
    'interface ethernet 0/3',
    'ipv6 add b:3:4:b::5/64',
    'exit',
    
    'interface loopback 4',
	'ipv6 add b55::1/128',
    'exit',
    
	'router bgp 45',
    'neigh b:3:4:b::3 remote-as 3',
	'neigh b:2:4:b::2 remote-as 2',
	'neigh b:1:4:b::4 remote-as 45',
	'address-family ipv6',
    'neigh b:3:4:b::3 activate',
    'neigh b:2:4:b::2 activate',
    'neigh b:1:4:b::4 activate',
    'network b55::1/128',
    'network 2001:4860:4860::8888/128',
    'network b:3:4:b::/64',
    'network b:2:4:b::/64',
    'network b:1:4:b::/64',
    'exit',
    'exit'
]

r1_commands = [
    f'hostname {r1_config["hostname"]}',
    
    # ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r1_config["r_id"]}',
    f'network {ospf["net_1_0"]}',
    f'network {r1_config["r_id"]} 0.0.0.0 area 12',
    f'{ospf["redis_bgp"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_1"]}',
    f'bgp router-id {r1_config["r_id"]}',
    'bgp log-neighbor-changes',
    f'{r1_config["neigh_209"]}',
    f'{r1_config["neigh_207"]}',
    f'{r1_config["neigh_208"]}',
    f'{bgp["ipv4_fam"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'{bgp["neigh_on"]}',
    f'network {r1_config["r_id"]} mask {ip["mask_32"]}',
    f'network {bgp["net_209"]} mask {ip["mask_24"]}',
    f'network {bgp["net_207"]} mask {ip["mask_24"]}',
    f'network {bgp["net_208"]} mask {ip["mask_24"]}',
    f'network {bgp["net_10"]} mask {ip["mask_30"]}',
    'exit',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
	'interface ethernet 1/3',
	'ipv6 add b:1:33:b::1/64',
    'exit',
    
	'interface ethernet 1/2',
	'ipv6 add b:1:22:b::1/64',
    'exit',
    
	'interface ethernet 1/1',
	'ipv6 add b:1:11:b::1/64',
    'exit',
    
    'router bgp 1',
    'neigh b:1:33:b::3 remote-as 3',
    'neigh b:1:22:b::2 remote-as 2',
    'neigh b:1:11:b::4 remote-as 45',
    'address-family ipv6',
    'neigh b:1:33:b::3 activate',
    'neigh b:1:22:b::2 activate',
    'neigh b:1:11:b::4 activate',
    'network FEC0:1::/122',
    'network b:1:33:b::/64',
    'network b:1:22:b::/64',
    'network b:1:11:b::/64',
    'exit',
    'exit',
    
    'interface Loopback 1',
    'ip address 1.1.1.1 255.255.255.255',
    'ipv6 address FEC0:1::1/122',
    'description Test I/F for BGP, OSPFv2 & OSPFv3 Routing',
    'exit',
    
    'interface ethernet 1/0',
    'ipv6 address 2026::12:1/122',
    'exit',
    
    # --ipv6 ospf config
    'ipv6 router ospf 6',
    'router-id 1.1.1.1',
    'exit',
    
    'interface loopback 1',
    'ipv6 ospf 6 area 12',
    'exit',
    
    'interface ethernet 1/0',
    'ipv6 ospf 6 area 12',
    'exit',
    
    # --ipv6 bgp-ospf redistribution
    'ipv6 router ospf 6',
    'default-information originate always',
    'redistribute bgp 1 metric 69',
    'exit',
    
    'router bgp 1',
    'address-family ipv6 unicast',
    'redistribute ospf 6 match internal external 1 external 2',
    'exit'
]

r2_commands = [
    f'hostname {r2_config["hostname"]}',
    
    # ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r2_config["r_id"]}',
    f'network {ospf["net_1_4"]}',
    f'network {ospf["net_1_0"]}',
    f'network {r2_config["r_id"]} 0.0.0.0 area 0',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
    'interface Loopback 2',
    'ip address 2.2.2.2 255.255.255.255',
    'ipv6 address FEC0:2::2/122',
    'description Test I/F for OSPFv2 & OSPFv3 Routing',
    'exit',
    
    'interface ethernet 1/2',
    'ipv6 address 2026::12:2/122',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 address 2026::1:1/122',
    'exit',
    
    # --ipv6 ospf config
    'ipv6 router ospf 6',
    'router-id 2.2.2.2',
    'exit',
    
    'interface loopback 2',
    'ipv6 ospf 6 area 0',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 ospf 6 area 0',
    'exit',
    
    'interface ethernet 1/2',
    'ipv6 ospf 6 area 12',
    'exit'
]

r3_commands = [
    f'hostname {r3_config["hostname"]}',
    
    # ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r3_config["r_id"]}',
    f'network {ospf["net_1_8"]}',
    f'network {ospf["net_1_4"]}',
    f'network {r3_config["r_id"]} 0.0.0.0 area 0',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
    'interface Loopback 3',
    'ip address 3.3.3.3 255.255.255.255',
    'ipv6 address FEC0:3::3/122',
    'description Test I/F for OSPFv2 & OSPFv3 Routing',
    'exit',
    
    'interface Tunnel34',
    'no ip address',
    'ipv6 address 2026::34:1/122',
    'tunnel source lo3',
    'tunnel destination 4.4.4.4',
    'tunnel mode ipv6ip',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 address 2026::1:2/122',
    'exit',
    
    # --ipv6 ospf config
    'ipv6 router ospf 6',
    'router-id 3.3.3.3',
    'exit',
    
    'interface loopback 3',
    'ipv6 ospf 6 area 0',
    'exit',
    
    'interface Tunnel34',
    'ipv6 ospf 6 area 34',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 ospf 6 area 0',
    'exit',
]
r4_commands = [
    f'hostname {r4_config["hostname"]}',
    
    # eigrp config
    f'router eigrp {eigrp["as100"]}',
    f'eigrp router-id {r4_config["r_id"]}',
    'no auto-summary',
    f'network {eigrp["net_4_4"]}',
    f'network {eigrp["net_4_8"]}',
    f'network {r4_config["r_id"]} 0.0.0.0',
    f'{eigrp["redis_ospf_1"]}',
    'exit',
    
    # ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r4_config["r_id"]}',
    f'network {ospf["net_1_8"]}',
    f'network {r4_config["r_id"]} 0.0.0.0 area 34',
    f'{ospf["redis_eigrp_100"]}',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
    'interface Loopback 4',
    'ip address 4.4.4.4 255.255.255.255',
    'ipv6 address FEC0::4:4/122',
    'description Test I/F for OSPFv2 & OSPFv3 Routing',
    'exit',
    
    'interface ethernet 1/0',
    'ip address 10.1.4.5 255.255.255.252',
    'ipv6 address 2026::2:1/122',
    'description L3 Link to DSW1',
    'exit',
    
    'interface ethernet 1/1',
    'ip address 10.1.4.9 255.255.255.252',
    'description L3 Link to DSW2 fa0/14',
    'exit',
    
    'interface Loopback 14',
    'no ip address',
    'ipv6 address FEC0::14:4/122',
    'description Test I/F for RIPng Routing',
    'exit',
    
    'interface Loopback 21',
    'ip address 10.1.21.129 255.255.255.224',
    'description Test I/F for EIGRPv4 Routing & IP(v4) Helper Loopback I/F',
    'exit',
    
    'interface Tunnel34',
    'no ip address',
    'ipv6 address 2026::34:2/122',
    'tunnel source loopback 4',
    'tunnel destination 3.3.3.3',
    'tunnel mode ipv6ip',
    'exit',
    
    # --ipv6 ospf config
    'ipv6 router ospf 6',
    'router-id 4.4.4.4',
    'exit',
    
    'interface loopback 4',
    'ipv6 ospf 6 area 34',
    'exit',
    
    'interface Tunnel34',
    'ipv6 ospf 6 area 34',
    'exit'
    
    # --ipv6 internal
    'interface ethernet 1/0',
    'ipv6 add 10:1:4:14::4/64',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 add 10:1:4:24::4/64',
    'exit',
    
    # --ipv6 eigrp config
    'ipv6 router eigrp 10',
    'eigrp router-id 4.4.4.4',
    'no shut',
    'exit',
    
    'interface loopback 4',
    'ipv6 eigrp 10',
    'exit',
    
    'interface ethernet 1/0',
    'ipv6 eigrp 10',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 eigrp 10',
    'exit',
    
    # --ipv6 eigrp-ospf redistribution
    'ipv6 router ospf 6',
    'redistribute eigrp 10 include-connected',
    'exit',
    
    'ipv6 router eigrp 10',
    'redistribute ospf 6 metric 10000 100 255 1 1500 include-connected',
    'exit'
]

d1_commands = [
    f'hostname {d1_config["hostname"]}',
    'interface ethernet 1/0',
    'switchport mode access',
    'switchport access vlan 200',
    'exit',
    
    # dhcp config
    f'ip dhcp excluded-address {d1_config["excip_01"]}',
    f'ip dhcp excluded-address {d1_config["excip_02"]}',
    f'ip dhcp pool {d1_config["dhcp_pool"]}',
    f'network {dhcp["net_v10"]} {ip["mask_24"]}',
    f'default-router {d1_config["gateway"]}',
    'exit',
    
    # eigrp config
    f'router {eigrp["named-eigrp"]}',
    f'address-family ipv4 unicast autonomous-system {eigrp["as100"]}',
    f'eigrp router-id {d1_config["r_id"]}',
    f'network {eigrp["net_4_4"]}',
    f'network {eigrp["net_1_0"]}',
    f'network {eigrp["net_2_0"]}',
    f'network {eigrp["net_v200"]}',
    f'network {d1_config["r_id"]} 0.0.0.0',
    'exit',
    'exit',
    
    # --ipv6 internal
    'ipv6 unicast-routing',
    
    'interface Loopback 1',
    'ip address 11.11.11.11 255.255.255.255',
    'ipv6 address 11:11:11:11::1/128',
    'ipv6 address FEC0::11:1/122',
    'description IPv4, IPv6 & RIPng Test I/F',
    'exit',
    
    'interface ethernet 1/1',
    'no switchport',
    'ip address 10.1.4.6 255.255.255.252',
    'ipv6 address 2026::2:2/122',
    'ipv6 add 10:1:4:14::1/64',
    'description L3 UpLink to R4',
    'exit',
    
    'interface vlan 200',
    'ipv6 address 2026::3:1/122',
    'ipv6 add 192:168:1:1234::1/64',
    'description IPv6 Link to DSW2',
    'exit',
    
    'int vlan 10',
    'ipv6 add 10:2:1:12::1/64',
    'exit',
    
    'int vlan 20',
    'ipv6 add 10:2:2:12::1/64',
    'exit',
    
    # --ipv6 eigrp config
    'interface loopback 1',
    'ipv6 address 11:11:11:11::1/64',
    'ipv6 router eigrp 10',
    'eigrp router-id 1.1.1.1',
    'no shut',
    'exit',
    
    'interface lo1',
    'ipv6 eigrp 10',
    'exit',
    
    'interface e1/1',
    'ipv6 eigrp 10',
    'exit',
    
    'interface vlan 10',
    'ipv6 eigrp 10',
    'exit',
    
    'interface vlan 20',
    'ipv6 eigrp 10',
    'exit',
    
    'interface vlan 200',
    'ipv6 eigrp 10',
    'exit'
]

d2_commands = [
    f'hostname {d2_config["hostname"]}',
    'interface ethernet 1/0',
    'switchport mode access',
    'switchport access vlan 20',
    'exit',
    
    # dhcp config
    f'ip dhcp excluded-address {d2_config["excip_01"]}',
    f'ip dhcp excluded-address {d2_config["excip_02"]}',
    f'ip dhcp pool {d2_config["dhcp_pool"]}',
    f'network {dhcp["net_v10"]} {ip["mask_24"]}',
    f'default-router {d2_config["gateway"]}',
    'exit',
    
    # eigrp config
    f'router {eigrp["named-eigrp"]}',
    f'address-family ipv4 unicast autonomous-system {eigrp["as100"]}',
    f'eigrp router-id {d2_config["r_id"]}',
    f'network {eigrp["net_4_8"]}',
    f'network {eigrp["net_1_0"]}',
    f'network {eigrp["net_2_0"]}',
    f'network {eigrp["net_v200"]}',
    f'network {d2_config["r_id"]} 0.0.0.0',
    'exit',
    'exit',
    
    # --ipv6 internal
    'ipv6 unicast-routing',
    
    'interface Loopback 2',
    'ip address 22.22.22.22 255.255.255.255',
    'ipv6 add 22:22:22:22::2/128',
    'ipv6 address FEC0::22:2/122',
    'description IPv4, IPv6 & RIPng Test I/F',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 add 10:1:4:24::2/64',
    'exit',
    
    'interface vlan 200',
    'ipv6 address 2026::3:2/122',
    'ipv6 add 192:168:1:1234::2/64',
    'description IPv6 Link to DSW1',
    'exit',
    
    'interface vlan 10',
    'ipv6 add 10:2:1:12::2/64',
    'exit',
    
    'interface vlan 20',
    'ipv6 add 10:2:2:12::2/64',
    'exit'
    
    # --ipv6 eigrp config
    'interface loopback 1',
    'ipv6 address 22:22:22:22::2/64',
    'ipv6 router eigrp 10',
    'eigrp router-id 2.2.2.2',
    'no shut',
    'exit',
    
    'interface loopback 1',
    'ipv6 eigrp 10',
    'exit',
    
    'interface ethernet 1/1',
    'ipv6 eigrp 10',
    'exit',
    
    'interface vlan 10',
    'ipv6 eigrp 10',
    'exit',
    
    'interface vlan 20',
    'ipv6 eigrp 10',
    'exit',
    
    'interface vlan 200',
    'ipv6 eigrp 10',
    'exit'
]

a1_commands = [
    f'hostname {a1_config["hostname"]}',
    'interface ethernet 0/0',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    
    f'ip route {ip["def_route"]} {ip["def_129"]} 1',
    f'ip route {ip["def_route"]} {ip["def_130"]} 2'
]

a2_commands = [
    f'hostname {a2_config["hostname"]}',
    'interface ethernet 1/0',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    
    f'ip route {ip["def_route"]} {ip["def_130"]} 1',
    f'ip route {ip["def_route"]} {ip["def_129"]} 2'
]

s1_commands = [
    f'hostname {s1_config["hostname"]}',
    
    'interface e1/0',
    'no shutdown',
    f'ip add {s1_config["int_1_0"]} {ip["mask_27"]}',
    'exit',
    
    f'ip route {ip["def_route"]} {s1_config["gateway_1"]} 1',
    f'ip route {ip["def_route"]} {s1_config["gateway_2"]} 2'
]

s2_commands = [
    f'hostname {s2_config["hostname"]}',
    
    'interface e1/0',
    'no shutdown',
    f'ip add {s2_config["int_1_0"]} {ip["mask_24"]}',
    'exit',
    
    f'ip route {ip["def_route"]} {s2_config["gateway_1"]} 1',
    f'ip route {ip["def_route"]} {s2_config["gateway_2"]} 2'
]

p1_commands = [
    f'hostname {p1_config["hostname"]}',
    
    f'ip route {ip["def_route"]} {ip["def_1_1"]} 1',
    f'ip route {ip["def_route"]} {ip["def_1_2"]} 2',
    
    'interface ethernet 0/0',
    'ip add dhcp',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
    'interface ethernet 0/0',
    'ipv6 en',
    'ipv6 add 10:2:1:12::B00B/64',
    'ipv6 add autoconfig',
    'exit',
    
    'ipv6 route ::/0 10:2:1:12::1'
    
]

p2_commands = [
    f'hostname {p2_config["hostname"]}',
    
    f'ip route {ip["def_route"]} {ip["def_1_2"]} 1',
    f'ip route {ip["def_route"]} {ip["def_1_1"]} 2',
    
    'interface ethernet 1/0',
    'ip add dhcp',
    'exit',
    
    # --ipv6
    'ipv6 unicast-routing',
    
    'ipv6 route ::/0 10:2:1:12::2',
    
    'interface ethernet 1/0',
    'ipv6 address 10:2:1:12::/64 eui-64',
    'exit',
    
    'ipv6 route ::/0 10:2:1:12::2'
]

# sequence of configuration
# configure ISPs First so that pinging 8.8.8.8 will be faster
seq_of_Config = ['isp4', 'isp3', 'isp2', 'isp1', 'r1', 's1', 's2', 'd1', 'd2', 'a1', 'a2', 'p1', 'p2', 'r3', 'r2', 'r4', 'END']

# for loop to configure each device
for device in seq_of_Config:    
    if device == 'd1':
        show_run_d1 = ConfigureDevice('d1', device_info).push(d1_commands, True)
    elif device == 'd2':
        show_run_d2 = ConfigureDevice('d2', device_info).push(d2_commands, True)
    elif device == 'a1':
        show_run_a1 = ConfigureDevice('a1', device_info).push(a1_commands, True)
    elif device == 's1':
        show_run_s1 = ConfigureDevice('s1', device_info).push(s1_commands, True)
    elif device == 's2':
        show_run_s2 = ConfigureDevice('s2', device_info).push(s2_commands, True)
    elif device == 'a2':
        show_run_a2 = ConfigureDevice('a2', device_info).push(a2_commands, True)
    elif device == 'p1':
        show_run_p1 = ConfigureDevice('p1', device_info).push(p1_commands, True)
    elif device == 'p2':
        show_run_p2 = ConfigureDevice('p2', device_info).push(p2_commands, True)
    elif device == 'r3':
        show_run_r3 = ConfigureDevice('r3', device_info).push(r3_commands, True)
    elif device == 'r2':
        show_run_r2 = ConfigureDevice('r2', device_info).push(r2_commands, True)
    elif device == 'r4':
        show_run_r4 = ConfigureDevice('r4', device_info).push(r4_commands, True)
    elif device == 'isp4': 
        show_run_i4 = ConfigureDevice('i4', device_info).push(i4_commands, True)
    elif device == 'isp3':
        show_run_i3 = ConfigureDevice('i3', device_info).push(i3_commands, True)
    elif device == 'isp2':
        show_run_i2 = ConfigureDevice('i2', device_info).push(i2_commands, True)
    elif device == 'isp1':
        show_run_i1 = ConfigureDevice('i1', device_info).push(i1_commands, True)
    elif device == 'r1':
        show_run_r1 = ConfigureDevice('r1', device_info).push(r1_commands, True)
    
    if device != 'END':
        print('Configuring ' + device.upper() + '...')
    else:
        print('Configuration Complete for : Clone of RSTallrun [' + device_info['host'] + ']')
        print(r'Please wait for BGP to build routes before pinging 8.8.8.8')
        input(r'Press Enter to close terminal. [A "show_run.txt" will be created containing show run output for all devices.]')

        # create a file for show run output of all devices
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
                + '@S1 \n\n' +
                show_run_s1
                + '\n\n\n' +
                '===================================================================== \n\n'
                + '@S2 \n\n' +
                show_run_s2
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

# save user's ip for future use
saveUserIP()