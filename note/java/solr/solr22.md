solr admin 命令
============
查看Solr的运行状态

    http://localhost:8983/solr/admin/cores?action=STATUS
查看Solr指定的core
    
    http://localhost:8983/solr/admin/cores?action=STATUS&core=collection1&wt=json

重新加载SOlr core
    
    http://localhost:8983/solr/admin/cores?action=reload&core=collection1&wt=json
