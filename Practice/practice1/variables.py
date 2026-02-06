#Exercises

# ex 1
x = 5 # basic int type automatic variable declaration

# ex 2

# my-var = 7 <-- incorrect declaration
myTemporalVar = 7 # < -- Camel case
MyTemporalVar = 7 # < -- Pascal case
my_temporal_var = 7 # < -- Snake case

# ex 3: One value for multiple variables
a = b = c = 7
print(a, b, c, sep = " ")

# Declaring multiple variables in one row
a, b, c = 7, 9, 18 # <-- a corresponds to the first value 7, b to the second 9 and so on
print(a, b, c, sep = " ")


# ex 4
a = "Hello"
b = "Furina"
print(a + b) # < -- without spaces they will combine and slip. To fix we either put space to one of them, or use sep parameter

print(a, b, sep = " ")
print(a, b.replace("Furina", " Furina"))

# ex 5: Global and local variables

x = "Furina"

def praise_neuvilette():
    x = "Neuvilette" # < -- now its local
    print(x, " is great!")
praise_neuvilette()
print(x, " is great!") # expected Furina is great, because x = Neuvilette is inside a function

x = "Navia"

def praise_nahida():
    global x
    x = "Nahida" # Now Navia has been changed to Nahida because x is now global
    print(x, "is great")
praise_nahida()
print(x, "is great")