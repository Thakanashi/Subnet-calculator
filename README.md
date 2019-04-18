# Subnet-calculator
Subnet calculator written in Python.
1. The script take as an argument the IP address (host or network) with the mask in the following format:
a.b.c.d / e.f.g.h
2. If the argument is not given, the script gets the address of the computer on which it's
launched
3. The script checks whether the entered address is a valid IP address. If not,
raises exception.
4. The script calculates the following data:
    i. Network address
    ii. Network class
    iii. Check if address is public or private
    iv. Network mask in decimal format (eg 255.255.255.0) and binary
    v. Broadcast address (decimal and binary)
    vi. The first host address (decimal and binary)
    vii. Last host address (decimal and binary)
    viii. The maximum number of hosts that can be assigned to a given subnet
5. Script displays calculated values in the console and saves this values to a text file
6. If the given address is the host address, the script asks whether to ping
for the given address. If the user types Y, the script executes the ping command
and presents its results.
