import csv
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone BIGINT UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_sql():
    conn = connect()
    cur = conn.cursor()
    for file in ["functions.sql", "procedures.sql"]:
        with open(file, "r", encoding="utf-8") as f:
            cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()

def search():
    p = input("Search: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (p,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def show():
    lim = int(input("Limit: "))
    off = int(input("Offset: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (lim, off))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def upsert():
    n = input("Name: ")
    p = input("Phone: ")
    if not p:
        print("Phone cannot be empty!")
        return
    p = int(p)
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (n, p))
    conn.commit()
    cur.close()
    conn.close()

def insert_many():
    count = int(input("Count: "))
    names, phones = [], []
    for i in range(count):
        names.append(input(f"Name {i+1}: "))
        phones.append(int(input(f"Phone {i+1}: ")))
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL insert_many_contacts(%s, %s, %s)", (names, phones, ""))
    res = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    print("Invalid:", res[0] if res[0] else "none")

def delete():
    n = input("Name: ")
    p = input("Phone: ")
    p = int(p) if p else 0
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s, %s)", (n, p))
    conn.commit()
    cur.close()
    conn.close()

def menu():
    while True:
        print("\n===== PhoneBook =====")
        print("1. Create table")
        print("2. Load SQL")
        print("3. Search")
        print("4. Show")
        print("5. Upsert")
        print("6. Insert many")
        print("7. Delete")
        print("0. Exit")
        c = input("> ")
        if c == "1": create_table()
        elif c == "2": load_sql()
        elif c == "3": search()
        elif c == "4": show()
        elif c == "5": upsert()
        elif c == "6": insert_many()
        elif c == "7": delete()
        elif c == "0": break

menu()