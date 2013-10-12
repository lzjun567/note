###Sphinx：SQL Phrase Index  基于SQL的全文检索引擎
####主要特性：
+ 高速建立索引（10MB/sec）
+ 快速搜索（在2到4G的文本中只需0.1秒） 
+ 可扩展（可达100G文本，10亿个文档）
+ 支持分布式
+ 支持MySQL（MyIASAM和InnoDB），原生支持PostgreSQL
+ 支持词语搜索
+ 支持短语相似度排名，相关度查询
+ 支持英语和俄语分词搜索
+ 支持文档组
+ 支持任何数量的文档字段
+ 支持不同的搜索模式（继承匹配，全部匹配，词语匹配，匹配任意）

####下载安装
以下都是基于Linux Ubuntu发行版环境下的操作。  

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
如果需要支持中文检索，建议参考下面这段  
####基于Sphinx检索引擎的coorseek安装配置（适用于中文环境）

1. 下载地址：[coreseek4.1](http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz)
2. 预安装包：

        apt-get install make gcc g++ automake libtool mysql-client libmysqlclient15-dev   libxml2-dev libexpat1-dev

3. 安装mmseg分词库

        tar -zvxf coreseek
        cd mmseg
        ./bootstrap
        ./configure --prefix=/usr/local/mmseg3
        make
        make install

4. 安装coreseek 

        cd csft
        sh buildconf.sh
        ./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql
        make
        make install

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

#####sphinx工作流概览
![dataflow](../../resource/image/dataflow.png)
由四个主要的组件构成：  
**数据源** 是真正存储数据的地方，比如MySQL  
**indexer** indexer从数据源获取数据，创建全文本索引数据。  
**searchd** searchd与客户端程序通信，使用索引快速处理查询，此外，它还能处理结果集（包括过滤、排序、分组等）  
![interaction](../../resource/image/interaction.png)

**相关度** 在搜索世界中是一个非常重要的概念。MySQL也支持全文检索，你只需要在指定的字段上添加“FULLTEXT” 索引。比如：在‘'post’表的'description'字段添加全文检索索引  

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

    打印结果：

        using config file '/usr/local/sphinx/etc/sphinx.conf'...
        indexing index 'test1'...
        collected 4 docs, 0.0 MB
        sorted 0.0 Mhits, 100.0% done
        total 4 docs, 193 bytes
        total 0.045 sec, 4280 bytes/sec, 88.72 docs/sec
        skipping non-plain index 'testrt'...
        total 3 reads, 0.000 sec, 0.1 kb/call avg, 0.0 msec/call avg
        total 9 writes, 0.000 sec, 0.1 kb/call avg, 0.0 msec/call avg

4. 查询索引  

        /usr/local/sphinx/bin/search test
    如果报错："index 'test1':search error" ，那么指定具体的index：   

        /usr/local/sphinx/bin/search -i test1 -q  'test' 

    查询结果：  

        using config file '/usr/local/sphinx/etc/sphinx.conf'...
        index 'test1': query 'test ': returned 3 matches of 3 total in 0.000 sec
        
        displaying matches:
        1. document=1, weight=2421, group_id=1, date_added=Wed Jun  5 08:00:56 2013
        2. document=2, weight=2421, group_id=1, date_added=Wed Jun  5 08:00:56 2013
        3. document=4, weight=1442, group_id=2, date_added=Wed Jun  5 08:00:56 2013
        
        words:
        1. 'test': 3 documents, 5 hits

如果使用第三方客户端API请求，需要启动searchd进程：  

    /usr/local/sphinx/bin/searchd

####简单介绍Sphinx配置文件
配置文件分成如下几部分：  
+ **source**：创建索引时需要用到的数据源  

        source src1
        {
                type                    = mysql
        
                sql_host                = localhost
                sql_user                = root
                sql_pass                = cloud
                sql_db                  = test
                sql_port                = 3306  # optional, default is 3306
        
                sql_query_pre           = SET NAMES utf8
                sql_query               = \
                        SELECT id, group_id, UNIX_TIMESTAMP(date_added) AS date_added, title, content \
                        FROM documents
        
                sql_attr_uint           = group_id
                sql_attr_timestamp      = date_added
        
                sql_query_info          = SELECT * FROM documents WHERE id=$id
        }
sql_query：获取待索引数据查询，最多可以指定32个数据字段，这些字段都会被全文检索  
sql_query_pre： 执行sql_query前的查询，可以有多个，按照配置文件顺序执行，于查询的结果会被忽略。它一般用于设置字符集编码，标记索引的记录，更新内部计数器等。  
sql_attr：属性，属性是附加在每个文档上的额外信息，可以在搜索的时候用于过滤和排序。下面详细介绍属性  

