import pymysql
import re

db=pymysql.connect(host="localhost",user="root",
password="123456",database="dict",charset="utf8")

cursor=db.cursor()

f= open('./dict.txt')
data = f.read()
pattern = r'\w+'
s = data.split('\n')
for x in s:
    word = re.match(pattern,x).group()
    x1=x.split(' ')
    plain1=' '.join(x1[1:])
    plain=plain1.strip()
    l=[word,plain]
    sql = 'insert into words(word,interpret) values(%s,%s)'
    cursor.execute(sql,l)
    try:
        db.commit()
    except:
        db.rollback()
f.close()