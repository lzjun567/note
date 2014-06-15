Solr配置文件介绍
=======================
Solr主目录结构通常是：  

    <solr-home-directory>/
      solr.xml
      conf/
        solrconfig.xml
        schema.xml
      data/

####solrconfig.xml：
首先打开solrconfig.xml文件看看，里面包括： 

* 请求处理器(request handlers)，比如：  

        <requestHandler name="/select" class="solr.SearchHandler">
        <requestHandler name="/query" class="solr.SearchHandler">
        <requestHandler name="/get" class="solr.RealTimeGetHandler">
* 监听器(listeners)，用于监听特定的查询相关的事件，可以用来触发执行指定的代码。
* 请求转发器(Request Dispatcher)：用来管理HTTP通信
* 用于分布式相关的参数

默认情况，索引存储在data目录下，你可以通过修改solrconfig.xml文件改变索引的存放位置：  

    <dataDir>/var/data/solr/</dataDir>  
Solr通过定义`<lib/>标签加载插件，支持正则表达式，比如：加入数据导入的插件：  

    <lib dir="../../../dist/" regex="solr-dataimporthandler-\d.*\.jar"/>ke
可以通过指定schemaFacotry以编程的方式修改schema.xml文件，默认不支持，除非指定：  

    <schemaFactory class="ManagedIndexSchemaFactory">
         <bool name="mutable">true</bool>
         <str name="managedSchemaResourceName">managed-schema</str>
    </schemaFactory>

####Schema.xml
在Solr中，文档(Document)是索引和搜索的基本单元，一个索引由一个或多个文档构成，而一个文档是由一个或者多个字段(Field)组成的。文档对应于数据库中表的一行，而字段对应的是表中的某一列。字段是包括了名称，类型以及如何处理内容的一种元数据。比如：   

    <field name="name" type="text_general" indexed="true" stored="true"/>

* Indexed：Indexed字段可以进行搜索和排序，还可以在这种字段上运行Solr分析过程
* Stored：Stored字段内容可以保存在索引中，不过绝大多数应用存储的是指向内容的指针而不是真正的文件内容。

凡是schema.xml中定义的字段，在搜索的时候可以指定参数q，比如：指定q为"name:java"，表示搜索字段name中有"java"的内容。

#####Schema文件主要包含三部分，字段（Field）、字段类型（FieldType）、唯一键（uniqueKey）  

* 字段类型（FieldType）：用来定义添加到索引中的xml文件字段（Field）中的类型，如：int，String，date，
* 字段（Field）：添加到索引文件中时的字段名称
* 唯一键（uniqueKey）：uniqueKey是用来标识文档唯一性的一个字段（Feild），在更新和删除时用到  

text_general是一种通用的文本字段，用StandardTokenizer来做分词处理，对照上一篇讲过的全文检索原理可以看出，在索引(index)时使用StandardTokenizerFactory来分词，停词和小写替换用相应的filter来处理，在查询(query)的使用也有类似的操作。

    <-- A general text field that has reasonable, generic
         cross-language defaults: it tokenizes with StandardTokenizer,
	 removes stop words from case-insensitive "stopwords.txt"
	 (empty by default), and down cases.  At query time only, it
	 also applies synonyms. -->

    <fieldType name="text_general" class="solr.TextField" positionIncrementGap="100">
      <analyzer type="index">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
        <!-- in this example, we will only use synonyms at query time
        <filter class="solr.SynonymFilterFactory" synonyms="index_synonyms.txt" ignoreCase="true" expand="false"/>
        -->
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
        <filter class="solr.SynonymFilterFactory" synonyms="synonyms.txt" ignoreCase="true" expand="true"/>
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
    </fieldType>

p173