####属性
搜索除了根据文档的匹配度和相关度排序外，还经常会根据其它方式对结果进行额外处理，如：用户需要对新闻检索结果依次按日期和相关度排序，或者将检索结果按月分组，Sphinx的属性就能完成上述任务。  
属性于字段不一样，它不会被全文检索，仅仅是存储在索引中。属性可以用于过滤，或者限制返回的数据，以及排序、分组。  

论坛帖子表是一个很好的例子。假设只有帖子的标题和内容这两个字段需要全文检索，但是有时检索结果需要被限制在某个特定的作者的帖子或者属于某个子论坛的帖子中（也就是说，只检索在SQL表的author_id和forum_id这两个列上有特定值的那些行），或者需要按post_date列对匹配的结果排序，或者根据post_date列对帖子按月份分组，并对每组中的帖子计数。  

为实现这些功能，可以将上述各列（除了标题和内容列）作为属性做索引，之后即可使用API调用来设置过滤、排序和分组。以下是一个例子：  

示例： sphinx.conf 片段:  

    ...
    sql_query = SELECT id, title, content, \
    	author_id, forum_id, post_date FROM my_forum_posts
    sql_attr_uint = author_id
    sql_attr_uint = forum_id
    sql_attr_timestamp = post_date
    ...
示例： 应用程序代码 (使用 PHP):  

    // 仅搜索ID为123的作者发布的内容
    $cl->SetFilter ( "author_id", array ( 123 ) );
    
    // 仅在id为1，3，7的子论坛中搜索
    $cl->SetFilter ( "forum_id", array ( 1,3,7 ) );
    
    // 按照发布时间倒序排列获取的结果
    $cl->SetSortMode ( SPH_SORT_ATTR_DESC, "post_date" );

示例：  


    sql_query_pre = REPLACE INTO sph_tag_counter SELECT 1,MAX(id) FROM subject_tag


+ **index**：指定索引数据的方法路径以及如何存放  

        index test1
        {
                source                  = src1
                path                    = /usr/local/sphinx/var/data/test1
                docinfo                 = extern
                charset_type            = sbcs
        }

charset_type：设置文档的编码，可以为sbcs（single-byte）和UTF-8  
+ **indexer**：indexer程序相关配置  
+ **searchd**：搜索索引时 searchd程序相关配置  

        searchd
        {
                listen                  = 9312
                listen                  = 9306:mysql41
                log                     = /usr/local/sphinx/var/log/searchd.log
                query_log               = /usr/local/sphinx/var/log/query.log
                read_timeout            = 5
                max_children            = 30
                pid_file                = /usr/local/sphinx/var/log/searchd.pid
                max_matches             = 1000
                seamless_rotate         = 1
                preopen_indexes         = 1
                unlink_old              = 1
                workers                 = threads # for RT to work
                binlog_path             = /usr/local/sphinx/var/data
        }

执行indexer时错误提示：  

    FATAL: failed to lock /usr/local/sphinx/var/data/test1.spl: Resource temporarily unavailable, will not index. Try --rotate option.

如果searchd进程启动了，那么先关闭它。或者 使用在indexer后面加参数`--rotate`，但是该参数在Windows环境下(2.1.1)的版本下不起作用

####使用Sphinx全文检索的好处
+ 快速建立索引，比MySQL的全文检索快上50到100倍，比其他全文检索快4到10倍
+ 更高的检索速度
+ 相关性
+ 良好的扩展性

Sphinx的作者Andrew Aksyonoff 在5GB文本，3百50万条记录中做的性能测试结果：  

    -------------------------------------------------------
                             MySQL       Lucene      Sphinx
    -------------------------------------------------------
    Indexing time, min       1627        176         84
    Index size, MB           3011        6328        2850
    Match all, ms/q          286         30          22
    Match phrase, ms/q       3692        29          21
    Match bool top-20, ms/q  24          29          13
    -------------------------------------------------------

####Indexing
索引在Sphinx中是最重要的组件之一。  
#####什么数据库索引
在数据库中，用于提高数据库表访问速度的数据库对象，虽然索引可以提高查询速度，但是它会导致数据库系统更新数据的性能下降，因为更新数据的时候同时要更新索引。  
#####sphinx中的索引
Sphinx中的索引与数据库索引有所区别，sphinx中的索引数据是结构化 **文档** 的集合，每个文档是字段（field）的集合。一行代表一个文档，每一列代表一个字段。索引还可以包含属性（attributes）用于过滤、排序、分组，这些属性不会被全文检索，仅仅是被存储在索引中。  

