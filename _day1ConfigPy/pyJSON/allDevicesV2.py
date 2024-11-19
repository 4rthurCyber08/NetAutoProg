import netmiko
import os
import re
import json
import colorama
from colorama import Fore, Back, Style
from netmiko import ConnectHandler

colorama.init(autoreset=True)

#regex patterns
regexMonitor = r'^[1-7][1,2]$'
regexMAC = r'^[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}$'
regexYesNo = r'^[Y,y][E,e][S,s]\s*$|^[N,n][O,o]\s*$|^[0,1]\s*$|^[y,n,Y,N]\s*$'
regexYes = r'^[Y,y][E,e][S,s]\s*$|^[1]\s*$|^[y,Y]\s*$'
regexNo = r'^[N,n][O,o]\s*$|^[0]\s*$|^[n,N]\s*$'

#initialize variables
monitorNumber = ''
camera6MAC = ''
camera8MAC = ''
ephone1MAC = ''
ephone2MAC = ''

def getMonitorNum():
    monitorNumber = input(r'What is your monitor number? ')
    monitorIsValid = bool(re.search(regexMonitor, monitorNumber))
    
    while monitorIsValid == False:
        print(Back.RED + 'INVALID MONITOR NUMBER: ' + monitorNumber)
        monitorNumber = input(r'What is your monitor number? ')
        monitorIsValid = bool(re.search(regexMonitor, monitorNumber))
    
    return monitorNumber

