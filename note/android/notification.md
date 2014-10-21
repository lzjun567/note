状态栏通知：Notification，NotificationManager介绍
=================================
Notification：当你告诉系统触发一个Notification时，它首先会在手机屏幕顶部位置（notification area）显示一个icon(icon后面还是有文字描述由方法setTicker来设置），当你想看详细的信息时，你可以下拉通知栏（notification drawer）。   
![notification](http://github-note.qiniudn.com/notification.png)   
####Notication元素
![element](http://github-note.qiniudn.com/notication_elements.png)  
Notification在notification drawer面板中可显示的元素有：1. 内容标题 2. 大icon 3. 内容正文 4. 内容信息 5. 小icon 6. 消息发送的时间，系统默认就会显示这个元素，值为消息收到的时间，也可以通过方法setWhen()明确指定触发通知的时间。必须要设置的元素包括1，3，5。
####如何创建Notification
Notification的UI信息和动作是通过NoticationCompat.Builder对象设定的， NotificationCompat.Builder.build()方法会返回一个Notification对象，对象创建好之后，在把对象传递给NotificatoinManager.notify()方法，系统就会创建出这个通知。  
    
    NotificationCompat.Builder nBuilder = new NotificationCompat.Builder(this);
    nBuilder.setSmallIcon(R.drawable.ic_launcher);
    nBuilder.setContentTitle("天气乱报");
    nBuilder.setContentText("明天阴转暴雨，记得带伞，别忘了哦");
    Notification notification = nBuilder.build();
    NotificationManager manager = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
    manager.notify(notificationId, notification);

####Notification动作
收到一条通知时，通常你会引导用户进入某个Activity，这个称之为通知的动作，这个动作定义在一个叫PendingIntent对象里面，这个对象包含一个普通的Intent，这个Intent就是你要关联Activity的Intent。    
    
    Intent resultIntent = new Intent(this, ResultActivity.class);
    PendingIntent resultPendinTent = PendingIntent.getActivity(this, 0, resultIntent, PendingIntent.FLAG_UPDATE_CURRENT );
    nBuilder.setContentIntent(resultPendinTent);


####PendingIntent
PendingIntent对Intent的一种描述，Intent的载体，使得Intent的执行变得可控（延迟Intent的执行）。另外一种理解是：  
> A PendingIntent is a token that you give to a foreign application (e.g. NotificationManager, AlarmManager, Home Screen AppWidgetManager, or other 3rd party applications), which allows the foreign application to use your application's permissions to execute a predefined piece of code.

> If you give the foreign application an Intent, and that application sends/broadcasts the Intent you gave, they will execute the Intent with their own permissions. But if you instead give the foreign application a PendingIntent you created using your own permission, that application will execute the contained Intent using your application's permission.

> 它一个允许外部应用程序执行自己的程序中某些预定义好的代码的凭证。外部应用程序会使用你应用程序所拥有的权限来执行。  

####发送通知的两个类是NotificationManager和Notification：  
1. NotificationManager负责发送和取消通知，它是系统Service，通过getSystemService(NOTIFICATION_SERVICE);方法获取。
2. Notification是通知对象

####Notification设置指南
