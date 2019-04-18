# Created by Michał Słomski

import os
import socket
import subprocess
import sys

# returns network class
def get_net_class(first_octet):
    if(first_octet>=0 and first_octet<128):
        return("A class")
    elif(first_octet>127 and first_octet<192):
        return("B class")
    elif(first_octet > 191 and first_octet < 224):
        return("C class")
    elif(first_octet > 223 and first_octet <240):
        return("D class")
    else:
        return("E class")

# returns ip address from your computer
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address

# validate if ip address is correct
def ip_validation(ip_address):
    address = ip_address.split('.')
    if len(address) !=4:
        raise Exception
    for i in address:
        if not i.isdigit():
            raise Exception
        i = int(i)
        if(i<0 or i>255):
            raise Exception
    return True

# This function splits ip and mask
def split_mask_and_ip(ip_and_mask):
    after_split = ip_and_mask.split('/')
    if(len(after_split)>2):
        raise Exception
    return after_split

# This function is parsing your CMD console for looking subnet mask
def get_subnet_mask():
    ip = get_ip_address()
    proc = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if ip.encode() in line:
            break
    mask = proc.stdout.readline().split(b':')[-1].replace(b' ', b'').decode()
    return mask

# This function splits your ip or mask by '.' and converts octets to int
def convert_to_int(ip_or_mask):
    ip_or_mask_int = [] # binary
    after_split = ip_or_mask.split('.')
    for i in after_split:
        list.append(ip_or_mask_int, int(i))
    return ip_or_mask_int

# This function converts int number to binary number and filling the binary number to maximum eight zeros
def get_bin(x,n=8):
    return format(x, 'b').zfill(n)

# converts list to binary
def convert_to_binary(list):
    tmp = []
    for i in list:
        tmp.append(get_bin(i, 8))
    return tmp

# returns first host address
def get_first_host_address(list):
    a='001'
    update_last_octet = bin(int(list[3],2) + int(a,2))
    tmp = update_last_octet[2:].zfill(8)
    list[3] = tmp
    return list

# returns last host address
def get_last_host_address(list):
    a = '001'
    update_last_octet = bin(int(list[3],2) - int(a,2))
    tmp = update_last_octet[2:]
    list[3] = tmp
    return list

# returns network address
def get_network_address(ip,mask):
    after_and_operation = []
    l1 = convert_to_int(ip)
    l2 = convert_to_int(mask)
    array_length = len(l1)
    for i in range(array_length):
        after_and_operation.append(bin(l1[i]&l2[i])[2:].zfill(8))

    return after_and_operation

# returns info if address is public or private
def get_public_or_private_address(first_octet, second_octet):
    if(first_octet==10 or (first_octet==172 and (second_octet>=16 and second_octet<=31))or(first_octet==192 and second_octet==168)):
        return("Address is private")
    else:
        return("Address is public")

# returns broadcast address
def get_broadcast_address(ip,mask):
    octets_from_broadcast = []
    l1 = convert_to_int(ip)
    l2 = convert_to_int(mask)
    array_length = len(l1)
    for i in range(array_length):
        tmp = bin(l1[i] | ~l2[i]& 0xFF)
        octets_from_broadcast.append(tmp[2:].zfill(8))
    return octets_from_broadcast

# returns maximum number of hosts
def get_maximum_number_of_hosts(mask):
    counts_of_1 = 0
    mask = convert_to_binary(convert_to_int(mask))
    for i in mask:
        counts_of_1 += i.count('1')

    return (2 ** (32-counts_of_1)) -2

# Function for printing binary numbers
def print_list(list):
     to_write =[]
     count = 0
     for i in list:
        count+=1
        if count<4:
            tmp=i+"."
            print(tmp,end='')
            to_write.append(tmp)
        else:
            print(i)
            to_write.append(i+'\n')

     return to_write

# Function for printing decimal numbers
def print_decimal_list(list):
     to_write = []
     count = 0
     for i in list:
        count += 1
        if count < 4:
            tmp = str(int(i,2))
            to_write.append(tmp+'.')
            print(tmp+'.',end='')
        else:
            print(int(i,2))
            to_write.append(str(int(i,2))+'\n')

     return to_write

# Function which ping if ip address you passed in argument is host address
def ping(host):
    user_input = input("Do you want to ping host address? (Y/N): ")

    while(user_input.lower() != 'y' and user_input.lower() !='n'):
        user_input=input("Error: wrong input")

    if(user_input.lower()=='y'):
        r = os.system("ping "+host)

