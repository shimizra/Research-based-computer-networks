"""
   EX Syn Flood
   Author: Shimon Mizrahi 203375563
   Date: 28/12/2021

    ********** Documentation of the nature of the program **********
    The program scans a pcap file where Syn Flood is suspected, the purpose of the program is:
    to locate the suspicious ip addresses.
    Addresses that the program finds We will export to a file named ResultFile.txt.
   ********* end Documentation of the nature of the program *********
"""
from scapy.all import *

# Constant:
SYN = 0x002
SYN_ACK = 0x012
ACK = 0x010
FLAG = 'w'
TXT_FILE = r"C:\Networks\work\SynFlood\ResultFile.txt"
PCAP_FILE = r"C:\Networks\work\SynFlood\SynFloodSample.pcap"
TIME = 0.001


def file_operations(ip_list):
    """
    :return non, The function writes to ResultFile.txt file the suspicious ip address.
    """
    with open(TXT_FILE, FLAG) as out_file:
        for item in ip_list:
            out_file.write(item + "\n")


# main function
def main():
    ip_suspect_dict = {}  # ip_suspect_dict will store each [ip] = count of SYN.
    ip_suspect_dict_time = {}  # ip_suspect_dict_time will store each [ip] = time.
    result = []  # final ip suspect list.
    pcapFile = rdpcap(PCAP_FILE)  # read pcap file.
    for packet_element in pcapFile:  # run foreach packet.
        tcp_flag = packet_element[TCP].flags
        ip_adder = packet_element[IP].src
        if tcp_flag == SYN:  # if tcp flag == SYN.
            if ip_adder not in ip_suspect_dict:  # first time.
                ip_suspect_dict_time[ip_adder] = packet_element.time  # save time.
                ip_suspect_dict[ip_adder] = 1
            else:  # not first time.
                # calculate if  Delta time < 0.001
                if packet_element.time - ip_suspect_dict_time[ip_adder] < TIME:
                    # ip_suspect_dict[ip address] ++.
                    ip_suspect_dict[ip_adder] += 1
                # save next ip time.
                ip_suspect_dict_time[ip_adder] = packet_element.time
    # check if SYN == ACK for every ip.
    for packet_element in pcapFile:
        ip_adder = packet_element[IP].src
        if packet_element[TCP].flags == ACK:  # if tcp flag == ACK.
            if ip_adder in ip_suspect_dict:
                ip_suspect_dict[ip_adder] -= 1  # ip_suspect_dict[ip address] --.
    # I decided that in my opinion for 2 requests or more is considered suspicious.
    for item, count in ip_suspect_dict.items():
        if count > 1:
            result.append(item)
    # call file_operations function for export to ResultFile.txt.
    file_operations(result)


if __name__ == "__main__":
    main()
