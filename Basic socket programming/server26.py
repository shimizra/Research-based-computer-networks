"""EX 2.6 server implementation
   Author: Shimon Mizrahi 203375563
   Date: 24/10/2021

    ********** Documentation of the nature of the program **********
    The purpose of the program is:
    to create a server that will enable certain information according to different requests of the customer.
    The server and client work against a pre-known communication protocol,
    the first 2 bits are the size of the request
   ********* end Documentation of the nature of the program *********

"""

import socket
import protocol


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            print(cmd)
            valid_cmd = protocol.check_cmd(cmd)
            if valid_cmd:
                response = protocol.create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        if response == protocol.EXIT:
            break
        client_socket.send(response.encode())

    print("Closing\n")
    server_socket.close()
    client_socket.close()


if __name__ == "__main__":
    main()
