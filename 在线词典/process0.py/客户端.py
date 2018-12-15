from socket import *
import sys

s = socket()
addr=('0.0.0.0',4444)
s.connect(addr)

data=s.recv(1024)
data= data.decode()
print(data)
cute = input('请输入要进行的操作>>')
s.send(cute.encode())
if cute == "C":
    s.close()
    sys.exit('客户端退出')

