FunctionQuery
==================
http://wiki.apache.org/solr/FunctionQuery#recip

recip(ms(NOW,startTime),3.16e-11,1,1)
recip(x,m,a,b) implementing a/(m*x+b). m,a,b are constants, x is any numeric field or arbitrarily complex function.

recip(abs(ms(NOW,startTime)),3.16e-11,1,1)

该函数可以用在bf中(booting function)