举例：论坛帖子表中帖子的标题和内容这两个字段需要全文检索，但是检索结果需要限制在某个特定的作者，或者按照post_date对结果排序，实现这个功能可以将出了标题和内容的各列作为属性来做索引，之后使用API调用设置过滤、排序等操作。  
sphinx.conf片段：  

    sql_query = SELECT id, title, content, \
    	author_id, forum_id, post_date FROM my_forum_posts
    sql_attr_uint = author_id
    sql_attr_uint = forum_id
    sql_attr_timestamp = post_date

应用程序代码：

    // only search posts by author whose ID is 123
    $cl->SetFilter ( "author_id", array ( 123 ) );
    
    // only search posts in sub-forums 1, 3 and 7
    $cl->SetFilter ( "forum_id", array ( 1,3,7 ) );
    
    // sort found posts by posting date in descending order
    $cl->SetSortMode ( SPH_SORT_ATTR_DESC, "post_date" );


属性支持的数据类型包括：  

+ 无符号整数（1-32位宽）;
+ UNIX 时间戳（timestamps）;
+ 浮点值（32位，IEEE 754单精度）;
+ 字符串序列 (尤其是计算出的整数值);
+ 多值属性 MVA( multi-value attributes ) (32位无符号整型值的变长序列).

属性的作用：过滤，排序，分组  

不同的索引类型为不同的任务设计，基于磁盘的B-Tree存储结构的索引更新起来比较简单（容易向已有的索引中插入新的文档），但是搜索起来比较慢。Sphinx为了最优化建立索引和检索速度而设计，因此它更新索引时很慢的，理论上更新索引甚至比从头重建索引还要慢。不过大多数情况下可以通过建立多个索引来解决索引更新慢的问题，更多参考： ** 实时更新索引**  

实时索引采用“主索引+增量索引”（main+delta）模式来实现“近实时”的索引更新。基本思路是设置两个数据源和两个索引，对更新或根本不更新的数据建立主索引，对新增文档建立增量索引。增量索引的更新频率可以非常快，文档可以在出现几分钟内就可以被检索到。  
确定具体某一文档分属哪个索引的分类工作可以自动完成，一个可选方案是建立一个计数器，记录将文档集分成两部分和那个文档ID，每次重新构建主索引时，这个表都会被更新。 

    CREATE TABLE sph_counter
    (
        counter_id INTEGER PRIMARY KEY NOT NULL,
        max_doc_id INTEGER NOT NULL
    );
    # in sphinx.conf
    source main
    {
        # ...
        sql_query_pre = REPLACE INTO sph_counter SELECT 1, MAX(id) FROM documents
        sql_query = SELECT id, title, body FROM documents \
            WHERE id<=( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )
    }
    source delta : main
    {
        sql_query_pre =
        sql_query = SELECT id, title, body FROM documents \
            WHERE id>( SELECT max_doc_id FROM sph_counter WHERE counter_id=1 )
    }
    index main
    {
        source = main
        path = /path/to/main
        # ... all the other settings
    }
    # note how all other settings are copied from main,
    # but source and path are overridden (they MUST be)
    index delta : main
    {
        source = delta
        path = /path/to/delta
    }



一个索引的数据可以来自多个数据源，这些数据将严格按照配置文件中定义的顺序进行处理，所有从这些数据源获取到的文档将被合并，合并索引一般比重新索引快。基本语法：  

    indexer --merge des_index src_index [--rotate]
src_index将被合并到des_index中去，如果des_index已经用于searrchd提供服务，则必须加参数--rotate。
####多值属性
定义的格式如下：  
    
    sql_attr_multi = unit tag_id from query;\
                    SELECT subject_id,tag_id FROM subject_subject_tags
程序中可以这样调用：  

    int[] tags = {25770,5};
	cl.SetFilter("tag_id", tags, false);
只保留包含tag id 为 25770、5的subject
    





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

找数据--> 建索引-->提供服务


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


####索引合并：  

    indexer --merge DST_INDEX SRC_INDEX [--ratate]

属性


SPH_SORT_TIME_SEGMENTS 这种排序模式在windows平台好像不生效，搜出来的结果是空

