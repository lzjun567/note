Lucene的分析过程
================
分析（Analysis）是指将域文本（Field）转换成项（Term）的过程，“项”是索引的最基本表示单元。分析器通过一系列操作（可能包括：提取单词，取出标点符号，字段转换成小写<称之为规范化>，词干还原，等），这个处理的过程称之为语汇单元化过程（tokenization），从文本流中提取的文本块成为语汇单元（token），语汇单元与域名结合后，就形成了项（Term）。  
####如何使用分析器
任何需要将文本转换成项的过程都将使用到分析器，对Lucene来说，建立索引和搜索这两个过程都将用到分析器。对于文本”use an implementation provided  Flow library”生成的语汇单元序列可能是：
[use] [implementation] [provide] [flow] [library]
####索引过程分析
索引期间，文档域值包含的文本信息需要被转换成语汇单元，![index_analysis.png]()

####语汇单元的构成
以“the quick brown fox”为例，该文本每个语汇单元都表示一个独立了的单词，一个语汇单元包含了一个文本值（单次本身）和其他的元数据，比如：原是文本从起点到终点的偏移量，语汇单元的类型，位置增量。

####词汇单元转换成项
在索引过程中进行分析后，每个语汇单元都作为一个项被传递给索引，、

####TokenStream
TokenStream是一个能在被调用后产生语汇单元序列的类，TokenStream有两个子类Tokenizer和TokenFilter。

