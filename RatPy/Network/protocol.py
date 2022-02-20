import base64
import hashlib

FORMAT = "ascii"

class Binary:
    def encode_binary(base64):
        binary_form = int.from_bytes(base64, "big")
        final_binary = bin(binary_form)
        return final_binary

    def decode_binary(binary):
        bianary_integer = int(binary, 2)
        byte_num = bianary_integer.bit_length() + 7 // 8

        text_encoded = bianary_integer.to_bytes(byte_num, "big")
        text = text_encoded.decode()
        return text

class Network:
    def send_command(conn, mes, client_name):
        encoded_com = mes.encode(FORMAT)
        b64_command = base64.b64encode(encoded_com)
        hashed_command = hashlib.sha256(b64_command).hexdigest()
        binary_b64 = Binary.encode_binary(b64_command)

        conn.send(binary_b64.encode())
        conn.send("\n".encode(FORMAT))

        conn.send(hashed_command.encode(FORMAT))
        conn.send("\n".encode(FORMAT))

        
        conn.send(client_name.encode(FORMAT))
        conn.send("\n".encode(FORMAT))

    
    def recv_command_client(conn):
        key_binary = ""
        command = ""
        client_name = ""
        
        while "\n" not in key_binary:
            key_recv = conn.recv(1).decode(FORMAT)
            key_binary += key_recv
        
        key_b64 = Binary.decode_binary(key_binary)
        
        while "\n" not in command:
            command_recv = conn.recv(1).decode(FORMAT)
            command += command_recv

        while "\n" not in client_name:
            client_recv = conn.recv(1).decode(FORMAT)
            client_name += client_recv
        
        hashed_command = hashlib.sha256(key_b64.encode(FORMAT)).hexdigest()

        if hashed_command == key_b64:
            final_command = base64.b64decode(key_b64.encode(FORMAT))
            return "{} \n".format(final_command.decode(FORMAT))
        else:
            final_form = base64.b64decode(key_b64.encode(FORMAT))
            return final_form.decode(FORMAT)
        
    def recv_command_server(conn):
        key_binary = ""
        command = ""
        client_name = ""
                
        while "\n" not in key_binary:
            key_recv = conn.recv(1).decode(FORMAT)
            key_binary += key_recv
                
        key_b64 = Binary.decode_binary(key_binary)
                
        while "\n" not in command:
            command_recv = conn.recv(1).decode(FORMAT)
            command += command_recv

        while "\n" not in client_name:
            client_recv = conn.recv(1).decode(FORMAT)
            client_name += client_recv
                
        hashed_command = hashlib.sha256(key_b64.encode(FORMAT)).hexdigest()
        if hashed_command == key_b64:
            final_command = base64.b64decode(key_b64.encode(FORMAT))
            return "{} \n".format(final_command.decode(FORMAT))
        else:
            final_form = base64.b64decode(key_b64.encode(FORMAT))

    
        print("Received from: {}".format(client_name))
        return final_form.decode(FORMAT)

if __name__ == "__main__":
    Network()