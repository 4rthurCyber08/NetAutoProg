import netmiko
from netmiko import ConnectHandler

monitorNumber = input(r'What is your monitor number? ')

deviceInfo = {
    'device_type': 'cisco_ios',
    'host': '10.' + monitorNumber + '.100.8',
    'port': 22,
    'username': 'admin',
    'password': 'pass',
    'secret': 'pass'
}

#activate IVRS
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
    'end'
]

#connect to the specified device  
accessCLI = ConnectHandler(**deviceInfo)

#sh_ip_int_br = accessCLI.send_command('sh ip int br')
#print(sh_ip_int_br)

#apply configurations
print(r'Configuring IVRS...')
output = accessCLI.send_config_set(configIVRS)
print(r'...Success!' + '\n')

print(r'Configurations Successful!!!')
print(output)

#disconnect from device
accessCLI.disconnect

input(r'Press Enter to close terminal.')