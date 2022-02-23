import socket
import threading
from random import randint


server_ip = 'localhost'
server_port = 3827
buffer_size = 1024

database = {}
prev = "No Prev"

hasCookie = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

print("----Server is listening----")

def checkforCookie(request):
    if "Cookie:" in request:
        hasCookie = True
    else:
        hasCookie = False
    return hasCookie

def logData(id, page):
    database[id] = page
    print(database)

def process_request(socket_request):
    global prev
    http_request = socket_request.recv(buffer_size).decode('utf-8')
    http_info = http_request.split()
    version = http_info[2]
    file = http_info[1]
    file = file.strip('/')

    userCookie = randint(0,100)

    try:
        myfile = open(file,'rb')
        requested_file = myfile.read()
        myfile.close()

        if(checkforCookie(http_info)):
            header = 'HTTP/1.1 200 OK\n\n'
            index = http_info.index('Cookie:') + 1

            logData(http_info[index], prev)

        else:
            header = 'HTTP/1.1 200 OK\r\nSet-Cookie: id= ' + str(userCookie) + ";Max-Age=3600\n\n"
            prev = "No Prev"

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        myfile = open('notFound.html','rb')
        requested_file = myfile.read()
        file = 'notFound.html'
        myfile.close()

    total_response = header.encode('utf-8')
    total_response += requested_file
    socket_request.send(total_response)
    prev = file
    socket_request.close()

while True:
    connection_socket, addr = server_socket.accept()
    threading.Thread(target=process_request, args=(connection_socket,)).start()
