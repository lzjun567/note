MySQL中innodb实现的事务的ACID，MySQL中的事务分为两种：第一种是标准事务（normal transaction），第二种是语句事务（statement transaction）.  

标准事务用begin,rollback,commit实现

语句事务通过set改变mysql的自动提交模式，默认mysql是自动提交的，也就是每一条语句对应一个事务
