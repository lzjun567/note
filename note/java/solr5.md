整合IK Analyzer
=====================
IK Analyzer是一款结合了词典和文法分析算法的中文分词组件，基于字符串匹配，支持用户词典扩展定义，支持细粒度和智能切分，比如：  

    张三说的确实在理

智能分词的结果是：  

    张三 |  说的 |  确实 |  在理 
最细粒度分词结果：  

    张三 |  三 |  说的 |  的确 |  的 |  确实 |  实在 |  在理

整合IK Analyzer比mmseg4j要简单很多，[下载](https://code.google.com/p/ik-analyzer/downloads/list)解压缩IKAnalyzer2012FF_u1.jar放到目录：E:\solr-4.8.0\example\solr-webapp\webapp\WEB-INF\lib，修改配置文件schema.xml，添加代码：  
   
      <field name="content" type="text_ik" indexed="true" stored="true"/> 

      <fieldType name="text_ik" class="solr.TextField">
            <analyzer type="index" isMaxWordLength="false" class="org.wltea.analyzer.lucene.IKAnalyzer"/>
    	    <analyzer type="query" isMaxWordLength="true" class="org.wltea.analyzer.lucene.IKAnalyzer"/>
      </fieldType>

    查询采用IK自己的最大分词法,索引则采用它的细粒度分词法

此时就算配置完成了，重启服务：java -jar start.jar，来看看IKAnalyzer的分词效果怎么样，打开Solr管理界面，点击左侧的Analysis页面  
![index4](http://blog-resource.qiniudn.com/index4.png)  
默认分词器进行最细粒度切分。IKAnalyzer支持通过配置IKAnalyzer.cfg.xml 文件来扩充您的与有词典以及停止词典（过滤词典），只需把IKAnalyzer.cfg.xml文件放入class目录下面，指定自己的词典mydic.dic  

    <?xml version="1.0" encoding="UTF-8"?> 
    <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">   
    <properties>   
      <comment>IK Analyzer 扩展配置</comment> 
      <!--用户可以在这里配置自己的扩展字典  -->  
      <entry key="ext_dict">/mydict.dic; 
    /com/mycompany/dic/mydict2.dic;</entry>  
     
       <!--用户可以在这里配置自己的扩展停止词字典--> 
      <entry key="ext_stopwords">/ext_stopword.dic</entry>    
    </properties> 

###更新：

前面的FieldType配置其实存在问题，根据目前最新的IK版本[IK Analyzer 2012FF_hf1.zip](https://code.google.com/p/ik-analyzer/downloads/list)，**索引时使用最细粒度分词，查询时最大分词（智能分词）**实际上是不生效的。  

据作者[linliangyi](http://linliangyi2007.iteye.com/)说，在2012FF_hf1这个版本中已经修复，经测试还是没用，详情请看[此贴](https://code.google.com/p/ik-analyzer/issues/detail?id=88)。

####解决办法：重新实现IKAnalyzerSolrFactory  

    package org.wltea.analyzer.lucene;
    
    import java.io.Reader;
    import java.util.Map;
    
    import org.apache.lucene.analysis.Tokenizer;
    import org.apache.lucene.analysis.util.TokenizerFactory;
    import org.apache.lucene.util.AttributeSource.AttributeFactory;
    
    public class IKAnalyzerSolrFactory extends TokenizerFactory{
    	
    	private boolean useSmart;
    	
    	public boolean useSmart() {
    		return useSmart;
    	}
    	
    	public void setUseSmart(boolean useSmart) {
    		this.useSmart = useSmart;
    	}
    	
    	 public IKAnalyzerSolrFactory(Map<String,String> args) {
    	     super(args);
    	     assureMatchVersion();
    	     this.setUseSmart(args.get("useSmart").toString().equals("true"));
    	   }
    
    
        @Override
        public Tokenizer create(AttributeFactory factory, Reader input) {
            Tokenizer _IKTokenizer = new IKTokenizer(input , this.useSmart);
            return _IKTokenizer;
        }
    
    }

重新编译后更新文件，更新schema.xml文件：  

    <fieldType name="text_ik" class="solr.TextField" >
            <analyzer type="index">
                <tokenizer class="org.wltea.analyzer.lucene.IKAnalyzerSolrFactory" useSmart="false"/>
            </analyzer> 
            <analyzer type="query">
                <tokenizer class="org.wltea.analyzer.lucene.IKAnalyzerSolrFactory" useSmart="true"/>
            </analyzer> 
    </fieldType>
