solr(7)：Field
================
####copyfield
可以实现一个字段的多次使用，比如：

说的简单一点，比如现在你要查询有"Java"的博客， 那么你肯定要查内容，标题是否包含Java，但是solr不能像SQL那样，where tittle like '%Java%'  or  content like '%Java%'.   这个时候copyField就派上用场了， 定义一个新字段，将title和content 复制到这个新字段，索引的时候，直接从这个新字段查询，这样就达到目地了。  这便是copyField的典型应用场景 。注意：如果dest由多个source构成，就需要将其指定为multiValued
    
    <field name="title"/>
    <field name="content"/>
    <field name="tc" multiValued="true"/>
    <copyFeild source="title" dest="tc" maxChars="3000"/>
    <copyFeild source="content" dest="tc" maxChars="3000"/>

现在就可以通过指定tc来搜索包括title、content在内的关键字了。

####multiValued
当某个文档内容一个字段多个值，比如：  

    <add>  
      <doc>  
        <field name="id">2</field>  
        ...  
        <field name="link">http://manning.com/</field>               
        <field name="link">http://lucene.apache.org/solr/</field>   
        ...  
         </doc> 
    </add>

那么在solr中可以配置一个字段的属性为multiValued="true"

    <field name="link"  
           type= "string"  
           indexed= "true"  
           stored="true"  
           multiValued="true"/> 

这样搜索`link:" http://manning.com/"`时，Solr会在

####dynamicField
动态字段（Dynamic fields）允许 solr 索引没有在 schema 中明确定义的字段。在忘记定义一些字段时很有用。动态字段和常规字段类似，除了它名字中包含一个通配符外，在索引文档时，一个字段如果在常规字段中没有匹配时，将到动态字段中匹配。  
比如schema中定义了一个叫*_i的动态动态字段，如果要文档中有一个叫 cost_i 的字段，但是 schema 中不存在 cost_i 的字段，这样 cost_i  将被索引到 *_i 字段中。

    <dynamicField name="*_i"
    type="sint"
    indexed="true"
    stored="true"/>
建议在 schema.xml 定义一些基本的动态字段，以备扩展之用。

#####################
###影响Luncene文档得分因素包括：  
1. tf（term Frequency）次元频率，表示改词在某个文档中出现的次数，当然是tf越大，分值就越大。
2. idf（inversed document Frequency）反转文档频率，计算公式是：  

        （float）（Math.log(numDocs/(double)(docFreq+1))+1.0） 
3. boost：建索引时对字段设置的激励因子，默认是1.0，boost越大，最后的得分也越大
4. lengthNorm：长度因子，也是建立索引时，影响得分的一种因子，一个字段内词元越多，长度因子越小，那么该词元所在文档的得分也就越低。

####Field高级属性（attribute）
**omitNorms：**这个属性最终会对应到Luncene中的lengthNorm，默认值为false，表示忽略规范，这对于节省不影响得分的字段的内存非常有用。
如果设置为true，那么搜索“工程师”时，无论字段的内容有多长，最终的得分都是一样的。  
    
    <field name="desc" type="text" indexed="true" stored="true" omitNorms="true"/> 
返回结果：

    <result name="response" numFound="5" start="0" maxScore="2.1541507">
    <doc>
    <float name="score">2.1541507</float>
    <str name="desc">高级工程师</str>
    <str name="id">001</str>
    </doc>
    <doc>
    <float name="score">2.1541507</float>
    <str name="desc">工程师</str>
    <str name="id">002</str>
    </doc>
    <doc>
    <float name="score">2.1541507</float>
    <str name="desc">十分牛逼的工程师</str>
    <str name="id">004</str>
    </doc>
    <doc>
    <float name="score">2.1541507</float>
    <str name="desc">好工程师</str>
    <str name="id">005</str>
    </doc>
    </result>
如果omitNorms设置为false：  

    <field name="desc" type="text" indexed="true" stored="true" omitNorms="false"/>  
返回结果，每个文档的分数不一样，字段越短，分数越高  

    <result name="response" numFound="5" start="0" maxScore="1.3463442">
    <doc>
    <float name="score">1.3463442</float>
    <str name="desc">工程师</str>
    <str name="id">002</str>
    </doc>
    <doc>
    <float name="score">1.0770754</float>
    <str name="desc">初级工程师</str>
    <str name="id">003</str>
    </doc>
    <doc>
    <float name="score">1.0770754</float>
    <str name="desc">好工程师</str>
    <str name="id">005</str>
    </doc>
    <doc>
    <float name="score">0.9424409</float>
    <str name="desc">十分牛逼的工程师</str>
    <str name="id">004</str>
    </doc>
    </result>

**positionIncrementGap** http://rockiee281.blog.163.com/blog/static/19385222920127225619919/    
