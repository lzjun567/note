SolrCloud（二）部署
=======================
####安装Zookeeper
ZooKeeper为分布式应用提供一致性服务（配置服务，同步服务和命名注册）的软件。SolrCloud使用ZooKeeper来同步配置和集群的状态（比如：选举共享的leader）。因此拥有一个高可用、容错性的ZooKeeeper安装显得非常重要。如果只有单实例ZooKeeper，那么如果ZooKeeper挂了，SolrCloud集群同样也跟着宕机。  

