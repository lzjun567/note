# -*- encoding:utf-8 -*-
import sqlalchemy
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship,backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()   #1.构建基类
engine = sqlalchemy.create_engine("mysql+mysqldb://root:@localhost/test2?charset=utf8",echo=True)
#2. 创建引擎

class Artist(Base):
    __tablename__ = 'artist'
    artist_id = Column('id',Integer,primary_key=True)
    name = Column('name',String(100))
    albums = relationship('Album',cascade='all,delete',backref='artist')   #定义在一的这一端就是这么写
                                                                            # album对象可以 通过album.artist对象访问他的artist
#http://stackoverflow.com/questions/5033547/sqlachemy-cascade-delete

class Album(Base):
    __tablename__ = 'album'
    album_id = Column('id',Integer,primary_key=True)
    name = Column('name',String(100))
    artist_id = Column('artist',ForeignKey('artist.id'))  #注意下这里的外键，就是关联对象的id属性
    #artist = relationship(Artist,backref=backref('albums',cascade='all,delete'))    #设置backref后，通过artist对象直接访问它有哪些albums --〉 artist.albums
                                                                                    #还有级联删除，删除artist后，相关的album也会被删除
                                                                                    #这里要明确调用backref函数

Session = sessionmaker(bind=engine)  #3、连接数据库的session
Base.metadata.create_all(engine)    #4.初始化表结构

def save_artist():
    artist = Artist(name='aki misawa')
    session = Session()
    try:
        session.add(artist)
        session.flush()
        #print "artist id:",artist.artist_id
        session.commit()
    finally:
        session.close()
    print "artist id:",artist.artist_id

def save():
    artist = Artist(name='liuzhijun3')
    album = Album(name='hello3',artist=artist)
    album = Album(name='hello4',artist=artist)
    session = Session()

    try:
        session.add(album)
        session.commit()
    finally:
        session.close()

def list_all():
    
    try:
        session = Session()
        print "artists"
        print type(session.query(Artist).all())
        for a in session.query(Artist).all():
            print 'artist name:',a.name
            for album in a.albums:
                print 'album name:',album.name

        for a in session.query(Album).all():
            print a.name
            print a.artist.name
    finally:
        session.close()


def remove():
    session = Session()
    artist = session.query(Artist).get(6)
    session.delete(artist)
    session.commit()
    session.close()

if __name__ == '__main__':
    list_all()
