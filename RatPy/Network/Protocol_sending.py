import os
import binascii
import base64

class Serialize:
    def serialize_mes(mes):
        length = len(mes)
        final_length = str(length).encode()
        return final_length
    
    def deserialize_mes(byte):
        string_length = byte.decode()
        length_to_recv = int(string_length)
        return length_to_recv

class B64:
    def encode_b64(mes):
        mes = binascii.b2a_base64(mes, newline=False)
        return mes

    def decode_b64(data):
        byte_encoded = data.encode()
        b64_bytes = base64.b64decode(byte_encoded)
        data_text = b64_bytes.decode()
        return data_text
        

class File_protocol:
    def send_file(conn, path, title):
        data = open(path, "rb")
        size_file = os.path.getsize(path)
        data_file = data.read(size_file)

        b64_data = B64.encode_b64(data_file)

        serialized_title = Serialize.serialize_mes(title)
        conn.send(serialized_title)
        conn.send(title.encode())

        conn.send(b64_data)
        conn.send("\n".encode())

    
    def recv_file(conn):
        title = ""
        file_data = ""
        
        length = conn.recv(4)
        deserialized_length = Serialize.deserialize_mes(length)
        title_recv = conn.recv(deserialized_length).decode()
        title += title_recv

        while "\n" not in file_data:
            file_recv = conn.recv(1).decode()
            file_data += file_recv
        
        data_decoded = B64.decode_b64(file_data)

        file = open(title, "wb")
        file.write(data_decoded.encode())
        file.close()


if __name__ == "__main__":
    File_protocol()