####基本概念
在Solr中，文档(Document)是搜索和索引的基本单元，一个索引由一个或多个文档构成，而一个文档是由一个或者多个字段(Field)组成的。文档对应于数据库中表的一行，而字段对应的是表中的某一列。  

#####Schema
给Solr添加文档前，需要指定schema，schema的表现形式就是文件schema.xml，在文档已经添加到索引中去了以后则不建议再去修改该文件。  

schema中声明有：

* 有哪些类型的字段
* 哪种字段应该作为主键/唯一键
* 哪些字段是必须的
* 如何索引和搜索每个字段

#####字段类型
在Solr中，每个字段都有一个类型，Solr队Lucene中的字段进行了扩展，Solr中基本的数据类型包括：  

* float
* long
* double
* date
* text
同时Solr还允许你自定义字段类型，只需要绑定好filters和tokenizers。例如：  

    <fieldtype name="phonetic" stored="false" indexed="true" class="solr.TextField" >
      <analyzer>
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.DoubleMetaphoneFilterFactory" inject="false"/>
      </analyzer>
    </fieldtype>

####定义字段
声明一个字段时，如下所示：

    <field name="id" type="text" indexed="true" stored="true" multiValued="true"/>
* name：字段的名称
* type：字段的类型
* indexed：这个字段是否假如到索引中
* sotred：这个字段的值是否被存储
* multiValued：这个字段是否可以有多个值

####分析
数据添加到Solr中后，在添加到索引前需要进过一系列的转换，这个步骤叫做词法分析，词法分析包括大小写转换，删除词根等等，分析的结果是一系列的tokens将加入到索引中，tokens不是原始的文本，是当你执行搜索查询的你说收到的文本。    

indexed字段是一个将会被加入到索引中的字段，如果不是indexed字段，也就不会被搜索到。  

####Term Storage
所显示给用户的搜索结果通常就是原始文档，而不是机器处理过的tokens（当然tokens与原始文档有相似之处）这个就是stored属性的作用，告诉Solr在索引的时候保存原始文档。有时，有些字段没有被搜索，但是需要显示在搜索结果中，那么就要设置stored=true,indexed=false。为什么不能存储所有字段呢？考虑到存储字段是需要增加索引的容量的，索引越大，搜索越缓慢，因为大的索引需要花更多的时间磁盘查找。










上篇文章提到有配置文件schema.xml，这在Solr中是个非常重要的文件，这篇文章就来详细的了解这个文件的作用。  

Solr把schema.xml文档翻译成Lucene索引，Solr提供了copy field和 dynamic fields。Copy fields提供了一种方式去


Lucene是一个高性能的java全文检索工具包，它使用的是倒排文件索引结构。该结构及相应的生成算法如下：    
0）设有两篇文章1和2   
文章1的内容为：Tom lives in Guangzhou,I live in Guangzhou too.  
文章2的内容为：He once lived in Shanghai.    
1)由于lucene是基于关键词索引和查询的，首先我们要取得这两篇文章的关键词，通常我们需要如下处理措施
 
* 我们现在有的是文章内容，即一个字符串，我们先要找出字符串中的所有单词，即分词。英文单词由于用空格分隔，比较好处理。中文单词间是连在一起的需要特殊的分词处理。 
* 文章中的”in”, “once” “too”等词没有什么实际意义，中文中的“的”“是”等字通常也无具体含义，这些不代表概念的词可以过滤掉 
* 用户通常希望查“He”时能把含“he”，“HE”的文章也找出来，所以所有单词需要统一大小写。 
* 用户通常希望查“live”时能把含“lives”，“lived”的文章也找出来，所以需要把“lives”，“lived”还原成“live” 
* 文章中的标点符号通常不表示某种概念，也可以过滤掉 
在lucene中以上措施由Analyzer类完成

