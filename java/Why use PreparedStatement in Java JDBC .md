####JDBC为什么要使用PreparedStatement而不是Statement

**PreparedStatement**是用来执行SQL查询语句的API之一，Java提供了 **Statement** , **PreparedStatement** 和 **CallableStatement** 三种方式来执行查询语句，其中 **Statement** 用于通用查询，**PreparedStatement** 用于执行参数化查询，而 **CallableStatement** 则是用于存储过程。同时PreparedStatement还经常会在Java面试中被提及，譬如：*Statement与PreparedStatement的区别以及如何避免SQL注入式攻击？*这篇教程中我们会讨论为什么要用PreparedStatement？使用PreparedStatement有什么样的优势？PreparedStatement又是如何避免SQL注入攻击的？  

####PreparedStatement是什么？
PreparedStatement是java.sql包下面的一个接口，用来执行SQL语句查询，通过调用connection.preparedStatement(sql)方法可以获得PreparedStatment对象。数据库系统会对sql语句进行预编译处理（如果JDBC驱动支持的话），预处理语句将被预先编译好，这条预编译的sql查询语句能在将来的查询中重用，这样一来，它比Statement对象生成的查询速度更快。下面是一个例子：  

    public class PreparedStmtExample {
    
        public static void main(String args[]) throws SQLException {
            Connection conn = DriverManager.getConnection("mysql:\\localhost:1520", "root", "root");
            PreparedStatement preStatement = conn.prepareStatement("select distinct loan_type from loan where bank=?");
            preStatement.setString(1, "Citibank");
        
            ResultSet result = preStatement.executeQuery();
          
            while(result.next()){
                System.out.println("Loan Type: " + result.getString("loan_type"));
            }       
        }
    } 
    Output:
    Loan Type: Personal Loan
    Loan Type: Auto Loan
    Loan Type: Home Loan
    Loan Type: Gold Loan

这个例子中，如果还是用 **PreparedStatement** 做同样的查询，哪怕参数值不一样，比如："Standard Chated" 或者"HSBC"作为参数值，数据库系统还是会去调用之前编译器编译好的执行语句（系统库系统初次会对查询语句做最大的性能优化）。默认会返回"TYPE_FORWARD_ONLY"类型的结果集（ **ResultSet** ）,当然你也可以使用preparedstatment()的重载方法返回不同类型的结果集。  

####预处理语句的优势

**PreparedStatement**提供了诸多好处，企业级应用开发中强烈推荐使用PreparedStatement来做SQL查询，下面列出PreparedStatement的几点优势。  

1. **PreparedStatement**可以写动态参数化的查询  
    用PreparedStatement你可以写带参数的sql查询语句，通过使用相同的sql语句和不同的参数值来做查询比创建一个不同的查询语句要好，下面是一个参数化查询：  

        SELECT interest_rate FROM loan WHERE loan_type=?  

    现在你可以使用任何一种loan类型如："personal loan","home loan" 或者"gold loan"来查询，这个例子叫做参数化查询，因为它可以用不同的参数调用它，这里的"?"就是参数的占位符。  

2. **PreparedStatement**比 **Statement** 更快  
    使用 **PreparedStatement** 最重要的一点好处是它拥有更佳的性能优势，SQL语句会预编译在数据库系统中。执行计划同样会被缓存起来，它允许数据库做参数化查询。使用预处理语句比普通的查询更快，因为它做的工作更少（数据库对SQL语句的分析，编译，优化已经在第一次查询前完成了）。为了减少数据库的负载，生产环境中德JDBC代码你应该总是使用 **PreparedStatement** 。值得注意的一点是：为了获得性能上的优势，应该使用参数化sql查询而不是字符串追加的方式。下面两个SELECT 查询，第一个SELECT查询就没有任何性能优势。  
    SQL Query 1:字符串追加形式的PreparedStatement  

        String loanType = getLoanType();
        PreparedStatement prestmt = conn.prepareStatement("select banks from loan where loan_type=" + loanType);

    SQL Query 2：使用参数化查询的PreparedStatement  

        PreparedStatement prestmt = conn.prepareStatement("select banks from loan where loan_type=?");
        prestmt.setString(1,loanType);  
    第二个查询就是正确使用PreparedStatement的查询，它比SQL1能获得更好的性能。  

