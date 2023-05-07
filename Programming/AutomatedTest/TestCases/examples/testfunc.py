def afunc(x, y, z) :
    if (x>1 and y==0) :
        print("第一个 if 语句判定为 true")
        print("x>1 的值为 %s，y==0 的值为 %s" % (x>1, y==0))
        z = z / x
    else :
        print("第一个 if 语句判定为 false")        
        print("x>1 的值为 %s，y==0 的值为 %s" % (x>1, y==0))
    if (x==2 or z>1) :
        print("第二个 if 语句判定为 true")
        print("x==2 的值为 %s，z>1 的值为 %s" % (x==2, z>1))
        z = z + 1
    else :
        print("第二个 if 语句判定为 false") 
        print("x==2 的值为 %s，z>1 的值为 %s" % (x==2, z>1))
        