[Lucene倒排索引](http://wenku.baidu.com/view/e1bff3150b4e767f5acfcef3.html)  
[Lucene评分算法](http://ericbao.blog.sohu.com/203348366.html)  
[Lucene/Solr修改评分规则](http://www.cnblogs.com/tq03/p/3615517.html)  
[Lunece大牛，全文检索的基本原理](http://www.cnblogs.com/forfuture1978/archive/2009/12/14/1623594.html)


* tf:表示词条(term)在文档中出现的词频
* idf：表示词条(term)在几个文档中出现过


###索引创建过程
原始文档：  
文件一：Students should be allowed to go out with their friends, but not allowed to drink beer.  
文件二：My friend Jerry went to school to see his students but found them drunk which is not allowed.  

####一：原始文档传分词组件(Tokenizer)
分词组件(Tokenizer)会做以下几件事情(这个过程称为：Tokenize)  

1. 将文档分成一个一个单独的单词
2. 去除标点符号
3. 去除停词(stop word)

    所谓停词(Stop word)就是一种语言中最普通的一些单词，由于没有特别的意义，因而大多数情况下不能成为搜索的关键词，因而创建索引时，这种词会被去掉而减少索引的大小。英语中停词(Stop word)如：“the”,“a”，“this”等。

对于每一种语言的分词组件(Tokenizer)，都有一个停词(stop word)集合。经过分词(Tokenizer)后得到的结果称为词元(Token)。上例子中，便得到以下词元(Token)：

    “Students”，“allowed”，“go”，“their”，“friends”，“allowed”，“drink”，“beer”，“My”，“friend”，“Jerry”，“went”，“school”，“see”，“his”，“students”，“found”，“them”，“drunk”，“allowed”

####二：词元(Token)传给语言处理组件(Linguistic Processor)
语言处理组件(linguistic processor)主要是对得到的词元(Token)做一些同语言相关的处理。对于英语，语言处理组件(Linguistic Processor)一般做以下几点：

1. 变为小写(Lowercase)。
2. 将单词缩减为词根形式，如“cars”到“car”等。这种操作称为：stemming。
3. 将单词转变为词根形式，如“drove”到“drive”等。这种操作称为：lemmatization。
    
**Stemming 和 lemmatization的异同：**  

* 相同之处：
    1. Stemming和lemmatization都要使词汇成为词根形式。  
* 两者的方式不同：  
    1. Stemming采用的是“缩减”的方式：“cars”到“car”，“driving”到“drive”。
    2. Lemmatization采用的是“转变”的方式：“drove”到“drove”，“driving”到“drive”。
* 两者的算法不同：
    1. Stemming主要是采取某种固定的算法来做这种缩减，如去除“s”，去除“ing”加“e”，将“ational”变为“ate”，将“tional”变为“tion”。
    2. Lemmatization主要是采用保存某种字典的方式做这种转变。比如字典中有“driving”到“drive”，“drove”到“drive”，“am, is, are”到“be”的映射，做转变时，只要查字典就可以了。
    3. Stemming和lemmatization不是互斥关系，是有交集的，有的词利用这两种方式都能达到相同的转换。

**语言处理组件(linguistic processor)的结果称为词(Term)**  

在我们的例子中，经过语言处理，得到的词(Term)如下：

    “student”，“allow”，“go”，“their”，“friend”，“allow”，“drink”，“beer”，“my”，“friend”，“jerry”，“go”，“school”，“see”，“his”，“student”，“find”，“them”，“drink”，“allow”。
也正是因为有语言处理的步骤，搜索drive时drove也能被搜索出来。

####三：得到的词(Term)传递给索引组件(Indexer)
1. 利用得到的词(Term)创建一个字典

        Term	Document ID
        student	    1
        allow	    1
        go	        1
        their	    1
        friend	    1
        allow	    1
        drink	    1
        beer	    1
        my	        2
        friend	    2
        jerry	    2
        go	        2
        school	    2
        see	        2
        his	        2
        student	    2
        find	    2
        them	    2
        drink	    2
        allow	    2
2. 对字典按字母顺序排序：

        Term	Document ID
        allow	    1
        allow	    1
        allow	    2
        beer	    1
        drink	    1
        drink	    2
        find	    2
        friend	    1
        friend	    2
        go	        1
        go	        2
        his	        2
        jerry	    2
        my	        2
        school	    2
        see	        2
        student	    1
        student	    2
        their	    1
        them	    2 
3. 合并相同的词(Term)成为文档倒排(Posting List)链表
![postlist](../resource/image/postinglist.jpg)
    * Document Frequency：文档频次，表示多少文档出现过此词(Term)
    * Frequency：词频，表示某个文档中该词(Term)出现过几次

    对词(Term) “allow”来讲，总共有两篇文档包含此词(Term)，词(Term)后面的文档链表总共有两项，第一项表示包含“allow”的第一篇文档，即1号文档，此文档中，“allow”出现了2次，第二项表示包含“allow”的第二个文档，是2号文档，此文档中，“allow”出现了1次

到此索引创建完成，搜索“drive”，“driving”，“drove”，“driven”也能够被搜到。因为在索引中，“driving”，“drove”，“driven”都会经过语言处理而变成“drive”，在搜索时，如果您输入“driving”，输入的查询语句同样经过一二步骤，变为查询“drive”，从而可以搜索到想要的文档。

###搜索步骤
搜索"microsoft job"，用户的目的是希望在微软找一份工作，如果搜出来的结果是:“Microsoft does a good job at software industry…”，这就与用户的期望偏离太远了。如何进行合理有效的搜索，搜索出用户最想要得结果呢？搜索主要有如下步骤：  

####一：
    

