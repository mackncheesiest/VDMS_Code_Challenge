from netaddr import IPNetwork, IPAddress

def enumerated_ip_range(CIDR_ip_range, exclusion_list):
    ipNet = IPNetwork(CIDR_ip_range)
    ipList = list(ipNet)
    for addr in exclusion_list:
        if ipList.__contains__(IPAddress(addr)):
            ipList.remove(IPAddress(addr))
    return ipList
    
def main():
    ip_range = enumerated_ip_range('192.168.0.0/24', ['192.168.0.23', '192.168.0.6'])
    for ipAddr in ip_range:
        print ipAddr
    
if __name__ == '__main__':
    main()