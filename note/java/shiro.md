Shiro走马观花
================
Shiro如其官方介绍的一样，功能齐全易用的Java安全框架，功能包括认证、授权、加密、会话管理。  

###Authentication认证

**Subject**：安全里面具体的“用户"，这个用户既可以指人也可以第三方程序或者是一个用来连接你的程序的程序。简单来说subject就是和应用通信的对象。  
**Pricipals**：Subject的标识属性，如果Subject一个User类的话，那么Pricipals可以是username或者是email，总之就是能唯一标识这个Subject的属性。  
**Credentials**：用来验证的私密数据，简单理解就是密码。  
**Realms**：一种认证方式，比如LDAP，或者JDBC等等。

###Shiro认证流程
1. 收集Subject的Pricipals和Credentials.
    
        UsernamePasswordToken token = new UsernamePasswordToken( username, password );

    token对象是对Pricipals和Credentials的简单封装。
2. 提交Pricipals和Credentials给认证系统

    封装好的token会提交到认证系统中去，认证系统就是Realms，Shiro通过封装后认证的步骤简单至极。

        Subject currentUser = SecurityUtils.getSubject()
        currentUser.login(token)
    login就是认证方法，为什么要获取currentUser呢？currentUser就是subject，前面说过subject即可指人或者一个进程等，在Shiro里面当前的执行线程中一直会有一个subject实例可用。

3. 允许访问或者重新认证或者禁止访问

        try {
            currentUser.login(token);
        } catch ( UnknownAccountException uae ) { ...
                //为注册账户
        } catch ( IncorrectCredentialsException ice ) { ...
                //密码错误
        } catch ( LockedAccountException lae ) { ...
                //被限制账户
        } catch ( ExcessiveAttemptsException eae ) { ...
                //超出登录次数
        } ... catch your own ...
        } catch ( AuthenticationException ae ) {
                //其他异常
            //unexpected error?
        }
        //No problems, show authenticated view…
    




