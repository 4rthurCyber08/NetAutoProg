import netmiko
from netmiko import ConnectHandler

#literally 'connect the handler(this python file)' to the device's cli with user privilege 15 access
accessCli = ConnectHandler(
    device_type = "cisco_ios",
    host = "192.168.102.5",
    port = 22,
    username = "admin",
    password = "pass"
)

#send_command : sends a single command in PRIVILEGED MODE
#   Router#sh ip int br
ipSample01 = accessCli.send_command("sh ip int br")
#print(ipSamples01)

#send_config_set : sends a command/s in GLOBAL CONFIGURATION MODE
#   Router(config)#do sh ip int br
#   Router(config)#do sh ip prot
ipSample02 = accessCli.send_config_set(["do sh ip int br", "do sh ip prot"])
#print(ipSample02)

#add IP to gi 1 & 2
addIP = [
    "hostname pythonOnly",
    "int gi 1",
    "ip add 192.168.108.5 255.255.255.0",
    "no shut",
    "desc configured from python",
    "exit",
    "int gi 3",
    "ip add 192.168.103.5 255.255.255.0",
    "no shut",
    "desc configured from python"
]
ipOutput = accessCli.send_config_set(addIP)
print(ipOutput)

descOutput = accessCli.send_command("sh int desc")
#print(descOutput)

#logout from host
accessCli.disconnect
