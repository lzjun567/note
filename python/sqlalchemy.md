SQLAlchemy 学习笔记
=====================
SQLAlchemy是Python界事实上的ORM（Object Relational Mapper）标准。  
两个主要的组件：** ORM**  和** SQL表达式语言**  。  

![架构图](http://docs.sqlalchemy.org/en/rel_0_8/_images/sqla_arch_small.png)

安装：  
    
    pip install SQLAlchemy

检查安装是否成功:  

    >>> import sqlalchemy
    >>> sqlalchemy.__version__
    0.8.0
没有没有报错就代表正确安装了。  


连接MySQL数据库使用：

    from sqlalchemy import create_engine
    DB_CONNECT_STRING = 'mysql+mysqldb://root:@localhost/test2?charset=utf8'
    engine = create_engine(DB_CONNECT_STRING,echo=False)
create_engine方法返回一个Engine实例，Engine实例直到触发数据库事件时才真正去连接数据库

    engine.execute("select 1").scalar()

执行上面的语句是，sqlalchemy就会从数据库连接池中获取一个连接用于执行语句。  

####声明一个映射（declare a Mapping)

`declarative_base`类维持了一个从类到表的关系，通常一个应用使用一个base实例，所有实体类都应该继承此类

    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

现在就可以创建一个domain类  

    from sqlalchemy import Column,Integer,String

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer,primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)   #这里的String可以指定长度，比如：String(20)

        def __init__(self,name,fullname,password):
            self.name = name
            self.fullname = fullname
            self.password = password
        
        def __repr(self):
            
            return "<User('%s','%s','%s')>"%(self.name,self.fullname,self.password)

Base.metadataa.create_all(engine)  
sqlalchemy 就是把Base子类转变为数据库表，定义好User类后，会生成`Table`和`mapper()`，分别通过User.__table__  和User.__mapper__来访问

对于主键，象oracle没有自增长的主键时，要使用：  

    from sqlalchemy import Sequence
    Column(Integer,Sequence('user_idseq'),prmary_key=True)

####创建Session

Session是真正与数据库通信的handler，  

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
创建完session就可以添加数据了  

    ed_user = User('ed','Ed jone','edpasswd')
    session.add(ed_user)
    session.commit()

也可以使用session.add_all()添加多个对象 

    session.add_all([user1,user2,user3])

如果没有提交事务，如果是在add方后有查询，那么回flush一下，把数据刷一遍，add最终会把数据保存到数据库。

一样有session.rollback()

####查询
Query对象通过Session.query获取，query接收类或属性参数  

    for instance in session.query(User).order_by(User.id)
        print instance.name

    for name,fullname in session.query(User.name,User.fullname):
        print name,fullname

####常用过滤操作：  

- equals

    query.filter(User.name == 'ed')
- not equal

    query.filter(User.name !='ed')

- LIKE

    query.filter(User.name.like('%d%')

- IN:
    
    query.filter(User.name.in(['a','b','c'])
-NOT IN:
    
    query.filter(User.name.in_(['ed','x'])
- IS NULL:

    filter(User.name==None)

IS NOT NULL:
    
    filter(User.name!=None)
-AND

    from sqlalchemy import and_
    filter(and_(User.name == 'ed',User.fullname=='xxx'))    
或者多次调用filter或filter_by

    filter(User.name =='ed').filter(User.fullname=='xx')

- OR

- match



all()返回列表
query = session.query(User).filter(xx)
query.all()
query.first()
query.one()有且只有一个元素时才正确返回。

####Relattionship

#####一对多  （one to many）

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer,primary_key = True)
        children = relationship("Child",backref='parent')
    
    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer,primary_key = True)
        parent_id = Column(Integer,ForeignKey('parent.id'))

在one的那端设置了backref后，反过来就是多对一，在保存child时不需要显示的保存parent

    def save_child():
        parent = Parent()
        child1 = Child(parent = parent)
        child2 = Child(parent = parent)
        child3 = Child(parent = parent)
        session = Session()
        session.add_all([child1,child2,child3])
        session.flush()
        session.commit()

设置 `cascade= 'all'`，可以级联删除  

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer,primary_key = True)
        children = relationship("Child",cascade='all',backref='parent')
    
    def delete_parent():
        session = Session()
        parent = session.query(Parent).get(2)
        session.delete(parent)
        session.commit()
不过不设置cascade，删除parent时，其关联的chilren不会删除，只会把chilren关联的parent.id置为空，设置cascade后就可以级联删除children  

####Session
Session 使用 connection发送query，把返回的result row 填充到一个object中，该对象同时还会保存在Session中，Session内部有一个叫 Identity Map的数据结构，为每一个对象维持了唯一的副本。primary key 作为 key ，value就是该object。  
session刚开始无状态，直到有query发起时。

对象的变化会被session的跟踪维持着，在数据库做下一次查询后者当前的事务已经提交了时，it fushed all pendings changes to the database.   
这就是传说中的 Unit of work 模式

