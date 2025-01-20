
==========================================

Find and Replace ( ctrl + h ): 

	replaceMe = Your monitor number

Replace all ( ctrl + alt + enter)

==========================================




=====| STEP 1 - Add routing to PC

@command prompt
route add 10.0.0.0 mask 255.0.0.0 10.replaceMe.1.4
route add 200.0.0.0 mask 255.255.255.0 10.replaceMe.1.4


=====| STEP 2 - Add ip address and routing to device

@coreBaba
conf t
 int vlan 1
  no shut
  ip add 10.replaceMe.1.4 255.255.255.0
  desc mgmtData-configuredManually
  exit
 vlan 100
  name VOICEVLAN
  exit
 int vlan 100
  no shut
  ip add 10.replaceMe.100.4 255.255.255.0
  desc vlanMgmtVoice-configuredManually
  exit
 int fa 0/3
  sw mo ac
  sw ac vlan 100
  exit
 int gi0/1
  no switchport
  no shut 
  ip add 10.replaceMe.replaceMe.4 255.255.255.0
  exit
 ip routing
 ip route 0.0.0.0 0.0.0.0 10.replaceMe.replaceMe.1 120
 enable secret pass
 line vty 0 14
  password pass
  transport input all
  login
  exec-timeout 0 0
  exit

@cucm
conf t
 int fa0/0
  no shut
  ip add 10.replaceMe.100.8 255.255.255.0
  exit
 ip routing
 ip route 0.0.0.0 0.0.0.0 10.replaceMe.100.4 120
 enable secret pass
 line vty 0 14
  password pass
  transport input all
  login
  exec-timeout 0 0
  exit

@edge
conf t
 int gi 0/0/0
  ip add 10.replaceMe.replaceMe.1 255.255.255.0
  no shut
  exit
 ip routing
 ip route 10.replaceMe.0.0 255.255.0.0 10.replaceMe.replaceMe.4 120
 enable secret pass
 line vty 0 14
  password pass
  transport input all
  login
  exec-timeout 0 0
  exit

=====| Step 3 - Note MAC Addresses

Open _note_mac_add.txt

=====| Step 4 - Run main.py


=====| Enable SSH

For an SSH connection to be established, the device must have:
    -a non-default hostname         [hostname coreBabareplaceMe]
    -a domain name                  [ip domain name day1lab.com]
    -a local user account           [username admin privilege 15 secret pass]
    -generated crypto keys          [crypto key generate rsa modulus 1024]
    -SSH enabled                    [ip ssh version 2]
    -enable remote access           [transport input all]
    -enable remote user/pass login  [login local]

Extra lines
    -password encryption            [service password-encryption]
    -no logs                        [no logging console]
    -no domain lookups              [no ip domain-lookup]
    -no timeout                     [exec-timeout 0 0]

@coreBaba
conf t
 hostname coreBaba-replaceMe
 service password-encryption
 no logging console
 no ip domain-lookup
 ip domain name autoday1.com
 username admin privilege 15 secret pass
 line vty 0 14
  transport input all
  login local
  exec-timeout 0 0
  exit
 crypto key generate rsa
    !How many bits in the modulus [512]: --> 1024
 ip ssh version 2

@cucm
conf t
 hostname cucm-replaceMe
 service password-encryption
 no logging console
 no ip domain-lookup
 ip domain name autoday1.com
 username admin privilege 15 secret pass
 line vty 0 14
  transport input all
  login local
  exec-timeout 0 0
 crypto key generate rsa modulus 1024
 ip ssh version 2

@edge
conf t
 hostname edge-replaceMe
 service password-encryption
 no logging console
 no ip domain-lookup
 ip domain name autoday1.com
 username admin privilege 15 secret pass
 line vty 0 14
  transport input all
  login local
  exec-timeout 0 0
 crypto key generate rsa modulus 1024
 ip ssh version 2