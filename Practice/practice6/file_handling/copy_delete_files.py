import shutil
import os

# копирование
shutil.copy("example.txt", "backup.txt")
print("File copied")

# удаление
if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("File deleted")
else:
    print("File not found")