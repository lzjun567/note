Android 四大基本组件
===================
####Activity
Activity三种状态：运行（当前界面可见）、暂停（被其他Activity覆盖时处于半透明状态）、停止（完全不可见）
Activity声明周期的七个方法：  
![lifecycle](http://github-note.qiniudn.com/activity_lifecycle.png)  
启动另一个Activity：startActivity(intent)  
Activity之间数据传递：  intent.putExtra，Bundle，getIntent  
回传：startActivityForResult，setResult，onActivityResult  

####Service
Service就两种状态，生与死，对应onCreate和onDestroy方法。Service不会随着Activity的销毁而销毁（如果是以startService的方式启动的话），不会重复启动，不会重复销毁  
new Intent(context, Service)
启动服务：  

    startService(intent)  
    stopService(intent)
绑定服务：  
    
    //绑定时同时会启动服务，Activity销毁的时候服务跟着destroy了
    bindService(intent, serviceconnection, Context.BIND_AUTO_CREATE)
    unbindService(serviceconnection)

    onServiceConnected(  //成功绑定时触发，只有Service的onbind方法返回Binder实例才可能成功绑定。  
    onServiceDisconnected //服务崩溃时触发

Service的创建的销毁都是有系统来控制的，开发人员是无法通过new的方式来实例化Service。Service的获取通过IBinder来获得。  

####Broadcast Receiver
静态注册Broadcast Receiver/发送广播：androidmainifest.xml  sendBroadcast(new Intent(context, class))    
动态注册Broadcast Receiver：registerReceiver(BroadcastReceiver, IntentFilter)  sendBroadcast(new Intent(Action)) / unregisterReceiver(BroadcastReceiver)

####ContentProvider
用来读取其他应用程序公开的数据：getContentResolver().query(ContactsContract.Contacts.CONTENT_URI)，返回的Cursor类似与JDBC中的Cursor， cursor.getString(cursor.getColumnIndex)  

####Intent
Intent用来指定要启动的目标组件

####IntentFilter

####隐式Intent与显式Intent
通过Action来决定打开哪个Intent：startActivity(Intent(String action))
action:projectname.intent.action.XXX





    

