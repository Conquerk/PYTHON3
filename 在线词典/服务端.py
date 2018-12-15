'''
name:tedu
modules:pymsql
this is a dict project for AID
'''

from socket import *
import os,sys
import pymysql
from threading import Thread
import time
#定义全局变量
DICT_TEXT = './dict.txt'
HOST='0.0.0.0'
PORT=8000
ADDR=(HOST,PORT)

#处理僵尸
def zombie():
    os.wait()

def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict')
    #创建套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    print("listen to 8844....")

    #循环等待客户端连接
    while True:
        try:
            c,addr=s.accept()
            print('connect from ',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print("服务器异常",e)
            continue
        
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c,db) #子进程函数
        else:
            c.close()
            t = Thread(target= zombie)
            t.setDaemon(True)
            t.start()
            continue

def do_child(c,db):
    while True:
        #接收客户端请求
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if(not data) or data[0] == 'E':
            print('客户端退出')
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)

def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor=db.cursor()

    sql= 'select * from user where name =%s'
    cursor.execute(sql,[name])
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXISTS')
        return

    sql = 'insert into user (name,password) values (%s,%s)'
    try:
        cursor.execute(sql,[name,password])
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FALL')
def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor= db.cursor()

    sql = 'select * from user where name = %s and password = %s'

    cursor.execute(sql,[name,password])
    r = cursor.fetchone()
    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')
def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
        sql='insert into hist(name,word,time) values(%s,%s,%s)'
        try:
            cursor.execute(sql,[name,word,tm])
            db.commit()
        except:
            db.rollback()
    #使用单词本查找
    try:
        f = open(DICT_TEXT)
    except:
        s.send(b'FALL')
        return
    for line in f :
        tmp = line.split(' ')[0]
        if tmp > word :
            c.send(b'FALL')
            f.close()
            return
        elif tmp == word:
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FALL')
    f.close()
def do_hist(c,db,data):
    l= data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql = 'select * from hist where name=%s'
    cursor.execute(sql,[name])
    r= cursor.fetchall()
    if not r:
        c.send(b'FALL')
    else:
        c.send(b'OK')
        time.sleep(0.1)
        for i in r:
            msg = 'name:%s  word:%s  time:%s'%(i[1],i[2],i[3])
            c.send(msg.encode())
            time.sleep(0.1)
        c.send(b'##')
            

if __name__ == '__main__':
    main()