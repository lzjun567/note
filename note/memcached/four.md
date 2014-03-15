####memcached分布式
计算hash: 公式:  h = Hash(key)%n  
n:memcached服务器的节点数量  
hash函数是一个从字符串到整数的转换函数.  
优点: 简单, key分布均匀  
缺点:  扩展性不好,容错性也不好, 如果有一台服务器宕机了

实验:  abc...xyz 二十六个字母代表26个key,需要分布在n0,n1,n2缓存上去.

    keys = [chr(i) for i in range(97,97+26)]
    result = {}
    for key in keys:
         k = hash(key)%3
         if k not in result:
             result[k] = [key,]
         else:
             result.get(k).append(key)

result:

    {
        0: ['v', 'x', 'z'], 
        1: ['b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', 'r', 't', 'w', 'y'], 
        2: ['a', 'c', 'e', 'g', 'i', 'k', 'm', 'o', 'q', 's', 'u']
    }

新增一个节点后, 命中率降到了原来的 10/26

    {
        0: ['a', 'e', 'i', 'm', 'q', 'u', 'y'], 
        1: ['d', 'h', 'l', 'p', 't', 'x'], 
        2: ['c', 'g', 'k', 'o', 's', 'w'], 
        3: ['b', 'f', 'j', 'n', 'r', 'v', 'z']
    }

一致性哈希具有良好的单调性,不会应为节点的增加或者减少而影响哈希的重新定位.  
http://amix.dk/blog/post/19367
http://blog.codinglabs.org/articles/consistent-hashing.html
https://www.adayinthelifeof.nl/2011/02/06/memcache-internals/
