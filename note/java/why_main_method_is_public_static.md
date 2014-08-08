为什么java的main方法是public static void
==================
Main方法是学习Java编程语言时知道的第一个方法，你是否曾经想过为什么main方法是public、static、void的。当然，很多人首先学的是C和C++，但是在Java中main方法与前者有些细微的不同，它不会返回任何值，**为什么main方式是public、static、void** ，这篇文章尝试去找到一些答案。  

Main方法是Java程序的入口，记住，我们这里不会讨论Servlet、MIDlet和其他任何容器管理的java程序，在java核心编程中，JVM会查找类中的**public static void main(String[] args)**，如果找不到该方法就抛出错误**NoSuchMethodError:main** 程序终止。  
Main方法必须严格遵循它的语法，方法签名必须是public static void，参数是字符串数组类型，如果是Java1.5及以后的版本也可以使用可变参数：**public static void main(String... args)**  

####为什么main方法是静态的（static）
1. 因为main方法是静态的，JVM调用这个方法不需要创建任何包含这个main方法的实例。  
2. 因为C和C++同样有类似的main方法作为程序执行的入口。
3. 如果main方法不声明为静态的，JVM就必须创建main类的实例，因为构造器可以被重载，JVM没法确定找哪个main方法。  
4. 静态方法和静态数据加载到内存就可以直接调用而不需要像实例方法一样创建了实例才能调用，如果main方法是静态的，那么它就会被加载到JVM上下文中成为可执行的方法。  
####为什么main方法是公有的（public）
Java指定了一些可访问的修饰符如：private、protected、public，任何方法或变量都可以声明为public，Java可以从该类之外的地方访问。因为main方法是公共的，JVM就可以轻松的访问执行它。  
####为什么main方法没有返回值（Void）
因为main方法不应该返回任何值，因此void意味着main不会返回任何值  

####总结

1. main方法必须声明为public、static、void，否则JVM没法运行程序
2. 如果JVM找不到main方法就跑出NoSuchMethodException:main异常，例如：如果你运行命令：`java HelloWrold`，JVM就会在HelloWorld.class文件中搜索public static void main (String[] args) 放法
3. main方式是程序的入口，程序执行的开始处。
4. main方法被一个特定的线程"main"运行，程序会一直运行直到main线程结束或者non-daemon线程终止。
5. 当你看到“Exception in Thread main”如：**Excpetion in Thread main:Java.lang.NullPointedException** ,意味着异常来自于main线程
6. 你可以声明main方法使用java1.5的可变参数的方式如：  

        public static void main(String... args)
7. 除了static、void、和public，你可以使用final，synchronized、和strictfp修饰符在main方法的签名中，如：  

        public strictfp  final synchronized static void main(String[] args)

8. main方法在Java可以像其他方法一样被重载，但是JVM只会调用上面这种签名规范的main方法。  
9. 你可以使用throws子句在方法签名中，可以抛出任何checked和unchecked异常
10. 静态初始化块在JVM调用main方法前被执行，它们在类被JVM加载到内存的时候就被执行了。


[javavisited](http://javarevisited.blogspot.com/2011/12/main-public-static-java-void-method-why.html)
