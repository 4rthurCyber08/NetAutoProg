import netmiko
import textfsm
import json
import re
from netmiko import ConnectHandler

with open('netLoop.json', 'r') as file:
    jsonConfig = json.load(file)

device_info = jsonConfig['device']
loopback1 = jsonConfig['loopback1_config']
loopback2 = jsonConfig['loopback2_config']
new_hostname = jsonConfig['new_hostname']
internet = jsonConfig['net_config']
set = jsonConfig['line_and_ip']

accessCli = ConnectHandler(**device_info)
sh_ip = accessCli.send_command('sh ip int br', use_textfsm=True)
#print(type(sh_ip))

#create then open the json file
with open('sh_ip_int_br.json', 'w') as blankFile:
    
    #convert the object type into str in order to write it into json
    content = json.dumps(sh_ip, indent=2)
    #write the content into the json file
    blankFile.write(content)


##Experiment with python reading specefic lines of a json file##
#read the json file and iterate through its contents
with open('sh_ip_int_br.json', 'r') as readFile:
    
    #make python read through the json file, then output as specific ip address: 192.168.102.5
    readContent = json.load(readFile)
    for i in readContent:
        ints = i['ip_address']
        
        #specify a string that ends with 2.5
        regex = r'2.5$'
        output = re.search(regex, ints)
        if output:
            print(ints)
        
accessCli.disconnect