####memcached协议
从第二篇介绍来看, memcached的[协议](https://github.com/memcached/memcached/blob/master/doc/protocol.txt)非常简单, 没有采用xml,json等数据格式, 就是简单的**文本行**(直接telnet就可以完成数据的存取操作)和**非结构化数据**.文本行总是以\r\n结尾, 非结构化数据同样也是以\r\n结尾  
####内存分配机制
slab是memcached用来存放item的机制., 如图:  
![](../note/resource/slab.png)

item:需要存储的数据, 包括item结构体, key和value  
slab class:相当于一个容器, 没有大小概念, 只有page, page默认大小是1MB,也就是slab是装有page的容器, page里面放的是chunk,chunk是存储item的最小单元.   
不同的slab中的page的大小多是一样的大小. 为1MB,  

    memcached -d -m 128 -vv
    slab class   1: chunk size        80 perslab   13107
    slab class   2: chunk size       104 perslab   10082
    slab class   3: chunk size       136 perslab    7710
    slab class   4: chunk size       176 perslab    5957
    slab class   5: chunk size       224 perslab    4681
    ...............
    ...............
    ...............
    slab class  38: chunk size    367192 perslab       2
    slab class  39: chunk size    458992 perslab       2
    slab class  40: chunk size    573744 perslab       1
    slab class  41: chunk size    717184 perslab       1
    slab class  42: chunk size   1048576 perslab       1

当然 这是memcache的内存分配策略, 此时还没有真正分配内存, 可以使用free前后对比一下就知道.  