3. **PreparedStatement**可以防止SQL注入式攻击  
    如果你是做Java web应用开发的，那么必须熟悉那声名狼藉的SQL注入式攻击。去年Sony就遭受了SQL注入攻击，被盗用了一些Sony play station（PS机）用户的数据。在SQL注入攻击里，恶意用户通过SQL元数据绑定输入，比如：某个网站的登录验证SQL查询代码为：  

        strSQL = "SELECT * FROM users WHERE name = '" + userName + "' and pw = '"+ passWord +"';"
    恶意填入：
        userName = "1' OR '1'='1";
        passWord = "1' OR '1'='1";
    那么最终SQL语句变成了：
        strSQL = "SELECT * FROM users WHERE name = '1' OR '1'='1' and pw = '1' OR '1'='1';"
    因为WHERE条件恒为真，这就相当于执行：  
        strSQL = "SELECT * FROM users;"
    因此可以达到无账号密码亦可登录网站。如果恶意用户要是更坏一点  
    用户填入：
        passWord = ';DROP TABLE users 
    SQL语句变成了：
        strSQL = "SELECT * FROM users WHERE name = 'any_value' and pw = ''; DROP TABLE users"
    这样一来，虽然没有登录，但是数据表都被删除了。  

    然而使用PreparedStatement的参数化的查询可以阻止大部分的SQL注入。在使用参数化查询的情况下，数据库系统（eg:MySQL）不会将参数的内容视为SQL指令的一部分来处理，而是在数据库完成SQL指令的编译后，才套用参数运行，因此就算参数中含有破坏性的指令，也不会被数据库所运行。  
    补充：避免SQL注入的第二种方式：
    在组合SQL字符串的时候，先对所传入的参数做字符取代（将单引号字符取代为连续2个单引号字符，因为连续2个单引号字符在SQL数据库中会视为字符中的一个单引号字符，譬如：

        strSQL = "SELECT * FROM users WHERE name = '" + userName + "';"
    传入字符串：

        userName  = " 1' OR 1=1 " 
    把userName做字符替换后变成：
        userName = " 1'' OR 1=1"
    最后生成的SQL查询语句为：  
        strSQL = "SELECT * FROM users WHERE name = '1'' OR 1=1'  
    这样数据库就会去系统查找name为“1' ' OR 1=1”的记录，而避免了SQL注入。  

4. 比起凌乱的字符串追加似的查询，PreparedStatement查询可读性更好、更安全。 

####PreparedStatement的局限性
尽管PreparedStatement非常实用，但是它仍有一定的限制。  
1. 为了防止SQL注入攻击，PreparedStatement不允许一个占位符（？）有多个值，在执行有**IN**子句查询的时候这个问题变得棘手起来。下面这个SQL查询使用PreparedStatement就不会返回任何结果  

    SELECT * FROM loan WHERE loan_type IN (?)
    preparedSatement.setString(1, "'personal loan', 'home loan', 'gold loan'");
那如何解决这个问题呢？请你继续关注本博客，下期告诉你答案。


####不算总结的总结 
关于PreparedStatement接口，需要重点记住的是：   
1. PreparedStatement可以写参数化查询，比Statement能获得更好的性能。  
2. 对于PreparedStatement来说，数据库可以使用已经编译过及定义好的执行计划，这种预处理语句查询比普通的查询运行速度更快。  
3. PreparedStatement可以阻止常见的SQL注入式攻击。  
4. PreparedStatement可以写动态查询语句  
5. PreparedStatement与java.sql.Connection对象是关联的，一旦你关闭了connection，PreparedStatement也没法使用了。  
6. "?" 叫做占位符。  
7. PreparedStatement查询默认返回FORWARD_ONLY的ResultSet，你只能往一个方向移动结果集的游标。当然你还可以设定为其他类型的值如："CONCUR_READ_ONLY"。   
8. 不支持预编译SQL查询的JDBC驱动，在调用connection.prepareStatement(sql)的时候，它不会把SQL查询语句发送给数据库做预处理，而是等到执行查询动作的时候（调用executeQuery()方法时）才把查询语句发送个数据库，这种情况和使用Statement是一样的。  
9. 占位符的索引位置从1开始而不是0，如果填入0会导致*java.sql.SQLException invalid column index*异常。所以如果PreparedStatement有两个占位符，那么第一个参数的索引时1，第二个参数的索引是2.  

以上就是为什么要使用PreparedStatement的全部理由，不过你仍然可以使用Statement对象用来做做测试。但是在生产环境下你一定要考虑使用 **PreparedStatement** 。  

原文：[Why use PreparedStatement in Java JDBC](http://javarevisited.blogspot.com/2012/03/why-use-preparedstatement-in-java-jdbc.html#ixzz2YjEhPIis)  
更多参考：  
[SQL注入攻击](http://zh.wikipedia.org/wiki/SQL%E8%B3%87%E6%96%99%E9%9A%B1%E7%A2%BC%E6%94%BB%E6%93%8A)  
[参数化查询](http://zh.wikipedia.org/wiki/%E5%8F%83%E6%95%B8%E5%8C%96%E6%9F%A5%E8%A9%A2)  
[预处理语句与存储过程](http://php.net/manual/zh/pdo.prepared-statements.php)  
