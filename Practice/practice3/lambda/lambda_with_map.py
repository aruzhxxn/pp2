# 1. Умножение на 2
nums = [1, 2, 3]
print(list(map(lambda x: x * 2, nums)))

# 2. Квадраты
print(list(map(lambda x: x ** 2, nums)))

# 3. Преобразование в строку
print(list(map(lambda x: str(x), nums)))

# 4. Длина строк
words = ["hi", "hello"]
print(list(map(lambda w: len(w), words)))