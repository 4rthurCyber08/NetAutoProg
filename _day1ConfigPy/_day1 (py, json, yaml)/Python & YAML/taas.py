import netmiko
from netmiko import ConnectHandler
import yaml
import pprint

# prompt user for info
user_m = input('What is your monitor number? ')


# 3 Steps (WRITE, CONNECT, PUSH)

# WRITE - device info and commands
# read the yaml file
with open('taas-configs.yaml') as file:
    # convert yaml data to usable python data
    yaml_configs = yaml.safe_load(file)

# update the key[ip] for connection
yaml_configs['device_info']['ip'] = f'10.{user_m}.1.2'

# parse data
# ConnectHandler arguments to establish SSH connection to device
device_info = yaml_configs['device_info']

# configurations for commands
ips = yaml_configs['ips']
svi = ips['svi']

# Commands to be sent to the device
ip_commands = [
    # console access
    'line cons 0',
    f'password {ips["password"]}',
    'login',
    f'exec-timeout {ips['no_timeout']}',
    'exit',
    
    # interface IPs
    'int vlan 10',
    'no shut',
    f'ip add 10.{user_m}.{svi['v10']} {ips['mask_24']}',
    f'desc mgmtWifi{ips['via_py']}',
    'exit',
    'int vlan 50',
    'no shut',
    f'ip add 10.{user_m}.{svi['v50']} {ips['mask_24']}',
    f'desc mgmtCCTV{ips['via_py']}',
    'exit',
    'int vlan 100',
    'no shut',
    f'ip add 10.{user_m}.{svi['v100']} {ips['mask_24']}',
    f'desc mgmtVOICE-{ips['via_py']}',
    'exit',
]

# CONNECT - to the device
# Establish connection and access cli
accessCLI = ConnectHandler(**device_info)


# PUSH - commands to the device
# inform user what is currently being configured
print('Configuring device...')
accessCLI.send_config_set(ip_commands)
print('Configuration Successful!!!\n')

#pprint.pp(reserve_commands, indent=4)