import socket, os, json
import constants as const

SERVER_CONTENT_PATH = 'srv_content'

print("Launching server (Sync)")
def download_file(basename : str, client_sock : socket.socket):
    print("Starting download")
    out_file = open(os.path.join(SERVER_CONTENT_PATH, basename), "wb")
    chunk = client_sock.recv(const.UPLOAD_CHUNK_SIZE)
    while chunk:
        out_file.write(chunk)
        chunk = client_sock.recv(const.UPLOAD_CHUNK_SIZE)
    out_file.close()
    print("Finish download")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((const.SERVER_HOST, const.SERVER_PORT))
    server_sock.listen(1)
    while True:
        print("Waiting for connection...")
        client_conn, client_addr = server_sock.accept()
        print("Connection get!")
        with client_conn:
            while True:
                data = client_conn.recv(4096)
                if not data:
                    print("No data")
                    break
                parsed_json = json.loads(data.decode())
                print("Received: " + data.decode())
                if(parsed_json["type"] == const.MSGTYPE_UPLOAD):
                    download_file(parsed_json["content"], client_conn)
                if(parsed_json["type"] == const.MSGTYPE_DEFAULT):
                    client_conn.sendall(parsed_json["content"].encode())