def getCam6MAC():  
    camera6MAC = input(r'What is the MAC Address of the camera on port fa 0/6? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidCamera6 = bool(re.search(regexMAC, camera6MAC))
    
    while macIsValidCamera6 == False:
        print(Back.RED + 'INVALID MAC ADDRESS: ' + camera6MAC)
        camera6MAC = input(r'What is the MAC Address of the camera on port fa 0/6? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidCamera6 = bool(re.search(regexMAC, camera6MAC))
    
    return camera6MAC

def getCam8MAC():
    camera8MAC = input(r'What is the MAC Address of the camera on port fa 0/8? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidCamera8 = bool(re.search(regexMAC, camera8MAC))
    
    while macIsValidCamera8 == False:
        print(Back.RED + 'INVALID MAC ADDRESS: ' + camera8MAC)
        camera8MAC = input(r'What is the MAC Address of the camera on port fa 0/8? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidCamera8 = bool(re.search(regexMAC, camera8MAC))
    
    return camera8MAC

def getPhone1MAC():  
    ephone1MAC = input(r'What is the MAC Address of ephone1 on port fa 0/5? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidEphone1 = bool(re.search(regexMAC, ephone1MAC))
    
    while macIsValidEphone1 == False:
        print(Back.RED + 'INVALID MAC ADDRESS: ' + ephone1MAC)
        ephone1MAC = input(r'What is the MAC Address of ephone1 on port fa 0/5? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidEphone1 = bool(re.search(regexMAC, ephone1MAC))
        
    return ephone1MAC

def getPhone2MAC():   
    ephone2MAC = input(r'What is the MAC Address of ephone2 on port fa 0/7? Answer in xxxx.xxxx.xxxx format. ')
    macIsValidEphone2 = bool(re.search(regexMAC, ephone2MAC))
    
    while macIsValidEphone2 == False:
        print(Back.RED + 'INVALID MAC ADDRESS: ' + ephone2MAC)
        ephone2MAC = input(r'What is the MAC Address of ephone2 on port fa 0/7? Answer in xxxx.xxxx.xxxx format. ')
        macIsValidEphone2 = bool(re.search(regexMAC, ephone2MAC))
    
    return ephone2MAC

def storeDeviceInfo(monitor, cam6MAC, cam8MAC, ep1MAC, ep2MAC):
    with open('userDeviceInfo.json', 'w') as file:
        userData = {
            'monitorNumber': monitor,
            'camera6MAC': cam6MAC,
            'camera8MAC': cam8MAC,
            'ephone1MAC': ep1MAC,
            'ephone2MAC': ep2MAC 
        }
        jsoncontent = json.dumps(userData, indent=2)
        file.write(jsoncontent)

def promptDeviceInfo():
    monitor = getMonitorNum()
    cam6MAC = getCam6MAC()
    cam8MAC = getCam8MAC()
    ep1MAC = getPhone1MAC()
    ep2MAC = getPhone2MAC()
    storeDeviceInfo(monitor, cam6MAC, cam8MAC, ep1MAC, ep2MAC)
    
def evalInfo():
    output = input(
        'There\'s an existing record of your device information: \n\n' +
        'Monitor number: ' + monitorNumber + '\n' +
        'Camera6 MAC: ' + camera6MAC + '\n' +
        'Camera8 MAC: ' + camera8MAC + '\n' +
        'Ephone 1 MAC: ' + ephone1MAC + '\n' +
        'Ephone 2 MAC: ' + ephone2MAC + '\n\n\n' +
        r'Are all of these information correct (yes/no)? '
    )
    return output

def configSuccess():
    print(r'...Success!' + '\n')

#   --PROMPT USER FOR DEVICE INFO--
# -check if user needs to be prompted for info
if os.path.exists('userDeviceInfo.json') == False:
    promptDeviceInfo()

# -otherwise, read info from userDeviceInfo.json
else:
    with open('userDeviceInfo.json', 'r') as file:
        userDeviceInfo = json.load(file)
    
    monitorNumber = userDeviceInfo['monitorNumber']
    camera6MAC = userDeviceInfo['camera6MAC']
    camera8MAC = userDeviceInfo['camera8MAC']
    ephone1MAC = userDeviceInfo['ephone1MAC']
    ephone2MAC = userDeviceInfo['ephone2MAC']
    
    needReInput = evalInfo()
    promptValid = bool(re.search(regexYesNo, needReInput))
    
    while promptValid == False:
        print(Back.RED + '-INPUT INVALID-')
        needReInput = evalInfo()
        promptValid = bool(re.search(regexYesNo, needReInput))
    else:
        isNo = bool(re.search(regexNo, needReInput))
        if isNo:
            promptDeviceInfo()
            
#   --OBTAIN DEVICE INFO--
with open('deviceInfo.json', 'r') as file:
    deviceInfo = json.load(file)

# -parse values from deviceInfo.json
coreBabaDevice = deviceInfo['coreBaba']
callManagerDevice = deviceInfo['callManager']
edgeRouterDevice = deviceInfo['edgeRouter']

# -test connection
def testConnection():
    accessCLI = ConnectHandler(**coreBaba)
    sh_ip = accessCLI.send_command('sh ip int br')
    print(sh_ip)

#   --OBTAIN DEVICE CONFIGS--
with open('deviceConfigs.json', 'r') as file:
    deviceConfigs = json.load(file)

# -replace underscores(_) in json file with monitorNumber
for primKey in deviceConfigs:
    for innerKey in deviceConfigs[primKey]:
        mValue = deviceConfigs[primKey][innerKey]
        updateValue = re.sub(r'_', '69', mValue)
        
        if innerKey != 'cam6_mac' and innerKey != 'cam8_mac' and innerKey != 'phone1_mac' and innerKey != 'phone2_mac':
            deviceConfigs[primKey][innerKey] = updateValue
        elif innerKey == 'cam6_mac':
            deviceConfigs[primKey][innerKey] = camera6MAC
        elif innerKey == 'cam8_mac':
            deviceConfigs[primKey][innerKey] = camera8MAC
        elif innerKey == 'phone1_mac':
            deviceConfigs[primKey][innerKey] = ephone1MAC
        elif innerKey == 'phone2_mac':
            deviceConfigs[primKey][innerKey] = ephone2MAC   
            

#parse values from primary keys from deviceConfigs.json
monitorList = deviceConfigs['class_m']
ip = deviceConfigs['ip_mask']
ospf = deviceConfigs['ospf_1']
coreBaba = deviceConfigs['cbaba_set']
callMan = deviceConfigs['cucm_set']
edge = deviceConfigs['edge_set']
dhcp = deviceConfigs['dhcp']
swPort = deviceConfigs['sw_port']
analog = deviceConfigs['dial_peer']
tele = deviceConfigs['vo_ip']

#   --DEVICE CONFIGURATIONS--
#-------------------------------CORE BABA
# -apply IP addresses
configIPs = [
    #console access
    'line cons 0',
    f'password {coreBaba["cons0_pass"]}',
    'login',
    'exec-timeout 0 0',
    'exit',
    
    #interface IPs
    'int gi 0/1',
    'no shut',
    'no switchport',
    f'ip add {coreBaba["g01_ip"]} {ip["mask_24"]}',
    'exit',
    'int vlan 10',
    'no shut',
    f'ip add {coreBaba["v10_ip"]} {ip["mask_24"]}',
    f'desc mgmtWifi-{coreBaba["description"]}n',
    'exit',
    'int vlan 50',
    'no shut',
    f'ip add {coreBaba["v50_ip"]} {ip["mask_24"]}',
    f'desc mgmtCCTV-{coreBaba["description"]}',
    'exit',
    'int vlan 100',
    'no shut',
    f'ip add {coreBaba["v100_ip"]} {ip["mask_24"]}',
    f'desc mgmtVOICE-{coreBaba["description"]}',
    'exit'
]

# -configure dhcp
configDHCP = [
    #reserve ips
    f'ip dhcp excluded-add {dhcp["reserve_ip_v1"]}',
    f'ip dhcp excluded-add {dhcp["reserve_ip_v10"]}',
    f'ip dhcp excluded-add {dhcp["reserve_ip_v50"]}',
    f'ip dhcp excluded-add {dhcp["reserve_ip_v100"]}',
    
    #dhcp pool
    f'ip dhcp pool {dhcp["data_pool"]}',
    f'network {dhcp["data_net"]} {ip["mask_24"]}',
    f'default-router {dhcp["data_gateway"]}',
    f'domain-name {dhcp["data_domain"]}',
    f'dns-server {dhcp["dns"]}',
    'exit',
    
    f'ip dhcp pool {dhcp["wifi_pool"]}',
    f'network {dhcp["wifi_net"]} {ip["mask_24"]}',
    f'default-router {dhcp["wifi_gateway"]}',
    f'domain-name {dhcp["wifi_domain"]}',
    f'dns-server {dhcp["dns"]}',
    'exit',
    
    f'ip dhcp pool {dhcp["cctv_pool"]}',
    f'network {dhcp["cctv_net"]} {ip["mask_24"]}',
    f'default-router {dhcp["cctv_gateway"]}',
    f'domain-name {dhcp["cctv_domain"]}',
    f'dns-server {dhcp["dns"]}',
    'exit',
    
    f'ip dhcp pool {dhcp["voice_pool"]}',
    f'network {dhcp["voice_net"]} {ip["mask_24"]}',
    f'default-router {dhcp["voice_gateway"]}',
    f'domain-name {dhcp["voice_domain"]}',
    f'dns-server {dhcp["dns"]}',
    f'option 150 ip {tele["source_add"]}',
    'exit'
]

# -switchport
configPorts = [
    #create vlans
    'vlan 1',
    f'name {coreBaba["v1_name"]}',
    'exit',
    'vlan 10',
    f'name {coreBaba["v10_name"]}',
    'exit',
    'vlan 50',
    f'name {coreBaba["v50_name"]}',
    'exit',
    'vlan 100',
    f'name {coreBaba["v100_name"]}',
    'exit',
    
    #access/voice port
    'int fa 0/2',
    'switchport mode access',
    f'switchport access {swPort["fa2_ac_vlan"]}',
    'exit',
    'int fa 0/4',
    'switchport mode access',
    f'switchport access {swPort["fa4_ac_vlan"]}',
    'exit',
    'int fa 0/6',
    'switchport mode access',
    f'switchport access {swPort["fa6_ac_vlan"]}',
    'exit',
    'int fa 0/8',
    'switchport mode access',
    f'switchport access {swPort["fa8_ac_vlan"]}',
    'exit',
    'int fa 0/3',
    'switchport mode access',
    f'switchport access {swPort["fa3_ac_vlan"]}',
    'exit',
    'int fa 0/5',
    'switchport mode access',
    f'switchport voice {swPort["fa5_vo_vlan"]}',
    f'switchport access {swPort["fa5_ac_vlan"]}',
    f'{swPort["qos_ephone"]}',
    'exit',
    'int fa 0/7',
    'switchport mode access',
    f'switchport voice {swPort["fa7_vo_vlan"]}',
    f'switchport access {swPort["fa7_ac_vlan"]}',
    f'{swPort["qos_ephone"]}',
    'exit'
]

# -specify device ip
configCameras = [
    f'ip dhcp pool {dhcp["cam6_pool"]}',
    f'host {dhcp["cam6_ip"]} {ip["mask_24"]}',
    f'client-identifier {dhcp["cam6_mac"]}',
    'exit',
    f'ip dhcp pool {dhcp["cam8_pool"]}',
    f'host {dhcp["cam8_ip"]} {ip["mask_24"]}',
    f'client-identifier {dhcp["cam8_mac"]}',
    'exit'
]

# -set default route
configDefaultRoute = [
    f'ip route 0.0.0.0 0.0.0.0 {coreBaba["gateway"]} 120'
]

# -set ospf
configOSPFBABA = [
    f'router ospf {ospf["proc_id"]}',
    f'router-id {ospf["cbaba_id"]}',
    f'network {ospf["cbaba_route_1"]} {ip["wild_16"]} {ospf["area"]}',
    'exit',
    'int gi 0/1',
    f'ip ospf network {ospf["p2p"]}',
    'exit'
]

#-------------------------------CALL MANAGER
# -console access
configCUCMConsole = [
    'line cons 0',
    f'password {callMan["cons0_pass"]}',
    'login',
    'exec-timeout 0 0',
    'exit'
]

# -configure analog phones
configAnalog = [
    'dial-peer voice 1 pots',
    f'destination-pattern {analog["vo_pat_000"]}',
    'port 0/0/0',
    'dial-peer voice 2 pots',
    f'destination-pattern {analog["vo_pat_001"]}',
    'port 0/0/1',
    'dial-peer voice 3 pots',
    f'destination-pattern {analog["vo_pat_002"]}',
    'port 0/0/2',
    'dial-peer voice 4 pots',
    f'destination-pattern {analog["vo_pat_003"]}',
    'port 0/0/3',
    'exit'
]

# -configure ephones
configEphone = [
    'no telephony-service',
    'telephony-service',
    'no auto assign',
    'no auto-reg-ephone',
    'max-ephones 5',
    'max-dn 20',
    f'ip source-address {tele["source_add"]} port 2000',
    'create cnf-files',
    'ephone-dn 1',
    f'number {tele["dn_1"]}',
    'ephone-dn 2',
    f'number {tele["dn_2"]}',
    'ephone-dn 3',
    f'number {tele["dn_3"]}',
    'ephone-dn 4',
    f'number {tele["dn_4"]}',
    'ephone-dn 5',
    f'number {tele["dn_5"]}',
    'ephone-dn 6',
    f'number {tele["dn_6"]}',
    'ephone-dn 7',
    f'number {tele["dn_7"]}',
    'ephone-dn 8',
    f'number {tele["dn_8"]}',
    'ephone 1',
    f'mac-address {tele["phone1_mac"]}',
    f'type {tele["type"]}',
    f'button {tele["e1_btn"]}',
    'restart',
    'ephone 2',
    f'mac-address {tele["phone2_mac"]}',
    f'type {tele["type"]}',
    f'button {tele["e2_btn"]}',
    'restart',
    'end'
]

# -allow video calls
configVideo = [
    'ephone 1',
    'video',
    'voice service voip',
    f'{tele["vid_prot"]}',
    'call start slow',
    'ephone 2',
    'video',
    'voice service voip',
    f'{tele["vid_prot"]}',
    'call start slow',
    'exit'
]

# -allow incoming calls
configIncoming = [
    'voice service voip',
    'ip address trusted list',
    'ipv4 0.0.0.0 0.0.0.0',
    'exit'
]

# -allow outgoing calls
callers = f'{monitorList["monitors_occupied"]}'
list_of_callers = callers.split(",")
outgoingConfig = []
for i in list_of_callers:
    out_per_user = [
        f'dial-peer voice {i} Voip',
        f'destination-pattern {i}..',
        f'session target ipv4:10.{i}.100.4',
        f'codec g711ULAW',
        'exit'
    ]
    outgoingConfig.append(out_per_user)

# -configure ivrs
configIVRS = [
    f'dial-peer voice {tele["ivrs_peer"]} voip',
    'service rivanaa out-bound',
    f'destination-pattern {tele["ivrs_pat"]}',
    f'session target ipv4:{tele["source_add"]}',
    f'incoming called-number {tele["ivrs_pat"]}',
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
    f'param aa-hunt1 {tele["hunt1"]}',
    f'param aa-hunt2 {tele["hunt2"]}',
    f'param aa-hunt3 {tele["hunt3"]}',
    f'param aa-hunt4 {tele["hunt4"]}',
    'param queue-manager-debugs 1',
    'param number-of-hunt-grps 4',
    'exit'
]

# -set ospf
configOSPFCUCM = [
    f'router ospf {ospf["proc_id"]}',
    f'router-id {ospf["cucm_id"]}',
    f'network {ospf["cucm_route_1"]} {ip["wild_24"]} {ospf["area"]}',
    'exit'
]

#-------------------------------EDGE ROUTER
# -apply IP addresses
configIPsEDGE = [
    #console access
    'line cons 0',
    f'password {edge["cons0_pass"]}',
    'login',
    'exec-timeout 0 0',
    'exit',
    
    #interface ips
    'int gi 0/0/1',
    'no shut',
    f'ip add {edge["g001_ip"]} {ip["mask_24"]}',
    'desc OUTSIDE',
    'exit',
    'int loopback 0',
    'no shut',
    f'ip add {edge["lo0_ip"]} {ip["mask_32"]}',
    'desc VIRTUALIP',
    'exit'
]

# -static route inside lan
configLANStaticRoute = [
    'ip routing',
    f'ip route {edge["lan_route"]} {ip["mask_16"]} {edge["lan_gateway"]} 120'
]

# -static route to other pcs
configStatic = []
for i in list_of_callers:
    static_route_class = [
        f'ip route 10.{i}.0.0 255.255.0.0 200.0.0.{i} 120',
    ]
    configStatic.append(static_route_class)

# -set ospf
configOSPFEDGE = [
    f'router ospf {ospf["proc_id"]}',
    f'router-id {ospf["edge_id"]}',
    f'network {ospf["edge_route_1"]} {ip["wild_24"]} {ospf["area"]}',
    f'network {ospf["edge_route_2"]} {ip["wild_24"]} {ospf["area"]}',
    f'network {ospf["edge_route_3"]} {ip["wild_32"]} {ospf["area"]}',
    'exit',
    'int gi 0/0/0',
    f'ip ospf network {ospf["p2p"]}',
    'exit'
]


#   --PUSH CONFIGURATIONS--
print(r' ')

#   --COREBABA
print(r'@----- Connecting to COREBABA')
accessCLI = ConnectHandler(**coreBabaDevice)

# -apply configurations to coreBABA
print(r'Applying IP addresses...')
accessCLI.send_config_set(configIPs)
configSuccess()

print(r'Configuring DHCP...')
accessCLI.send_config_set(configDHCP)
configSuccess()

print(r'Configuring Switchport...')
accessCLI.send_config_set(configPorts)
configSuccess()

print(r'Reserving Camera IPs...')
accessCLI.send_config_set(configCameras)
configSuccess()

print(r'Configuring OSPF...')
accessCLI.send_config_set(configOSPFBABA)
configSuccess()

accessCLI.disconnect
print(r'-----@ Configurations for COREBABA is Successful!!!' + '\n')

#   --CALL MANAGER
print(r'@----- Connecting to CALLMANAGER')
accessCLI = ConnectHandler(**callManagerDevice)

# -apply configurations to callManager
print(r'Configuring Console Connection...')
accessCLI.send_config_set(configCUCMConsole)
configSuccess()

print(r'Configuring Analog Phones...')
accessCLI.send_config_set(configAnalog)
configSuccess()

for i in range(1,3):
    print(r'Configuring Ephones ' + str(i) + '/2')
    accessCLI.send_config_set(configEphone)
configSuccess()

print(r'Configuring Video Calls...')
accessCLI.send_config_set(configVideo)
configSuccess()

print(r'Allowing Incoming Calls...')
accessCLI.send_config_set(configIncoming)
configSuccess()

print(r'Allowing Outgoing Calls...')
for i in outgoingConfig:
    accessCLI.send_config_set(i)
configSuccess()

print(r'Configuring IVRS...')
accessCLI.send_config_set(configIVRS)
configSuccess()

print(r'Configuring OSPF...')
accessCLI.send_config_set(configOSPFCUCM)
configSuccess()

accessCLI.disconnect
print(r'-----@ Configurations for CALLMANAGER is Successful!!!' + '\n')

#   --EDGE ROUTER
print(r'@----- Connecting to EDGEROUTER')
accessCLI = ConnectHandler(**edgeRouterDevice)

# -apply configurations to edgeRouter
print(r'Applying IP addresses...')
accessCLI.send_config_set(configIPsEDGE)
configSuccess()

print(r'Configuring Static Routes...')
accessCLI.send_config_set(configLANStaticRoute)
configSuccess()

print(r'Configuring Static Routes to other PCs...')
accessCLI.send_config_set(configStatic)
configSuccess()

print(r'Configuring OSPF...')
accessCLI.send_config_set(configOSPFEDGE)
configSuccess()

accessCLI.disconnect
print(r'-----@ Configurations for EDGEROUTER is Successful!!!' + '\n')

print(r'@----- Finishing configurations' + '\n')
accessCLI = ConnectHandler(**callManagerDevice)

for i in range(1,3):
    print(r'Forcing ephone numbers to appear ' + str(i) + '/2')
    accessCLI.send_config_set(configEphone)

accessCLI.disconnect
print(r'-----@ Configurations Complete!!!' + '\n')

