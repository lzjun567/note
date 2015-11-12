Android 应用集成 LeanCloud 推送
========================
推送服务是唤醒用户继续使用App的一种手段，今天花时间了解LeanCloud的推送服务，读了下大概的文档，再结合Demo把推送服务集成到了[西源坊](https://github.com/lzjun567/XiYuanFang)的App中。罗列了一下开发的流程以及遇到的一些问题总结：  

####第一步：注册账号，创建应用
注册账号是普通的注册流程，应用是对接App的一个LeanCloud应用，创建好应用之后会分配 AppID，AppKey，这两个参数非常重要，App端需要根据这两个参数来对接到LeanCloud中创建的应用。

####第二步：配置App开发环境
官方文档写的还是比较清晰，基本能读懂，这样我们就可以对着文档来一步步设置。
  
1. 配置项目的build.gradle，主要是设置LeanCloud的maven仓库地址  
        
        buildscript {
            repositories {
                jcenter()
                maven {
                 url "http://mvn.leancloud.cn/nexus/content/repositories/releases"
                }
            }
            dependencies {
                classpath 'com.android.tools.build:gradle:1.2.3'
            }
        }
        
        allprojects {
            repositories {
                jcenter()
                maven {
                    url "http://mvn.leancloud.cn/nexus/content/repositories/releases"
                }
            }
        }
    新增的两行是leancloud的maven地址。这里有可能遇到的一个问题：
        >>>“Gradle: resolve dependancies '_debugCompile'” or 'detachedConfiguration1'`，

    Android Studio一直处于挂起的状态，始终停在_debugCompile的状态。有可能是Android Studio的问题，也有可能是网络问题，但具体问题不祥。解决的办法之一是：把Gradle设置为**work offline**模式。  
    ![work offline](http://i.stack.imgur.com/qrWdJ.png)
2. 配置app目录下的build.gradle，主要是指定LeanCloud所必须的依赖包：  
        
        android {
            //为了解决部分第三方库重复打包了META-INF的问题
            packagingOptions{
                exclude 'META-INF/LICENSE.txt'
                exclude 'META-INF/NOTICE.txt'
            }
            lintOptions {
                abortOnError false
            }
        }
        
        dependencies {
        
          //avoscloud-sdk 为 LeanCloud基础包
          compile 'cn.leancloud.android:avoscloud-sdk:v3.+'
    
          //avoscloud-push 与 Java-WebSocket 为推送与IM需要的包
          compile 'cn.leancloud.android:avoscloud-push:v3.+@aar'
          compile 'cn.leancloud.android:Java-WebSocket:1.2.0-leancloud'
    
          //avoscloud-statistics 为 LeanCloud 统计包
          compile 'cn.leancloud.android:avoscloud-statistics:v3.+@aar'
        }
    需要注意的是：推送服务也必须包含Java-WebSocket包，否则推送的时候会出现类似ClassNotFoundError的错误。  
    
基本的配置就完成了，接下来就是更新APP中的代码。

####第三步：配置AndroidManifest

1. 确保app设置了基本网络相关的权限  
        
        <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
        <uses-permission android:name="android.permission.INTERNET" />
        <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
        <uses-permission android:name="android.permission.READ_PHONE_STATE" />
        <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
        <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
        <uses-permission android:name="android.permission.VIBRATE" />
2. 指定PushService

        <service android:name="com.avos.avoscloud.PushService"
            android:exported="true"/>

3.  在`<application>`中指定AVBroadcastReceiver，App能在关闭的情况下也可以收到推送

        <receiver android:name="com.avos.avoscloud.AVBroadcastReceiver">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.USER_PRESENT" />
            </intent-filter>
        </receiver>

####第四步：初始化LeanCloud信息
在应用访问 LeanCloud 之前，需要使用 AppID 和 AppKey 在代码中对 LeanCloud SDK 进行初始化。
 
```java   
public class MyApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        // 初始化应用信息
        AVOSCloud.initialize(this, "your app id", "your app key");
        // 启用崩溃错误统计
        AVAnalytics.enableCrashReport(this.getApplicationContext(), true);
        AVOSCloud.setLastModifyEnabled(true);
        AVOSCloud.setDebugLogEnabled(true);
}
```

####第五步：保存 Installation
Installation 是 LeanCloud中定义的一个和App所在的设备关联的一个类，它能唯一定位到具体的哪台设备。在App启动的时候需要把Installation保存到LeanCloud平台。  
    
    AVInstallation.getCurrentInstallation().saveInBackground(new SaveCallback() {
            @Override
            public void done(AVException e) {
                String installationId = AVInstallation.getCurrentInstallation().getInstallationId();
            }
    });
这段代码在应用启动的时候调用，通常就是你的MainActivity，此外在它保存到LeanCloud的时候，它还有一个回调方法，这个方法能方便你用installationId做数据关联。

####第六步：启动推送服务，设置默认打开的Activity
    
     PushService.setDefaultPushCallback(this, MainActivity.class);
到此为止，App端的工作已经完成，现在就可以在LeanCloud平台手动发送推送测试是否正常。你会看到应用启动成功后，LeanCloud平台会新增一条Installation记录。  
![leancloud_installation](http://7i7hhc.com1.z0.glb.clouddn.com/leancloud_installation.jpg)

现在选择在线发送的推送方式来测试：
  
![leancloud_push](http://7i7hhc.com1.z0.glb.clouddn.com/leancloud-push.jpg)

发送成功后，app就收到了推送消息：  
![message](http://7i7hhc.com1.z0.glb.clouddn.com/device-2015-08-22-095319.png)

接下来的任务如何通过API在服务端控制推送的业务逻辑，不过这是另外一个话题了，会另外开篇文章。
