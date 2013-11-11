SQLAlchemy 学习笔记
=====================
SQLAlchemy是Python语言事实上的ORM（Object Relational Mapper）标准实现，两个主要的组件： **SQLAlchemy ORM** 和 **SQLAlchemy Core**  。  

![架构图](http://docs.sqlalchemy.org/en/rel_0_8/_images/sqla_arch_small.png)

#####安装  
    
    pip install SQLAlchemy

检查安装是否成功:  

    >>> import sqlalchemy
    >>> sqlalchemy.__version__
    0.8.0
没有报错就代表正确安装了，连接MySQL数据库(需要MySQLdb支持)：  

    from sqlalchemy import create_engine
    DB_CONNECT_STRING = 'mysql+mysqldb://root:@localhost/test2?charset=utf8'
    engine reate_engine(DB_CONNECT_STRING,echo=False)
create_engine方法返回一个Engine实例，Engine实例只有直到触发数据库事件时才真正去连接数据库，如执行：

    engine.execute("select 1").scalar()

执行上面的语句是，sqlalchemy就会从数据库连接池中获取一个连接用于执行语句。  

####声明一个映射（declare a Mapping)

`declarative_base`类维持了一个从类到表的关系，通常一个应用使用一个base实例，所有实体类都应该继承此类对象

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

sqlalchemy 就是把Base子类转变为数据库表，定义好User类后，会生成`Table`和`mapper()`，分别通过User.__table__  和User.__mapper__返回这两个对象，对于主键，象oracle没有自增长的主键时，要使用：  

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
- NOT IN:
    query.filter(User.name.in_(['ed','x'])
- IS NULL:
    filter(User.name==None)
- IS NOT NULL:
    filter(User.name!=None)
- AND
    from sqlalchemy import and_
    filter(and_(User.name == 'ed',User.fullname=='xxx'))    
或者多次调用filter或filter_by
    filter(User.name =='ed').filter(User.fullname=='xx')
    等同于 func.add_()
- OR
- match


Django中ORM的filter方法里面只有一个等号，比如：  

    Entry.objects.all().filter(pub_date__year=2006)

all()返回列表
query = session.query(User).filter(xx)
query.all()
query.first()
query.one()有且只有一个元素时才正确返回。

####Relattionship
SQLAlchemy中的映射关系有四种,分别是**一对多**,**多对一**,**一对一**,**多对多**  
#####一对多(one to many）
一对多与多对一的区别在于其关联(relationship)的属性在多的一方还是一的一方,因为外键(ForeignKey)始终定义在多的一方.如果relationship和ForeignKey都定义在多的一方,那就是多对一,如果relationship定义在一的一方那就是一对多.  
这里的例子中,一指的是Parent,一个parent有多个child.  

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer,primary_key = True)
        children = relationship("Child",backref='parent')
    
    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer,primary_key = True)
        parent_id = Column(Integer,ForeignKey('parent.id'))

#####多对一(many to one)
这个例子中many是指parent了,意思是一个child可能有多个parent(父亲和母亲),这里的外键(child_id)和relationship(child)都定义在多(parent)的一方  

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", backref="parents")
    
    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)

为了建立双向关系,可以在relationship()中设置backref,Child对象就有parents属性.设置 `cascade= 'all'`，可以级联删除  

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

#####一对一
一对一就是多对一和一对多的一个特例,只需在relationship加上一个参数uselist=False替换多的一端就是一对一:  
从一对多转换到一对一:  

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child = relationship("Child", uselist=False, backref="parent")
    
    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
从多对一转换到一对一:  

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", backref=backref("parent", uselist=False))
    
    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
#####多对多
多对多关系需要一个中间关联表,通过参数secondary来指定,  

    from sqlalchemy import Table,Text
    post_keywords = Table('post_keywords',Base.metadata,
            Column('post_id',Integer,ForeignKey('posts.id')),
            Column('keyword_id',Integer,ForeignKey('keywords.id'))
    )

    class BlogPost(Base):
        __tablename__ = 'posts'
        id = Column(Integer,primary_key=True)
        body = Column(Text)
        keywords = relationship('Keyword',secondary=post_keywords,backref='posts')
            
    class Keyword(Base):
        __tablename__ = 'keywords'
        id = Column(Integer,primary_key = True)
        keyword = Column(String(50),nullable=False,unique=True)


