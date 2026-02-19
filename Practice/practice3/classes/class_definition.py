# 1. Пустой класс
class A:
    pass

a = A()

# 2. Метод класса
class Dog:
    def bark(self):
        print("Гав")

Dog().bark()

# 3. Несколько методов
class Math:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b
        
# 4. Использование объекта
m = Math()
print(m.add(3, 2))