通信类型：AF_INET   
协议家族一般是表示TCP通信的SOC_STREAM和UDP通信的SOCK_DGRAM。对于TCP通信，建立socket连接，：

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
连接socket，
        
        s.connect((host,port))

socket通信建立连接后，利用它发送接收数据，python提供了两种方式：socket对象和文件类对象  

socket对象提供了操作系统的send()、sendto()、recv()、recvfrom()方法，文件对象提供了read()、write()、readline()方法。


