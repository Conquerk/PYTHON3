from socket import *
import sys
from multiprocessing import Process
class fuwu(object):
    def __init__(self,ADDR):
        self.ADDR=ADDR
        self.create_socket()
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.ADDR)
    def jiemian(self):
        self.sockfd.listen()
        print('等待客户端连接')
        while True:
            try:
                connfd,addr = self.sockfd.accept()
                print('客户端连接',addr)
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务端退出')
            t = Process(target = self.handler,args = (connfd,))
            t.Daemon=True
            t.start()
    def handler(self,connfd):
        data = '=========================\n'
        data+= '| A:登录 B:注册 C:退出  |\n'
        data+= '========================='
        connfd.send(data.encode())
        connfd.close()
        cute = connfd.recv(1024).decode()
        if cute == 'A':
            self.denglu(connfd)
        if cute == 'B':
            self.zhuce(connfd)
    def denglu(self,connfd):
        connfd.send('登录'.encode())
    def zhuce(self,connfd):
        connfd.send('登录'.encode())




if __name__ == "__main__":
    ADDR=('0.0.0.0',4444)
    guanli = fuwu(ADDR)
    guanli.jiemian()#启动界面