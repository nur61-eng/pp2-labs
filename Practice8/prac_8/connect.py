import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="0706",
        port="5432"
    )