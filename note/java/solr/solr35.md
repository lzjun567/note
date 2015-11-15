优化查询性能使用的技术包括：缓存（caching）、字段懒加载（lazy field loading）、预热新的searcher（new searcher warming）。  
在Solr中，查询是由一个叫做“searcher”的组件处理的，在Solr中有且只有一个“活动的”searcher，所有搜索请求都是通过这个“活动的”searcher完成。该searcher有一个Lucene索引快照视图。如果添加一个新的文档（document）到Solr中，那么该文档对当前这个searcher来说是不可见的，那么问题来了，新的文档怎能才能出现在搜索结果中？答案就是：关闭当前searcher，打开一个新的searcher，这个新的searcher是包含被更新过的索引视图。也就是说，每一次commit操作都会创建一个新的searcher使得新的文档的索引的更新操作都能及时反映到searcher上去，创建新searcher时，首先老searcher必须销毁，但是有可能当前有查询是基于老的searcher，所以Solr必须等到所有的查询都完成后才能销毁。同时所有基于当前searcher所做的缓存对象要撤销掉，因为缓存结果中的某些文档可能被是删除了，或者有新的文档是和这个查询是匹配的。  正因为如此，打开一个新的searcher是一项昂贵的操作，他会直接影响到用户体验，假设某用户正在分页浏览搜索结果，此时一个新的searcher在你点击了第二页后打开了，当用户去请求第3页的时候，前面所有缓存的对象不再生效，用户就会感觉很慢，尤其是对于复杂的查询。  

Solr有一系列工具来帮助应付这些问题，首先，Solr支持在后台“预热（warming）”一个新的searcher，同时保持当前的searcher是“活动的”，直到新的searcher完全预热完毕才会关闭当前的searcher。  预热有两种方式：一种是从旧的缓存中自动预热到新的缓存中去，另一种是执行“缓存预热（cache-warming）”查询。  

缓存预热查询是预先在solrconfig.xml中配置查询参数，新searcher创建的时候就会根据这个配置执行查询，然后把缓存填充到新searcher的缓存中去。  
    
        <listener event="newSearcher" class="solr.QuerySenderListener">
                <arr name="queries">
                  <!--
                     <lst><str name="q">solr</str><str name="sort">price asc</str></lst>
                     <lst><str name="q">rocks</str><str name="sort">weight asc</str></lst>
                    -->
                </arr>
        </listener>

自动预热的方式不能简单的直接把旧的缓存移到新的缓存中去，因为底层的索引可能会发生变化，相应的缓存也会发生变化。Solr采用的方式就是：每个缓存对象都有一个对应的key，比如过滤器缓存，key就是过滤器查询，如：“manu:Belkin”。预热新的缓存时，会重新根据过滤器计算查询结果，再缓存之。  

Cache
===================
4个需要关心的事儿：  
1. 缓存大小和回收策略
2. 命中率和回收率
3. 缓存对象的失效
4. 自动预热（当前搜索器最后访问的缓存将被自动填充进新的搜索器的缓存，以在索引、搜搜器变更时获得更高的缓存命中率）。  

缓存回收策略：
LRU：最近最少使用
LFU：最不经常使用

缓存不是越大越好，因为一旦在commit发生后，缓存失效后，大量无用对象等着GC回收，关闭一个searcher会使所有的缓存值失效。

Filter cache  

