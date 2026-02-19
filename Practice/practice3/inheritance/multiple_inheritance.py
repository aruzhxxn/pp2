# 1. Первый родитель
class A:
    def f(self):
        print("A")

# 2. Второй родитель
class B:
    def f(self):
        print("B")

# 3. Наследование
class C(A, B):
    pass
    
# 4. MRO
C().f()  # A