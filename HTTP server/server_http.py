# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

"""
EX 4.4 server implementation
   Completed by: Shimon Mizrahi 203375563
   Date: 24/11/2021

    ********** Documentation of the nature of the program **********
    The purpose of the program is:
    to create a server that will enable certain information according to http protocol.
   ********* end Documentation of the nature of the program *********
"""

# TO DO: import modules
import socket
import os

# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2
MESSAGE_SIZE = 1024
PART_URL = r'C:\Networks\work\Exe4.4\webroot'
DEFAULT_URL = r'\index.html'
FORBIDDEN_URL = r'\uploads\forbidden.html'
INTERNAL_SERVER_URL = r'\uploads\internalServerError.html'
MOVED_TEMPORARILY_URL = r'\uploads\moveTemporarily.html'
NEW_MOVED_TEMPORARILY_URL = "newMoveTemporarily.html"
GET = "GET"
VERSION = "HTTP/1.1"
NEW_LINE = "\r\n"
HTTP_404 = VERSION + " 404 NOT FOUND" + NEW_LINE + NEW_LINE
HTTP_200 = VERSION + " 200 OK\r\nContent-Length: "
HTTP_403 = VERSION + " 403 FORBIDDEN" + NEW_LINE + NEW_LINE
HTTP_500 = VERSION + " 500 INTERNAL SERVER ERROR" + NEW_LINE + NEW_LINE
HTTP_302 = VERSION + " 302 MOVED TEMPORARILY\r\nLocation: " + NEW_MOVED_TEMPORARILY_URL + NEW_LINE + NEW_LINE
HTML = "html"
TXT = "txt"
JPG = "jpg"
CSS = "css"
JS = "js"
ICO = "ico"
GIF = "gif"
CONTENT_TYPE_HTML_TXT = "Content-Type: text/html; charset=utf-8" + NEW_LINE
CONTENT_TYPE_IMG = "Content-Type: image/jpeg" + NEW_LINE
CONTENT_TYPE_CSS = "Content-Type: text/css" + NEW_LINE
CONTENT_TYPE_JS = "Content-Type: text/javascript; charset=utf-8" + NEW_LINE
CONTENT_TYPE_ICON = "Content-Type: image/icon" + NEW_LINE
CONTENT_TYPE_GIF = "Content-Type: image/gif" + NEW_LINE


def get_file_data(filename):
    """ Get data from file """
    with open(filename, 'rb') as file:
        data = file.read()
    return data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '/':
        url = DEFAULT_URL  # index path.
    else:
        url = resource.replace("/", "\\")  # full path.
    if not os.path.isfile(PART_URL + url):  # if not find file.
        response = HTTP_404
        client_socket.send(response.encode())
        return
    else:
        length = str(os.stat(PART_URL + url).st_size)
    type_of_file = url.split(".")[-1]
    # TO DO: check if URL had been redirected, not available or other error code. For example:
    # TO DO: send 302 redirection response
    if url == FORBIDDEN_URL:
        response = HTTP_403
        client_socket.send(response.encode())
        return
    '''
    if url == INTERNAL_SERVER_URL:
        response = HTTP_500
        client_socket.send(response.encode())
        return
    '''
    if url == MOVED_TEMPORARILY_URL:
        response = HTTP_302
        client_socket.send(response.encode())
        return
    response = HTTP_200 + length + NEW_LINE
    # TO DO: extract requested file type from URL (html, jpg etc)
    if type_of_file == TXT or type_of_file == HTML:
        header = CONTENT_TYPE_HTML_TXT
    elif type_of_file == JPG:
        header = CONTENT_TYPE_IMG
    # TO DO: handle all other headers
    elif type_of_file == CSS:
        header = CONTENT_TYPE_CSS
    elif type_of_file == JS:
        header = CONTENT_TYPE_JS
    elif type_of_file == ICO:
        header = CONTENT_TYPE_ICON
    elif type_of_file == GIF:
        header = CONTENT_TYPE_GIF
    # TO DO: read the data from the file
    result = response + header + NEW_LINE
    client_socket.send(result.encode())
    file_data = get_file_data(PART_URL + url)
    client_socket.send(file_data)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    headers_lines = request.split("\r\n")
    list_get_http = headers_lines[0].split(" ")
    if len(list_get_http) < 3:  # if incorrect http header.
        return False, None
    path = list_get_http[1]
    if not list_get_http[0] == GET or not list_get_http[2] == VERSION:  # if incorrect http fields.
        return False, None
    return True, path


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        # ...
        client_request = client_socket.recv(MESSAGE_SIZE).decode()
        print(client_request)
        valid_http, resource = validate_http_request(client_request)

        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            # General Error: 500
            response = HTTP_500
            client_socket.send(response.encode())
            print('Closing connection')
            # if Error => close connection
            client_socket.close()
            break


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print('New connection received')
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except socket.timeout as e:
            print("Error! Time out:{}".format(e))


if __name__ == "__main__":
    # Call the main handler function
    main()
