## Physical Firewall Decomission Script

A Python script I created that makes use of Netmiko & Pandas to automate a number of checks required before a client firewall can be decomissioned.

The script takes a CSV file (provided by the user) with the firewalls IP information & hostname and uses the information to carry out the below checks on the firewall.

### Checks

- Is the firewall online?
- Can the script authenticate to the firewall?
- Are there any ARP records present on the firewall?
- Any NAT statements present on the firewall?
    - If present do they currently respond to ping attempts?
- Does the firewall havew the FirePower module running?

As the script checks each firewall it creates a log file for all commands run and their output should the engineer running the script need to review these.

Once these checks are completed, the script creates a new CSV file with the results of the checks for the engineer to review and then decide on the next steps of the decomission.
