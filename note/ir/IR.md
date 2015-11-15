采集  
线性扫描，顺序扫描：grepping 

新的需求：  

* 大规模文档集，比如：千万，上亿甚至十亿
* 更灵活的匹配方式，比如：hello REAR word，NEAR：可能的定义是：5个词以内，或者同一个句子中。  
* 对结果进行排序

词项-文档（term-document）关联矩阵![矩阵](http://github-note.qiniudn.com/matrix.png)  
布尔检索： 布尔检索模型接受布尔表达式查询。即通过AND OR NOT连接起来查询。   
检索包含“python”和“ruby”但是不包括“go”的文档：  
分别取出python，ruby，go对应的行向量，对go取反操作，三者进行“与”操作：  
01101 & 01110 & 10100 = 00100，表明符合条件的就只有doc3  
