# 1. Возврат числа
def square(x):
    return x * x

print(square(5))

# 2. Возврат строки
def full_name(name, surname):
    return name + " " + surname

print(full_name("Aruzhan", "Aidyn"))

# 3. Возврат логического значения
def is_even(x):
    return x % 2 == 0

print(is_even(4))

# 4. Возврат нескольких значений
def calc(a, b):
    return a + b, a - b

s, d = calc(10, 3)
print(s, d)
