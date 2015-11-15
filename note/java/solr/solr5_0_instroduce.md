Apache Lucene、Solr 5.0 发布
=======================
Java搜索引擎Apache Lucene和NoSQL服务Apache Solr经过两年多的等待终于迎来了新的主版本号5.0。  近日，Apache软件基金会最近宣布了Lucene 5.0 和 Apache Solr 5.0的发布，两个项目加入了大量新特性以及核心组件的改进。  

####新版Solr的亮点
Solr5.0的很多工作都集中在易用性的改进，同时新增了不少API，然而，实现细节仅仅以必要悉知的原则显示。包含在4.10版本用于启动，停止和运行Solr实例的脚本已经以函数选项的方式被扩展，现在可以使用脚本的方式索引文档、删除Solr collection。    

此外，可扩展性和稳定性同样有所改进，5.0之前的版本整个集群的状态写在单个文件中，需要的时候才被每个节点所监控。现在每个collection有自己的集群状态，这极大提高了系统的可扩展性。

最后，SOlr5.0支持分布式的IDF，此功能可以通过配置来使之生效。  

所有的这些特性、改进以及bug修复都可以在官方发布[声明](http://lucene.apache.org/solr/news.html)中查看，与之同步的一份[引用指南](https://www.apache.org/dyn/closer.cgi/lucene/solr/ref-guide/)也做了一次完整的修订。

####Lucene5.0
伴随着Solr最新版新特性的出现，我们不能忘记的还有Lucene也同步更新了，Lucene5.0提供了更加安全的索引，降低堆内存的使用率，基于ConcurrentMergeScheduler的自动化的IO调节。  
FieldCache成为过去，NormsFormat有了它自己专用的NormsConsumer/Producer，混合文件的处理更加简单。  

另外Michael McCandless的[博客](http://blog.mikemccandless.com/2014/11/apache-lucene-500-is-coming.html)对所有新特性做了更详细的解释。

http://jaxenter.com/apache-lucene-solr-5-0-released-114899.html