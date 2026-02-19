# 1. Функция без параметров
def hello():
    print("Hello!")

hello()
# 2. Функция с одним параметром
def greet(name):
    print("Привет,", name)

greet("Аружан")

# 3. Функция с двумя параметрами
def add(a, b):
    print(a + b)

add(3, 5)

# 4. Функция, которая вызывает другую функцию
def say_hi():
    print("Hi!")

def start():
    say_hi()

start()