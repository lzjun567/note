**Sphinx：SQL Phrase Index**
####主要特性：
+ 高速建立索引（10MB/sec）
+ 快速搜索（在2到4G的文本中只需0.1秒） 
+ 可扩展（上到100文本，10亿个文档，在单个CPU上面）
+ 支持分布式
+ 支持MySQL（MyIASAM和InnoDB），原生支持PostgreSQL
+ 支持词语搜索
+ 支持语法排名，相关度查询
+ 支持英语和俄语分词搜索
+ 支持 文档组
+ 支持任何数量的文档字段
+ 支持不同的搜索模式（继承匹配，全部匹配，词语匹配，匹配任意）

####下载安装
以下都是基于Linux环境下操作。  

    wget http://sphinxsearch.com/files/sphinx-2.0.7-release.tar.gz
    tar -zvxf Sphinx-2.0.7-release.tar.gz  
    cd sphinx-2.0.7-release/
    ./configure --prefix=/usr/local/sphinx --with-mysql  
    make  
    sudo make install  

--prefix=/path：该选项制定Sphinx的安装路径  
--with-mysql=/path：Sphinx会自动检测MySQL的库文件，如果没有找到，你可以制定路径  
--with-pgsql=/path：同上  
安装时出现MySQL相关错误参考：http://stackoverflow.com/questions/3095040/help-setting-up-sphinx  

####快速了解
安装完后，在安装目录（/usr/local/sphinx）用`tree`命令可以看到如下目录结构，就代表安装成功了。  

    root@60:/usr/local/sphinx# tree
    ├── bin
    │   ├── indexer
    │   ├── indextool
    │   ├── search
    │   ├── searchd
    │   └── spelldump
    ├── etc
    │   ├── example.sql
    │   ├── sphinx.conf.dist
    │   └── sphinx-min.conf.dist
    ├── share
    │   └── man
    │       └── man1
    │           ├── indexer.1
    │           ├── indextool.1
    │           ├── search.1
    │           ├── searchd.1
    │           └── spelldump.1
    └── var
        ├── data
        └── log

bin目录存放二进制执行文件  
etc目录存放配置文件  
var目录存放索引数据和搜索日志  

相关度在搜索世界中是一个非常重要的概念。MySQL也支持全文检索，你只需要在指定的字段上添加“FULLTEXT” 索引。比如：在‘'post’表的'description'字段添加全文检索索引  

    ALTER TABLE 'posts' ADD FULLTEXT(`description`);
不过这里要注意的是只有MyISAM引擎才支持全文索引。添加索引后，就可以使用语句：  

    SELECT * FROM posts WHERE MATCH (description) AGAINST('beautiful programming');
返回结果会根据相关度排序，这比使用LIKE语句速度要快不少。

####全文检索的优点
+ 相比传统搜索更快，它的优势来自于通过单词的索引查询记录取代全表扫描  
+ 查询结果可以根据相关度排序  
+ 在上百万条数据的数据库中性能表现非常好  
+ 他能跳过一些通用的词如：an for the 等等   

####Sphinx的主要组件
**indexer**：indexer用来建立或者重新建立全文本索引，默认情况Sphinx读取/usr/local/sphinx/etc/sphinx.conf配置文件。  
**searchd**：它是用来搜索索引的进程，需要客户端访问Sphinx API。  

####Sphinx简单实战

1. 创建数据库,执行脚本  

            mysql -uroot -proot test < /usr/localsphinx/etc/example.sql
2. 创建配置文件：  

            cd /usr/local/sphinx/etc
            cp sphinx-min.conf.disk sphinx.conf
    配置文件内容：

        source src1
        {
          type         = mysql
          sql_host        = localhost
          sql_user        = test
          sql_pass        =
          sql_db          = test
          sql_port        = 3306  # optional, default is 3306
          sql_query        = \
            SELECT id, group_id, UNIX_TIMESTAMP(date_added)
              AS date_added, title, content \
            FROM documents
          sql_attr_uint      = group_id
          sql_attr_timestamp    = date_added
          sql_query_info      = SELECT * FROM documents WHERE id=$id
        }
3. 创建索引：

        /usr/local/sphinx/bin/indexer --all

