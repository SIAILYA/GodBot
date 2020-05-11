from random import choice

key = ''
for i in range(10):
    key += choice('qwertyuiopasdfghjklzxcvbnm1234567890')
print(key)
