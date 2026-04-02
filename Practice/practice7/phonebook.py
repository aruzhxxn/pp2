import psycopg2
import csv
from connect import conn

cur=conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (  
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                phone VARCHAR(20)
                );
""")
    conn.commit()
create_table()

def add_contact():
    with open("pp2/Practice/practice7/contacts.csv", "r", encoding="utf-8") as file:
        b = csv.reader(file)
        for row in b:
            name=row[0]
            phone=row[1]
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )
    conn.commit()


def add_console():
    a=input("введите имя ")
    b=input("введите номер ")
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (a,b)
    )
    conn.commit()

def update_name_phone():
    print("1-изменить имя")
    print("2-изменить номер ")
    a=input()
    
    if a=="1":
        b=input("Введите текущее имя: ")
        c=input("Введите новое имя: ")
        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (c, b)
        )
    elif a=="2":
        n=input("Введите текущий номер: ")
        m=input("Введите новый номер: ")
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE phone=%s",
            (m, n)
        )
    else:
        print("Неверный выбор")
        return
    conn.commit()

def filtr_contacts():
    print("1-фильтр по имени")
    print("2-фильтр по номеру")
    a=input()
    if a=="1":
        b=input("Введите имя: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE name LIKE %s",
            (b+ "%",)
            )
        n=cur.fetchall()
        for i in n:
            print(i)
    elif a=="2":
        c=input("Введите номер: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (c+ "%",)
        )
        v=cur.fetchall()
        for j in v:
            print(j)
    else:
        print("Неверный выбор")
    


def delete_name_phone():
    print("1-удалить по имени")
    print("2-удалить по номеру")
    a=input()

    if a=="1":
        n=input("Введите имя: ")
        cur.execute(
            "DELETE FROM phonebook WHERE name=%s",
            (n,)
        )
    elif a=="2":
        c=input("Введите номер: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone=%s",
            (c,)
        )
    else:
        print("Неверный выбор")
        return 
        
    conn.commit()

def show_all_contacts():
    cur.execute(
        "SELECT * FROM phonebook "
    )
    z=cur.fetchall()
    for i in z:
        print(i)
        
menu=True
while menu:
    print("Выберите функцию:")
    print("1-Загрузить контакты из CSV")
    print("2-Добавить контакт вручную")
    print("3-Обновить контакт")
    print("4-Фильтр")
    print("5-Удалить контакт")
    print("6-Показать все контакты")
    print("0-Выход")

    m=input("Выбирайте: ")

    if m=="1":
        add_contact()
    elif m=="2":
        add_console()
    elif m=="3":
        update_name_phone()
    elif m=="4":
        filtr_contacts()
    elif m=="5":
        delete_name_phone()
    elif m=="6":
        show_all_contacts()
    elif m=="0":
        menu=False
    else:
        print("Неверный выбор")


cur.close()
conn.close()
