查询语法和查询解析
================
####通用查询参数
以下通用查询参数在Standard、DisMax和eDisMax请求处理器下都支持  

* defType：该参数用来指定使用哪种查询解析器来处理请求，查询解析器默认是dismax，defType=dismax  
* sort：排序，默认按照socre desc排序，排序的语法是：  
    
        sort=<field name> <direction>,<fieldname> <direction>],...
        例如： 
        price asc 
        inStock desc, price asc
* start：返回所有搜索结果中第一条记录的偏移量，默认从0开始
* rows：指定返回结果的记录条数，与start配合实现分页
* wt（write type）输出格式，如：xml、json、python
* fq（Filter Query）：对搜索结果进行过滤的查询器参数，对于加速复杂查询速度非常有帮助，因为每个fq都会缓存。在一个查询中fq可以指定多次  

        fq=popularity:[10 TO *]&fq=section:0
        fq=+popularity:[10 TO *]+section:0
    
    对于时间比较，需要注意：如果是DateField类型，那么需要完全是ISO 88601日期语法支持，例如：  

       *  timestamp:[* TO NOW]
       *  createdate:[1976-03-06T23:59:59.999Z TO *]  这里*表示现在
       *  createdate:[1995-12-31T23:59:59.999Z TO 2007-03-06T00:00:00Z]
       *  pubdate:[NOW-1YEAR/DAY TO NOW/DAY+1DAY]
       *  createdate:[1976-03-06T23:59:59.999Z TO 1976-03-06T23:59:59.999Z+1YEAR]
       *  createdate:[1976-03-06T23:59:59.999Z/YEAR TO 1976-03-06T23:59:59.999Z]

    TO必须是大写：当然都必须是URL-encoding的，像这样：  

            q=%2Bpopularity:[10%20TO%20*]%20%2Bsection:0

* fl（Field list）：搜索结果响应时需要显示的字段，默认是*，表示返回文档中所有字段，多个字段之间用逗号或空格或者+隔开  

        fl=id,title   #只显示id和title，
        fl = score title add_time  #显示得分，标题，添加时间

####Standard Query Parser
在Solr1.3之前的版本，Standard Request Handler会调用Standard query parser作为默认的查询解析器。1.3之后Standard Request handler调用DisMax作为默认的查询解析器。standard query parser的好处是精确性高，缺点是容错性稍差，而DisMax相反。  

除了通用参数外，Standard Query Parser还支持的参数有：  

* q：要查询的关键字，这个参数是强制要求的。  
* q.op：指定查询表达式的默认行为，它的值可以是“AND”或“OR”，它可以用来覆盖schema.xml中<solrQueryParser defaultOperator="OR"/> (配置在schema.xml这个参数现在不推荐使用，而使用q.op）
* df：default field，默认搜索字段，可以配置在solrconfig.xml中：  
        
         <requestHandler name="/query" class="solr.SearchHandler">
            <lst name="defaults">
              <str name="echoParams">explicit</str>
              <str name="wt">json</str>
              <str name="indent">true</str>
              <str name="df">text</str>
            </lst>
         </requestHandler>
        
    也可以在请求的时候指定：  
    [http://localhost:8983/solr/collection1/query?q=%E9%81%87%E5%88%B0&df=title&start=0&rows=18&wt=json&indent=true](http://localhost:8983/solr/collection1/query?q=%E9%81%87%E5%88%B0&df=title&start=0&rows=18&wt=json&indent=true)

    如果参数q指定了类型：比如：q=title:python，那么就可以不指定df，否则必须指定df


通配符搜索
？ 匹配单个字符
* 匹配0个或多个字符

模糊搜索
使用~
比如：roam~ 可以匹配roams, foam和本身roam，~接受一个可选的数字，可选范围为：0-2，默认是2，表示最多可以有两个字母不相同
如：roam~1 能匹配roams，foam，但是不能匹配foams,这里有两个字母不相同了。  

####Boosting ^  这个能影响搜索的排名
比如搜索 python^4 django
这样python相关的会排在前头。



以上都是基于标准查询解析器的。

####基于DisMax的查询参数

* qf：query field表示只在指定的字段上查询，如果没有该参数，那么默认值就取df，比如：  

        qf="fieldOne^2.3 fieldTwo fieldThree^0.4"
    在fieldOne、filedTwo、fieldThree上查询，而且每个字段的权重也不一样，当然搜索结果的排序也会有变化。

    再比如：solrconfig.xml中默认的配置：
    
        <str name="qf">
              text^0.5 features^1.0 name^1.2 sku^1.5 id^10.0 manu^1.1 cat^1.4
              title^10.0 description^5.0 keywords^5.0 author^2.0 resourcename^1.0
        </str>


* pf：phrase field
    在查询关键字下面做boosting，比如： python^2 django

* bq：boost query
* bf：Booting Function，


####二、 Solr运算符

1. “:” 指定字段查指定值，如返回所有值*:*，name:zhangsan-->返回字段name为zhangsan的结果
2. “?” 表示单个任意字符的通配
3. “*” 表示多个任意字符的通配（不能在检索的项开始处使用*或者?符号）
4. “~” 表示模糊检索，如检索拼写类似于”roam”的项这样写：roam~将找到形如foam和roams的单词；roam~0.8，检索返回相似度在0.8以上的记录。
5. 邻近检索，如检索相隔10个单词的”apache”和”jakarta”，”jakarta apache”~10
6. “^” 控制相关度检索，如检索jakarta apache，同时希望去让”jakarta”的相关度更加好，那么在其后加上”^”符号和增量值，即jakarta^4 apache
7. 布尔操作符AND、||
8. 布尔操作符OR、&&
9. 布尔操作符NOT、!、- （排除操作符不能单独与项使用构成查询）
10. “+” 存在操作符，要求符号”+”后的项必须在文档相应的域中存在
11. ( ) 用于构成子查询
12. [] 包含范围检索，如检索某时间段记录，包含头尾，date:[200707 TO 200710]
13. {} 不包含范围检索，如检索某时间段记录，不包含头尾
date:{200707 TO 200710}
14. / 转义操作符，特殊字符包括+ - && || ! ( ) { } [ ] ^ ” ~ * ? : /

 注：①“+”和”-“表示对单个查询单元的修饰，and 、or 、 not 是对两个查询单元是否做交集或者做差集还是取反的操作的符号
　　 比如:AB:china +AB:america ,表示的是AB:china忽略不计可有可无，必须满足第二个条件才是对的,而不是你所认为的必须满足这两个搜索条件
　　 如果输入:AB:china AND AB:america ,解析出来的结果是两个条件同时满足，即+AB:china AND +AB:america或+AB:china +AB:america
　　总而言之，查询语法：  修饰符 字段名:查询关键词 AND/OR/NOT 修饰符 字段名:查询关键词
