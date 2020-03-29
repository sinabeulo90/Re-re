import socket

HOST = ""
PORT = 10011
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

print ('tcp server :: server wait...')

while True:
	connection, clientAddress = serverSocket.accept()
	print ("tcp server :: connect :", clientAddress)

	message = [{'id': '9bZkp7q19f0', 'seconds': [5, 6, 8, 18, 33, 47, 55, 56, 69, 76, 88, 89, 90, 109, 111, 114, 128, 131, 136, 137, 144, 145, 152, 176, 196, 201, 203, 207, 208, 225, 226, 227, 236, 238, 242, 248, 250], 'title': '싸이 노래'}]
	message = str(message)
	while True:
		data = connection.recv(1024).decode()
		print(data)

		if not data or len(data) < 1024:
			break

	connection.sendall(message.encode())

connection.close()


"""

	while True:
		data = connection.recv(1024).decode()
		message += data

		if not data or len(data) < 1024:
			break

"""
