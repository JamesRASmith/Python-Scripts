## Switchport config Checker

A Python script that was used to aid in resolving a large number of tasks that required switch interfaces and their configuration be checked and then possibly removed.

The script takes a hostname/IP address and a switchport to carry out it's checks.

First the script checks the status of the interface, if the interface was showing as 'connected' the script would stop as the port is currently active and does not need to be shut down.

Once the status of the switchport has been checked the script then grabs the configuration present on the switchport and presents this to the user and also presents the user with the configuration it believes could be used to remove the current configuration (this is simply achieved by adding the keywork 'no' before certain lines of configuration.)

----------------------------------------------------------

**IMPORTANT NOTE** - The script does not take into account the order configuration needs to be removed in and is really only present as a guide!
