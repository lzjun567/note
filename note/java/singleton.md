单例模式
==============
单例模式在设计模式中属于最基本的设计模式之一，相信每个写过面向对象程序的程序员都知道：“**单例模式必须确保单例类在JVM中只能有一个实例存在。**”，这个老生常谈的问题为什么还要搬到这里来讨论呢？笔者试着以初学者的心态来重新认识单例模式，如果你是初、中级初学者（尼玛，初学者还分三六九等啊）不妨跟着我来重新学习一遍，不保证干活，但绝非软文。高级初学者可以不要往下看了。  

####为什么要创建单例类
+ 频繁创建对象，浪费创建时间，尤其是重量级的对象，使用单例可以减轻GC压力
+ 内存中只有一个对象，节省内存空间  
+ 全局可访问
+ 避免对共享资源的多重占用

####如何创建单例类

创建单例类难吗？真的很简单，看：  

    public class Foo{
        private static Foo INSTANCE;
        Private Foo(){}
        public static Foo getInstance(){
            if (INSTANCE==null){
                INSTANCE = new Foo();
            }
            return INSTANCE;
        }
    }

几行代码轻松搞定，借用我们老师的话来说就是“这个简单得要死”（你妹的，当时我心里就在骂他，你写了十几年程序和我们连HelloWorld都写不出的屌丝说这话），跑题了，快回来。  
结合代码，我们来总结一下创建单例模式的思路：1.一个类必须而且只能构建一个对象。2.获取该对象的方法（必须是静态的，为什么？）3.构造函数必须为私有方法（为什么？）  
那么这个程序真的能保证创建的实例唯一吗？我们用代码测试一下就知道：  

测试一：  

    public static void main(String[] args) {
    		Foo foo1 = Foo.getInstance();
    		Foo foo2 = Foo.getInstance();
    		System.out.println(foo1 == foo2);
    }

程序输入出：True  
看起来这个单例没什么问题，那么再来看看另外一种测试方法：  

    public static void main(String[] args) {
    		//线程一
    		Thread thread1 = new Thread(new Runnable() {
    			@Override
    			public void run() {	
    				Foo foo1 = Foo.getInstance();
    				System.out.println(foo1);
    			}
    		});
    		
    		//线程二
    		Thread thread2 = new Thread(new Runnable() {
    			@Override
    			public void run() {
    				Foo foo2 = Foo.getInstance();
    				System.out.println(foo2);
    			}
    		});
    		thread1.start();
    		thread2.start();
    }

程序输出：  

    Foo@5f186fab
    Foo@3d4b7453
原来还真是两个不同的对象，（如果你测试的结果不是我说期待的，那么说明你的运气还差点了，你可以多试试几次，再不行也没关系，我们在代码中做点小动作）：  

    public class Foo {
    	
    	private static  Foo foo;
    	private Foo(){}
    	public static Foo getInstance(){
    		
    		if (foo==null){
    			//人工干预
    			try {
    				Thread.sleep(100);
    			} catch (InterruptedException e) {}
    			foo = new Foo();
    		}
    		return foo;
    	}
    	
    	public static void main(String[] args) throws Exception {
    		
    		//线程一
    		final Thread thread1 = new Thread(new Runnable() {
    			@Override
    			public void run() {	
    				Foo foo1 = Foo.getInstance();
    				System.out.println(foo1);
    			}
    		});
    		
    		//线程二
    		Thread thread2 = new Thread(new Runnable() {
    			@Override
    			public void run() {
    				Foo foo2 = Foo.getInstance();
    				System.out.println(foo2);
    			}
    		});
    		thread1.start();
    		//人工干预
    		try {
    			Thread.sleep(1);  //主线程（main）暂停一毫秒
    		} catch (InterruptedException e) {/*为了代码简洁忽略异常，实际编码一般别这么干，除非你能驾驭异常*/}
    		thread2.start();
    	}
    }

改编后，新增的两处人工干预的代码，多线程环境下，CPU的时间片非常短，所以如果不采用人工干预，就有可能当一个线程执行完`foo=new Foo()`的时候第二个线程才运行到`if (foo==null)`语句，因此，启动thread1的时候，主线程暂停一毫秒，让thread1先执行到`if (foo==null)`语句处，然后等着thread2也跑起来，thread2执行到`if(foo==null)`的时候，发现`foo`实例（严格来说是引用）还没有创建，因此两个线程都进入了if条件语句，因此两个线程就创建的两个不同的对象。  

啰啰嗦嗦就是想说明这个最简单的单例创建方式在多线程并发环境下会违反实例单一原则的。









使用枚举:  

    public enum Foo{
        INSTANCE
    }



3.这样在其他地方就无法通过调用该类的构造方法来实例化这个类。
http://stackoverflow.com/questions/70689/what-is-an-efficient-way-to-implement-a-singleton-pattern-in-java

http://zh.wikipedia.org/wiki/%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F

http://stackoverflow.com/questions/2832297/java-singleton-pattern

http://stackoverflow.com/questions/2832297/java-singleton-pattern

http://balan.iteye.com/blog/164873
http://www.blogjava.net/dreamstone/archive/2006/11/04/79026.aspx
http://stackoverflow.com/questions/228164/on-design-patterns-when-to-use-the-singleton
