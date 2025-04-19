import socket

target_host = "127.0.0.1"
target_port = 5000

#creating socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connecting the client
client.connect((target_host, target_port))
#sending data
client.send("this is a message\r\n\r\n".encode())
#receiving the data
response = client.recv(4096)
print(response.decode())