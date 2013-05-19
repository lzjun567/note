git 常用命令解析
 ==================
###git merge 合并分支
merge 的功能就是做分支合并，假如分支结构如下：  

                               master
                              /
     C0 ---- C1 ---- C2 ---- C4
                         \
                         C3 ---- C5
                                  \
                                   issueFix

切换到master分支  

    $git checkout master

把issueFix分支的内容合并（merge）到当前分支（master）  

    $git merge issueFix


