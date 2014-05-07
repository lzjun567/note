细说finally
===============
在网上有一个热议的微薄[大家觉得这段代码返回值是什么？为什么？](http://weibo.com/1970145123/AD5uLyBUm),代码如下:  

    int x = 0;
    try{
        return x;
    }
    finally{
        x++;
        System.out.println(x);  // Prints new value of x
    }

回答地一个问题, finally代码块会不会执行, 如果会执行那么返回值是1还是0 


