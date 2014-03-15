keys = [chr(i) for i in range(97,97+26)]
result = {}
for key in keys:
     k = hash(key)%4
     if k not in result:
         result[k] = [key,]
     else:
         result.get(k).append(key)


print result
