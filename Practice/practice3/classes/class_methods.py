# 1. classmethod
class A:
    x = 10

    @classmethod
    def show(cls):
        print(cls.x)


# 2. Изменение переменной класса
class Counter:
    count = 0

    @classmethod
    def inc(cls):
        cls.count += 1


# 3. Вызов через класс
Counter.inc()

# 4. Вызов через объект
obj = Counter()
obj.inc()
print(Counter.count)