"""
   EX 2.7 client implementation
   Author: Shimon Mizrahi 203375563
   Date: 08/11/2021

    ********** Documentation of the nature of the program **********
    The purpose of the program is:
    to allow the client to send commands to the server to receive information according to the client's desire.
    The server and client work against a pre-known communication protocol,
    the first 4 bits are the size of the request
   ********* end Documentation of the nature of the program *********
"""

import socket
import protocol

IP = "127.0.0.1"
SAVED_PHOTO_LOCATION = r'C:\Networks\work\clientScreenShots.jpg'


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    valid_protocol, data = protocol.get_msg(my_socket)
    if valid_protocol:
        if not cmd == "SEND_PHOTO":
            print(data)
        else:
            if data == "Bad command or parameters":
                print("Bad command or parameters")
            else:
                count = 0
                file = open(SAVED_PHOTO_LOCATION, 'ab')
                try:
                    while count <= int(data):
                        packet = my_socket.recv(protocol.SIZE)
                        file.write(packet)
                        count += protocol.SIZE
                    print("The image saved successfully \n")
                except NameError:
                    print("Error, Failed to save image\n")
                finally:
                    file.close()
    # (10) treat SEND_PHOTO


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol.PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOTS\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            if cmd == 'EXIT':
                break
            handle_server_response(my_socket, cmd)
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
