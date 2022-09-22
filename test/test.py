import socket
from scapy.all import *

# constants
SRC_IP = '0.0.0.0'
DST_IP = "127.0.0.1"
GOOGLE = "8.8.8.8"
PORT = 8153
TIMEOUT = 2
MESSAGE_SIZE = 1024
ADDR = ".in-addr.arpa"
ARRAY = []


def calcIPs(url):
    ARRAY = []
    pack = IP(dst=GOOGLE) / UDP(sport=24601, dport=53) / DNS(qdcount=1) / DNSQR(qname=url)
    result = sr1(pack, timeout=TIMEOUT)  # Send and receive packets

    if result:  # if timeout then receive = None
        count = result[DNS].ancount  # count  = number of answer.
        for i in range(count):
            data = result[DNSRR][i].rdata
            if type(data) == bytes:  # Then we will ask for a non-show of bytes
                ARRAY.append(result[DNSRR][i].rdata.decode())
            else:
                ARRAY.append(result[DNSRR][i].rdata)
        ips = ""
        for item in ARRAY:
            ips += item + "<br>"
    else:
        print("timeout error")
    return ips


def send_to_client(ips, client_socket):
    response = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(ips)) + "\r\n"
    header = "Content-Type: text/html; charset=utf-8" + "\r\n"
    result = response + header + "\r\n"
    client_socket.send(result.encode())
    client_socket.send(ips.encode())
    print('Closing connection')
    client_socket.close()


def reverse(url):
    ARRAY = []
    ip_add = url.split("/")[1]
    ip = ip_add.split(".")
    ip.reverse()
    fix_ip = ".".join(ip) + ADDR
    pack = IP(dst=GOOGLE) / UDP(sport=24601, dport=53) / DNS(qdcount=1) / DNSQR(qtype="PTR", qname=fix_ip)
    result = sr1(pack, timeout=TIMEOUT)  # Send and receive packets
    if result:  # if timeout then receive = None
        count = result[DNS].ancount  # count  = number of answer.
        for i in range(count):
            data = result[DNSRR][i].rdata
            if type(data) == bytes:  # Then we will ask for a non-show of bytes
                ARRAY.append(result[DNSRR][i].rdata.decode())
            else:
                ARRAY.append(result[DNSRR][i].rdata)
        ips = ""
        for item in ARRAY:
            ips += item + "<br>"
        print(ips)
    else:
        print("timeout error")
    return ips



def handle_client(client_socket):
    result = client_socket.recv(MESSAGE_SIZE).decode()
    headers_lines = result.split("\r\n")
    list_get_http = headers_lines[0].split(" ")
    url = list_get_http[1][1:]
    if "reverse" in url:
        ips = reverse(url)
    else:
        ips = calcIPs(url)
    send_to_client(ips, client_socket)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SRC_IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print('New connection received')
            client_socket.settimeout(TIMEOUT)
            handle_client(client_socket)
        except socket.timeout as e:
            print("Error! Time out:{}".format(e))


            
            
if __name__ == "__main__":
    main()
