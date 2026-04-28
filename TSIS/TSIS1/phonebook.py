import csv
import json
from connect import connect

def add_phone():
    name  = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")
    conn = connect()
    cur  = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()
    cur.close()
    conn.close()
    print("Phone added")

def move_to_group():
    name  = input("Contact name: ")
    group = input("Group (Family/Work/Friend/Other): ")
    conn  = connect()
    cur   = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    cur.close()
    conn.close()
    print("Moved to group")

def search():
    query = input("Search: ")
    conn  = connect()
    cur   = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def filter_by_group():
    group = input("Group name: ")
    conn  = connect()
    cur   = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.email, p.birthday
        FROM phonebook p
        JOIN groups g ON g.id = p.group_id
        WHERE g.name ILIKE %s
    """, (group,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def search_by_email():
    email = input("Email: ")
    conn  = connect()
    cur   = conn.cursor()
    cur.execute("SELECT id, name, email FROM phonebook WHERE email ILIKE %s", ('%' + email + '%',))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def sort_contacts():
    print("Sort by: 1.name  2.birthday  3.id")
    c = input("Choose: ")
    order = "name" if c == "1" else "birthday" if c == "2" else "id"
    conn  = connect()
    cur   = conn.cursor()
    cur.execute(f"SELECT id, name, email, birthday FROM phonebook ORDER BY {order}")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def paginate():
    limit  = int(input("Limit: "))
    offset = 0
    while True:
        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows:
            print("No more contacts")
            break
        for row in rows:
            print(row)
        cmd = input("next / prev / quit: ")
        if   cmd == "next": offset += limit
        elif cmd == "prev": offset = max(0, offset - limit)
        elif cmd == "quit": break

def export_json():
    conn = connect()
    cur  = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.email, p.birthday::TEXT, g.name as group_name,
               array_agg(ph.phone) as phones
        FROM phonebook p
        LEFT JOIN groups g  ON g.id  = p.group_id
        LEFT JOIN phones ph ON ph.contact_id = p.id
        GROUP BY p.id, p.name, p.email, p.birthday, g.name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    contacts = []
    for row in rows:
        contacts.append({
            "id":       row[0],
            "name":     row[1],
            "email":    row[2],
            "birthday": row[3],
            "group":    row[4],
            "phones":   row[5]
        })
    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print("Exported to contacts.json")

def import_json():
    with open("contacts.json", "r", encoding="utf-8") as f:
        contacts = json.load(f)
    conn = connect()
    cur  = conn.cursor()
    for c in contacts:
        cur.execute("SELECT id FROM phonebook WHERE name = %s", (c["name"],))
        existing = cur.fetchone()
        if existing:
            ans = input(f"{c['name']} already exists. skip/overwrite: ")
            if ans == "overwrite":
                cur.execute("UPDATE phonebook SET email=%s, birthday=%s WHERE name=%s",
                            (c["email"], c["birthday"], c["name"]))
        else:
            cur.execute("INSERT INTO phonebook (name, email, birthday) VALUES (%s, %s, %s)",
                        (c["name"], c["email"], c["birthday"]))
    conn.commit()
    cur.close()
    conn.close()
    print("Imported")

def import_csv():
    conn = connect()
    cur  = conn.cursor()
    with open("contacts.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute("""
                INSERT INTO phonebook (name, email, birthday)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (row.get("name"), row.get("email"), row.get("birthday") or None))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported")

def menu():
    while True:
        print("\n===== TSIS1 PhoneBook =====")
        print("1.  Add phone")
        print("2.  Move to group")
        print("3.  Search")
        print("4.  Filter by group")
        print("5.  Search by email")
        print("6.  Sort contacts")
        print("7.  Paginate")
        print("8.  Export JSON")
        print("9.  Import JSON")
        print("10. Import CSV")
        print("0.  Exit")
        c = input("> ")
        if   c == "1":  add_phone()
        elif c == "2":  move_to_group()
        elif c == "3":  search()
        elif c == "4":  filter_by_group()
        elif c == "5":  search_by_email()
        elif c == "6":  sort_contacts()
        elif c == "7":  paginate()
        elif c == "8":  export_json()
        elif c == "9":  import_json()
        elif c == "10": import_csv()
        elif c == "0":  break

menu()