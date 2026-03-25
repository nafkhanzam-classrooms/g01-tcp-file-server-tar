import socket, os, json
import constants as const

print("Launching client")

def file_upload(filename : str, client_sock : socket.socket):
    basename = os.path.basename(filename)
    msg_dict = {"type":const.MSGTYPE_UPLOAD, "content":basename}
    client_sock.sendall(json.dumps(msg_dict).encode())
    file = open(filename, "rb")
    chunk = file.read(const.UPLOAD_CHUNK_SIZE)
    while chunk:
        client_sock.send(chunk)
        chunk = file.read(const.UPLOAD_CHUNK_SIZE)
    client_sock.shutdown(socket.SHUT_WR)
    print("Upload Finished")
    client_sock.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
    client_sock.connect((const.SERVER_HOST, const.SERVER_PORT))
    try:
        while True:
            message = input("> ")
            if not message:
                continue
            if len(message) > const.MESSAGE_CHAR_LIMIT:
                print("Too many characters! (limit: " + const.MESSAGE_CHAR_LIMIT + ")")
            if message.startswith("/"):
                command_args = message[1:].split()
                if(command_args[0] == "upload"):
                    if(len(command_args) < 2):
                        print("Invalid command use. USAGE: /upload <filename>")
                        continue
                    file_upload(command_args[1], client_sock)
                elif(command_args[0] == "download"):
                    if(len(command_args) < 2):
                        print("Invalid command use. USAGE: /download <filename>")
                        continue
                    
                elif(command_args[0] == "list"):
                    pass
            msg_dict = {"type":const.MSGTYPE_DEFAULT,"content":message}
            client_sock.sendall(json.dumps(msg_dict).encode())
            received = client_sock.recv(4096).decode()
            print(received)
    except KeyboardInterrupt:
        print("Keyboard interrupt!")