守护进程方式启动mongodb进程
    mongod --fork --dbpath data/rs0-0 --logpath log/rs0-0/rs0-0.log --rest --replSet rs0 --port 37017
    
    2015-06-18T13:57:11.637+0800 ** WARNING: --rest is specified without --httpinterface,
    2015-06-18T13:57:11.638+0800 **          enabling http interface
    about to fork child process, waiting until server is ready for connections.
    forked process: 14141
    child process started successfully, parent exiting