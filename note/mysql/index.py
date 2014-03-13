#! encoding=utf-8

import MySQLdb
import random

try:
    conn = MySQLdb.connect(
                host='localhost', 
                user='root',
                passwd='root',
                db='django_blog'
            )
except MySQLdb.Error, e:
    print "MySQL error %d:%s" % [e.args[0], e.args[1]]


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE  IF NOT EXISTS my_user\
                    (id int NOT NULL PRIMARY KEY AUTO_INCREMENT,\
                    name varchar(50) NOT NULL,\
                    code varchar(50) NOT NULL \
                    )'
                  )
    cursor.close()

def insert_data(conn):
    '''
    随机插入10万条数据
    '''
    cursor = conn.cursor()
    names = ((random_name(), random_code()) for i in xrange(100000))
    cursor.executemany('INSERT INTO my_user (name, code) VALUES (%s, %s)', names)
    conn.commit()

def random_name():
    a_z = [ chr(97+i) for i in range(26)]
    return ''.join(random.sample(a_z, random.randint(1,26)))

def random_code():
    
    return  ''.join((str(random.randint(0,10)) for i in range(18)))



if __name__ == '__main__':
    create_table(conn)
    insert_data(conn)

