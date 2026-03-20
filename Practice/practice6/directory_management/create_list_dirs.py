import os

# создать папку
os.mkdir("test_dir")

# вложенные папки
os.makedirs("parent/child/grandchild")

# список файлов
print(os.listdir("."))

# текущая директория
print(os.getcwd())