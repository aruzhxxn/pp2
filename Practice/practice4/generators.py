# generators.py

# ----- Iterator (через список) -----
numbers = [1, 2, 3, 4, 5]
it = iter(numbers)

print(next(it))
print(next(it))
print(next(it))


# ----- Generator function -----
def count_to_n(n):
    for i in range(1, n + 1):
        yield i

for x in count_to_n(5):
    print(x)


# ----- Generator expression -----
gen = (i * 2 for i in range(5))
print(list(gen))