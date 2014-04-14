mysqldump备份恢复数据库
=======================
mysqldump程序可以用来备份和恢复数据库,默认情况mysqldump会创建drop table, create table,和insert into的sql语句.  

语法  

    > mysqldump [options] db_name [tbl_name ...]
    > mysqldump [options] --databases db_name ...
    > mysqldump [options] --all-databases

备份指定数据库  

    mysqldump -uroot -p[passwd] db1 > dumpfilename.sql

备份多个数据库   

    mysqldump -uroot -p[passwd] --databases db1 db2 > dumpfilename.sql
备份所有数据库  

    mysqldump -uroot -p[passwd] --all-databases > dumpfile.sql

备份指定表  

    mysqldump -uroot -p[passwd] db1 table1 > db1_table1.sql

只备份表结构  
    
    mysqldump -uroot -p[passwd] -d db1 > dumpfile.sql

如果不想要drop table, 附上参数`--compact`  

    mysqldump -uroot -p[passwd] --compact db1 > dumpfile.sql

还原  
    
    mysql -uroot -ppassword db1 < dumpfile.sql


如果存储引擎是MYISAM,还可以使用`mysqlhotcopy`  

    mysqlhotcopy -u root -p passwd db1 备份目录

注意,-u后面有个空格, mysqlhotcopy相当于把数据库文件拷贝到新的目录. 恢复的方法就是把该备份目录拷贝到mysql数据目录下面. 
