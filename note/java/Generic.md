在没有泛型前，从集合中读取的元素都必须进行强制转换，比如：

    List foos = new ArrayList();
    foos.add(new Foo());
    Foo = (Foo)foos.get(0);  //必须强制转换

否则连编译没法通过，但是有了泛型之后，编译器可以在插入数据的时候自动帮你转换，编译时告知是否插入了错误类型。  

    List<Foo> foos = new ArrayList<Foo>();
    foos.add(new Foo());
    Foo = foos.get(0);  //无需转换

####使用泛型的需要注意的陷进

首先需要知道几个术语：

+ **泛型**：声明的时候，拥有一个或多个类型参数的类或者接口，称之为泛型类或泛型接口，两者又统称为泛型（generic type） 如：List<String>就声明了一个String类型的参数 

+ **参数化类型（parameterized type）**：参数化类型包含一个类或者接口名称C，以及实际的类型参数列表<T1,...Tn>

+ **原生类型（raw type）**：原生类型是满足以下条件之一：   
    1. 使用的泛型类型声明的名称，而没有任何伴随的实际类型的参数  
    2. 元素的类型为原生类型的数组类型  
    3. 原生类型R的任何非静态类型成员，且它不是从R的超类或者超接口派生而来的  

举例：  

    public class MyType<E> {
        class Inner { }
        static class Nested { }
    
        public static void main(String[] args) {
            MyType mt;          // warning: MyType is a raw type
            MyType.Inner inn;   // warning: MyType.Inner is a raw type
    
            MyType.Nested nest; // no warning: not parameterized type
            MyType<Object> mt1; // no warning: type parameter given
            MyType<?> mt2;      // no warning: type parameter given (wildcard OK!)
        }
    }
这里，`mt`和`inn`就是原生类型的，而`ntst`不是，因为他是静态类型成员，`mt1`和`mt2`属于参数化类型。  

####陷进一：  不要使用原生态类型
本质上，原生类型的行为方法和泛型没什么两样，就像如下代码：  

    List names = new ArrayList(); // warning: raw type!
    names.add("John");
    names.add("Mary");
    names.add(Boolean.FALSE); // not a compilation error!

代码没有任何问题，但是，  

    for (Object o : names) {
        String name = (String) o;
        System.out.println(name);
    } // throws ClassCastException!
      //    java.lang.Boolean cannot be cast to java.lang.String


如上代码在运行的时候，就会抛出`ClassCastException`的异常。  

有了泛型，编译器就能帮你完成类型检测的工作.

    List<String> names = new ArrayList<String>();
    names.add("John");
    names.add("Mary");
    names.add(Boolean.FALSE); // compilation error!

####原生类型List与List<Object>参数化类型的区别  

原生类型List躲避了泛型检查，参数化类型List<Object>告知编译器，它能装任意类型的对象，虽然你可以将List<String>传递给类型List的参数，但是不能将它传递给类型List<Object>的参数。为什么呢？这是子类型化（subtyping）的规则。

####子类型化（subtyping）

常规类中，如果类B继承A，那么类B就是类A的子类，但是这条规则并不能适用于泛型中。

    class A {}
    class B extends A {}

    List<B> lb = new ArrayList<>();
    List<A> la = lb;  //compile-time error
[generics-listParent.gif]
尽管Integer是Number的子类，但是List<Integer>并不是List<Number>的子类，两者没有任何关系，而他两的共同父类是List<?>.  

为了通过List<Integer>的元素来访问Number的方法，可以使用向上通配符：  
    
    List<? extends Integer> intList = new ArrayList<>();
    List<? extends Number> numList = intList  //Ok，List<? extends Integer> is a subtype of List<? extends Number>



http://stackoverflow.com/questions/2770321/what-is-a-raw-type-and-why-shouldnt-we-use-it
http://docs.oracle.com/javase/specs/jls/se7/html/jls-4.html#jls-4.8
http://docs.oracle.com/javase/tutorial/java/generics/subtyping.html

