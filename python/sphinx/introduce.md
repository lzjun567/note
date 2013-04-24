1. 下载安装：http://sphinxsearch.com/downloads/beta/  

Sphinx 可以通过三种不同的接口于Sphinx的搜索服务（searchd）通信
1. 原生搜索API
2. 


indexer：用于创建索引  
search：一个简单的命令行测试程序，用于测试全文索引  
searchd：守护进程，web程序可以通过这个进程进行全文检索
sphinxapi：searchd的客户端API库
spelldump：命令行工具，用于提取词条
indextool：用来转储关于索引的调试信息
mmseg：用于提供中文分词和词典处理：


sphinx配置文件:  
source:指定数据源  
index：设置索引
searchd：

http://davidx.me/2010/10/31/understanding-sphinx/

找数据--> 建索引-->提供服务
