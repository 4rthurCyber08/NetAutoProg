import netmiko
import os
import re
import json
from netmiko import ConnectHandler

# --PROMPT USER FOR DEVICE INFO--
#check if user needs to be prompted for info
if os.path.exists('userDeviceInfo.json') == False:
    #print('Working')
    
    #regex patterns
    regexMonitor = r'^[1-7][1,2]$'
    regexMAC = r'^[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}$'
    
    #monitor number
    monitorNumber = input(r'What is your monitor number? ')
    monitorIsValid = bool(re.search(regexMonitor, monitorNumber))
    
    while monitorIsValid == False:
        print('INVALID MONITOR NUMBER: ' + monitorNumber)
        monitorNumber = input(r'What is your monitor number? ')
        monitorIsValid = bool(re.search(regexMonitor, monitorNumber))
    
    #camera6 MAC Address    
    camera6MAC = input(r'What is the MAC Address of the camera on port fa 0/6? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidCamera6 = bool(re.search(regexMAC, camera6MAC))
    
    while macIsValidCamera6 == False:
        print('INVALID MAD ADDRESS: ' + camera6MAC)
        camera6MAC = input(r'What is the MAC Address of the camera on port fa 0/6? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidCamera6 = bool(re.search(regexMAC, camera6MAC))
    
    #camera8 MAC Address
    camera8MAC = input(r'What is the MAC Address of the camera on port fa 0/8? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidCamera8 = bool(re.search(regexMAC, camera8MAC))
    
    while macIsValidCamera8 == False:
        print('INVALID MAD ADDRESS: ' + camera8MAC)
        camera8MAC = input(r'What is the MAC Address of the camera on port fa 0/8? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidCamera8 = bool(re.search(regexMAC, camera8MAC))

    #ephone1 MAC Address    
    ephone1MAC = input(r'What is the MAC Address of ephone1 on port fa 0/5? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidEphone1 = bool(re.search(regexMAC, ephone1MAC))
    
    while macIsValidEphone1 == False:
        print('INVALID MAD ADDRESS: ' + ephone1MAC)
        ephone1MAC = input(r'What is the MAC Address of ephone1 on port fa 0/5? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidEphone1 = bool(re.search(regexMAC, ephone1MAC))
    
    #ephone2 MAC Address    
    ephone2MAC = input(r'What is the MAC Address of ephone2 on port fa 0/7? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidEphone2 = bool(re.search(regexMAC, ephone2MAC))
    
    while macIsValidEphone2 == False:
        print('INVALID MAD ADDRESS: ' + ephone2MAC)
        ephone2MAC = input(r'What is the MAC Address of ephone2 on port fa 0/7? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidEphone2 = bool(re.search(regexMAC, ephone2MAC))
    
    #store monitor number and mac addresses in a JSON file
    with open('userDeviceInfo.json', 'w') as file:
        userData = {
            'monitorNumber': monitorNumber,
            'camera6MAC': camera6MAC,
            'camera8MAC': camera8MAC,
            'ephone1MAC': ephone1MAC,
            'ephone2MAC': ephone2MAC 
        }
        jsoncontent = json.dumps(userData, indent=2)
        file.write(jsoncontent)

#don't prompt user if they already provided their monitor number and mac addresses
else:
    with open('userDeviceInfo.json', 'r') as file:
        userInfo = json.load(file)
    monitorNumber = userInfo['monitorNumber']
    camera6MAC = userInfo['camera6MAC']
    camera8MAC = userInfo['camera8MAC']
    ephone1MAC = userInfo['ephone1MAC']
    ephone2MAC = userInfo['ephone2MAC']


# --OBTAIN DEVICE INFO--
with open("deviceInfo.json", "r") as file:
    deviceInfo = json.load(file)

#parse information for each device
coreBabaInfo = deviceInfo["coreBaba"]
cucmInfo = deviceInfo["callManager"]
edgeRouterInfo = deviceInfo["edgeRouter"]


#DEVICE CONFIGURATIONS
#-------------------------------coreBABA
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

#Use only if routing will use OSPF
configOSPFBABA = [
    'router ospf 1',
    f'router-id 10.{monitorNumber}.{monitorNumber}.4',
    f'network 10.{monitorNumber}.0.0 0.0.255.255 area 0',
    'exit',
    'int gi 0/1',
    'ip ospf network point-to-point',
    'exit'
]

#-------------------------------callManager
configCUCMConsole = [
    #console access
    'line cons 0',
    'password pass',
    'login',
    'exec-timeout 0 0',
    'exit',
]

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
    'exit',
]

configIncoming = [
    'voice service voip',
    'ip address trusted list',
    'ipv4 0.0.0.0 0.0.0.0',
    'exit'
]

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

configIVRS = [
    'dial-peer voice 69 voip',
    'service rivanaa out-bound',
    f'destination-pattern {monitorNumber}69',
    f'session target ipv4:10.{monitorNumber}.100.8',
    f'incoming called-number {monitorNumber}69',
    'dtmf-relay h245-alphanumeric',
    'codec g711ulaw',
    'no vad',
 
    'telephony-service',
    r'moh "flash:/en_bacd_music_on_hold.au"',

    'application',
    'service rivanaa flash:app-b-acd-aa-3.0.0.2.tcl',
    'paramspace english index 1',
    'param number-of-hunt-grps 2',
    'param dial-by-extension-option 8',
    'param handoff-string rivanaa',
    'param welcome-prompt flash:en_bacd_welcome.au',
    'paramspace english language en',
    'param call-retry-timer 15',
    'param service-name rivanqueue',
    r'paramspace english location flash:',
    'param second-greeting-time 60',
    'param max-time-vm-retry 2',
    'param voice-mail 1234',
    'param max-time-call-retry 700',
    'param aa-pilot _69',
    'service rivanqueue flash:app-b-acd-3.0.0.2.tcl',
    'param queue-len 15',
    f'param aa-hunt1 {monitorNumber}00',
    f'param aa-hunt2 {monitorNumber}01',
    f'param aa-hunt3 {monitorNumber}77',
    f'param aa-hunt4 {monitorNumber}33',
    'param queue-manager-debugs 1',
    'param number-of-hunt-grps 4',
    'exit'
]

#Use only if routing will use OSPF
configOSPFCUCM = [
    'router ospf 1',
    f'router-id 10.{monitorNumber}.100.8',
    f'network 10.{monitorNumber}.100.0 0.0.0.255 area 0',
    'exit'
]

#-------------------------------edgeRouter
#apply IP addresses
configIPsEDGE = [
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
    'exit',
]

#apply static route
configStaticRoute = [
    'ip routing'
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
    f'ip route 10.{monitorNumber}.0.0 255.255.0.0 10.{monitorNumber}.{monitorNumber}.4',
]

##Use only if routing will use OSPF
configOSPFEDGE = [
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


#CONNECT AND PUSH CONFIGURATIONS
print(r' ')
#parse connection to devices
#coreBABA
print(r'@----- Connecting to COREBABA')
accessCLI = ConnectHandler(**coreBabaInfo)

#apply configurations for coreBABA
print(r'Applying IP addresses...')
accessCLI.send_config_set(configIPs)
print(r'...Success!' + '\n')

print(r'Configuring DHCP...')
accessCLI.send_config_set(configDHCP)
print(r'...Success!' + '\n')

print(r'Configuring Switchport...')
accessCLI.send_config_set(configPorts)
print(r'...Success!' + '\n')

print(r'Reserving Camera IPs...')
accessCLI.send_config_set(configCameras)
print(r'...Success!' + '\n')

print(r'Configuring OSPF...')
accessCLI.send_config_set(configOSPFBABA)
print(r'...Success!' + '\n')

accessCLI.disconnect
print(r'-----@ Configurations for COREBABA is Successful!!!' + '\n')

#callManager
print(r'@----- Connecting to CALLMANAGER')
accessCLI = ConnectHandler(**cucmInfo)

#apply configurations for callManager
print(r'Configuring Console Connection...')
accessCLI.send_config_set(configCUCMConsole)
print(r'...Success!' + '\n')

print(r'Configuring Analog Phones...')
accessCLI.send_config_set(configAnalog)
print(r'...Success!' + '\n')

for i in range(1,3):
    print(r'Configuring Ephones ' + str(i) + '/2')
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

print(r'Configuring IVRS...')
accessCLI.send_config_set(configIVRS)
print(r'...Success!' + '\n')

print(r'Configuring OSPF...')
accessCLI.send_config_set(configOSPFCUCM)
print(r'...Success!' + '\n')

#disconnect from device
accessCLI.disconnect
print(r'-----@ Configurations for CALLMANAGER is Successful!!!' + '\n')

#edgeRouter
print(r'@----- Connecting to EDGEROUTER')
accessCLI = ConnectHandler(**edgeRouterInfo)

#apply configurations for edgeRouter
print(r'Applying IP addresses')
accessCLI.send_config_set(configIPsEDGE)
print(r'...Success!' + '\n')

print(r'Configuring Static Routes')
accessCLI.send_config_set(configStaticRoute)
print(r'...Success!' + '\n')

print(r'Configuring OSPF...')
accessCLI.send_config_set(configOSPFEDGE)
print(r'...Success!' + '\n')

accessCLI.disconnect
print(r'-----@ Configurations for EDGEROUTER is Successful!!!' + '\n')

#Make ephone Numbers Appear, please
print(r'@----- Finishing configurations' + '\n')
accessCLI = ConnectHandler(**cucmInfo)

#apply configurations for callManager
for i in range(1,3):
    print(r'Forcing ephone numbers to appear ' + str(i) + '/2')
    accessCLI.send_config_set(configEphone)

#disconnect from device
accessCLI.disconnect
print(r'-----@ Configurations Complete!!!' + '\n')


#test connection
#sh_ip = accessCLI.send_command('sh ip int br')
#print(sh_ip)