例如：

    def unit_of_work():
        session = Session()
        album = session.query(Album).get(4)
        album.name = "jun"   #这里不会修改album的name属性，不会触发update语句

    def unit_of_work():
        session = Session()
        album = session.query(Album).get(4)
        album.name = "jun"   #这里修改了album的name属性，会触发一个update语句
        session.query(Artist).get(11)
        session.commit()

####构造了session，何时commit，何时close
规则：始终保持session与function和objecct分离

####transaction scope  和  session scope


#####对象的四种状态
 对象在session中可能存在的四种状态包括：  

 - **Transient** ：实例还不在session中，还没有保存到数据库中去，没有数据库身份，想刚创建出来的对象比如`User()`，仅仅只有`mapper()`与之关联  
 - **Pending** ：用add()一个transient对象后，就变成了一个pending对象，这时候仍然没有flushed到数据库中去，直到flush发生。  
 - **Persistent** ：实例出现在session中而且在数据库中也有记录了，通常是通过flush一个pending实例变成Persistent或者从数据库中querying一个已经存在的实例。
 - **Detached**：一个对象它有记录在数据库中，但是不在任何session中，


#### Hibernate中的Session
SessionFactory创建Session，SessionFactory是线程安全的，而Session是线程不安全的。Session是轻量级的，创建和删除都不需要耗太大的资源，这与JDBC的connection不一样，Connection的创建时很好资源的。  
Session对象内部有一个缓存，称之为Hibernate第一级缓存，每个session实例都有自己的缓存，存放的对象是当前工作单元中加载的对象。  
Hibernate Session 缓存三大作用：  
1. 减少数据库的访问频率，提高访问性能
2. 保证缓存的对象与数据库同步，位于缓存中的对象称为持久化对象
3. 当持久化对象存在关联时，session保证不出现对象图的死锁

####Session什么时候清理缓存
1. commit()方法调用的时候
2. 查询时会清理缓存，保证查询结果能反映对象的最新状态
3. 显示调用session的flush方法
4.  


####Querying

    q = session.query(SomeMappedClass)

session的query方法就可以创建一个查询对象，





    def add_before_query():
        session = Session()
        ed_user = User(name='zhangsan')
        session.add(ed_user)
        user = session.query(User).filter_by(name='zhangsan').first()
        print ed_user == user
这里的ed_user == user 返回True，session中会根据用主键作为key，object作为vlaue缓存在session中



    def test1():
        session = Session()
        jack = session.query(User).filter_by(name='lzjun').one()
        print jack
        print jack.addresses
默认sqlalchemy 使用的时懒加载的模式，查询user的时候，并不会查询user.addresses，只有真正使用user.addresses的时候
才会触发user.addresses的查询语句。  

    from sqlalchemy.orm import subqueryload
    def subquery_load_test():
        session = Session()
        jack = session.query(User).\
                options(subqueryload(User.addresses)).\
                filter_by(name='lzjun').one()
        print jack
使用subqueryload操作，饿汉式加载，查询user的时候，就把addresses查询出来了。  


####ManyToMany

    from sqlalchemy import Table,Text
    post_keywords = Table('post_keywords',Base.metadata,
            Column('post_id',Integer,ForeignKey('posts.id')),
            Column('keyword_id',Integer,ForeignKey('keywords.id'))
    )

假如博客与关键字是多对多的关系，用Table。

    class BlogPost(Base):
        __tablename__ = 'posts'
        id = Column(Integer,primary_key=True)
        user_id = Column(Integer,ForeignKey('user.id'))
        headline = Column(String(255),nullable=False)
        body = Column(Text)
        keywords = relationship('Keyword',secondary=post_keywords,backref='posts')
    
        def __init__(self,headline,body,author):
            self.headline = headline
            self.body = body
            self.author = author
            
        def __repr__(self):
            return "BlogPost(%r,%r,%r)"%(self.headline,self.body,self.author)
    
    class Keyword(Base):
        __tablename__ = 'keywords'
        id = Column(Integer,primary_key = True)
        keyword = Column(String(50),nullable=False,unique=True)
    
        def __init__(self,keyword):
            slef.keyword = keyword

    BlogPost.author = relationship(User,backref=backref('posts',lazy='dynamic'))

secondary 用来关联中间表的  


####传统映射
用Table构建一个table metadata，然后通过映射函数mapper与User关联起来  

    from sqlalchemy import Table,Metadata
    metadata = Metadata()
    
    user = Table('user',metadata,
            Column('id',Integer,primary_key = True),
            )
    class User(object):
        def __init__(self,name):
            self.name = name
    mapper(User,user)

等价于：  

    class User(Base):
        id = Column(Integer,primary_key = True)
        name = Column(String)
        def __init__(self,name):
            self.name = name

###使用加载策略（懒加载，饿加载）
SQLAlchemy 默认使用 Lazy Loading 策略加载对象的 relationships。因此，如果你在对象 detached 之后访问对象的 relationships，会报 "DetachedInstanceError" 错误。例如：

