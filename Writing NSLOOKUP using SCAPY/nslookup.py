"""
   EX nslookup implementation
   Author: Shimon Mizrahi 203375563
   Date: 06/12/2021

    ********** Documentation of the nature of the program **********
    The purpose of the program is:
    to realize nslookup command so that the user sends as the first argument an action type,
    and the second argument the domain address.
    The system will return the ip or CNAME address respectively.
   ********* end Documentation of the nature of the program *********
"""
from scapy.all import *
import sys

# const vars:
TYPE_A = "-type=A"
TYPE_PTR = "-type=PTR"
ARGUMENT_LEN = len(sys.argv)
ADDR = ".in-addr.arpa"
TIMEOUT = 2.5


def valid_ip(ip_add):
    """
    :param ip_add: ip address
    :return: True if IP address is valid.
    """
    result = True
    lst = ip_add.split(".")
    if len(lst) != 4:  # The IP address structure contains 4 points.
        result = False
    else:
        for item in lst:
            if not item.isdigit():  # if not digit e.g 10.45.a.b.
                result = False
                break
            elif int(item) > 255:  # max number 255.255.255.255
                result = False
                break
    return result


def private_ip(ip_add):
    """
    :param ip_add:  ip address
    :return: True if IP address is not private.
    """
    result = True
    lst = ip_add.split(".")
    # we check if IP is private address.
    if int(lst[0]) == 10:  # range 10.0.0.0 - 10.255.255.255
        result = False
    elif int(lst[0]) == 172 and 16 <= lst[1] <= 31:  # range 172.16.0.0 - 172.31.255.255
        result = False
    elif int(lst[0]) == 192 and lst[1] == 168:  # range 192.168.0.0 - 192.168.255.255
        result = False
    return result


def valid_request():
    """
    :return: True when user did'nt sent domain address, or command is incorrect.
    """
    if ARGUMENT_LEN == 1:
        return True, "Missing arguments"
    if ARGUMENT_LEN == 2 and valid_ip(sys.argv[1]):  # if not use -type=PTR
        return True, "No valid command, should use " + TYPE_PTR
    if ARGUMENT_LEN == 3 and sys.argv[1] == TYPE_PTR and (not valid_ip(sys.argv[2]) or not private_ip(sys.argv[2])):
        return True, "can't find " + sys.argv[2] + ": Non-existent domain"  # e.g -type=PTR 12.12.1
    if ARGUMENT_LEN == 3 and sys.argv[1] == TYPE_A and valid_ip(sys.argv[2]):  # e.g use -type=A 200.22.22.22
        return True, "No valid command"
    return False, ""


def build_request(op_code, argument_count):
    """
    :param op_code: TYPE_A or TYPE_PTR
    :param argument_count: number of argv.
    :return: request package
    """
    if argument_count > 2:
        domain_adder = sys.argv[2]
    else:
        domain_adder = sys.argv[1]

    if op_code == TYPE_A:
        return IP(dst='8.8.8.8') / UDP(sport=24601, dport=53) / DNS(qdcount=1) / DNSQR(qname=domain_adder)
    else:
        ip = domain_adder.split(".")
        ip.reverse()
        fix_ip = ".".join(ip) + ADDR
        return IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1) / DNSQR(qtype="PTR", qname=fix_ip)


def main():
    result = valid_request()
    if result[0]:
        print(result[1])
    else:
        first_argument = sys.argv[1]
        if ARGUMENT_LEN == 3:  # for example: -type=A www.amazon.con
            if first_argument == TYPE_A:
                request = build_request(TYPE_A, ARGUMENT_LEN)
            elif first_argument == TYPE_PTR:
                request = build_request(TYPE_PTR, ARGUMENT_LEN)
            else:  # if not TYPE_A or TYPE_PTR.
                sys.exit("No valid command")
        elif ARGUMENT_LEN == 2:  # for example: www.amazon.con
            request = build_request(TYPE_A, ARGUMENT_LEN)  # default is: TYPE_A
        receive = sr1(request, timeout=TIMEOUT)  # Send and receive packets
        # sr1() is a variant that only returns one packet that answered the packet (or the packet set) sent.

        if receive:  # if timeout then receive = None
            count = receive[DNS].ancount  # count  = number of answer.
            for i in range(count):
                data = receive[DNSRR][i].rdata
                if type(data) == bytes:  # Then we will ask for a non-show of bytes
                    print(receive[DNSRR][i].rdata.decode())
                else:
                    print(receive[DNSRR][i].rdata)
        else:
            print("timeout error")


if __name__ == "__main__":
    main()
