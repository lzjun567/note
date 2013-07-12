###Java为什么需要Lambda表达式（-）

Lambda表达式即将出现在Java8中，但似乎还是遇到了些阻力，并不是所有Java 开发者都愿意买账，他们觉得添加函数式编程（[参考](http://www.ruanyifeng.com/blog/2012/04/functional_programming.html) ）的特性到Java中本身就是一种错误，因为这样不得不在Java所擅长的面向对象和指令式编程（[参考](http://zh.wikipedia.org/wiki/%E6%8C%87%E4%BB%A4%E5%BC%8F%E7%B7%A8%E7%A8%8B) ）中做出妥协。这篇文章的目的就是希望能用一些直白的例子来明确阐述Lambda的必要性以及打消部分开发者的顾虑---作为一门流行大众化编程语言支持Lambda表达式的的必要性。  

####外部与内部迭代  
先来看一个简单的例子：  

    List<Interger> numbers = Arrays.asList(1,2,3,4,5,6);

迭代所有元素并打印结果：  

    for (int number : numbers){
        System.out.println(number);
    }
（此处省略68字，俺实在是不知道作者说的啥，如果你看明白了，不妨在评论里告诉我，谢谢！）下面是作者与他两岁的女儿在玩玩具后的一段对话：  

>我：“Sofia，我们把完全收好吧，地上还有玩具吗？”
>Sofia：“好的，还有一个球”
>我：“嗯，把球放到盒子里去，还有其它东西吗？”
>Sofia：“有，还有我的洋娃娃”
>我：“好吧，把洋娃娃也放进盒子里，还有吗？”
>Sofia：“还有一本书”
>我：“把书也放进去，还有吗”
>Sofia：“没有了”
>我：“非常好，任务完成了”

这是我们天用着Java集合做的事情，但我们已不是两岁的小孩了，从外部迭代集合，逐个取出来处理，如果这样告诉Sofia：“把所有的玩具放进盒子里”，这种方式会更好。另外两个原因，为什么内部迭代更好呢？首先，Sofia可以同时选择一手拿娃娃，一手拿球，第二，他可以优先把最近的玩具放进盒子里。同理，使用内部迭代，[JIT编译器](http://zh.wikipedia.org/wiki/%E5%8D%B3%E6%99%82%E7%B7%A8%E8%AD%AF)可以并行处理元素达到优化或者按照不同的顺序处理。这些优化效果要是放在外部迭代那是没法实现的。   

为什么不在内部迭代？我认为这仅仅只是糟糕的心理习惯在作祟，Java集合框架中缺乏这样的支持。在Java8预览版中可以创建匿名内部类，如下：

    numbers.forEach(new Consumer<Interger>(){
        public void accept(Integer value){
            System.out.print(value);
        }
    });

重点来了....  

事实上，forEach方法和Consumer接口已经添加到Java8中来了，但是你可以在Java5+中使用类似guava或者lambdaj做一些类似的操作，然而lambda表达试可以用更少的代码和易读的方式实现相同的结果：  
    
    numbers.forEach((Integer value) -> System.out.println(value));

lambda表达式由两部份组成，箭头左边是参数部分右边是函数体，在这个例子中编译器自动计算出lambda表达式有相同的签名唯一没有实现的接口consumer（这就叫函数结果的原因），即使声称的直接骂可以潜在不同，类型声明lambda表达式参数可以，最大的部分  

    numbers.forEach(value -> System.out.println(value))；

但我们可以重写写它，最后一条语句甚至可以更简洁地使用方法引用，Java8中另一个特性：可以使用**::**操作符引用一个静态或实例方法：
      
    numbers.forEach(System.out::println);

以这种方式，函数式编程因[eta扩展](http://hongjiang.info/tag/java8/)而闻名。方法的名字被编译器expaned被编译器。

####不仅仅传递值，还有行为
我们看到前面些例子主要可能的原因为什么lambda表达式如此有用，传递一个lambda表达式给另一个方法，允许我们传递的不仅仅是值，还包括行为，这使得戏剧性的上升到我们抽象的级别，更加泛型，灵活可用的API，让我们看一个更深的例子：  

    List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
我们请求些一个方法，所有整数的和：  

    public int sumAll(List<Integer> numbers) {
        int total = 0;
        for (int number : numbers) {
            total += number;
        }
        return total;
    }

没过几天，经理跑过来告诉我们说，因业务需求还需要要一个函数求偶数项的和，因此什么样的方法是最快的呢？很简单，只要拷贝粘贴前面那个方法就行了：

    public int sumAllEven(List<Integer> numbers) {
        int total = 0;
        for (int number : numbers) {
            if (number % 2 == 0) {
                total += number;
            }
        }
        return total;
    }
    
又有一天，另外一个需求来了，这次他们需要求和只对大于3的数求和。那怎么做呢？我们再一次拷贝粘贴代码调整条件，但是这样感觉代码很乱，不是吗？现在，我们可以“First write，Second Copy，ThirdRefactor"原则，式时候考虑一个更聪明的更通用的方法去处理了。在这个例子中实现了一个更高顺序函数接受列表，还有断言（另一个函数式接口java8中出现的），定义了如何过滤。

    public int sumAll(List<Integer> numbers, Predicate<Integer> p) {
        int total = 0;
        for (int number : numbers) {
            if (p.test(number)) {
                total += number;
            }
        }
        return total;
    }

换句话说，我们传递方法不仅仅是这些数据，而且还有行为，定义如何使用他们。这样方法我们可以满足所有3种需求用一个更通用可重用的方法  

    sumAll(numbers, n -> true);
    sumAll(numbers, n -> n % 2 == 0);
    sumAll(numbers, n -> n > 3);

在第二篇文章中，我将展示更多例子说明lambda可以使我们的Java代码更可度更简洁。









https://jdk8.java.net/lambda/
