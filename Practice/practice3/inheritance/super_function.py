# 1. Родитель
class Person:
    def __init__(self, name):
        self.name = name

# 2. super()
class Student(Person):
    def __init__(self, name, uni):
        super().__init__(name)
        self.uni = uni

# 3. Создание объекта
s = Student("Aruzhan", "KBTU")

# 4. Доступ к данным родителя
print(s.name, s.uni)