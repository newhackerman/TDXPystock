import socket
cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=8818
cs.connect((host,port))
msg=cs.recv(1024)
cs.close()
print(msg.decode('utf-8'))