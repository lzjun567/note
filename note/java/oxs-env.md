#OSX平台搭建Java开发环境
###安装JDK

###安装Maven

###安装Tomcat
	$HOME/Java/tomcat

	chmod +x ./*.sh

###配置zsh
	
	vim  ~/.zshrc

	export JAVA_HOME=`/usr/libexec/java_home`
	export M2_HOME=$HOME/Java/maven
	export M2=$M2_HOME/bin
	export PATH=$M2:$PATH


