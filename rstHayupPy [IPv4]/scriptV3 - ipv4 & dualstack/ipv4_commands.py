from json import load

# read json file
with open('pre_config.json') as file:
    # convert json data types to python data types
    json_configs = load(file)

# parse device configs
dhcp = json_configs['dhcp_config']
ip = json_configs['i_protocol']
eigrp = json_configs['eigrp_config']
ospf = json_configs['ospf_config']
bgp = json_configs['bgp_config']
p2_config = json_configs['p2_config']
p1_config = json_configs['p1_config']
a2_config = json_configs['a2_config']
a1_config = json_configs['a1_config']
d2_config = json_configs['d2_config']
d1_config = json_configs['d1_config']
s1_config = json_configs['s1_config']
s2_config = json_configs['s2_config']
r4_config = json_configs['r4_config']
r3_config = json_configs['r3_config']
r2_config = json_configs['r2_config']
r1_config = json_configs['r1_config']
i1_config = json_configs['i1_config']
i2_config = json_configs['i2_config']
i3_config = json_configs['i3_config']
i4_config = json_configs['i4_config']

# commands to be pushed to cli
i1_commands = [
    f'Hostname {i1_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i1_config["lo0"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_45"]}',
    f'bgp router-id {i1_config["lo0"]}',
    'bgp log-neighbor-changes',
    f'{i1_config["neigh_45"]}',
    f'{i1_config["neigh_24"]}',
    f'{i1_config["neigh_208"]}',
    f'{bgp["ipv4_fam"]}',
    f'{i1_config["neigh_45_on"]}',
    f'{i1_config["neigh_24_on"]}',
    f'{i1_config["neigh_208_on"]}',
    f'network {i1_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_45"]} mask {ip["mask_24"]}',
    f'network {bgp["net_24"]} mask {ip["mask_24"]}',
    f'network {bgp["net_208"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    'exit',
    'exit',
    
    # fake internet
    f'ip route {bgp["fake_net"]} 208.8.8.1',
    f'ip route {ip["def_route"]} null 0'
]

i2_commands = [
    f'hostname {i2_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i2_config["lo0"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_2"]}',
    f'bgp router-id {i2_config["lo0"]}',
    'bgp log-neighbor-changes',
    f'{i2_config["neigh_32"]}',
    f'{i2_config["neigh_25"]}',
    f'{i2_config["neigh_24"]}',
    f'{i2_config["neigh_207"]}',
    f'{bgp["ipv4_fam"]}',
    f'{i2_config["neigh_32_on"]}',
    f'{i2_config["neigh_25_on"]}',
    f'{i2_config["neigh_24_on"]}',
    f'{i2_config["neigh_207_on"]}',
    f'network {i2_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_32"]} mask {ip["mask_24"]}',
    f'network {bgp["net_25"]} mask {ip["mask_24"]}',
    f'network {bgp["net_24"]} mask {ip["mask_24"]}',
    f'network {bgp["net_207"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    'exit',
    'exit',
    
    # fake internet
    f'ip route {bgp["fake_net"]} 207.7.7.1',
    f'ip route {ip["def_route"]} null 0'
]

i3_commands = [
    f'hostname {i3_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i3_config["lo0"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_3"]}',
    f'bgp router-id {i3_config["lo0"]}',
    'bgp log-neighbor-changes',
    f'{i3_config["neigh_35"]}',
    f'{i3_config["neigh_32"]}',
    f'{i3_config["neigh_209"]}',
    f'{bgp["ipv4_fam"]}',
    f'{i3_config["neigh_35_on"]}',
    f'{i3_config["neigh_32_on"]}',
    f'{i3_config["neigh_209_on"]}',
    f'network {i3_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_35"]} mask {ip["mask_24"]}',
    f'network {bgp["net_32"]} mask {ip["mask_24"]}',
    f'network {bgp["net_209"]} mask {ip["mask_24"]}',
    f'network {bgp["net_0"]}',
    'exit',
    'exit',
    
    # fake internet
    f'ip route {bgp["fake_net"]} 207.9.9.1',
    f'ip route {ip["def_route"]} null 0'
]

