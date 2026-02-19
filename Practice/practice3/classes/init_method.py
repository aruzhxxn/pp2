# 1. __init__ с одним параметром
class User:
    def __init__(self, name):
        self.name = name


# 2. __init__ с двумя параметрами
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# 3. Метод использует self
class Car:
    def __init__(self, model):
        self.model = model

    def show(self):
        print(self.model)

        
# 4. Создание объектов
c = Car("BMW")
c.show()