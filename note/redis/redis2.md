Redis“发布/订阅”模式
====================
发布订阅者模式可以实现进程之间的消息传递，该模式包含两个角色，分别为“发布者”和“订阅者”。订阅者可以订阅一个或多个频道（channel），发布者可以向指定的频道（channel）发送消息。订阅了此频道的订阅者都会收到该消息。  

publish：发布者发布消息的命令，语法：publish channel message。例如：像频道channel1发送消息“hi”    

    127.0.0.1:6379> publish chanel1.1 hi
    (integer) 0
客户端只能收到当前及之后发布的消息，之前的消息没法收到，上面返回0表示还没有任何客户端订阅该频道。  

subscribe：订阅频道的命令，语法：subscribe channel [channel2 ...]，一个客户端可以订阅多个频道。例如：  
    
    127.0.0.1:6379> subscribe channel1.1
    Reading messages... (press Ctrl-C to quit)
    1) "subscribe"
    2) "channel1.1"
    3) (integer) 1  

进入订阅状态的客户端返回数据包括3个值，
* 第一个值是消息类型：可能的值包括：
    * subscribe：订阅成功的反馈信息，第二个值是订阅成功的频道名称，第三个值是当前客户端订阅的频道数量

