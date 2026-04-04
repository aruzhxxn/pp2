import csv
from connect import conn

cur = conn.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        );
    """)
    conn.commit()


def add_contact_from_csv():
    with open(r"c:\Users\lashy\OneDrive\Рабочий стол\1\pp2\Practice\practice7\contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                continue
            name = row[0]
            phone = row[1]
            cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    conn.commit()
    print("Контакты из CSV добавлены")


def add_or_update_user():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    conn.commit()
    print("Пользователь добавлен или обновлен")


def search_pattern():
    value = input("Введите шаблон для поиска: ")
    cur.execute("SELECT * FROM filtr(%s);", (value,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено")


def show_page():
    limit_value = int(input("Введите LIMIT: "))
    offset_value = int(input("Введите OFFSET: "))
    cur.execute("SELECT * FROM get_phonebook_page(%s, %s);", (limit_value, offset_value))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Записей нет")


def add_many_users():
    n = int(input("Сколько пользователей хотите добавить? "))
    names = []
    phones = []

    for i in range(n):
        name = input(f"Введите имя {i + 1}: ")
        phone = input(f"Введите телефон {i + 1}: ")
        names.append(name)
        phones.append(phone)

    cur.execute("CALL insert_many_users(%s, %s);", (names, phones))
    conn.commit()
    print("Добавление завершено")


def delete_user():
    value = input("Введите имя или телефон для удаления: ")
    cur.execute("CALL delete_by_name_or_phone(%s);", (value,))
    conn.commit()
    print("Удаление выполнено")


def show_all_contacts():
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Таблица пустая")


create_table()

menu = True
while menu:
    print("\nВыберите функцию:")
    print("1 - Загрузить контакты из CSV")
    print("2 - Добавить или обновить одного пользователя")
    print("3 - Поиск по шаблону")
    print("4 - Показать данные с пагинацией")
    print("5 - Добавить несколько пользователей")
    print("6 - Удалить по имени или телефону")
    print("7 - Показать все контакты")
    print("0 - Выход")

    choice = input("Выбирайте: ")

    if choice == "1":
        add_contact_from_csv()
    elif choice == "2":
        add_or_update_user()
    elif choice == "3":
        search_pattern()
    elif choice == "4":
        show_page()
    elif choice == "5":
        add_many_users()
    elif choice == "6":
        delete_user()
    elif choice == "7":
        show_all_contacts()
    elif choice == "0":
        menu = False
    else:
        print("Неверный выбор")

cur.close()
conn.close()