import netmiko
import getpass

## Config ##
# 2 options for how to connect to a switch in the estate
# Option 1 - Local creds
#ssh_user = 'xxxxxxx'
#ssh_pass = 'XXXX'
# Option 2 - AAA Creds
ssh_user = input(str("Enter username: "))
ssh_pass = getpass.getpass(prompt="Password for '" + ssh_user + "': ")

##Taking switch and switchport from user
def main():
    print("\n==============================================")
    switch_hostname = input(str("Enter the switch hostname: "))
    switchport = input("Enter the switchport: ")
    ##Connecting to switch, catching errors and starting the script again
    try:
        device = {
            "device_type": 'cisco_asa',
            "host": switch_hostname,
            "username": ssh_user,
            "password": ssh_pass,
            "secret": ssh_pass,
            }
        net_connect = netmiko.ConnectHandler(**device)
    except:
        print("Failed to connect! Check you entered your creds correctly & entered the hostname correctly")
        main()
    interface_checks(net_connect,switchport,switch_hostname)

def interface_checks(net_connect,switchport,switch_hostname):
    ##Show interface status
    print("\nInterface status\n")
    int_status = net_connect.send_command("sho int status | i "+ switchport)
    print(int_status)
    if "connected" in int_status.lower():
        print("\nSwitchport is connected! Not proceeding with shutting the switchport!\n")
        mac_table = net_connect.send_command("sho mac address-table interface "+ switchport)
        print("Following MAC Address(es) being learnt on this switchport, investigate these:")
        print(mac_table)
        main()
    else:
        print("\nSwitchport is not live! Continuing script\n")

    ##Grabbing the config from the switchport
    config_for_removal = []
    ignored_config = ['end', '']
    current_config = net_connect.send_command("sho run int "+ switchport)
    print("Current Interface Configuration:\n")
    current_config = current_config.split("\n")
    current_config = current_config[4:]
    for i in current_config:
        if i in ignored_config:
            continue
        else:
            print(i)
            config_for_removal.append(i)
    config_removal(net_connect,switchport,config_for_removal,switch_hostname)

def config_removal(net_connect,switchport,config_for_removal,switch_hostname):
    print("\nUse following config to clear and shutdown switchport:\n")
    print("If there is no config displayed except the interface then there is no config to remove")
    print("\nSwitch Hostname: ", switch)
    ignored_config = [' shutdown', ' no cdp enable']
    for i in config_for_removal:
        if i in ignored_config:
            continue
        elif 'interface' in i:
            print(i)
        else:
            print("no", i)
    main()

main()
