import csv
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id    SERIAL PRIMARY KEY,
            name  VARCHAR(100),
            phone BIGINT UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created")

def insert_csv():
    conn = connect()
    cur = conn.cursor()
    with open("contacts.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (row["name"], int(row["phone"]))
            )
    conn.commit()
    cur.close()
    conn.close()
    print("CSV inserted")

def insert_console():
    name  = input("Name: ")
    phone = int(input("Phone: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Added")

def update():
    name      = input("Name to update: ")
    new_phone = int(input("New phone: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE name=%s",
        (new_phone, name)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Updated")

def query():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT ROW_NUMBER() OVER (ORDER BY id), name, phone
        FROM phonebook
    """)
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def delete():
    name = input("Name to delete: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")

def menu():
    while True:
        print("\n1. Create table")
        print("2. Insert CSV")
        print("3. Insert console")
        print("4. Update")
        print("5. Show all")
        print("6. Delete")
        print("0. Exit")
        c = input("Choose: ")
        if   c == "1": create_table()
        elif c == "2": insert_csv()
        elif c == "3": insert_console()
        elif c == "4": update()
        elif c == "5": query()
        elif c == "6": delete()
        elif c == "0": break

menu()