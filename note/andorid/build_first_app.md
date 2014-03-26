1. 下载Android SDK
2. 安装ADT插件(Eclipse)
3. 下载最新的SDK工具和平台用于SDK管理

直接下载[SDK ADT Bundle](https://dl.google.com/android/adt/22.6.2/adt-bundle-windows-x86_64-20140321.zip)，这是一个工具包含有了所有开发所需要的工具，包括（Android SDK组件，Eclipse IDE和内建的ADT（android developer tools）

下载解压完成后，创建第一个Android应用，直接点下一步直到最后完成就可以了。  

创建完成后，项目的目录结构如下：

![](http://foofish.qiniudn.com/layout1.png)
####AndroidManifest.xml
manifest 文件定义了app的说需要的基本组件，其中`<uses-sdk>`元素用来兼容Android的版本信息的。你应该这样设置：  

    <manifest xmlns:android="http://schemas.android.com/apk/res/android" ... >
        <uses-sdk android:minSdkVersion="8" android:targetSdkVersion="19" />
        ...
    </manifest>

####在模拟器上运行
在模拟器上运行app，首先需要创建一个AVD(Android Virtual Device)，这是一个Android模拟器的设备配置，他能模仿不同的设备。  
![](http://foofish.qiniudn.com/avd.png)

设置好AVD参数后，点击 Start--〉Launch，然后就能看到一个虚拟的Android设备了，看到下面的图要等很久。  
![](http://foofish.qiniudn.com/emulator.png)

接下来打开AndroidManifest.xml，然后选择Eclipse工具栏中的Run---〉Run As---〉Android Application，这样你的app就安装到了模拟器中去了。

在真机上运行的话只要把手机调为DEBUG模式就可以了。  


###构建一个简单的UI









Download the Android SDK.
Install the ADT plugin for Eclipse (if you’ll use the Eclipse IDE).
Download the latest SDK tools and platforms using the SDK Manager.

