Gradle 教程 PART 1： 入门
===================
####什么是Gradle？
Gradle是一种依赖管理工具（待确定），基于Groovy语言，面向Java应用为主，它抛弃了基于XML的各种繁琐配置，取而代之的是一种基于Groovy的内部领域特定（DSL）语言。
####下载安装Gradle
Gradel版本2.4，下载地址在[这里](http://gradle.org/)，下载后是一个文件名为gradle-2.4-all.zip压缩包，解压之后设置环境变量。编辑~/.profile   
    
    GRADLE_HOME=/Users/lzjun/Dev/gradle-2.4;
    export GRADLE_HOME
    export PATH=$PATH:$GRADLE_HOME/bin

####Gradle基本命令

    gradle -q tasks
查看所有task，`-q`参数是简单输出模式，如果不想看太多的细节就可以使用它  

build.gradle文件是标准的构建文件，编辑example/build.gradle ：  
    
    task compileTask << { 
    System.out.println "compiling..." 
    }
    
 执行
 
    gradle -q tasks

就会列出很多可以执行的task出来，最后你还注意到，有个我们自己创建的task：  
    
    Other tasks
    -----------
    compileTask


gradle构建文件就是一系列的task，执行某个具体的task命令就是：  
    
    gradle -q compileTask

此外，你可以在build.gradle中指定默认的tasks：  
    
    defaultTasks 'buildTask'

    task compileTask << {
      System.out.println "compiling..." 
    }
    
    task buildTask << {
      System.out.println "building..."
    }

当执行gradle没有指定哪个task时，gradle会执行defaultTasks，执行：  
    
    gradle -q

一个task可以依赖于另外一个task，当a依赖b时，执行a的时候gradle会先执行b，  
    
    defaultTasks 'buildTask'

    task compileTask << {
      System.out.println "compiling..." 
    }
    
    task buildTask (dependsOn:compileTask) << {
      System.out.println "building..."
    }

构建工具要做的事情就是：comple，build，run tests, package等等，在gradle中就是一个个的task，有时你不必手写task，使用plugins来构建项目。有很多plugin包括 Java plugin, WAR plugin, Android plugin等等。

Gradle 教程 PART 2： 构建Java项目
===================
这节主要包括：如果使用Gradle来编译、构建、测试你的Java项目，构建Java项目不需要我们去挨个的手写task，因为先辈们已经写了plugin，我们直接拿来用即可。任何plugin添加到build.gradle文件的可通过语句：  
    
    apply plugin: <plugin-name>
我们的例子是使用java plugin，那么直接使用语句：  
    
    apply plugin: "java"

现在开始编辑example2/build.gradle文件，添加如下文本：  
    
    apply plugin: "java"
这个plugin会添加一系列的task来处理java项目，现在执行tasks看看该plugin包含了哪些task：  
    
    gradle -q tasks
输出：  
    
    Build tasks
    -----------
    assemble - Assembles the outputs of this project.
    build - Assembles and tests this project.
    buildDependents - Assembles and tests this project and all projects that depend on it.
    buildNeeded - Assembles and tests this project and all projects it depends on.
    classes - Assembles classes 'main'.
    jar - Assembles a jar archive containing the main classes.
    testClasses - Assembles classes 'test'.

每个task都有说明具体是的任务内容是什么。Gradle构建Java项目时，plugin要求Java的目录结构遵循规范：  
    
    src/main/java    
    src/main/resources
    
    src/test/java
    src/test/resources

按照规范创建一个项目：  
    
    └── example2
    ├── build.gradle
    └── src
        ├── main
        │   ├── java
        │   │   └── net
        │   │       └── foofish
        │   │           └── quoteapp
        │   │               └── Quote.java
        │   └── resources
        └── test
            ├── java
            └── resources
编辑Quote.java：  
    
    package net.foofish.quoteapp;

    public class Quote {
         private Long id;
         private String who;
         private String what;
    
     public void setId(Long id) {
        this.id = id;
     }
     public void setWho(String who) {
        this.who = who;
     }
     public void setWhat(String what) {
        this.what = what;
     }
     public Long getId() {
        return id;
     }
     public String getWho() {
        return who;
     }
     public String getWhat() {
        return what;
     }
    }

执行：  
    
    gradle assemble

assemble的过程会对项目进行编译，最后把打包成jar文件，当然该命令并不会涉及test，从输出结果中可以看出只有4个依赖的task：  
    
    ➜  example2  gradle assemble
    :compileJava UP-TO-DATE
    :processResources UP-TO-DATE
    :classes UP-TO-DATE
    :jar UP-TO-DATE
    :assemble UP-TO-DATE
    
    BUILD SUCCESSFUL
    
    Total time: 2.738 secs

如果assemble命令顺利执行的话，那么将会在项目的根目录生成build目录，example2.jar在build/libs下：  
    
    ├── build
    │   ├── classes
    │   │   └── main
    │   │       └── net
    │   │           └── foofish
    │   │               └── quoteapp
    │   │                   └── Quote.class
    │   ├── dependency-cache
    │   ├── libs
    │   │   └── example2.jar
    │   └── tmp
    │       ├── compileJava
    │       └── jar
    │           └── MANIFEST.MF

如果要清空build目录，那么执行clean命令即可。如果需要指定版本号以及jar文件名，都可以在build.gradle文件中指定：  
    
    apply plugin: "java"
    archivesBaseName = "quote"
    version = '1.0-FINAL'
重新build后，得到的文件名将是： quote-1.0-FINAL.jar，了解更多有关java plugin的东西，你必须参看其[官方文档](https://docs.gradle.org/current/userguide/java_plugin.html)

####处理代码依赖
如果源代码中需要用到第三方的依赖包，比如 Apache Commons JAR：  
    
    package net.foofish.quoteapp;
    import org.apache.commons.lang3.builder.ToStringBuilder;
    
    public class Quote {
     private Long id;
     private String who;
     private String what;
     
     public void setId(Long id) {
     this.id = id;
     }
     public void setWho(String who) {
     this.who = who;
     }
     public void setWhat(String what) {
     this.what = what;
     }
     public Long getId() {
     return id;
     }
     public String getWho() {
     return who;
     }
     public String getWhat() {
     return what;
     }
    
     public String toString() {
     return ToStringBuilder.reflectionToString(this);
     }
    }

现在如果直接build，那么肯定会出现BUILD FAILED的消息，因为gradle根本找不到ToStringBuilder类在哪里，要想Gradle定位到相应的JAR文件，你需要告诉gradle对应JAR文件所在的仓库在哪儿。  
好在Gradle支持主流的如Maven Central， lvy，甚至是本地仓库都行，所以如果你了解Maven的话，理解起来就没任何压力。现在你需要在build.gradle文件中配置远程仓库。  
    
    repositories {
      mavenCentral()
    }

这样就能确保Gradle可以在Maven Central 仓库找到任何依赖的JAR文件，在Maven Central中定位一个JAR文件需要三个元素：  
    
    A Group Id (group)
    An Artifact Id (name)
    A Version (version)

比如你要依赖Apache Commons 3.3.2 JAR ，那么需要提供：  
    
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.3.2</version>
类似的，在Gradle中通过dependdencies元素来指定，依赖配置有几种标准的类型，分别是：  
    
* compile
* runtime
* testCompile
* testRuntime

现在把Apache Commons Lang 3.3.2的依赖加进来：  
    
    apply plugin: 'java'
    archivesBaseName = "quote"
    version = '1.0-FINAL'
    
    repositories {
     mavenCentral()
    }
    
    dependencies {
     compile group: 'org.apache.commons', name: 'commons-lang3', version: '3.3.2'
    }
    
每个依赖包单独一行，此外还有一种简化格式来指定denpendency：  
    
    dependencies {
      compile 'org.apache.commons:commons-lang3:3.3.2'
    }
最后添加单元测试的依赖包时，比如JUnit，仅仅需要更新denpendencies：  
    
    dependencies {
     compile group: 'org.apache.commons', name: 'commons-lang3', version: '3.3.2'
     testCompile group: 'junit', name: 'junit', version: '4.+'
    }
`+`表示下载4.x中最新的版本。

Gradle 教程 PART 3： build 多个java项目
===========================
假设有多个项目是相互依赖的，例如：  
    
    javaprojects
    |- api
    |- common
    |- app
他们的依赖关系是： 
 
1. common：这个项目是一些工具类，他不会依赖其他项目，当然他有可能依赖第三方库。  
2. api：这个项目包含API代码，需要依赖common项目。
3. app：这个项目包含应用代码，需要依赖common和api两个项目。

Gradle需要有一个中心位置来构建这三个项目，达到这个目的很简单，Gradle会要求你在javaprojects目录下创建一个settings.gradle文件。编辑文件：  
    
    include ":api", ":common", ":app"
把三个项目包含进来即可。
####通用配置
创建build.gradle在javaprojects目录，在build.gradle文件中，  
    
    allprojects {
      //Put instructions for all projects
        task hello << { task -> println "I'm $task.project.name" }
    }
    
    subprojects {
      //Put instructions for each sub project
      task hello2 << { task -> println "I'm $task.project.name" }
    }

保存文件，执行：  
    
    gradle -q hello
输出：    
    
    I'm javaprojects
    I'm api
    I'm app
    I'm common

你可以单独执行某个子项目的task，如：   
    
    gradle -q app:hello
现在你应该清楚你可以在所有项目中执行命令，也可以应用在每一个子项目中或者指定的项目。  















Gradle 教程 PART 3： Android Studio + Gradle
===========================












