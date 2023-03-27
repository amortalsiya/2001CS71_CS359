from scapy.all import *

dst_ip = "104.23.141.25"# OMEGLE.COM
dst_port = 443
src_port = 4439

syn_pkt = IP(dst=dst_ip) / TCP(dport=dst_port, flags="S")
syn_ack_pkt = sr1(syn_pkt)
ack_pkt = IP(dst=dst_ip) / TCP(dport=dst_port, flags="A",
                               seq=syn_ack_pkt.ack, ack=syn_ack_pkt.seq + 1)

send(ack_pkt)
wrpcap('./output/TCP_handshake_start_2001CS71.pcap',
       [syn_pkt, syn_ack_pkt, ack_pkt])


syn_packet = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S")

print("sending syn")
syn_ack_response = sr1(syn_packet)


ack_packet = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="A",
                                  seq=syn_packet[TCP].seq + 1, ack=syn_ack_response[TCP].seq + 1)

print("sending syn-ack")
send(ack_packet)

# Create the FIN packet
fin_packet = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port,
                                  flags="FA", seq=ack_packet[TCP].seq, ack=ack_packet[TCP].ack)

print("sending fin")
send(fin_packet)

fin_ack_response = sr1(fin_packet)
final_ack_packet = IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port,
                                     flags="A", seq=fin_ack_response[TCP].ack, ack=fin_ack_response[TCP].seq + 1)
send(final_ack_packet)
#ARP REQUEST


wrpcap("./output/TCP_handshake_close_2001CS71.pcap",
       [fin_packet, fin_ack_response, final_ack_packet])

#DNS REQUEST
dns_query = IP(dst="8.8.8.8")/UDP(sport=RandShort(), dport=53) / \
    DNS(rd=1, qd=DNSQR(qname="omegle.com", qtype="A"))

send(dns_query)

answer = sr1(dns_query)

wrpcap("./output/DNS_request_response_2001CS71.pcap", [dns_query, answer])

#PING REQUEST
ping = IP(dst=dst_ip)/ICMP()
send(ping)

ping_answer = sr1(ping)

wrpcap("./output/PING_request_response_2001CS71.pcap", [ping, ping_answer])

#ARP PACKET BRODCASTING
arp_send = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst='172.16.176.1')

arp_response = srp1(arp_send)
wrpcap("./output/ARP_request_response_2001CS71.pcap", [arp_send, arp_response])

#FTP CONNECTION 

ftp_pkt = IP(dst='195.144.107.198')/TCP(sport=20, dport=21, flags="S")
ftp_res = sr1(ftp_pkt)

wrpcap("./output/FTP_Connection_Start_2001CS71.pcap", [ftp_pkt, ftp_res])
#FTP CLOSE
ftp_close = IP(dst='195.144.107.198')/TCP(sport=20, dport=21, seq=ftp_res.ack,
                                          ack=ftp_res.seq+1, flags="PA")

wrpcap("./output/FTP_Connection_End_2001CS71.pcap", [ftp_close])
#2001CS71 SIYARAM KUMAR
