import re


regex_mac = r"^[a-fA-F0-9]{4}\.[a-fA-F0-9]{4}\.[a-fA-F0-9]{4}$"

ephone_1_mac = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
mac_is_valid = bool(re.search(regex_mac, ephone_1_mac))

while mac_is_valid == False:
    print(r'INVALID MAC ADDRESS')
    print(r'Use the format: xxxx.xxxx.xxxx')
    ephone_1_mac = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
    mac_is_valid = bool(re.search(regex_mac, ephone_1_mac))
    
ephone_2_mac = input(r'What is the MAC ADDRESS of your ephone 2? (Use the format: xxxx.xxxx.xxxx): ')
mac_is_valid2 = bool(re.search(regex_mac, ephone_2_mac))

while mac_is_valid2 == False:
    print(r'INVALID MAC ADDRESS')
    print(r'Use the format: xxxx.xxxx.xxxx')
    ephone_1_mac = input(r'What is the MAC ADDRESS of your ephone 1? (Use the format: xxxx.xxxx.xxxx): ')
    mac_is_valid2 = bool(re.search(regex_mac, ephone_2_mac))
