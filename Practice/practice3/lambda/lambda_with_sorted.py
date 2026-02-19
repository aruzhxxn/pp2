# 1. Сортировка чисел
nums = [5, 1, 4]
print(sorted(nums))

# 2. По убыванию
print(sorted(nums, reverse=True))

# 3. По длине строки
words = ["hi", "hello", "a"]
print(sorted(words, key=lambda x: len(x)))

# 4. Сортировка словарей
students = [{"age": 18}, {"age": 17}]
print(sorted(students, key=lambda s: s["age"]))