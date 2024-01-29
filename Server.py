import socket
import threading
size = 1024
server_main = ""    # IPv4 Address of Server
port = 5050
disconnect = "quit"
command = "transfer"
add = (server_main , port)
format = "utf-8"
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(add)
def transfer_file(connection , address , source):
    connection.send(source.encode(format))
    file_size = connection.recv(size).decode(format)
    print(f"File size: {file_size}")
    name = input("Enter name for incoming file: ")
    file = open(name , "wb")
    file_bytes = b""
    finished = False
    while not finished:
        data = connection.recv(size)
        if data[-3:] == b"<e>":
            to_write = data[:-3]
            file_bytes += to_write
            finished = True
        else:
            file_bytes += data
    file.write(file_bytes)
    file.close()
    print(f"File {name} recieved from {address}")
def handle_client(connection , address):
    print(f"New Connection established with {address}")
    try:
        while True:
            message = input("Enter the command to execute: ")
            if message == disconnect:
                print(f"Disconnected from: {server_main}")
                connection.send(message.encode(format))
                break
            elif message[:8] == command:
                transfer_file(connection , address , message[9:])
            else:
                msg_ = message.encode(format)
                connection.send(msg_)
                msg = connection.recv(size).decode(format)
                print(f"Message from {address}: {msg}")
        connection.close()
    except OSError as e:
        print(f"Error occurred: {e}")
def init():
    server.listen()
    print(f"Listning on {server_main}")
    while True:
        connection , address = server.accept()
        thread = threading.Thread(target = handle_client , args = (connection , address))
        thread.start()
        print(f"Active Connections: {threading.active_count() - 1}")
print("The server is starting..." )
init()
               