# main function which prints results to console and saves this results to .txt file
def main():

    plik = open("results",'a')
    try:
      if len(sys.argv) > 1:
        mask_and_ip = []
        mask_and_ip = split_mask_and_ip(sys.argv[1])
        ip_validation(mask_and_ip[0])
        first_octet = convert_to_int(mask_and_ip[0])[0]
        second_octet = convert_to_int(mask_and_ip[0])[1]

        print("Network address(2): ")
        plik.write("Network address(2):" + '\n')
        l=print_list(get_network_address(mask_and_ip[0],mask_and_ip[1]))
        plik.writelines(l)

        print("Network address(10): ")
        plik.write("Network address(10):" + '\n')
        l1=print_decimal_list(get_network_address(mask_and_ip[0], mask_and_ip[1]))
        plik.writelines(l1)

        plik.write("Network class: ")
        print("Network class: " + get_net_class(first_octet))
        plik.write(get_net_class(first_octet)+'\n')

        plik.write("Private or public: ")
        print("Private or public: " + get_public_or_private_address(first_octet, second_octet))
        plik.write(get_public_or_private_address(first_octet, second_octet)+'\n')

        plik.write("Subnet mask(10): ")
        print("Subnet mask(10): " + mask_and_ip[1])
        plik.write(mask_and_ip[1]+'\n')

        plik.write("Subnet mask(2): "+ '\n')
        print("Subnet mask(2): ")
        l2=print_list(convert_to_binary(convert_to_int(mask_and_ip[1])))
        plik.writelines(l2)

        plik.write("Broadcast address(10): "+ '\n')
        print("Broadcast address(10): ")
        l3=print_decimal_list(get_broadcast_address(mask_and_ip[0],mask_and_ip[1]))
        plik.writelines(l3)

        plik.write("Broadcast address(2): "+ '\n')
        print("Broadcast address(2): ")
        l4=print_list(get_broadcast_address(mask_and_ip[0],mask_and_ip[1]))
        plik.writelines(l4)

        plik.write("The first one host address(10): "+ '\n')
        print("The first one host address(10): ")
        l5=print_decimal_list(get_first_host_address(get_network_address(mask_and_ip[0],mask_and_ip[1])))
        plik.writelines(l5)

        plik.write("The first one host address(2): "+ '\n')
        print("The first one host address(2): ")
        l6=print_list(get_first_host_address(get_network_address(mask_and_ip[0],mask_and_ip[1])))
        plik.writelines(l6)

        plik.write("The last one host address(10): "+ '\n')
        print("The last one host address(10): ")
        l7=print_decimal_list(get_last_host_address(get_broadcast_address(mask_and_ip[0],mask_and_ip[1])))
        plik.writelines(l7)

        plik.write("The last one host address(2): "+ '\n')
        print("The last one host address(2): ")
        l8=print_list(get_last_host_address(get_broadcast_address(mask_and_ip[0],mask_and_ip[1])))
        plik.writelines(l8)

        plik.write("Maximum number of hosts: "+ '\n')
        print("Maximum number of hosts: ")
        tmp = get_maximum_number_of_hosts(mask_and_ip[1])
        print(tmp)
        plik.write(str(tmp))

        if (mask_and_ip[0]==get_ip_address()):
            ping(mask_and_ip[0])
        else:
            print("there is no possible to ping")



      else:
        first = convert_to_int(get_ip_address())[0]
        second = convert_to_int(get_ip_address())[1]

        plik.write("Network address(2):" + '\n')
        print("Network address(2): ")
        l=print_list(get_network_address(get_ip_address(),get_subnet_mask()))
        plik.writelines(l)

        plik.write("Network address(10):" + '\n')
        l1=print_decimal_list(get_network_address(get_ip_address(),get_subnet_mask()))
        plik.writelines(l1)

        plik.write("Network class: ")
        print("Network class(10): " + get_net_class(first))
        plik.write(get_net_class(first)+'\n')

        plik.write("Private or public: ")
        print("Private or public: " + get_public_or_private_address(first,second))
        plik.write(get_public_or_private_address(first,second)+'\n')

        plik.write("Subnet mask(10): ")
        print("Subnet mask(10): " + get_subnet_mask(), end='')
        plik.write(get_subnet_mask())

        plik.write("Subnet mask(2): " + '\n')
        print("Subnet mask(2): ")
        l2=print_list(convert_to_binary(convert_to_int(get_subnet_mask())))
        plik.writelines(l2)

        plik.write("Broadcast address(10): " + '\n')
        print("Broadcast address(10): ")
        l3=print_decimal_list(get_broadcast_address(get_ip_address(),get_subnet_mask()))
        plik.writelines(l3)

        plik.write("Broadcast address(2): " + '\n')
        print("Broadcast address(2): ")
        l4=print_list(get_broadcast_address(get_ip_address(),get_subnet_mask()))
        plik.writelines(l4)

        plik.write("The first one host address(10): " + '\n')
        print("The first one host address(10): ")
        l5=print_decimal_list(get_first_host_address(get_network_address(get_ip_address(),get_subnet_mask())))
        plik.writelines(l5)

        plik.write("The first one host address(2): " + '\n')
        print("The first one host address(2): ")
        l6=print_list(get_first_host_address(get_network_address(get_ip_address(),get_subnet_mask())))
        plik.writelines(l6)

        plik.write("The last one host address(10): " + '\n')
        print("The last one host address(10): ")
        l7=print_decimal_list(get_last_host_address(get_broadcast_address(get_ip_address(),get_subnet_mask())))
        plik.writelines(l7)

        plik.write("The last one host address(2): " + '\n')
        print("The last one host address(2): ")
        l8=print_list(get_last_host_address(get_broadcast_address(get_ip_address(),get_subnet_mask())))
        plik.writelines(l8)

        plik.write("Maximum number of hosts: " + '\n')
        print("Maximum number of hosts: ")
        tmp= get_maximum_number_of_hosts(get_subnet_mask())
        print(tmp)
        plik.write(str(tmp))



    finally:
        plik.close()



main()
