import socket
import struct
import textwrap
import colorama
from colorama import Fore
colorama.init()

TAB_1 = '\t  - '
TAB_2 = '\t\t  - '
TAB_3 = '\t\t\t  - '
TAB_4 = '\t\t\t\t  - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '


def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        print(Fore.RED + '\nIncomming Frame')
        print(TAB_1 + Fore.BLUE + 'Destination: {}, Source{}, Protocol: {}'.format(dest_mac, src_mac, eth_proto))


        # 8 for IPV4
        if eth_proto == 8:
            (version, header_length, ttl, proto, src, target, data) = ipv4_packets(data)
            print(TAB_1 + Fore.CYAN +'IPV4 Packet:')
            print(TAB_2 + Fore.GREEN + 'Version: {}, Header Length: {}, TTL: {}'.format(version, header_length, ttl))
            print(TAB_2 + Fore.GREEN + 'Protocol: {}, Source: {}, Target: {}'.format(proto, src, target))
            
            # 1 for ICMP
            if proto == 1:
                icmp_type, code, checksum, data = icmp_packet(data)
                print(TAB_1 + Fore.LIGHTBLUE_EX + 'ICMP Packet:')
                print(TAB_2 + Fore.GREEN + 'Type: {}, Code: {}, CheckSum: {}'.format(icmp_type, code, checksum))
                print(TAB_2 + Fore.MAGENTA + 'Data:')
                print(Fore.RED + format_multi_line(DATA_TAB_3, data))
            
            # 6 for TCP
            elif proto == 6:
                (src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data) = tcp_segment(data)
                print(TAB_1 + Fore.CYAN + 'TCP Segment:')
                print(TAB_2 + Fore.GREEN + 'Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
                print(TAB_2 + Fore.GREEN + 'Sequence: {}, Acknowledgement: {}'.format(sequence, acknowledgement))
                print(TAB_2 + Fore.GREEN + 'Flags:')
                print(TAB_3 + Fore.GREEN + 'URG: {}, ACK: {}, PSH: {}, SYN: {}, FIN: {}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                print(TAB_2 + Fore.MAGENTA + 'Data:')
                print(Fore.RED + format_multi_line(DATA_TAB_3, data))

            # 17 for UDP
            elif proto == 17:
                (src_port, dest_port, size, data) = udp_segment(data)
                print(TAB_1 + Fore.YELLOW + 'UDP Segment:')
                print(TAB_2 + Fore.GREEN +'Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, size))
               
            # others
            else:
                print(TAB_1 + Fore.LIGHTRED_EX + 'Data:')
                print(Fore.RED + format_multi_line(DATA_TAB_2, data))
        else:
            print(Fore.LIGHTMAGENTA_EX + 'Data:')
            print(Fore.RED + format_multi_line(DATA_TAB_1, data))



# unpack ethernet frame
def ethernet_frame(data):
    dest_mac, source_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(source_mac), socket.htons(proto), data[14:]


# Return proper formatted MAC address (AA:BB:CC:DD:FF)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


# unpacks IPV4 packets (ttl -> time to live (Monitor the packets time to time)
def ipv4_packets(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]


# return proper formatted IPV4 address (127.0.0.1)
def ipv4(addr):
    return '.'.join(map(str, addr))


# unpack ICMP packet
def icmp_packet(data):
    icmp_type, code, checksum = sstruct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]


# unpack TCP segment
def tcp_segment(data):
    (src_port, dest_port, sequence, acknowledgement, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]


# unpack_udp segment
def udp_segment(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, size, data[8:]


# Formats multi line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -=1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

    






