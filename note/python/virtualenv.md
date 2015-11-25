Python虚拟环境
====================
动态语言中Ruby、Python都有自己的虚拟环境，通过创建虚拟环境能够使不同的项目之间的运行环境保持独立性而相互不受影响。例如项目A依赖Django1.4，而项目B依赖Django1.5，这时它就能解决此类问题。Ruby有Vagrant，Python有virtualenv，本文讨论Python虚拟环境。[virtualenv](http://pypi.python.org/pypi/virtualenv)可用于创建独立的Python环境，它会创建一个包含项目所必须要的执行文件。

####安装 

    $ pip install virtualenv
####使用方法
    
    $ cd my_project_folder
    $ virtualenv venv 
如，创建名为**ENV**的虚拟环境  

    $ virtualenv ENV
执行完命令后它会在当前目录下创建文件夹，这个文件夹包含一些Python执行文件，以及pip副本用于安装其他的packges。  
    
    .
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── activate_this.py
    │   ├── easy_install
    │   ├── easy_install-3.5
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.5
    │   ├── python -> python3
    │   ├── python3
    │   ├── python3.5 -> python3
    │   └── wheel
    ├── include
    │   └── python3.5m -> /Library/Frameworks/Python.framework/Versions/3.5/include/python3.5m
    └── lib
        └── python3.5

此外在创建env的时候可以选择Python解释器，例如：  
    
    $ virtualenv -p /usr/local/bin/python3 venv
默认情况下，虚拟环境会依赖系统环境中的site packages，就是说系统中已经安装好的第三方package也会安装在虚拟环境中，如果不想依赖这些package，那么可以加上参数 `--no-site-packages`建立虚拟环境  

    virtualenv --no-site-packages [虚拟环境名称]

####启动虚拟环境

    cd ENV
    source ./bin/activate

注意此时命令行会多一个`(ENV)`，ENV为虚拟环境名称，接下来所有模块都只会安装到这个虚拟的环境中去。

####退出虚拟环境  
    
    $ deactivate

如果想删除虚拟环境，那么直接运行`rm -rf venv/`命令即可。  

####在虚拟环境安装Python packages 

Virtualenv 附带有pip安装工具，因此需要安装的packages可以直接运行：  
    
    pip install [套件名称]
如果没有启动虚拟环境，系统也安装了pip工具，那么packages将被安装在系统环境中，为了避免发生此事，可以在`~/.bashrc`文件中加上：  
    
    export PIP_REQUIRE_VIRTUALENV=true
如果在没开启虚拟环境时运行pip，就会提示错误：Could not find an activated virtualenv (required).  


####Virtualenvwrapper
Virtaulenvwrapper是virtualenv的扩展包，用于更方便管理虚拟环境，它可以做：  
1. 将所有虚拟环境整合在一个目录下  
2. 管理（新增，删除，复制）虚拟环境  
3. 切换虚拟环境  
4. ...  

#####安装（确保virtualenv已经安装）

    $ pip install virtualenvwrapper

此时还不能使用virtualenvwrapper，默认virtualenvwrapper安装在/usr/local/bin下面，实际上你需要运行virtualenvwrapper.sh文件才行，先别急，打开这个文件看看,里面有安装步骤，我们照着操作把环境设置好。  

1. 创建目录用来存放虚拟环境

        mkdir $HOME/Envs
2. 编辑~/.zshrc或~/.bashrc（根据你使用shell类型决定）
        
        export WORKON_HOME=$HOME/Envs
        source /usr/local/bin/virtualenvwrapper.sh
3. 运行： 
        
        $ source    ~/.zshrc

此时virtualenvwrapper就可以使用了。virtualenvwrapper的基本使用方式：   

1. 列出虚拟环境列表  
    
        workon 或者 lsvirtualenv
2. 新建虚拟环境  
    
        mkvirtualenv [虚拟环境名称]

3. 启动/切换虚拟环境  
    
        workon [虚拟环境名称]

4. 删除虚拟环境  

        rmvirtualenv [虚拟环境名称]

5. 离开虚拟环境，和virutalenv一样的命令
    
        deactivate


参考：  
http://www.virtualenv.org/en/latest/  
http://stackoverflow.com/questions/11372221/virtualenvwrapper-not-found  
http://www.openfoundry.org/tw/tech-column/8516-pythons-virtual-environment-and-multi-version-programming-tools-virtualenv-and-pythonbrew  
http://virtualenvwrapper.readthedocs.org/en/latest/index.html  


