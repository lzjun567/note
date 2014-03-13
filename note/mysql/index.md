####MySQL索引
索引是一种特殊的文件(InnoDB数据表上的索引是表空间的一个组成部分)，它们包含着对数据表里所有记录的引用指针。更通俗的说，数据库索引好比是一本书前面的目录，能加快数据库的查询速度。在没有索引的情况下，做查询操作的时候数据库会遍历全部数据后选择符合条件的；而有索引之后，数据库会直接在索引中查找符合条件的选项。如果SQL语句换SELECT * FROM article WHERE id=2000000”，那么在没有索引时（注：一般数据库默认都会为主键生成索引）数据库按照顺序读取完200万行数据。  
####查看索引

    show index from TABLE_NAME
    比如:
    show index from blog_blog;
    返回:
    +-----------+------------+--------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | Table     | Non_unique | Key_name           | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type |
    +-----------+------------+--------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | blog_blog |          0 | PRIMARY            |            1 | id          | A         |           5 |     NULL | NULL   |      | BTREE      |
    | blog_blog |          0 | title              |            1 | title       | A         |           5 |     NULL | NULL   |      | BTREE      |
    | blog_blog |          1 | blog_blog_6f33f001 |            1 | category_id | A         |        NULL |     NULL | NULL   |      | BTREE      |
    | blog_blog |          1 | blog_blog_e969df21 |            1 | author_id   | A         |        NULL |     NULL | NULL   |      | BTREE      |
    +-----------+------------+--------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+

####创建索引
首先我们使用[代码](xxx)创建一个my_user表,表结构如下, 里面有10万条数据, 其中name是值是随机长度的  

    mysql> show create table my_user;
    +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Table   | Create Table                                                                                                                                                                    |
    +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | my_user | CREATE TABLE `my_user` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=MyISAM AUTO_INCREMENT=200001 DEFAULT CHARSET=utf8 |
    +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.02 sec)

my_user数据表相关的文件:  

    root@lzjun:/var/lib/mysql/django_blog# ll -h my_user.*
    -rw-rw---- 1 mysql mysql  8.4K  3月 13 15:11 my_user.frm
    -rw-rw---- 1 mysql mysql  2.5M  3月 13 15:17 my_user.MYD
    -rw-rw---- 1 mysql mysql 1005K  3月 13 15:17 my_user.MYI

在name没有创建索引时,查询一条数据的时间是:0.12s  

    mysql> select * from my_user where name like 'pkhavwcrybsjoimztnq';
    +--------+---------------------+
    | id     | name                |
    +--------+---------------------+
    | 100093 | pkhavwcrybsjoimztnq |
    +--------+---------------------+
    1 row in set (0.12 sec)

#####普通索引
1. 方式一:  

        CREATE INDEX index_name on TABLE_NAME(Column_name)

        mysql> create index i_name on my_user(name);
        Query OK, 100000 rows affected (0.84 sec)
        Records: 100000  Duplicates: 0  Warnings: 0

2. 方式二:  

        ALTER  TABLE  表名  ADD   [ UNIQUE | FULLTEXT | SPATIAL ]   INDEX  
        索引名（属性名  [ (长度) ]  [ ASC | DESC]）; 

        mysql> alter table my_user add index i_name  (name);
        Query OK, 100000 rows affected (0.51 sec)
        Records: 100000  Duplicates: 0  Warnings: 0
3. 方式三:  
    直接在创建表的时候创建索引.  
    
        CREATE TABLE my_user2 ( 
                id int not null primary key auto_increment, 
                name varchar(50), 
                index iname (name));

创建索引后,相应的索引文件也增大了不少.  

#####唯一索引
普通索引允许被索引的列包含重复的值, 比如人的名字. 如果这列的值都是唯一的那么就可以使用唯一索引.他能改善查询的效率.另外一点是在有新数据插入的时候, 会自动检查新记录的字段的值是否已经存在了,如果存在MySQL会拒绝插入.因此很多场合,唯一索引的另一个目的是避免数据重复插入.  

    ALTER TABLE my_user ADD UNIQUE INDEX i_name (name);

或者是创建表的时候指定:  

    CREATE TABLE my_user(
        id int not null PRIMARY key AUTO_INCREMENT,
        name varchar(50),
        code varchar(50),
        UNIQUE KEY ui_name_code (name,code)
    )
主键与唯一索引的区别是:PRIMARY KEY is equivalent to UNIQUE NOT NULL,也就是说唯一索引的字段可以是重复的NULL.   






####设计索引原则
1. 适合做索引的列一般是WHERE字句中出现的列,或者连接子句中的列,或者ORDERBY排序子句中.而不是要查询的列.   
2. 