i4_commands = [
    f'hostname {i4_config["hostname"]}',
    'interface loopback 0',
    f'ip address {i4_config["lo0"]} {ip["mask_32"]}',
    'exit',
    
    # bgp config
    f'router {bgp["as_45"]}',
    f'bgp router-id {i4_config["lo0"]}',
    'bgp log-neighbor-changes',
    f'{i4_config["neigh_35"]}',
    f'{i4_config["neigh_25"]}',
    f'{i4_config["neigh_45"]}',
    f'{bgp["ipv4_fam"]}',
    f'{i4_config["neigh_35_on"]}',
    f'{i4_config["neigh_25_on"]}',
    f'{i4_config["neigh_45_on"]}',
    f'network {i4_config["google"]} mask {ip["mask_32"]}',
    f'network {i4_config["lo0"]} mask {ip["mask_32"]}',
    f'network {bgp["net_35"]} mask {ip["mask_24"]}',
    f'network {bgp["net_25"]} mask {ip["mask_24"]}',
    f'network {bgp["net_45"]} mask {ip["mask_24"]}',
    'exit',
    'exit',
    
    # fake google
    'interface loopback 8',
    f'ip address {i4_config["google"]} {ip["mask_32"]}',
    f'description Google',
    'exit'
]

r1_commands = [
    f'hostname {r1_config["hostname"]}',
    
    'interface loopback 1',
    f'ip address {r1_config["r_id"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    'exit',
    
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
    f'{r1_config["neigh_209_on"]}',
    f'{r1_config["neigh_207_on"]}',
    f'{r1_config["neigh_208_on"]}',
    f'network {r1_config["r_id"]} mask {ip["mask_32"]}',
    f'network {bgp["net_209"]} mask {ip["mask_24"]}',
    f'network {bgp["net_207"]} mask {ip["mask_24"]}',
    f'network {bgp["net_208"]} mask {ip["mask_24"]}',
    f'network {bgp["net_10"]} mask {ip["mask_30"]}',
    'exit',
    'exit'
]

r2_commands = [
    f'hostname {r2_config["hostname"]}',
    
    'interface loopback 2',
    f'ip address {r2_config["r_id"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    # ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r2_config["r_id"]}',
    f'network {ospf["net_1_4"]}',
    f'network {ospf["net_1_0"]}',
    f'network {r2_config["r_id"]} 0.0.0.0 area 0',
    'exit'
]

r3_commands = [
    f'hostname {r3_config["hostname"]}',
    
    'interface loopback 3',
    f'ip address {r3_config["r_id"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
    # ospf config
    f'router ospf {ospf["process_id"]}',
    f'router-id {r3_config["r_id"]}',
    f'network {ospf["net_1_8"]}',
    f'network {ospf["net_1_4"]}',
    f'network {r3_config["r_id"]} 0.0.0.0 area 0',
    'exit'
]
r4_commands = [
    f'hostname {r4_config["hostname"]}',
    
    'interface loopback 4',
    f'ip address {r4_config["r_id"]} {ip["mask_32"]}',
    f'description {ip["int_desc"]}',
    
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
    'exit'
]

a1_commands = [
    f'hostname {a1_config["hostname"]}',
    'interface ethernet 0/0',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    
    f'ip route {ip["def_route"]} {ip["def_129"]} 1',
    f'ip route {ip["def_route"]} {ip["def_130"]} 2',
    'exit'
]

a2_commands = [
    f'hostname {a2_config["hostname"]}',
    'interface ethernet 1/0',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    
    f'ip route {ip["def_route"]} {ip["def_130"]} 1',
    f'ip route {ip["def_route"]} {ip["def_129"]} 2',
    'exit'
]

s1_commands = [
    f'hostname {s1_config["hostname"]}',
    
    'interface e1/0',
    'no shutdown',
    f'ip add {s1_config["int_1_0"]} {ip["mask_27"]}',
    'exit',
    
    f'ip route {ip["def_route"]} {s1_config["gateway_1"]}',
    f'ip route {ip["def_route"]} {s1_config["gateway_2"]} 2'
]

s2_commands = [
    f'hostname {s2_config["hostname"]}',
    
    'interface e1/0',
    'no shutdown',
    f'ip add {s2_config["int_1_0"]} {ip["mask_24"]}',
    'exit',
    
    f'ip route {ip["def_route"]} {s2_config["gateway_1"]}',
    f'ip route {ip["def_route"]} {s2_config["gateway_2"]} 2'
]

p1_commands = [
    f'hostname {p1_config["hostname"]}',
    
    f'ip route {ip["def_route"]} {ip["def_1_1"]} 1',
    f'ip route {ip["def_route"]} {ip["def_1_2"]} 2',
    
    'interface ethernet 0/0',
    'ip add 10.2.1.111 255.255.255.0',
    'exit'
]

p2_commands = [
    f'hostname {p2_config["hostname"]}',
    
    f'ip route {ip["def_route"]} {ip["def_1_2"]} 1',
    f'ip route {ip["def_route"]} {ip["def_1_1"]} 2',
    'interface ethernet 1/0',
    'ip add 10.2.1.222 255.255.255.0',
    'exit'
]