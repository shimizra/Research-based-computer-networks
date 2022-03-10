"""EX 2.6 client implementation
   Author: Shimon Mizrahi 203375563
   Date: 24/10/2021

    ********** Documentation of the nature of the program **********
    The purpose of the program is:
    to allow the client to send commands to the server to receive information according to the client's desire.
    The server and client work against a pre-known communication protocol,
    the first 2 bits are the size of the request
   ********* end Documentation of the nature of the program *********
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        valid_cmd = protocol.check_cmd(user_input)
        if valid_cmd:
            user_input = protocol.create_msg(user_input)
            my_socket.send(user_input.encode())
            if user_input[protocol.LENGTH_FIELD_SIZE:] == protocol.EXIT:
                break
            length = my_socket.recv(protocol.LENGTH_FIELD_SIZE).decode()
            data = my_socket.recv(int(length)).decode()
            '''
            if not data == "Wrong command" and not data == "Wrong protocol":
                print(data)
            else:
                print("Response not valid\n")
            '''
            print(data)
        else:
            print("Not a valid command")

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
