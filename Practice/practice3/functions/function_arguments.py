# 1. Аргументы по умолчанию
def power(x, p=2):
    print(x ** p)

power(3)
power(3, 3)

# 2. Именованные аргументы
def info(name, age):
    print(name, age)

info(age=17, name="Аружан")

# 3. Смешанные аргументы
def city_info(name, city="Almaty"):
    print(name, city)

city_info("Dana")
city_info("Dana", "Astana")

# 4. Передача выражений
def multiply(a, b):
    print(a * b)

multiply(2 + 3, 4)