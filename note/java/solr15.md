索引更新
=======
http://wiki.apache.org/solr/UpdateJSON
更新的请求处理器是： <requestHandler name="/update" class="solr.UpdateRequestHandler"/>  
请求头需要指定：Content-type:application/json or Content-type:text/json  



Solr有两种方法来局部更新文档，第一种事原子更新(atomic updates)，第二种是乐观并行或称之为乐观锁。它是很多NoSQL的特性，基于版本号有条件的更新文档。这种方法包含语言和规则来处理如何匹配版本和不匹配版本。  

####原子更新
Solr支持三种原子修改器：set,add,inc
* set：设置或替换特定的值，如果value为“null”那么就代表删除
* add：添加一个值到列表中
* inc：递增一个数字值

    {
      "id"        : "TestDoc1",
      "player_name"     : {"set":"艾弗森"},
      "group_name" : {"add":"76人"}    #用于多值字段
     }
    
    
     
    {
      "id"        : "TestDoc1",
      "player_name"     : {"set":"艾弗森"}
     }
    
     
    {
      "id"        : "TestDoc1",
      "player_name"  :"艾弗森"
     }
像shang 这会替换原来的文档


[{
      "id": "TestDoc1",
      "followers": {"inc":3}
     },
 {
  "id": "TestDoc2",
  "followers" : {"set":10}
 }]

 不行

 {"add":{ "doc":{
      "id": "TestDoc1",
      "followers": {"inc":3}
     },"boost":1.0,"overwrite":true,"commitWithin":1000}}


真正的请求时这样子的：更新多个文档： 
    
    {"add":{ "doc":{
      "id": "TestDoc1",
      "followers": {"inc":3}
     },"boost":1.0,"overwrite":true,"commitWithin":1000},
     
     "add":{ "doc":{
      "id": "TestDoc2",
      "followers": {"inc":3}
     }}
     
     }


     {"add":{
	"doc":{
		"id": "TestDoc1",
		"followers": {"inc":3}
	},"boost":1.0,"overwrite":true,"commitWithin":1000},
 "add":{ 
	"doc":{
      "id": "TestDoc2",
      "followers": {"inc":3}
     }},
     "add":{ "doc":{
      "id": "TestDoc3",
      "followers": {"inc":3}
     }}
     
     }