运行结果：

    using config file '/usr/local/sphinx/etc/sphinx.conf'...
    indexing index 'test1'...
    collected 4 docs, 0.0 MB
    sorted 0.0 Mhits, 100.0% done
    total 4 docs, 193 bytes
    total 0.045 sec, 4280 bytes/sec, 88.72 docs/sec
    skipping non-plain index 'testrt'...
    total 3 reads, 0.000 sec, 0.1 kb/call avg, 0.0 msec/call avg
    total 9 writes, 0.000 sec, 0.1 kb/call avg, 0.0 msec/call avg






创建配置文件  
cd /usr/local/sphinx/etc
cp sphinx.conf.disk sphinx.conf
sudo vim sphinx.conf
修改数据源配置，执行:

    mysql -uroot -proot test < /usr/localsphinx/etc/example.sql
运行indexer 创建全文索引  
cd /usr/local/sphinx/etc
/usr/local/sphinx/bin/indexer --all

启动searchd进程  
/usr/local/sphinx/bin/searchd  

api 测试  
cd /sphinx/api
。。。。。

Sphinx 可以通过三种不同的接口于Sphinx的搜索服务（searchd）通信
1. 原生搜索API
2. 


indexer：用于创建索引  
search：一个简单的命令行测试程序，用于测试全文索引  
searchd：守护进程，web程序可以通过这个进程进行全文检索
sphinxapi：searchd的客户端API库
spelldump：命令行工具，用于提取词条
indextool：用来转储关于索引的调试信息
mmseg：用于提供中文分词和词典处理：


sphinx配置文件:  
source:指定数据源  
index：设置索引
searchd：

http://davidx.me/2010/10/31/understanding-sphinx/

找数据--> 建索引-->提i供服务


####数据源
索引的数据可以来自：SQL数据库，纯文本，HTML文本等等，数据数据一个结构化的**文档**集合，一行就代表一个文档，每一列代表字段.  

####属性
属性是附加在每个文档上的额外信息，在搜索时可以用于过滤和排序，属性不会被全文索引，只是被存储在索引中，对属性检索时会报错。  

各个文档全部属性信息构成了一个集合，被称为文档信息，docinfo,他又两种存储方式  ：
1. 与全文索引数据分开存储（“外部存储，在.spa文件中存储） 
2. 在全文索引数据中，每出现一次文档Id，就出现相应的文档信息，（内联存储，在.spd文件中存储）

####MVA（多值属性）
对文章的tags，产品类型非常重要，他是文档属性的一中特例，他可以向文档附加一系列值作为属性。  他支持过滤和分组（不支持分组排序）

MVA列表项的值被限制为32位无符号整数，列表的长度不受限制，只有有足够的RAM

###索引

所有文档的ID必须是唯一的无符号非零整数，

建立索引的过程如下：
连接到数据库
执行预查询，以便完成所有必须的初始化设置，比如MySQL连接设置编码。
执行住查询 ,返回的数据将被索引。
执行后查询：清理工作
关闭数据库连接
对短语排序，索引后处理
再次链接到数据库连接
执行后索引查询，以便完成最终的清理工作
再次关闭到数据库的连接

###区段查询
从数据库中取出文档ID的最小值和最大值，将最大值和最小值定义自然数区间分成若干份，一次获取数据，建立索引。

可以使用”主索引+增量索引‘模式来实现“近实时”的索引更新  

设置两个数据源和两个索引，对很少更新或根本不更新的数据连理主索引，而对新增文档建立增量索引，



Sphinx要求每个记录（数据库中的记录）有id字段，
也就意味着配置文件sphinx.conf中source段的sql_query 的查询语句的第一个字段必须是唯一的，
无符号的正整数ID数字，。配置文件中，最多可以指定32个文本字段和任意数量的属性。
Sphinx会全文索引除ID（第一个字段）的属性之外的所有列。

Sphinx支持的属性类型： 

sql_attr_uint  和 sql_attr_bigint  32位无符号整数值和64位有符号整数值。整数和date类型可以使用  

sql_attr_float  

sql_attr_bool  类似mysql的tinyint值

sql_attr_timestamp   Unix时间戳   从1970-01-01 到2038-01-19.

sql_attr_string

索引的类型可以有：plain，默认   distributed  分布式的  rt：实时的，可以立即更新索引。ooo
preopen=1告诉searchd在加载时打开所有索引文件

配置文件的斜杠后面不能有任何空格


对于myisam的引擎，mysql也支持全文检索  alter table posts add fulltext('description')

select * from posts where match(descriptioin) against ('beautiful programming');


关于错误：  search test 出现的错误：
index 'test1':search error: .
解决的办法是：search -i test1 -q  'test'：指定具体的index
