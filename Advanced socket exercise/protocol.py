#   Ex. 2.7 template - protocol

LENGTH_FIELD_SIZE = 4
MAX_SIZE = 9999
PORT = 8820
DIR = "DIR"
DELETE = "DELETE"
COPY = "COPY"
EXECUTE = "EXECUTE"
TAKE_SCREENSHOTS = "TAKE_SCREENSHOTS"
PHOTO_SEND = "SEND_PHOTO"
EXIT = "EXIT"
COMMANDS = [DIR, DELETE, COPY, EXECUTE, TAKE_SCREENSHOTS, PHOTO_SEND, EXIT]
SIZE = 1024


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    cmd = data.split(" ")
    if cmd[0] in COMMANDS and len(data) <= MAX_SIZE:
        if (cmd[0] == DIR or cmd[0] == DELETE or cmd[0] == EXECUTE) and len(cmd) == 2:
            return True
        elif cmd[0] == COPY and len(cmd) == 3:
            return True
        elif (cmd[0] == TAKE_SCREENSHOTS or cmd[0] == EXIT or cmd[0] == TAKE_SCREENSHOTS or cmd[0] == PHOTO_SEND) \
                and len(cmd) == 1:
            return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    return (str(len(str(data))).zfill(LENGTH_FIELD_SIZE) + str(data)).encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if length.isdigit():
        try:
            return True, my_socket.recv(int(length)).decode()
        except NameError:
            return False, "Error"
    else:
        return False, "Error"
