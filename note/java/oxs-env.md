#OSX平台搭建Java开发环境
###安装JDK

###安装Maven

修改maven默认下载地址，修改settings.xml
	
	  <mirrors>
	    <mirror>
	      <id>alimaven</id>
	      <name>aliyun maven</name>
	      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
	      <mirrorOf>central</mirrorOf>        
	    </mirror>
	  </mirrors>


###安装Tomcat
	$HOME/Java/tomcat

	chmod +x ./*.sh

###配置zsh
	
	vim  ~/.zshrc

	export JAVA_HOME=`/usr/libexec/java_home`
	export M2_HOME=$HOME/Java/maven
	export M2=$M2_HOME/bin
	export PATH=$M2:$PATH


直接部署基于maven的war包到tomat：https://www.mkyong.com/maven/how-to-deploy-maven-based-war-file-to-tomcat/

maven dependency中scope=compile 和 provided区别  http://supercharles888.blog.51cto.com/609344/981316



