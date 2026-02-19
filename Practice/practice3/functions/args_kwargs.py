# 1. *args — сумма чисел
def total(*args):
    return sum(args)

print(total(1, 2, 3))

# 2. *args — перебор
def show(*args):
    for x in args:
        print(x)

show("a", "b", "c")

# 3. **kwargs — словарь
def profile(**kwargs):
    print(kwargs)

profile(name="Aruzhan", age=17)

# 4. *args + **kwargs
def all_args(*args, **kwargs):
    print(args)
    print(kwargs)

all_args(1, 2, 3, city="Almaty")