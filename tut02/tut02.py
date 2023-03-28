import scapy.all as scapy
import socket

x = 0


def get_ip_address(hostname):
    return socket.gethostbyname(hostname)


def process_tcp_3_way_handshake_start(packet):
    print(packet)
    filename = "./output/TCP_3_Way_Handshake_Start_2001CS71.pcap"
    scapy.wrpcap(filename, packet, append=True)


def tcp_3_way_handshake_start(ip_address, interface):
    filter = "tcp and host " + ip_address
    scapy.sniff(iface=interface, store=False, filter=filter,
                count=3, prn=process_tcp_3_way_handshake_start)


def process_tcp_handshake_close(packet):
    print(packet)
    filename = "./output/TCP_Handshake_Close_2001CS71.pcap"
    scapy.wrpcap(filename, packet, append=True)


def tcp_handshake_close(ip_address, interface):
    filter = "tcp and host " + ip_address + " and tcp[tcpflags] & tcp-fin != 0"
    scapy.sniff(iface=interface, store=False, filter=filter,
                count=2, prn=process_tcp_handshake_close)


def process_arp(packet):
    global x
    filename = "./output/ARP_2001CS71.pcap"
    if (x == 0 and packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 1):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        x = 1
    if (x == 1 and packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        x = 2


def arp(interface):
    filter = "arp"
    scapy.sniff(iface=interface, store=False,
                filter=filter, count=10, prn=process_arp)


def process_arp_request_response(packet):
    print(packet)
    filename = "./output/ARP_Request_Response_2001CS71.pcap"
    scapy.wrpcap(filename, packet, append=True)


def arp_request_response(interface):
    filter = "arp"
    scapy.sniff(iface=interface, store=False, filter=filter,
                count=2, prn=process_arp_request_response)


def process_dns_request_response(packet):
    global x
    filename = "./output/DNS_Request_Response_2001CS71.pcap"
    if (x < 2 and packet.haslayer(scapy.DNSQR) and packet[scapy.DNSQR].qtype == 1 and ("omegle" in str(packet[scapy.DNSQR].qname))):
        print(packet)
        scapy.wrpcap(filename, packet, append=True)
        x = x+1


def dns_request_response(ip_address, interface):
    filter = "port 53"
    scapy.sniff(iface=interface, store=False, filter=filter,
                count=20, prn=process_dns_request_response)


def process_ping_request_response(packet):
    print(packet)
    filename = "./output/PING_Request_Response_2001CS71.pcap"
    scapy.wrpcap(filename, packet, append=True)


def ping_request_response(ip_address, interface):
    filter = "icmp and host " + ip_address
    scapy.sniff(iface=interface, store=False, filter=filter,
                count=2, prn=process_ping_request_response)


def process_ftp_connection_start(packet):
    print(packet)
    filename = "./output/FTP_Connection_Start_2001CS71.pcap"
    scapy.wrpcap(filename, packet, append=True)


def ftp_connection_start(interface):
    filter = "port 21"
    scapy.sniff(iface=interface, store=False, filter=filter,
                count=3, prn=process_ftp_connection_start)


def process_ftp_connection_close(packet):
    global x
    if (packet[scapy.TCP].flags.F):
        print(packet)
        filename = "./output/FTP_Connection_Close_2001CS71.pcap"
        scapy.wrpcap(filename, packet, append=True)
        x -= 1


def ftp_connection_close(interface):
    global x
    filter = "port 21"
    while (x):
        scapy.sniff(iface=interface, store=False, filter=filter,
                    count=1, prn=process_ftp_connection_close)


def sniffer(interface, hostname):
    global x
    ip_address = get_ip_address(hostname)
    print(ip_address)
#     tcp_3_way_handshake_start(ip_address, interface)
    # tcp_handshake_close(ip_address, interface)
    arp(interface)
    arp_request_response(interface)  # localhost

    x = 0

#     dns_request_response(ip_address, interface)
    # ping_request_response(ip_address, interface)
    # interface="\\Device\\NPF_Loopback"
    # ftp_connection_start(interface)
    # x=1
    # ftp_connection_close(interface)


def main():
    hostname = "omegle.com"
    interface = "Wi-Fi"
    sniffer(interface, hostname)


if __name__ == "__main__":
    main()
