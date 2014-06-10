查询语法和查询解析
================
查询解析器默认是dismax，defType=dismax
fq：用于复杂查询，每个fq都会缓存。比如：  
    
    如果是时间比较，需要注意：  
    如果是DateField类型，那么需要完全是ISO 88601日期语法支持，例如：  

       *  timestamp:[* TO NOW]
       *  createdate:[1976-03-06T23:59:59.999Z TO *]  这里*表示现在
       *  createdate:[1995-12-31T23:59:59.999Z TO 2007-03-06T00:00:00Z]
       *  pubdate:[NOW-1YEAR/DAY TO NOW/DAY+1DAY]
       *  createdate:[1976-03-06T23:59:59.999Z TO 1976-03-06T23:59:59.999Z+1YEAR]
       *  createdate:[1976-03-06T23:59:59.999Z/YEAR TO 1976-03-06T23:59:59.999Z]
TO必须是大写

fq有两种形式：  

    fq=popularity:[10 TO *]&fq=section:0
    fq=+popularity:[10 TO *]+section:0
当然都必须是URL-encoding的，像这样：  

    q=%2Bpopularity:[10%20TO%20*]%20%2Bsection:0

fl：field list,需要显示的字段，比如：
    
    fl=id,title
只显示id和title，

通配符搜索
？ 匹配单个字符
* 匹配0个或多个字符

模糊搜索
使用~
比如：roam~ 可以匹配roams, foam和本身roam
~接受一个可选的数字，可选范围为：0-2，默认是2，表示最多可以有两个字母不相同
如：roam~1 能匹配roams，foam，但是不能匹配foams,这里有两个字母不相同了。  

Boosting ^
这个能影响搜索的排名
比如搜索 python^4 django
这样python相关的会排在前头。

以上都是基于标准查询解析器的。

下面这个是基于DisMax的

qf：query field表示只在指定的字段上查询，比如：  

    qf="fieldOne^2.3 fieldTwo fieldThree^0.4"
在field1,2,3上查询，而且每个字段的权重也不一样，当然搜索结果的排序也会有变化。

pf：phrase field
在查询关键字下面做boosting，比如： python^2 django

bq：boost query

