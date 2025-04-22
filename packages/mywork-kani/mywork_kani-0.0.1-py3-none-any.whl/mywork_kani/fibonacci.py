def fibo(n):
    if n<= 1:
        return n
    else:
        return fibo(n-1)+fibo(n-2)
numterms=int(input("enter the numbers:"))
if numterms<=0:
    print("enter positive number")
else:
    print("fibonacci sequence:")
    for i in range(numterms):
        print(fibo(i),end="  ")
