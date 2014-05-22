http://blog.csdn.net/robinblog/article/details/17967991

hg pull
hg branch 查看当前分支
hg branches 列出分支

hg update branch_name 切换分支

hg commit 

hg push

hg branch newbranch 创建分支，新创建的分支下次commit的时候才能生成

分支合并：  
hg update 将要关闭的分支
hg commit --close-branch 
hg update default
hg merge 将要关闭的分支
