

def create_user(username, password, cursor):
    cursor.execute("INSERT INTO users (username, passwrd) VALUES (%s,%s)", (username, password))
    

def create_password(username, password, email, url, cursor):
    cursor.execute("INSERT INTO passwrds (username, passwrd, email, url) VALUES (%s, %s, %s, %s)", (username, password, email, url))

def get_password_query(q, username, cursor):
    ext = f'%{q}%'
    cursor.execute("SELECT * FROM passwrds WHERE username = %s AND url LIKE %s", (username, ext))

    password = cursor.fetchall()

    if password:
        return password
    else:
        return None
    
def update_password_by_password(password, new_password, username, cursor):
    cursor.execute("UPDATE passwrds SET passwrd = %s WHERE username = %s AND passwrd = %s", (new_password, username, password))


def update_email(password, new_email, username, cursor):
    cursor.execute("UPDATE passwrds SET email = %s WHERE username = %s AND passwrd = %s", (new_email, username, password))

def update_url(password, new_url, username, cursor):
    cursor.execute("UPDATE passwrds SET url = %s WHERE username = %s AND passwrd = %s", (new_url, username, password))

def get_all_password(username, cursor):
    cursor.execute("SELECT * FROM passwrds WHERE username = %s", (username, ))
    passwords = cursor.fetchall()

    if passwords:
        return passwords
    else:
        return None
    
def delete_password(password, username, cursor):
    cursor.execute("DELETE FROM passwrds WHERE username = %s AND passwrd = %s", (username, password))

def get_user(username, cursor):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username, ))
    user = cursor.fetchone()



    if user:
        return user
    else:
        print("User not found")
        return None
