import netmiko
from netmiko import ConnectHandler

monitorNumber = input(r'What is your monitor number? ')

#prompt users for info
deviceInfo = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.' + monitorNumber + '.1',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

#apply IP addresses
configIPs = [
    #console access
    'line cons 0',
    'password pass',
    'login',
    'exec-timeout 0 0',
    'exit',
    
    #interface IPs
    'int gi 0/0/1',
    'no shut',
    f'ip add 200.0.0.{monitorNumber} 255.255.255.0',
    'desc OUTSIDE',
    'exit',
    'int loopback 0',
    'no shut',
    f'ip add {monitorNumber}.0.0.1 255.255.255.255',
    'desc VIRTUALIP',
    'exit'
]

#apply static route
configStaticRoute = [
    'ip routing',
    'ip route 10.11.0.0 255.255.0.0 200.0.0.11',
    'ip route 10.12.0.0 255.255.0.0 200.0.0.12',
    'ip route 10.21.0.0 255.255.0.0 200.0.0.21',
    'ip route 10.22.0.0 255.255.0.0 200.0.0.22',
    'ip route 10.31.0.0 255.255.0.0 200.0.0.31',
    'ip route 10.32.0.0 255.255.0.0 200.0.0.32',
    'ip route 10.41.0.0 255.255.0.0 200.0.0.41',
    'ip route 10.42.0.0 255.255.0.0 200.0.0.42',
    'ip route 10.51.0.0 255.255.0.0 200.0.0.51',
    'ip route 10.52.0.0 255.255.0.0 200.0.0.52',
    'ip route 10.61.0.0 255.255.0.0 200.0.0.61',
    'ip route 10.62.0.0 255.255.0.0 200.0.0.62',
    'ip route 10.71.0.0 255.255.0.0 200.0.0.71',
    'ip route 10.72.0.0 255.255.0.0 200.0.0.72',
    'ip route 10.81.0.0 255.255.0.0 200.0.0.81',
    'ip route 10.82.0.0 255.255.0.0 200.0.0.82',
    f'ip route 10.{monitorNumber}.0.0 255.255.0.0 10.{monitorNumber}.{monitorNumber}.4'
]

##Use only if routing will use OSPF
configOSPF = [
    'router ospf 1',
    f'router-id {monitorNumber}.0.0.1',
    'network 200.0.0.0 0.0.0.255 area 0',
    f'network 10.{monitorNumber}.{monitorNumber}.0 0.0.0.255 area 0',
    f'network {monitorNumber}.0.0.1 0.0.0.0 area 0',
    'exit',
    'int gi 0/0/0',
    'ip ospf network point-to-point',
    'exit'
]

#parse connection to device
accessCLI = ConnectHandler(**deviceInfo)

#test connection
#sh_ip = accessCLI.send_command('sh ip int br')
#print(sh_ip)

#apply configurations
print(r'Applying IP addresses')
accessCLI.send_config_set(configIPs)
print(r'...Success!' + '\n')

print(r'Configuring Static Routes')
accessCLI.send_config_set(configStaticRoute)
print(r'...Success!' + '\n')

print(r'Configurations Successful!!!')

showRun = accessCLI.send_command('sh run')

#disconnect from device
accessCLI.disconnect

input(r'Press Enter to close terminal. [A "_3-edgeRouter-shrun.txt" will be created containing show run output for the device]')

#create a text file for show run command
with open(r'_3-edgeRouter-shrun.txt', 'w') as file:
    file.write(showRun)
