import netmiko
import getpass
import pandas
import socket
import os
import re
import csv

##Regex for IP addresses
ip_regex = re.compile("((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])")

## Config ##
## 2 options for how to connect to a switch in the estate
## Option 1 - Local creds
##ssh_user = 'xxxxx'
##ssh_pass = 'XXXX'
## Option 2 - AAA Creds
ssh_user = input(str("Enter username: "))
ssh_pass = getpass.getpass(prompt="Password for '" + ssh_user + "': ")

def main():
    ##Create CSV file to output data into once script complete
    with open('results.csv','w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Hostname", "Any ARP Records", "Any Active NAT Stmts", "External IP", "Internal IP"])
    ##Reading from the provided CSV file
    df = pandas.read_csv('decoms.csv')
    hostnames = []
    ext_ips = []
    int_ips = []
    hostnames = df.Hostname
    ext_ips = df.Server_External_IP
    int_ips = df.Server_Internal_IP
    ##Iterating through list of hostnames in the CSV file
    for i in range(len(hostnames)):
        current_fw = hostnames[i]
        external_ip = ext_ips[i]
        internal_ip = int_ips[i]
        check_fw_ping = check_ping(external_ip)
        if check_fw_ping is True:
            try:
                ##Connecting to the firewall
                device = {
                    "device_type": '',
                    "host": current_fw,
                    "username": ssh_user,
                    "password": ssh_pass,
                    "secret": ssh_pass,
                    "session_log": current_fw + '-log.txt',
                    "fast_cli": False,
                    }
                net_connect = do_connect(device,current_fw)
                i += 1
                decom_checks(net_connect,current_fw,external_ip,internal_ip)
            except netmiko.NetmikoAuthenticationException:
                print("Failed to authenticate to" + current_fw + "! Check provided credentials")
                continue
        else:
            results = []
            results.append([current_fw, "FW OFFLINE", "FW OFFLINE",external_ip,internal_ip])
            output_to_csv(results)

##Works through the checks and will output the results to a CSV file for easier review
def decom_checks(net_connect,current_fw,external_ip,internal_ip):
    results = []
    arp_check = get_arp_table(net_connect)
    nat_check = get_nat_stmts(net_connect)
    results.append([current_fw,arp_check,nat_check,external_ip,internal_ip])
    ##Output results to a CSV file
    output_to_csv(results)

def output_to_csv(results):
    with open('results.csv','a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

##Grabbing NAT statements from the firewall
def get_nat_stmts(net_connect):
    try:
        nat_stmts = net_connect.send_command('sho xlate | i NAT')
    except:
        return ("Cannot Access")
    ping_result = []
    for line in nat_stmts.split('\n'):
        ping_result = []
        if 'NAT' in line:
            ##Regex to find the first IP in the line
            IP = re.search(ip_regex,line)
            IP = IP.group()
            ##Have to specify 12 second wait time to allow ping to come back
            check_ping = net_connect.send_command('ping '+ IP, read_timeout=12)
            ##If internal IP pings return True
            if '!!!!!' in check_ping:
                return True
            ##If internal IP does not ping return False
            else:
                ping_result.append(False)
        elif '0 in use':
            ping_result.append(False)

    ##Once the above check has been done for all internal IPs found, this is compared again here
    ##If any of the found IPs ping then the function returns True and the firewall will not be decommed
    if True in ping_result:
        return True
    else:
        return False
    
##Grabbing ARP records form the firewall
def get_arp_table(net_connect):
    try:
        arp_table = net_connect.send_command('sho arp | exc outside|failover|fo')
    except:
        return ("Cannot Access")
    if len(arp_table) > 0:
        return True
    else:
        return False

##Connecting to the device using provided details
def do_connect(device,current_fw):
    try:
        net_connect = netmiko.ConnectHandler(**device)
        return net_connect
    except netmiko.NetmikoTimeoutException as error:
        print("Failed to SSH to " + current_fw + "! Is firewall online?")

def check_ping(external_ip):
    ping = os.system("ping -n 5 " + external_ip)
    if ping == 0:
        return True
    else:
        return False

###################################################
            
if __name__ == "__main__":
    main()
