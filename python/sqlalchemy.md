SQLAlchemy 学习笔记
=====================
SQLAlchemy算是Python界事实上的ORM（Object Relational Mapper）标准。  
两个主要的组件：ORM 和SQL表达式语言。  

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

`declarative_base`类维持了一个从类到表的关系，通常一个应用使用一个base实例  

    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

现在就可以创建一个domain类了  

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
sqlalchemy 就是把Base子类转变为数据库表

对于主键，象oracle没有自增长的主键时，要使用：  

    from sqlalchemy import Sequence
    Column(Integer,Sequence('user_idseq'),prmary_key=True)

####创建Session

Session是真正与数据库通信的handle，  

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

session.query(User).options(joinedload('*')).get(id)
_session.close()
print user.comments  # OK
print user.posts  # OK
=======
####Relattionship

#####一对多  （one to many）