#####relationship()API
[relationships api](http://docs.sqlalchemy.org/en/latest/orm/relationships.html#relationships-api),参数非常多,列举一下我用到的参数:  

- backref:在一对多或多对一之间建立双向关系,比如:  

        class Parent(Base):
            __tablename__ = 'parent'
            id = Column(Integer, primary_key=True)
            children = relationship("Child", backref="parent")
        
        class Child(Base):
            __tablename__ = 'child'
            id = Column(Integer, primary_key=True)
            parent_id = Column(Integer, ForeignKey('parent.id'))
    Prarent对象获取children,parent.children,反过来Child对象可以获取parent:child.parent.
- lazy:默认值是True,说明关联对象只有到真正访问的时候才会去查询数据库,比如有parent对象,只有知道访问parent.children的时候才做关联查询.  
- remote_side:表中的外键引用的是自身时,如Node类,如果想表示多对一的关系,那么就可以使用remote_side  

        class Node(Base):
            __tablename__ = 'node'
            id = Column(Integer, primary_key=True)
            parent_id = Column(Integer, ForeignKey('node.id'))
            data = Column(String(50))
            parent = relationship("Node", remote_side=[id])
    如果是想建立一种双向的关系,那么还是结合backref:  

        class Node(Base):
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        data = Column(String(50))
        children = relationship("Node",
                    backref=backref('parent', remote_side=[id])
                )
- primaryjoin:用在一对多或者多对一的关系中,默认情况连接条件就是主键与另一端的外键,用primaryjoin参数可以用来指定连接条件 ,比如:下面user的address必须现address是一'tony'开头:  

        class User(Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            name = Column(String)
        
            addresses = relationship("Address",
                            primaryjoin="and_(User.id==Address.user_id, "
                                "Address.email.startswith('tony'))",
                            backref="user")
        
        class Address(Base):
            __tablename__ = 'address'
            id = Column(Integer, primary_key=True)
            email = Column(String)
            user_id = Column(Integer, ForeignKey('user.id'))

- secondary:


#####association_proxy
[associationproxy](http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/associationproxy.html)是sqlalchemy扩展包里面的一个函数,是一个无关痛痒的提供便捷性的功能,在多的言语也不及官方文档的例子,还是看看文档吧.  

#####column_propety
可以用[column_property](http://docs.sqlalchemy.org/en/latest/orm/mapper_config.html#using-column-property)来实现SQL表达式作为映射类的属性(另外一种方式就是用hybrid),
 


对比Django中的ORM:  
Django 中提供了三种通用的数据库关系类型，many-to-one，many-to-many，one-to-one，  

many-to-one：  
用ForeignKey来定义多对一的关系，假设一个员工只能隶属于一个部门，但部门可以有多个员工，则可以：

    class Department(models.Model):
        ...
    
    class Employee(models.Model):
       department = models.ForeignKey(Department)
       ...

如果一个对象和自身有多对一的关系，则可以是：  

    models.ForeignKey('self'):

    class Employee(models.Model):
        manager = models.ForeignKey('self')

many-to-many：  
用ManyToManyField来定义多对多的关系，假设Blog可以有多个Tag，一个Tag也可以在多篇Blog里面，那么就可以用ManyToManyField  

    class Blog(models.Model):
        tags = ManyToManyField(Tag)
    class Tag(models.Model):
        ....

同样可以通过ManyToManyField('self')和自身建立多对多的关系.  

one-to-one:  
用OneToOneField来定义一对一的关系

相比较而言,django的orm可谓简单很多,但是性能方面未必优于sqlalchemy,不同点,sqlalchemy的model需要指定id,而django会自动帮你生成id.








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
属性在类和实例上有特殊的行为  

    from sqlalchemy import Column, Integer
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import Session, aliased
    from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
    
    Base = declarative_base()
    
    class Interval(Base):
        __tablename__ = 'interval'
    
        id = Column(Integer, primary_key=True)
        start = Column(Integer, nullable=False)
        end = Column(Integer, nullable=False)
    
        def __init__(self, start, end):
            self.start = start
            self.end = end
    
        @hybrid_property
        def length(self):
            print self
            return self.end - self.start
    
        @hybrid_method
        def contains(self,point):
            return (self.start <= point) & (point < self.end)
    
        @hybrid_method
        def intersects(self, other):
            return self.contains(other.start) | self.contains(other.end)

这个hybrid_property和python中的@property有什么区别呢？区别就在这个hybrid上，既然是混合的属性，也就是说，既可以作为实例属性
也可以作为类属性，

    if __name__ == '__main__':
        Base.metadata.create_all(engine)
        i = Interval(5, 10)
        print i.length
        print Interval.length


输出结果是：

    <__main__.Interval object at 0x9cfdd8c> ----
    5
    <class '__main__.Interval'> ----
    interval."end" - interval.start

而Interval.length的type是

    <class 'sqlalchemy.sql.expression.BinaryExpression'>

那它有什么用呢？  

    Session().query(Interval).filter(Interval.length > 10)

它的用法看起来跟属性start、end一样的，而你却无需在数据库中像start、end一样定义一个字段，多好。  

那@hibrid_method有什么用呢？ ,如果是判断point是不是contains，直接:  

    i.contains(7) 
就好了啊，干嘛要用@hibrid_method呢？

    Session().query(Interval).filter(Interval.contains(15))
看到了吧，和hybrid_property有相似之处


####区别于属性的表达式装饰器

    from sqlalchemy import func
    
    class Interval(object):
        # ...
    
        @hybrid_property
        def radius(self):
            return abs(self.length) / 2
    
        @radius.expression
        def radius(cls):
            return func.abs(cls.length) / 2
    

这里为什么还要用radius.expression呢，对于查询：  

    Session().query(Interval).filter(Interval.radius > 5)
直接像length一样不行吗?当然不行，不信，注释掉radius.expression试试。  

    TypeError: bad operand type for abs(): 'BinaryExpression'
其实它接收的是一个sqlahclemy里面的函数，func.abs，因为这里面使用的length也是一个hybrid的属性

    @length.setter
    def length(self, value):
        self.end = self.start + value

也支持setter

####mapping class inheritance hierarchies 


使用memecache做缓存的时候，出现了错误：读取一篇article，异常信息：  

    DetachedInstanceError: Parent instance <Article at 0xb22da4c> is not bound to a Session; lazy load operation of attribute 'user' cannot proceed

访问代码：  

     session = DBSession()
        @cache_region('long_term')
        def func_to_cache(session):
            article = session.query(Article).get(articleId)
            return article
    
        article = func_to_cache(session)

这段代码的意思相当于：  
   
    article = mc.get(key)
    if not article:
        article = session.query(Article).get(articleid)
        mc.set(key, article)

因为Article类还关联了user  

    userId = Column('user_id', IdDataType, ForeignKey(
        'user_profile.user_id'), nullable=False)
    user = relationship(UserProfile)

默认SQLAlchemy的实体是使用Lazyload模式，也就是说只有真正访问article.user的时候才会去数据库查询该用户，而这里事先把article缓存起来了，在访问article的时候延迟查询所使用的session跟原对象的关联被切断了。没法触发sql查询了。可以使用 eager loading，通过joinedload()，
http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
http://docs.sqlalchemy.org/en/latest/orm/loading.html



####错误总结:  
1.用column_property()函数做为类属性的时候:  

    Article.recommendCnt = column_property(select([func.count(ArticlePGoal.id)]).where(and_( 
                    Article.id == ArticlePGoal.articleId, 
                    ArticlePGoal.artType == ArticlePGoal.ART_TYPE_RECOMMEND, 
                    Article.id == ArticlePGoal.articleId, 
                    ~Article.isDeleted)))  
抛出的异常:  

    InvalidRequestError: Select statement 'SELECT count(article_pgoal.id) AS count_1 
    FROM article_pgoal, article 
    WHERE article.id = article_pgoal.article_id AND article_pgoal.art_type = %s AND article.id = article_pgoal.article_id AND NOT article.is_deleted' returned no FROM clauses due to auto-correlation; specify correlate(<tables>) to control correlation manually.

关键看错误信息的最后一句,它告诉我们需要手动指定关联的表  

    Article.recommendCnt = column_property(select([func.count(ArticlePGoal.id)]).where(and_( 
                    Article.id == ArticlePGoal.articleId, 
                    ArticlePGoal.artType == ArticlePGoal.ART_TYPE_RECOMMEND, 
                    Article.id == ArticlePGoal.articleId, 
                    ~Article.isDeleted)).correlate(Article.__table__))

2. 使用memecache做缓存的时候,异常:  

    DetachedInstanceError: Instance <Article at 0xb3b239ec> is not bound to a Session; attribute refresh operation cannot proceed

可以设置 `session.expire_on_commit = False`
