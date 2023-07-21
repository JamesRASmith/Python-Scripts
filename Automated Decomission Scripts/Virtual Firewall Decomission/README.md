# Virtual Firewall Decomission Script

This Python script is designed to assist in the decommissioning process of firewalls in an estate. It takes a list of hostnames, external IPs, and internal IPs of the firewalls from a CSV file named decoms.csv. The script attempts to connect to each firewall using either local credentials or AAA (Authentication, Authorization, and Accounting) credentials, and then performs several checks to determine if it is safe to decommission each firewall.

## Prerequisites
Python 3.x

netmiko library

pandas library

## How to Use
1) Prepare a CSV file named decoms.csv containing the following columns:

   Hostname: The hostname or IP address of the firewall to be decommissioned.
   
   Server_External_IP: The external IP address of the firewall.
   
   Server_Internal_IP: The internal IP address of the firewall.

   ![image](https://github.com/JamesRASmith/Python-Scripts/assets/57868272/24ec2d77-4ec3-495f-aa56-8b29573b4efc)

2) Run the script and provide the required credentials for connecting to the firewalls. You have two options:

    Option 1: Local credentials (ssh_user and ssh_pass) - Uncomment and set the values of these variables in the script.
   
    Option 2: AAA credentials - The script will prompt you to enter a username and password for authentication.
   
3) The script will then perform the following checks for each firewall:

    Check Ping: It will ping the external IP address of the firewall to ensure it is online and reachable.

    Firepower Status: If the firewall is reachable, it will check if the firewall is running Firepower (an intrusion prevention system). If Firepower is active, the script will alert the user. You can later deactivate Firepower if needed.

    NAT Statements: It will retrieve NAT (Network Address Translation) statements from the firewall and check if any internal IP addresses are being translated. It will ping each internal IP address to see if it responds. If any internal IP address successfully responds to the ping, it means the firewall should not be decommissioned.

    ARP Records: It will check for ARP records on the firewall. If there are any ARP records, it means there are active connections, and the firewall should not be decommissioned.

4) The results of each firewall's checks will be saved in the results.csv file in the same directory as the script. The CSV file will have the following columns:

    Hostname: The hostname of the firewall.
   
    Any ARP Records: "True" if there are ARP records; otherwise, "False".

    Any Active NAT Stmts: "True" if there are active NAT statements with pinging internal IPs; otherwise, "False".

    External IP: The external IP address of the firewall.

    Internal IP: The internal IP address of the firewall.

    ![image](https://github.com/JamesRASmith/Python-Scripts/assets/57868272/20543049-d022-40c4-a462-38a2d4c944d7)

Please ensure that you have proper authorization before running this script and decommissioning any firewalls. This script is intended for use in specific decommissioning scenarios and should be used with caution. Always review the results carefully and verify the findings before taking any action on the firewalls.
