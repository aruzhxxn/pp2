# 1. Родительский метод
class A:
    def show(self):
        print("A")

# 2. Переопределение
class B(A):
    def show(self):
        print("B")

# 3. Разное поведение
A().show()

# 4. Наследник
B().show()