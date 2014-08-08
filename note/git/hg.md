http://blog.csdn.net/robinblog/article/details/17967991

    hg pull
    hg branch 查看当前分支
    hg branches 列出分支
    
    hg update branch_name 切换分支
    
    hg commit -m "xxx"
    
    hg push
    如果出现错误：  
    
        中止: push creates new remote head 463b0a4add1e!
        (merge or see "hg help push" for details about pushing new heads)
    hg push -r branch_name
    
    hg branch newbranch 创建分支，新创建的分支下次commit的时候才能生成
    
    分支合并：  
    hg update 将要关闭的分支
    hg commit --close-branch 
    hg update default
    hg merge 将要关闭的分支

    如果某个文件不想同步，比如a.pyc 执行了add操作，此时可以使用revert 撤销
