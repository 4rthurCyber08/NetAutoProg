import json
import netmiko
from netmiko import ConnectHandler

#remove pythonLab/
#open the json file ("netLoop.json") in read only mode ("r") and set it as a variable (netLoop)
    #using 'with open' command will auto close the json file so no need for the close() command
with open("netLoop.json", "r") as netLoop:
    #convert the json file to a python dictionary
    jsonConfig = json.load(netLoop)
    
#breakdown the key:value of the converted json into separate variables
device_info = jsonConfig["device"]
loopback1 = jsonConfig["loopback1_config"]
loopback2 = jsonConfig["loopback2_config"]
new_hostname = jsonConfig['new_hostname']
internet = jsonConfig["net_config"]
set = jsonConfig["line_and_ip"]

#connect to the host
accessCli = ConnectHandler(**device_info)

#enters the enable command to go from privilege 1 to privilege 15
#   Router>enable
#   Router#
accessCli.enable

#create commands using the format string to match key:values in the json file
commands = [
    f"hostname {new_hostname}",
    f"int {loopback1['interface']}",
    f"ip add {loopback1['new_ip']} {set['subnet_mask']}",
    f"desc {set['desc']}",
    f"{set['turn_on']}",
    f"{set['ex']}",
    f"int {loopback2['interface']}",
    f"ip add {loopback2['new_ip']} {set['subnet_mask']}",
    f"desc {set['desc']}",
    f"{set['turn_on']}",
    f"{set['ex']}",
    f"ip route {internet['default']} {internet['default']} {internet['gateway']}"
]

#excecute commands to the host
finalOutput = accessCli.send_config_set(commands)
#print(finalOutput)

#test internet connection
pingNET = accessCli.send_command("ping 8.8.8.8")
#print(pingNET)

#logout from host
accessCli.disconnect