[中文分词核心配置](http://www.coreseek.cn/products-install/coreseek_mmseg/)

####搜索c++,.net 等关键字时：
在index中配置

    exceptions:   /path/to/exception.txt
执行命令：

    mmseg -b /path/to/exception.txt

生成的synonyms.dat 拷贝到uni.lib所在目录

exception.txt:

    C/C++ => cdpluspluscd
    c/C++ => cdpluspluscd
    c/c++ => cdpluspluscd
    C/c++ => cdpluspluscd
    C++ => dplusplusc
    c++ => dplusplusc
    C# => csharpcs
    c# => csharpcs
    J++ =>jshhdjs
    j++ => jshhdjs
    J# => jshhhejs
    j# => jshhhejs
    .NET => dotnet
    .net => dotnet
    * => asterisk
    R&B => rhythmblues
    VB.NET => vbdontnetvb
    vB.NET => vbdotnetvb



=================================
sphinx-coreseek 优化指南
=================================
####html_strip：HTML标记清除

只保留标记之间的内容，HTML标签和HTML注释会被删除。比如:  

    <a href="http://www.google.com">google</a>
开启html_strip=1后，就只保留内容google。默认情况html_strip的值是0，表示禁用，1表示启用。如果要把标签之间的内容也删除的话，那么就要使用**html_remove_elements** 属性了。    

看下面这个例子：  
![search_html](../../resource/image/html_search0.png)
第一条记录看上去就是无相关的，点进去看了下，就是一个一个视频链接，里面有这么一段：  

    <embed src="http://player.youku.com/player.php/Type/Folder/Fid/18841125/Ob/1/sid/XNTA1MTg0NDg0/v.swf" 
    type="application/x-shockwave-flash" width="660" height="500" autostart="true" loop="true">

这个embed标签里面有一个链接包含php的字符。我们设置html_strip=1，再来看结果就只有一条记录了。  
 ![search_html1](../../resource/image/html_search1.png)

####exceptions：
在搜索c++、c#等词的时候，包含c的内容都搜索出来了，显然这不是我们想要的，exceptions的功能就是将一个或多个Token映射成一个单独的关键字，与wordforms类似，但是也有很多不同的地方。  

![exception](../../resource/image/exceptions0.png)

* exceptions 大小写敏感，wordforms大小写无关  
* exeptions 可以使用charset_table中没有的特殊符号，wordforms完全遵从charset_table。  

示例：  

    AT & T => AT&T
    AT&T => AT&T
    Standarten   Fuehrer => standartenfuhrer
    Standarten Fuhrer => standartenfuhrer
    MS Windows => ms windows
    Microsoft Windows => ms windows
    C++ => cplusplus
    c++ => cplusplus
    C plus plus => cplusplus

注意 “=》”的字符串都是单个完成的字符串，无论是"&"还是空格“ ”都是看作单个字符串的一部分。  
![exception](../../resource/image/exceptions1.png)  

你妹的，exception和wordform还相互影响   

####wordforms：词形字典

    wordforms = /usr/local/sphinx/data/wordforms.txt

用来将不同形式的词形编程单一的标准形式，如："microsoft、ms、微软"变成同一的形式microsoft。格式是：  

    ms > microsoft
    微软 > microsoft

![wordform](../../resource/image/wordform.png)  
目标词形(microsoft)只能是单个词，比如：  

     zhang san > 张三
查询chang san 的时候，只匹配张，就是说只要是含有“张”字的都匹配，无论是张三还是张四。  

####一元切分模式
有时候使用一元切分模式，反而降低的搜索的准确率。比如我在搜索”小小“时，使用一元分词后，凡是含有”小“字的内容都被搜索出来了。显然不是我们想要的。  
![yiyuan0.png](../../resource/image/yiyuan.png)  

一元分词的详细配置在http://www.coreseek.cn/products-install/ngram_len_cjk/ ，如果不想启动一元分词时，charset_type=utf-8，要改成 charset_type=zh_cn.utf-8,否则是搜出去东西来的。  



####sphnix的匹配模式
* SPH_MATCH_ALL:匹配所有查询此，这是sphinx的默认模式，比如搜索：“中国"，那么只有文档中同时出现”中国“二字时才会匹配，当然“中国”可以不出现在一块.  
* SPH_MATCH_ANY:匹配任意一个  
* SPH_MATCH_PHRASE



####数据源的一些限制条件

document 的 id 必须是唯一的无符号的非0的整数，直白点就是要大于0的整数，至于是32位还是64位的根据自己的喜好设定。我们的线上环境就有一个id为-1的数据，搜不出来，该主键是非常麻烦的，所以在新建数据的时候就要特别注意。  
