IndexReader/IndexWriter/IndexSearcher
=====================================
####IndexWriter
[indexwriter](http:)

####IndexReader
[indexreader](https://lucene.apache.org/core/4_9_0/core/index.html)用来读取索引的抽象类，是线程安全的类，任何通过IndexWriter更新索引对IndexReader来说都是不可见得，只有等到新的IndexReader才能看见。获得IndexReader的最好的方法是使用DirectoryReader.open(IndexWriter, boolean)，如果IndexWriter在处理过程中，那么需要重新打开才能看见索引，那么就是用DirectoryReader.openIfChanged(DirectoryReader)，新的reader会和之前的旧的共享资源。

DirectoryReader.open(IndexWrter, boolean)会返回一个近实时的IndexerReader。如果参数为true，applyAllDeletes - If true, all buffered deletes will be applied (made visible) in the returned reader. If false, the deletes are not applied but remain buffered (in IndexWriter) so that they will be applied in the future. Applying deletes can be costly, so if your app can tolerate deleted documents being returned you might gain some performance by passing false.

有两种不同类型的IndexReader：  
* AtomicReader：
* CompositeReader：
indexreader可以获取文档总数，删除的文档数，

####[IndexSearcher](https://lucene.apache.org/core/4_9_0/core/index.html)
在IndexReader之上通过IndexSearcher来实现搜索功能，IndexSearcher实例也是线程安全的，应用搜索的时候通过调用search(Query,int)方法或者search(Query, Filter, int)，为了提高性能，如果你的索引没有发生变化，那么应该通过共享单个IndexSearcher实例当需要多个search的时候，而不是每个搜索对应一个IndexSearcher实例。如果索引发生了改变，如果你希望能够这些变化能立马反应到搜索结果里面来，那么你要使用DirectoryReader.openIfChange(DirectoryReader)来获取新的reader，然后用这个reader来创建新的IndexSearcher实例。  
对于低延迟的转化，最好是使用(DirectoryReader.open(IndexWriter,boolean))获取一个近实时的IndexReader，这样相对来说创建一个新的IndexSearcher成本要低些。  


