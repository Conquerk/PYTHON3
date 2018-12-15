from socket import *
import sys
import getpass

#网络连接
def main():
    if len(sys.argv) < 3 :
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    
    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print("链接服务器失败",e)
        return
    while True:
        print('=========================')
        print('| 1:注册 2:登录 3:退出  |')
        print('=========================\n')

        try:
            cmd = int(input('请输入选项'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1,2,3]:
            print('没有该选项')
            continue
        elif cmd == 1:
            do_register(s)
        elif cmd == 2:
            do_login(s)
        elif cmd == 3:
            s.send(b'E')
            sys.exit('谢谢使用')

def do_register(s):
    while True:
        name=input('User:')
        password = getpass.getpass()
        password1 = getpass.getpass('Again:')

        if (' ' in name) or (' ' in password):
            print('用户名和密码不能有空格')
            continue
        if password != password1:
            print("两次密码不一致")
            continue
        msg = 'R %s %s'%(name,password)
        #发送求情
        s.send(msg.encode())
        
        #等待回复
        data = s.recv(1024).decode()
        if data == 'OK':
            print('注册成功')
        elif data == 'EXISTS':
            print('该用户已存在')
        else:
            print('注册失败')
        return

def do_login(s):
    name = input("User:")
    password = getpass.getpass()
    msg = 'L %s %s'%(name,password)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'OK':
        print('登录成功')
        login(s,name)
    else:
        print('登录失败')

def login(s,name):
    while True:
        print('=========================')
        print('| 1:查词 2:历史 3:注销  |')
        print('=========================\n')

        try:
            cmd = int(input('请输入选项'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1,2,3]:
            print('没有该选项')
            continue
        elif cmd == 1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return

def do_query(s,name):
    while True:
        word = input('请输入单词:')
        if word == '##':
            break
        msg = 'Q %s %s'%(name,word)
        s.send(msg.encode())
        data= s.recv(1024).decode()
        if data == 'FALL':
            print('没有找到该单词')
        else:
            print(data)

def do_hist(s,name):
    msg = 'H %s'%(name)
    s.send(msg.encode())
    data=s.recv(1024).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print('没有历史记录')








if __name__ == '__main__':
    main()