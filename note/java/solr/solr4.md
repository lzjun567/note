Solr(4)：整合mmseg4j
=====================
默认Solr提供的分词组件对中文的支持是不友好的，比如：“VIM比作是编辑器之神”这个句子在索引的的时候，选择FieldType为"text_general"作为分词依据时，分词效果是：  
![index1](http://blog-resource.qiniudn.com/index1.png)

它把每一个词都分开了，可以想象如果一篇文章这样分词的搜索的体验效果非常差。目前来说中文分词组件mmseg4j是比较好的选择，这篇文章讲述如何整合Solr与mmseg4j。mmeseg4j最新版本是1.9.1，[下载](https://code.google.com/p/mmseg4j/downloads/list)解压，提取其中的三个文件：mmseg4j-analysis-1.9.1.jar， mmseg4j-core-1.9.1.jar，mmseg4j-solr-1.9.1.jar。放到目录：E:\solr-4.8.0\example\solr-webapp\webapp\WEB-INF\lib，修改配置文件schema.xml，添加下面的两段代码：    
fieldType:

    <!-- mmseg4j-->
    <fieldType name="text_mmseg4j_complex" class="solr.TextField" positionIncrementGap="100" >  
        <analyzer>  
            <tokenizer class="com.chenlb.mmseg4j.solr.MMSegTokenizerFactory" mode="complex" dicPath="dic"/>  
        </analyzer>  
    </fieldType>  
    <fieldType name="text_mmseg4j_maxword" class="solr.TextField" positionIncrementGap="100" >  
        <analyzer>  
            <tokenizer class="com.chenlb.mmseg4j.solr.MMSegTokenizerFactory" mode="max-word" dicPath="dic"/>  
        </analyzer>  
    </fieldType>  
    <fieldType name="text_mmseg4j_simple" class="solr.TextField" positionIncrementGap="100" >  
        <analyzer>  
          <!--
            <tokenizer class="com.chenlb.mmseg4j.solr.MMSegTokenizerFactory" mode="simple" dicPath="n:/OpenSource/apache-solr-1.3.0/example/solr/my_dic"/> 
            -->
            <tokenizer class="com.chenlb.mmseg4j.solr.MMSegTokenizerFactory" mode="simple" dicPath="dic"/>     
        </analyzer>  
    </fieldType>
    <!-- mmseg4j-->

与fieldType对应的field：

    <!-- mmseg4j -->
    <field name="mmseg4j_complex_name" type="text_mmseg4j_complex" indexed="true" stored="true"/>
    <field name="mmseg4j_maxword_name" type="text_mmseg4j_maxword" indexed="true" stored="true"/>
    <field name="mmseg4j_simple_name" type="text_mmseg4j_simple" indexed="true" stored="true"/>
    <!--mmseg4j -->

此时就算配置完成了，重启服务：java -jar start.jar，来看看mmseg4j的分词效果怎么样，打开Solr管理界面，点击左侧的Analysis页面  
![index2](http://blog-resource.qiniudn.com/index2.png)  
对比之前的分词效果，改进了很多，差不多就是正常的语义了。这里在分词的时候你有可能会遇到一个问题：  
    >>TokenStream contract violation: reset()/close() call missing, reset() called multiple times, or subclass does not call super.reset(). Please see Javadocs of TokenStream class for more information about the correct consuming workflow.

这个是Solr4.8环境下mmseg4j的一个bug，这是mmseg4j-analysis-1.9.1.jar引起的，需要修改源码，找到文件：mmseg4j-1.9.1\mmseg4j-analysis\src\main\java\com\chenlb\mmseg4j\analysis\MMSegTokenizer.java，加上`super.reset()`：     

    public void reset() throws IOException {
		//lucene 4.0
		//org.apache.lucene.analysis.Tokenizer.setReader(Reader)
		//setReader 自动被调用, input 自动被设置。
        super.reset(); //加上这一行
		mmSeg.reset(input);
	}

修改完之后用maven重启编译：mvn clean package -DskipTests，用新的mmseg4j-1.9.1\mmseg4j-analysis\target\mmseg4j-analysis-1.9.2-SNAPSHOT.jar替换掉原来那个文件，重启服务就ok了。      

mmeseg4j-1.9.1这个版本的的词库全部打包放在了jar文件里面，因此无需再指定词库文件(chars.dic，units.dic，words.dic)，当然你也可以覆盖这些文件，只需要吧预替换的文件放在在WEB-INF\data\即可。
    
现在添加两个中文文档到索引中去，试试mmeseg4j的效果怎么样：  

    <add>  
        <doc>  
            <field name="id">0001</field>  
            <field name="mmseg4j_complex_name">把Emacs比作是神的编辑器，VIM比作是编辑器之神，2012年开始接触VIM，一直沿用至今，也曾今总结过VIM的相关知识，文章都整理在以前的ITeye博客和GitHub，这款古而不老的编辑器至今仍受众多程序员追捧，当然我也是忠实的VIM用户，这篇文章就是用VIM编辑完成。</field>  
        </doc>  
        <doc>  
            <field name="id">0002</field>  
            <field name="mmseg4j_complex_name">用Google搜索"Python IDE"，第一条就是stackoverflow上一个非常热门的问题："what IDE to use for Python"，上百种编辑器的功能对比图让人眼花缭乱。其中有我接触过的几款编辑器（IDE）包括：Eclilpse(PyDev)、VIM、NotePad++、PyCharm。如果你的日常开发语言是Python的话，再搜索"python vim"，大约有328万条结果，可见用VIM做Python开发的程序员那是相当之多，我大概总结的几点原因，当然不一定正确</field>  
        </doc>  
    </add> 

保存为utf-8格式的文件名：mmseg4j-solr-demo-doc.xml，加入到Solr中去：   

    E:\solr-4.8.0\example\exampledocs>java -jar post.jar mmseg4j-solr-demo-doc.xml
    SimplePostTool version 1.5
    Posting files to base url http://localhost:8983/solr/update using content-type application/xml..
    POSTing file mmseg4j-solr-demo-doc.xml
    1 files indexed.
    COMMITting Solr index changes to http://localhost:8983/solr/update..
    Time spent: 0:00:01.055

看搜索结果：  
![index4](http://blog-resource.qiniudn.com/index3.png)
