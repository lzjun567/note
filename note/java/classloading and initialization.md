Java 类加载与初始化
==================
理解类在JVM中什么时候被加载和初始化是Java编程语言中的基础概念，正因为有了Java语言规范，我们才可以清晰的记录和解释这个问题，但是很多Java程序员仍然不知道什么时候类被加载什么时候类被初始化，类加载和初始化好像让人很困惑，对初学者难以理解，在这篇教程中我们将看看类加载什么时候发生，类和接口是如何被初始化的，我并不会拘泥于类加载器的细节或者说类加载器的工作方式。仅仅使这篇文章更加专注和简结。  

#####类什么时候加载
类的加载是通过类加载器（Classloader）完成的，它既可以是饿汉式[eagerly load]（只要有其它类引用了它就加载）加载类，也可以是懒加载[lazy load]（等到类初始化发生的时候才加载）。不过我相信这跟不同的JVM实现有关，然而他又是受JLS保证的（当有静态初始化需求的时候才被加载）。  

####类什么时候初始化
加载完类后，类的初始化就会发生，意味着它会初始化所有类静态成员，以下情况一个类被初始化：  

1. 实例通过使用new()关键字创建或者使用class.forName()反射，但它有可能导致ClassNotFoundException。  
2. 类的静态方法被调用
3. 类的静态域被赋值
4. 静态域被访问，而且它不是常量
5. 在顶层类中执行assert语句

反射同样可以使类初始化，比如java.lang.reflect包下面的某些方法，JLS严格的说明：一个类不会被任何除以上之外的原因初始化。  

####类是如何被初始化的
现在我们知道什么时候触发类的初始化了，他精确地写在Java语言规范中。但理清域（fields，静态的还是非静态的）、块（block静态的还是非静态的）、不同类（之类和超类）和不同的接口（子接口，实现类和超接口）的初始化顺序也很重要类。事实上很多核心Java面试题和SCJP问题都是基于这些概念，下面是类初始化的一些规则：  

1. 类从顶至底的顺序初始化，所以声明在顶部的字段的早于底部的字段初始化
2. 超类早于子类和衍生类的初始化
3. 如果类的初始化是由于访问静态域而触发，那么只有声明静态域的类才被初始化，而不会触发超类的初始化或者子类的初始化即使静态域被子类或子接口或者它的实现类所引用。  
4. 接口初始化不会导致父接口的初始化。
5. 静态域的初始化是在类的静态初始化期间，非静态域的初始化时在类的实例创建期间。这意味这静态域初始化在非静态域之前。  
6. 非静态域通过构造器初始化，子类在做任何初始化之前构造器会隐含地调用父类的构造器，他保证了非静态或实例变量（父类）初始化早于子类

#####初始化例子
这是一个有关类被初始化的例子，你可以看到哪个类被初始化  

    /**
     * Java program to demonstrate class loading and initialization in Java.
     */
    public class ClassInitializationTest {
    
        public static void main(String args[]) throws InterruptedException {
      
            NotUsed o = null; //this class is not used, should not be initialized
            Child t = new Child(); //initializing sub class, should trigger super class initialization
            System.out.println((Object)o == (Object)t);
        }
    }
    
    /**
     * Super class to demonstrate that Super class is loaded and initialized before Subclass.
     */
    class Parent {
        static { System.out.println("static block of Super class is initialized"); }
        {System.out.println("non static blocks in super class is initialized");}
    }
    
    /**
     * Java class which is not used in this program, consequently not loaded by JVM
     */
    class NotUsed {
        static { System.out.println("NotUsed Class is initialized "); }
    }
    
    /**
     * Sub class of Parent, demonstrate when exactly sub class loading and initialization occurs.
     */
    class Child extends Parent {
        static { System.out.println("static block of Sub class is initialized in Java "); }
        {System.out.println("non static blocks in sub class is initialized");}
    }
    
    Output:
    static block of Super class is initialized
    static block of Sub class is initialized in Java
    non static blocks in super class is initialized
    non static blocks in sub class is initialized
    false

从上面结果可以看出：  

1. 超类初始化早于子类
2. 静态变量或代码块初始化早于非静态块和域
3. 没使用的类根本不会被初始化，因为他没有被使用

再来看一个例子：  

    /**
     * Another Java program example to demonstrate class initialization and loading in Java.
     */
    
    public class ClassInitializationTest {
    
        public static void main(String args[]) throws InterruptedException {
      
           //accessing static field of Parent through child, should only initialize Parent
           System.out.println(Child.familyName);
        }
    }
    
    class Parent {
        //compile time constant, accessing this will not trigger class initialization
        //protected static final String familyName = "Lawson";
      
        protected static String familyName = "Lawson";
      
        static { System.out.println("static block of Super class is initialized"); }
        {System.out.println("non static blocks in super class is initialized");}
    }
    
    Output:
    static block of Super class is initialized
    Lawson

分析：  

1. 这里的初始化发生是因为有静态域被访问，而且不一个编译时常量。如果声明的"familyName"是使用final关键字修饰的编译时常量使用（就是上面的注释代码块部分）超类的初始化就不会发生。
2. 尽管静态与被子类所引用但是也仅仅是超类被初始化

还有另外一个例子与接口相关的，JLS清晰地解释子接口的初始化不会触发父接口的初始化。强烈推荐阅读JLS14.4理解类加载和初始化细节。以上所有就是有关类被初始化和加载的全部内容。  



