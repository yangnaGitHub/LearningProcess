num = int(input("enter: "))
lastsum = 0
number = len(str(num))

temp = num
while temp > 0:
    digit = temp % 10
    lastsum += digit ** number
    temp //= 10

if num == lastsum:
    print("YES")
else:
    print("NO")
