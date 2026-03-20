# write_files.py

# создаем и записываем файл
with open("example.txt", "w") as file:
    file.write("Hello, this is first line\n")
    file.write("Second line\n")

print("File created and written successfully")