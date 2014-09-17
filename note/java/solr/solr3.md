Solr核心概念、配置文件
=======================
Lucene中有几个基本的概念，他们是索引（index）、文档（document）、字段（field）、词汇单元（term），这些概念在Solr中同样存在。  
* 索引包含一系列的文档
* 文档是字段的集合
* 字段就是词汇单元的集合
* 词汇单元就是一个字符串
相同的字符串在不同的字段中认为是不同的词汇单元，因为词汇单元代表的是字符串对，类似于key-value一样的映射关系的map类型。  
####Document
Document是Solr索引（动词，indexing）和搜索的最基本单元，它类似于关系数据库表中的一条记录，可以包含一个或多个字段（Field），每个字段包含一个name和文本值。字段在被索引的同时可以存储在索引中，搜索时就能返回该字段的值，通常文档都应该包含一个能唯一表示该文档的id字段。例如：   

    <doc>
        <field name="id">company123</field>
        <field name="companycity">Atlanta</field>
        <field name="companystate">Georgia</field>
        <field name="companyname">Code Monkeys R Us, LLC</field>
        <field name="companydescription">we write lots of code</field>
        <field name="lastmodified">2013-06-01T15:26:37Z</field>
    </doc>
    


####Schema
Solr中的Schema类似于关系数据库中的表结构，它以schema.xml的文本形式存在在conf目录下，在添加文当到索引中时需要指定Schema，Schema文件主要包含三部分：**字段（Field）、字段类型（FieldType）、唯一键（uniqueKey）**    

* 字段类型（FieldType）：用来定义添加到索引中的xml文件字段（Field）中的类型，如：int，String，date，
* 字段（Field）：添加到索引文件中时的字段名称
* 唯一键（uniqueKey）：uniqueKey是用来标识文档唯一性的一个字段（Feild），在更新和删除时用到  
  
例如：  

    <schema name="example" version="1.5">
    	<field name="id" type="string" indexed="true" stored="true" required="true" multiValued="false" />
    	<field name="title" type="text_general" indexed="true" stored="true" multiValued="true"/>
    
    	<uniqueKey>id</uniqueKey>
    	<fieldType name="string" class="solr.StrField" sortMissingLast="true" />
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
    </schema>
####Field
在Solr中，字段(Field)是构成Document的基本单元。对应于数据库表中的某一列。字段是包括了名称，类型以及对字段对应的值如何处理的一种元数据。比如：   

    <field name="name" type="text_general" indexed="true" stored="true"/>

* Indexed：Indexed=true时，表示字段会加被Sorl处理加入到索引中，只有被索引的字段才能被搜索到。
* Stored：Stored=true，字段值会以保存一份原始内容在在索引中，可以被搜索组件组件返回，考虑到性能问题，对于长文本就不适合存储在索引中。

####Field Type
Solr中每个字段都有一个对应的字段类型，比如：float、long、double、date、text，Solr提供了丰富字段类型，同时，我们还可以自定义适合自己的数据类型，例如：  

    <!-- Ik 分词器 --> 
    <fieldType name="text_cn_stopword" class="solr.TextField">
        <analyzer type="index"> 
            <tokenizer class="org.wltea.analyzer.lucene.IKAnalyzerSolrFactory" useSmart="false"/>
        </analyzer>
        <analyzer type="query"> 
            <tokenizer class="org.wltea.analyzer.lucene.IKAnalyzerSolrFactory" useSmart="true"/>
        </analyzer>
    </fieldType>
    <!-- Ik 分词器 --> 

####Solrconfig：
如果把Schema定义为Solr的Model的话，那么Solrconfig就是Solr的Configuration，它定义Solr如果处理索引、高亮、搜索等很多请求，同时还指定了缓存策略，用的比较多的元素包括：  

* 指定索引数据路径

        <!-- 
        Used to specify an alternate directory to hold all index data
        other than the default ./data under the Solr home.
        If replication is in use, this should match the replication configuration. 
        -->
        <dataDir>${solr.data.dir:./solr/data}</dataDir>
    
* 缓存参数
        
        <filterCache
          class="solr.FastLRUCache"
          size="512"
          initialSize="512"
          autowarmCount="0"/>

        <!-- queryResultCache caches results of searches - ordered lists of
             document ids (DocList) based on a query, a sort, and the range
             of documents requested.  -->
         <queryResultCache
          class="solr.LRUCache"
          size="512"
          initialSize="512"
          autowarmCount="0"/>

         <!-- documentCache caches Lucene Document objects (the stored fields for each document).
           Since Lucene internal document ids are transient, this cache will not be autowarmed.  -->
         <documentCache
          class="solr.LRUCache"
          size="512"
          initialSize="512"
          autowarmCount="0"/>
* 请求处理器  
    请求处理器用于接收HTTP请求，处理搜索后，返回响应结果的处理器。比如：query请求：  
        
        <!-- A request handler that returns indented JSON by default -->
        <requestHandler name="/query" class="solr.SearchHandler">
             <lst name="defaults">
               <str name="echoParams">explicit</str>
               <str name="wt">json</str>
               <str name="indent">true</str>
               <str name="df">text</str>
             </lst>
        </requestHandler>
    每个请求处理器包括一系列可配置的搜索参数，例如：wt,indent,df等等。  

* 搜索组件
