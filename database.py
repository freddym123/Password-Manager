import mysql.connector

def connect_to_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="hello",
        database="passwordmanager"
    )

    return conn

if __name__ == "__main__":
    connect_to_db()