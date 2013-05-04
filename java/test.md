Java虚拟机中，内存分为三个代：分别是：新生代（new）、老生代（Old）、永久代（Perm）。  
新生代：新建的对象都存放在这个地方  
老生代：存放从新生代中迁移过来的生命周期较久的对象，new和old共同组成堆内存。  
永久代：非堆内存，

OutOfMemoryError:Java heap space异常：所名Java虚拟机堆内存不够，主要原因：
Java 虚拟机的堆内存设置不够，通过参数-Xms  -Xmx来调整。  
代码中创建了大量大对象，长时间不能被垃圾收集器收集（存在被引用）。

OutOfMemoryError:PermGen space,Java虚拟机对永久代Perm内存设置不够。
这种情况出现可能是程序启动需要加载大量第三方jar包。

配置：
JAVA_OPTS="-server -Xms768m -Xmx768m -XX:PermSize=768m -XX:MaxPermSize=768m -XX:NewSize=256m -XX:MaxNewSize=512m"


应用占用CPU很高：两种可能：计算密集性应用，或者是死循环了。

ps -m 显示所有执行者
ps -p 进程识别码



调用jdk工具jps查看当前的java进程  