user = session.query(User).get(id)
_session.close()
print user.comments  # this will raise DetachedInstanceError
如果你需要在对象 detach 后访问 relationships（例如需要跨进程共享对象），则应该使用 Eager Loading 策略：

session.query(User).options(joinedload('comments')).get(id)
_session.close()
print user.comments  # OK
如果需要加载所有的 relationships ，可以设置 Default Loading Strategies :

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer,primary_key = True)
        children = relationship("Child",backref='parent')
    
    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer,primary_key = True)
        parent_id = Column(Integer,ForeignKey('parent.id'))

在one的那端设置了backref后，反过来就是多对一，在保存child时不需要显示的保存parent

    def save_child():
        parent = Parent()
        child1 = Child(parent = parent)
        child2 = Child(parent = parent)
        child3 = Child(parent = parent)
        session = Session()
        session.add_all([child1,child2,child3])
        session.flush()
        session.commit()

设置 `cascade= 'all'`，可以级联删除  

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer,primary_key = True)
        children = relationship("Child",cascade='all',backref='parent')
    
    def delete_parent():
        session = Session()
        parent = session.query(Parent).get(2)
        session.delete(parent)
        session.commit()
不过不设置cascade，删除parent时，其关联的chilren不会删除，只会把chilren关联的parent.id置为空，设置cascade后就可以级联删除children  

####Session
Session 使用 connection发送query，把返回的result row 填充到一个object中，该对象同时还会保存在Session中，Session内部有一个叫 Identity Map的数据结构，为每一个对象维持了唯一的副本。primary key 作为 key ，value就是该object。  
session刚开始无状态，直到有query发起时。

对象的变化会被session的跟踪维持着，在数据库做下一次查询后者当前的事务已经提交了时，it fushed all pendings changes to the database.   
这就是传说中的 Unit of work 模式

例如：

    def unit_of_work():
        session = Session()
        album = session.query(Album).get(4)
        album.name = "jun"   #这里不会修改album的name属性，不会触发update语句

    def unit_of_work():
        session = Session()
        album = session.query(Album).get(4)
        album.name = "jun"   #这里修改了album的name属性，会触发一个update语句
        session.query(Artist).get(11)
        session.commit()

####构造了session，何时commit，何时close
规则：始终保持session与function和objecct分离

####transaction scope  和  session scope

#####对象的四种状态
 对象在session中可能存在的四种状态包括：  

 - **Transient** ：实例还不在session中，还没有保存到数据库中去，没有数据库身份，想刚创建出来的对象比如`User()`，仅仅只有`mapper()`与之关联  
 - **Pending** ：用add()一个transient对象后，就变成了一个pending对象，这时候仍然没有flushed到数据库中去，直到flush发生。  
 - **Persistent** ：实例出现在session中而且在数据库中也有记录了，通常是通过flush一个pending实例变成Persistent或者从数据库中querying一个已经存在的实例。
 - **Detached**：一个对象它有记录在数据库中，但是不在任何session中，


#### Hibernate中的Session
SessionFactory创建Session，SessionFactory是线程安全的，而Session是线程不安全的。Session是轻量级的，创建和删除都不需要耗太大的资源，这与JDBC的connection不一样，Connection的创建时很好资源的。  
Session对象内部有一个缓存，称之为Hibernate第一级缓存，每个session实例都有自己的缓存，存放的对象是当前工作单元中加载的对象。  
Hibernate Session 缓存三大作用：  
1. 减少数据库的访问频率，提高访问性能
2. 保证缓存的对象与数据库同步，位于缓存中的对象称为持久化对象
3. 当持久化对象存在关联时，session保证不出现对象图的死锁

####Session什么时候清理缓存
1. commit()方法调用的时候
2. 查询时会清理缓存，保证查询结果能反映对象的最新状态
3. 显示调用session的flush方法
4.  


















session.query(User).options(joinedload('*')).get(id)
_session.close()
print user.comments  # OK
print user.posts  # OK
======
####Relattionship

#####一对多  （one to many）




mapping class link to table metadata  



    print session.query(func.count(User.id)).all()
    print session.query(func.count(User.id)).first()
    print session.query(func.count(User.id)).scalar()


    all()返回的是list，[(10,)]
    first()返回的是tuple，(10,)，就是all()里面的的第0个元组
    scalar()返回的就是单一值，元组中的第0个值，而且scalar只使用于当前返回的是单个值，比如all()里面返回的10


####Classic mapping

    from sqlalchemy import Table, MetaData
    from sqlalchemy.orm import mapper
    metadata = MetaData()
    subject = Table('subject', metadata,
                Column('id', Integer, primary_key=True),
                Column('title', String(100))
            )
    class Subject(object):
        def __init__(self, name):
            self.name = name
    metadata.create_all(engine)  #生成数据库表
    mapper(Subject,subject)   #建立映射


####Hybrid Attributes  混合属性
属性在类级别和实例级别有特殊的属性
