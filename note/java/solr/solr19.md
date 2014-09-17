SolrCloud
=========
Solr3.0引出了SolrCloud概念，也是顺应云计算，它能够大规模地使用分布式的索引和搜索。  
####概述
SolrCloud：集中式配置信息，自动容错，近实时搜索，查询自动负载均衡。先来了解下分布式搜索中常见的术语：  
####术语
* Cluster：集群，用来管理solr节点集合的单元，整个集群必须包含一个schema和solrconfig文件。
* Node：节点，一个运行Solr的JVM实例
* Partition：分区，它是整个文档集合的一个子集，分区中的文档可以包含在一个单独索引中。
* Shard：分片，一个分区需要存储在多个节点中（具体由复制(replication)因子指定），这些节点形成了一个分片，一个节点可以是多个分片的一部分。
* Leader：领导节点，每个分片都会拿一个节点作为领导节点，属于分片文档写操作都是经过leader节点路由出去的。Shard中的其他节点叫replicas 
* Replication Factor：赋值因子，一个文档的拷贝份数的最小值，这个值由cluster维护。
* Transaction Log：事务日志，一种append-only的写操作日志，由每个节点维护
* Partition Version：计数器，由每个分片的leader维护，每次写操作会递增，并发送给其他同片的兄弟。
* Cluster Lock：集群锁，如果要改变分区的范围或者是分区的节点映射（range->partition or partition-> node mapping)，那么就要先获得cluster lock。  
####原则
* 任何操作都可以被集群中的任意节点调用
* 没有不可恢复的单点故障
* 集群必须是弹性的
* 写操作永远不能丢失，也就是说持久化要得到保证
* 写的顺序应该保留
* 如果两个客户端同时发送文档"A"到两个不同的replicas中，必须有一个replicas在所有replicas中获胜。
* 集群配置应该中心管理化，而且可以通过集群中的任意节点来更新。
* 读故障自动转移
* 写故障自动转移
* 节点失败事件中复制因此自动更新

####Zookeeper
zookepper用于存储集群中中心配置





[new solrcloud design](https://wiki.apache.org/solr/NewSolrCloudDesign)
