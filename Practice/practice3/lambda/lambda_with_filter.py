# 1. Чётные числа
nums = [1, 2, 3, 4]
print(list(filter(lambda x: x % 2 == 0, nums)))

# 2. Больше 5
print(list(filter(lambda x: x > 5, [2, 6, 8])))

# 3. Непустые строки
words = ["", "hi", ""]
print(list(filter(lambda x: x != "", words)))

# 4. Положительные числа
print(list(filter(lambda x: x > 0, [-1, 2, -3, 4])))