n = int(input())
j = 1
k = 0
while j*j < n:
    if n % j == 0:
        k = k + 2
    j = j + 1
if j*j == n:
    k = k + 1
print(k)
