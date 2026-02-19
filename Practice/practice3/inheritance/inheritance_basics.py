# 1. Базовый класс
class Animal:
    def eat(self):
        print("Eat")

# 2. Наследник
class Dog(Animal):
    pass

# 3. Использование метода родителя
Dog().eat()

# 4. Свой метод
class Cat(Animal):
    def meow(self):
        print("Meow")