1. 下载安装：http://sphinxsearch.com/downloads/beta/  
wget http://sphinxsearch.com/files/sphinx-2.0.7-release.tar.gz
tar -zvxf Sphinx-2.0.7-release.tar.gz  
cd sphinx-2.0.7-release/
./configure --prefix=/usr/local/sphinx --with-mysql  
make  
sudo make install  

2. 快速了解  
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
