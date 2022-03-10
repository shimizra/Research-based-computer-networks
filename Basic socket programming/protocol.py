"""EX 2.6 protocol implementation
   Author: Shimon Mizrahi 203375563
   Date: 24/10/2021

   ********** Documentation of the nature of the program **********
    The purpose of a protocol file is:
    to establish a communication protocol so that the server and client are synchronized.
    The server and client work against a pre-known communication protocol,
    the first 2 bits are the size of the request
   ********* end Documentation of the nature of the program *********

"""
import random
import datetime

ZERO = 0
LENGTH_FIELD_SIZE = 2
PORT = 8820
RAND = "RAND"
NAME = "NAME"
TIME = "TIME"
EXIT = "EXIT"
COMMANDS = [RAND, NAME, TIME, EXIT]
MAX_SIZE = 99


def check_cmd(data):
    """
    :param data: str => client user input
    :return: True if True input is correct, else return False
    """
    if len(data) <= MAX_SIZE and data in COMMANDS:
        return True
    return False


def create_msg(data):
    """
    :param data: str => client user input
    :return: length field size + client user input
    """
    return str(len(data)).zfill(LENGTH_FIELD_SIZE) + data


def get_msg(my_socket):
    """
    :param my_socket: str => server receive client
    :return: True + input if my_socket is correct input, else False + Error
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if length.isdigit():
        return True,  my_socket.recv(int(length)).decode()
    else:
        return False, "Error"


def create_server_rsp(cmd):
    """
    :param cmd: str => user input command only
    :return: Command solution
    """
    if cmd == RAND:
        return create_msg(str(random.randint(1, 10)))
    elif cmd == NAME:
        return create_msg("Nobody is Perfect My name is Nobody")
    elif cmd == TIME:
        return create_msg(str(datetime.datetime.now()))
    else:
        return EXIT
