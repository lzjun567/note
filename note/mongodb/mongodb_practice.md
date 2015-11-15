1. ObjectId用ObjectId存储，不要用字符串来存，ObjectId只占用12个字节，而字符串是它的两倍多，其次可以从ObjectId对象中获取时间等信息。  

导入/导出

    mongodump -d <our database name> -o <directory_backup>
    
    mongorestore -d DATABASE ./dump-folder
    
    
or 查询  
查询时，有时需要一个值在多个字段中，比如：用户输入的可能是邮箱，也可能是手机号码，那么我需要用or来操作：  
    
    {$or: [{username: xxxxx}, {phone: xxxxxxx}]}


