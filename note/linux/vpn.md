Linode VPS搭建VPN
=====================
###安装PPTP服务器

    apt-get update
    apt-get install pptpd
###配置PPTP服务器
编辑/etc/pptpd.conf，将如下内容：

    #localip 192.168.0.1
    #remoteip 192.168.0.234-238,192.168.0.245
替换为：

    localip 192.168.217.1
    remoteip 192.168.217.234-238,192.168.217.245

上面的两行为VPN服务器的IP和VPN客户端连接后获取到的IP范围。

###添加PPTP VPN用户
编辑/etc/ppp/chap-secrets 添加如下内容：

    lzjun pptpd 123456 *
其中lzjun为你要添加的VPN帐号的用户名，123456为你VPN帐号的密码。
###修改DNS服务器
编辑/etc/ppp/options，添加如下内容：

    ms-dns 8.8.8.8
    ms-dns 8.8.4.4
###开启IPv4转发
编辑/etc/sysctl.conf文件，去掉net.ipv4.ip_forward=1前的注释，运行如下命令，使配置修改生效

    sysctl -p
###重启pptpd服务

    /etc/init.d/pptpd restart
###安装iptables

    apt-get install iptables #如果已经安装可以跳过
###开启iptables转发

    iptables -t nat -A POSTROUTING -s 192.168.217.0/24 -o eth0 -j MASQUERADE
    iptables-save > /etc/iptables.pptp

在/etc/network/if-up.d/目录下创建iptables文件，内容如下：

    #!/bin/sh
    iptables-restore < /etc/iptables.pptp
给脚本添加执行权限：

    chmod +x /etc/network/if-up.d/iptables
至此PPTP VPN服务器端的设置就完成了。

###客户端设置
Windows的话直接打开网络连接，创建一个VPN链接方式，按提示步骤设置上VPN服务器的IP，用户名、密码链接就可以了。
