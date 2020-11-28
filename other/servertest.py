import socket
import sys
import os
ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=8818
ss.bind((host,port))
ss.listen(5)
while True:
    print("listen...")
    cs ,addr=ss.accept()
    print("连接地址: %s" % str(addr))
    msg = '欢迎访问菜鸟教程！' + "\r\n"
    cs.send(msg.encode('utf-8'))
    cs.close()




