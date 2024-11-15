import netmiko
from netmiko import ConnectHandler

monitorNumber = input(r'What is your monitor number? ')
camera6MAC = input(r'What is the MAC Address of the camera on port fa 0/6? Answer in xxxx.xxxx.xxxx format. ')
camera8MAC = input(r'What is the MAC Address of the camera on port fa 0/8? Answer in xxxx.xxxx.xxxx format. ')

deviceInfo = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.1.4',
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
    'int gi 0/1',
    'no shut',
    'no switchport',
    f'ip add 10.{monitorNumber}.{monitorNumber}.4 255.255.255.0',
    'exit',
    'int vlan 10',
    'no shut',
    f'ip add 10.{monitorNumber}.10.4 255.255.255.0',
    'desc mgmtWifi-configuredFromPython',
    'exit',
    'int vlan 50',
    'no shut',
    f'ip add 10.{monitorNumber}.50.4 255.255.255.0',
    'desc mgmtCCTV-configuredFromPython',
    'exit',
    'int vlan 100',
    'no shut',
    f'ip add 10.{monitorNumber}.100.4 255.255.255.0',
    'desc mgmtVOICE-configuredFromPython',
    'exit'
]

#apply dhcp
configDHCP = [
    #reserve IPs
    f'ip dhcp excluded-add 10.{monitorNumber}.1.1 10.{monitorNumber}.1.100',
    f'ip dhcp excluded-add 10.{monitorNumber}.10.1 10.{monitorNumber}.10.100',
    f'ip dhcp excluded-add 10.{monitorNumber}.50.1 10.{monitorNumber}.50.100',
    f'ip dhcp excluded-add 10.{monitorNumber}.100.1 10.{monitorNumber}.100.100',
    
    #dhcp pool
    'ip dhcp pool POOLDATA',
    f'network 10.{monitorNumber}.1.0 255.255.255.0',
    f'default-router 10.{monitorNumber}.1.4',
    'domain-name MGMTDATA.COM',
    f'dns-server 10.{monitorNumber}.1.10',
    'exit',
    
    'ip dhcp pool POOLWIFI',
    f'network 10.{monitorNumber}.10.0 255.255.255.0',
    f'default-router 10.{monitorNumber}.10.4',
    'domain-name WIFIDATA.COM',
    f'dns-server 10.{monitorNumber}.1.10',
    'exit',
    
    'ip dhcp pool POOLCCTV',
    f'network 10.{monitorNumber}.50.0 255.255.255.0',
    f'default-router 10.{monitorNumber}.50.4',
    'domain-name CCTVDATA.COM',
    f'dns-server 10.{monitorNumber}.1.10',
    'exit',
    
    'ip dhcp pool POOLVOICE',
    f'network 10.{monitorNumber}.100.0 255.255.255.0',
    f'default-router 10.{monitorNumber}.100.4',
    'domain-name VOICEDATA.COM',
    f'dns-server 10.{monitorNumber}.1.10',
    f'option 150 ip 10.{monitorNumber}.100.8',
    'exit'
]

#switchport
configPorts = [
    #create VLANs
    'vlan 1',
    'name MGMTVLAN',
    'exit',
    'vlan 10',
    'name WIFIVLAN',
    'exit',
    'vlan 50',
    'name CCTVVLAN',
    'exit',
    'vlan 100',
    'name VOICEVLAN',
    'exit',
    
    'int fa 0/2',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    'int fa 0/4',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    'int fa 0/6',
    'switchport mode access',
    'switchport access vlan 50',
    'exit',
    'int fa 0/8',
    'switchport mode access',
    'switchport access vlan 50',
    'exit',
    'int fa 0/3',
    'switchport mode access',
    'switchport access vlan 100',
    'exit',
    'int fa 0/5',
    'switchport mode access',
    'switchport voice vlan 100',
    'switchport access vlan 1',
    'mls qos trust device cisco-phone',
    'exit',
    'int fa 0/7',
    'switchport mode access',
    'switchport voice vlan 100',
    'switchport access vlan 1',
    'mls qos trust device cisco-phone',
    'exit',
]

#camera
configCameras = [
    'ip dhcp pool CAMERA6',
    f'host 10.{monitorNumber}.50.6 255.255.255.0',
    f'client-identifier {camera6MAC}',
    'exit',
    'ip dhcp pool CAMERA8',
    f'host 10.{monitorNumber}.50.8 255.255.255.0',
    f'client-identifier {camera8MAC}',
    'exit',
]

#set default route
configDefaultRoute = [
    f'ip route 0.0.0.0 0.0.0.0 10.{monitorNumber}.{monitorNumber}.1'
]

configOSPF = [
    'router ospf 1',
    f'router-id 10.{monitorNumber}.{monitorNumber}.4',
    f'network 10.{monitorNumber}.0.0 0.0.255.255 area 0',
    'exit',
    'int gi 0/1',
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
print(r'Configuring DHCP')
accessCLI.send_config_set(configDHCP)
print(r'Configuring Switchport')
accessCLI.send_config_set(configPorts)
print(r'Reserving Camera IPs')
accessCLI.send_config_set(configCameras)


#disconnect from device
accessCLI.disconnect