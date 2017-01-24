#!python

import sys
from netaddr import IPNetwork, IPAddress, AddrFormatError

def enumerated_ip_range(CIDR_ip_range, exclusion_list):
    try:
        #Works well except for checking the type of elements in the exclusion list
        #That will be caught by the AddrFormatError block if necessary, though
        if type(CIDR_ip_range) != str:
            print "The CIDR_ip_range must be a string"
            return []
        elif type(exclusion_list) != list:
            print "The exclusion_list must be a list of strings"
            return []      
        
        #Enumerate the list of IP Addresses and then remove the ones that shouldn't be there
        ipNet = IPNetwork(CIDR_ip_range)
        ipList = list(ipNet)
        for addr in exclusion_list:
            if IPAddress(addr) in ipList:
                ipList.remove(IPAddress(addr))
        
        #Return the list
        return ipList
    except AddrFormatError:
        print "Invalid IP Range or invalid IP Address listed in exclusion_list"
        return []

def printMainUsage():
    print "Usage: IP_Range.py [-h] [--help] IP_Range Excluded_IP_1 Excluded_IP_2 ..."

def main():
    if (len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help')) or len(sys.argv) == 1:
        printMainUsage()
        return
    
    CIDR_ip_range = sys.argv[1]
    #Works even with no excluded addresses -- becomes empty list
    excluded_ips = sys.argv[2:]        
    
    ip_range = enumerated_ip_range(CIDR_ip_range, excluded_ips)
    for ipAddr in ip_range:
        print ipAddr
    
    return
    
if __name__ == '__main__':
    main()