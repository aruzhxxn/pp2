import csv
import json
from connect import conn

cur = conn.cursor()


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s);
    """, (name, email, birthday, group_id))

    conn.commit()
    print("Contact added")


def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Type (home/work/mobile): ")

    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
    conn.commit()
    print("Phone added")


def move_to_group():
    name = input("Contact name: ")
    group_name = input("New group: ")

    cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
    conn.commit()
    print("Contact moved")


def search_contacts():
    query = input("Search: ")

    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)


def filter_by_group():
    group_name = input("Group name: ")

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s;
    """, (group_name,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def search_by_email():
    email = input("Email search: ")

    cur.execute("""
        SELECT id, name, email, birthday
        FROM contacts
        WHERE email ILIKE %s;
    """, (f"%{email}%",))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def sort_contacts():
    print("1 - Sort by name")
    print("2 - Sort by birthday")
    print("3 - Sort by date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "name"
    elif choice == "2":
        order_by = "birthday"
    else:
        order_by = "id"

    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order_by};
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def show_all_contacts():
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id;
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def export_to_json():
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id;
    """)

    contacts = cur.fetchall()
    data = []

    for contact in contacts:
        contact_id = contact[0]

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = cur.fetchall()

        data.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]),
            "group": contact[4],
            "phones": [
                {"phone": p[0], "type": p[1]} for p in phones
            ]
        })

    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Exported to contacts.json")


def import_from_json():
    try:
        with open("contacts.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            name = item["name"]

            cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
            existing = cur.fetchone()

            if existing:
                answer = input(f"{name} already exists. overwrite/skip? ")

                if answer == "skip":
                    continue

                if answer == "overwrite":
                    cur.execute("DELETE FROM contacts WHERE name = %s;", (name,))

            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (item["group"],))

            cur.execute("SELECT id FROM groups WHERE name = %s;", (item["group"],))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (item["name"], item["email"], item["birthday"], group_id))

            contact_id = cur.fetchone()[0]

            for phone in item["phones"]:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s);
                """, (contact_id, phone["phone"], phone["type"]))

        conn.commit()
        print("Imported from contacts.json")

    except FileNotFoundError:
        print("contacts.json not found")


def import_from_csv():
    try:
        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                group_name = row["group"]

                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING;
                """, (group_name,))

                cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
                group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                """, (row["name"], row["email"], row["birthday"], group_id))

                contact_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s);
                """, (contact_id, row["phone"], row["type"]))

        conn.commit()
        print("Imported from contacts.csv")

    except FileNotFoundError:
        print("contacts.csv not found")


def pagination_loop():
    limit_value = 3
    offset_value = 0

    while True:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            LIMIT %s OFFSET %s;
        """, (limit_value, offset_value))

        rows = cur.fetchall()

        print("\nPage:")
        for row in rows:
            print(row)

        command = input("next / prev / quit: ")

        if command == "next":
            offset_value += limit_value
        elif command == "prev":
            offset_value = max(0, offset_value - limit_value)
        elif command == "quit":
            break


menu = True

while menu:
    print("\nPHONEBOOK MENU")
    print("1 - Add contact")
    print("2 - Add phone")
    print("3 - Move contact to group")
    print("4 - Search contacts")
    print("5 - Filter by group")
    print("6 - Search by email")
    print("7 - Sort contacts")
    print("8 - Show all contacts")
    print("9 - Export to JSON")
    print("10 - Import from JSON")
    print("11 - Import from CSV")
    print("12 - Pagination")
    print("0 - Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        add_phone()
    elif choice == "3":
        move_to_group()
    elif choice == "4":
        search_contacts()
    elif choice == "5":
        filter_by_group()
    elif choice == "6":
        search_by_email()
    elif choice == "7":
        sort_contacts()
    elif choice == "8":
        show_all_contacts()
    elif choice == "9":
        export_to_json()
    elif choice == "10":
        import_from_json()
    elif choice == "11":
        import_from_csv()
    elif choice == "12":
        pagination_loop()
    elif choice == "0":
        menu = False
    else:
        print("Wrong choice")

cur.close()
conn.close()