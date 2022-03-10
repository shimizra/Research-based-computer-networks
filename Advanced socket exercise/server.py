"""
EX 2.7 server implementation
   Author: Shimon Mizrahi 203375563
   Date: 08/11/2021

    ********** Documentation of the nature of the program **********
    The purpose of the program is:
    to create a server that will enable certain information according to different requests of the customer.
    The server and client work against a pre-known communication protocol,
    the first 4 bits are the size of the request
   ********* end Documentation of the nature of the program *********
"""

import socket
import protocol
import os
import glob
import shutil
import subprocess
import pyautogui

IP = "0.0.0.0"
PHOTO_PATH = r'C:\Networks\work\ScreenShots.jpg'


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    lst_command = cmd.split(" ")
    if protocol.check_cmd:
        command = lst_command[0]
        if command == protocol.EXIT:
            return True, command, []
        if command == protocol.DIR:
            cmd_param1 = lst_command[1]
            return True, command, [cmd_param1]
        elif command == protocol.DELETE:
            cmd_param1 = lst_command[1]
            if os.path.isfile(cmd_param1):
                return True, command, [cmd_param1]
            else:
                return False, "Error file not exist!", []
        elif command == protocol.COPY:
            cmd_param1 = lst_command[1]
            if os.path.isfile(cmd_param1):
                return True, command, [cmd_param1, lst_command[2]]
            else:
                return False, "Error one or two of file/s not exist!", []
        elif command == protocol.EXECUTE:
            cmd_param1 = lst_command[1]
            if os.path.isfile(cmd_param1):
                return True, command, [cmd_param1]
            else:
                return False, "Error file not exist!", []
        elif command == protocol.PHOTO_SEND:
            if os.path.isfile(PHOTO_PATH):
                return True, command, []
            else:
                return False, "Error file not exist!", []
        elif command == protocol.TAKE_SCREENSHOTS or command == protocol.EXIT:
            return True, command, []
    else:
        return False, "Error", []

    # Use protocol.check_cmd first

    # Then make sure the params are valid

    # (6)


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data
    """
    if command == protocol.DIR:
        response = glob.glob(params[0] + "\\*.*")
    elif command == protocol.DELETE:
        try:
            os.remove(params[0])
            response = "The file has been deleted"
        except NameError:
            response = "Error, The file was not deleted"
    elif command == protocol.COPY:
        try:
            shutil.copy(params[0], params[1])
            response = "The file has been copied"
        except NameError:
            response = "Error, Copy were not performed"
    elif command == protocol.EXECUTE:
        try:
            subprocess.call(params[0])
            response = "The file has been executed"
        except NameError:
            response = "Error, Action not executed"
    elif command == protocol.TAKE_SCREENSHOTS:
        try:
            image = pyautogui.screenshot()
            image.save(PHOTO_PATH)
            response = "The photo was taken successfully"
        except NameError:
            response = "Error, Action not executed"
    elif command == protocol.PHOTO_SEND:
        response = command
    elif command == protocol.EXIT:
        response = command
    # (7)
    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # (6)
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)

                if command == protocol.PHOTO_SEND:
                    file_size = os.stat(PHOTO_PATH).st_size
                    client_socket.send(protocol.create_msg(str(file_size)))
                    with open(PHOTO_PATH, 'rb') as input_file:
                        file = input_file.read()
                    client_socket.send(file)
                else:
                    # add length field using "create_msg"
                    answer = protocol.create_msg(response)
                    # send to client
                    if command == 'EXIT':
                        break
                    client_socket.send(answer)
                    # (9)
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                client_socket.send(protocol.create_msg(response))
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            client_socket.send(protocol.create_msg(response))
            # Attempt to clean garbage from socket
            client_socket.recv(protocol.SIZE)

    # close sockets
    print("Closing connection")
    server_socket.close()
    client_socket.close()


if __name__ == '__main__':
    main()
