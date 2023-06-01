import getpass
import netmiko

print(r"""
             _                       _
          (\/ )        _  _         ( \/)
           \  |       ( \/ )        |  /
            ) |        \  /         | (
           /  \         \/         /   \
         ,-    \       /  \       /    -,
        /6 6    \     / _  \     /     a a
     &/(_x_ ),_/`)   / 6 6  \   (`\_,( _x_)-/}
               `  `-'>(_x_)< `-' `
      What does the networking seal say?
      
                  ARP ARP ARP

        """)

ssh_user = input(str("Enter TACACS username: "))
ssh_pass = getpass.getpass(prompt="Password for '" + ssh_user + "': ")

def main():
    print("\n==============================================")
    hostname = input(str("Enter the firewall hostname: "))
    server_ip = input(str("Server IP: "))
    try:
        device = {
                "device_type": 'cisco_asa',
                "host": hostname,
                "username": ssh_user,
                "password": ssh_pass,
                "secret": ssh_pass,
                }
        net_connect = netmiko.ConnectHandler(**device)
    except:
        print("Failed to connect! Check you entered your creds correctly & entered the hostname correctly")
        main()
    check_arp(net_connect,server_ip)

def check_arp(net_connect,server_ip):
    print("+--------------------------------------------------------------------+")
    print("|                   Checking for ARP's on the fw                     |")
    print("+--------------------------------------------------------------------+")
    print("Below ARPs have been found for the provided IP: \n")
    arp = net_connect.send_config_set("sho arp | i " + server_ip)
    arp_record = arp.split('\n')
    for i in arp_record:
        if '#' in i:
            continue
        elif 'configure' in i:
            continue
        else:
            print(i)
    main()

main()
