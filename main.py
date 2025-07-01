from cryptography.fernet import Fernet
import os
import hashlib
import sys
from dotenv import load_dotenv
import mysql.connector
from hashtext import hash_string, verify_hash
from operations import create_user, get_user, create_password, get_all_password, get_password_query, delete_password, update_password_by_password, update_email, update_url
from database import connect_to_db 
import re
import mysql.connector
from mysql.connector import errorcode



conn = connect_to_db()
cursor = conn.cursor()

def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def add_password(username):
    
    while True:
        print()
        print("---- Add Password -----")
        print("1. Own Password")
        print("2. Generate a password")
        print("3. Exit")
        choice = input("Choose an option: ")

        phrase = ""
        if(choice == "1" or choice == "2"):
            phrase = input("Enter a phrase to use: ")
            if(choice == "2"):
                phrase = hash_string(phrase)

            email = input("Enter email: ")
            while not validate_email(email):
                print("Invalid email")
                email = input("Enter email: ")
            url = input("Enter url: ")

            try:
                create_password(username, phrase, email, url, cursor)
                conn.commit()
                print("Password successfully created")
            except mysql.connector.IntegrityError as e:
                if(e.errno == errorcode.ER_DUP_ENTRY):
                    print("A password already exist for that url.")
                else:
                    print("An Integrity error has occured")
            except mysql.connector.DatabaseError as e:
                print(e)
                print("An Error occured with the database")
                print("Try again")
            except Exception as e:
                print(e)
                print("Error in creating password")
            



        elif choice == "3":
            break
        else:
            print("Invalid Option")
    
    return None

def password_table(passwrds):
    if not passwrds:
        print("No password found")
    else:
        print()
        headers = ["user", "password", "email", "url"]
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *passwrds)]
        header_row = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
        print(header_row)
        print("-" * len(header_row))

        # Print data rows
        for row in passwrds:
            print(" | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row)))
        
        print()

def get_password(username):
    while True:
        print()
        print("---- Get Password Menu ----")
        print("1. List all passwords")
        print("2. Query password")
        print("3. Exit")
        option = input("Select and option: ")
        try:
            if option == "1":
                password_table(get_all_password(username, cursor))
            elif option == "2":
                q = input("Enter a phrase to search for: ")
                password_table(get_password_query(q, username, cursor))
                pass
            elif option == "3":
                break
            else:
                print("Invalid Option")

        except mysql.connector.DatabaseError as e:
            print(e)
            print("An Error occured with the database")
            print("Try again")
        except Exception as e:
            print(e)
            print("Error in creating password") 

def delete_password_menu(username):
    

    while(True):
        print()
        print("---- Delete Password Menu----")
        q = input("Search for an existing password or enter q to quit: ")

        if(q.lower() == "q"):
            return

        passwrds = get_password_query(q, username, cursor)

        password_table(passwrds)

        while True:
            if not passwrds:
                break
            passwrd_option = input(f"Select a password to delete (1-{len(passwrds)}) or q to exit:  ")

            if(passwrd_option.lower() == "q"):
                break
            
            try:
                passwrd_indx = int(passwrd_option) - 1 
                
                if(passwrd_indx >= len(passwrds) or passwrd_indx < 0):
                    print("Invalid option")
                    continue

                
                delete_password(passwrds[passwrd_indx][1], username, cursor)
                conn.commit()
                print("Successfully deleted password")
                break
            except ValueError:
                print("Invalid option")



def update_password_screen(username):
     while(True):
        print()
        print("---- Update Password Menu----")
        q = input("Search for an existing password or enter q to quit: ")

        if(q.lower() == "q"):
            return

        passwrds = get_password_query(q, username, cursor)

        

        while True:
            password_table(passwrds)
            if not passwrds:
                break
            passwrd_option = input(f"Select a password to update (1-{len(passwrds)}) or q to exit: ")

            if(passwrd_option.lower() == "q"):
                break
            
            try:
                passwrd_indx = int(passwrd_option) - 1 
                
                if(passwrd_indx >= len(passwrds) or passwrd_indx < 0):
                    print("Invalid option")
                    continue

                password_to_update = passwrds[passwrd_indx][1]

                print()
                print("--- Select what to update ---")
                print("1. Password")
                print("2. Email")
                print("3. Url")
                print("4. Exit")

                option = input("Enter an option: ")

                if(option == "1"):
                    print()
                    print("---- What kind of password to store -----")
                    print("1. Own Password")
                    print("2. Generated password")
                    print("3. Exit")

                    

                    phrase = ""
                    while True:
                        password_type = input("Enter an option to make password: ")
                        if(password_type == "1" or password_type == "2"):
                            phrase = input("Enter a phrase to use: ")
                            if(password_type == "2"):
                                phrase = hash_string(phrase)

                            try:
                                update_password_by_password(password_to_update, phrase, username, cursor)
                                conn.commit()

                                print("Password updated sucessfully")
                                
                            except Exception as e:
                                print(e)
                            
                            break

                        elif password_type == "3":
                            break
                        else:
                            print("Invalid Option")
                elif option == "2":
                    new_email = input("Enter a new email: ")
                    try:
                        update_email(password_to_update, new_email, username, cursor)
                        conn.commit()
                        print("Sucessfully updated email.")
                    except Exception as e:
                        print(e)
                elif option == "3":
                    new_url = input("Enter new url: ")
                    try:
                        update_url(password_to_update, new_url, username, cursor)
                        print("Sucessfully updated url.")
                    except Exception as e:
                        print(e)
                
            except ValueError:
                print("Invalid option")
                continue
            break

def create_account():
    print("Enter q or Q to exit")
    print("--------------------")

    while True:
        username = input("Enter username: ")
        if(username.strip().lower() == "q"):
            return
        password = input("Enter password: ")
        hashed_password = hash_string(password)

        try:
            create_user(username, hashed_password, cursor)
            conn.commit()
            print("User successfully create")
            return
        except Exception as e:
            print(e)
        


def login():
   

    while True:
        print()
        print("Enter q or Q to exit")
        print("--------------------")
        username = input("Enter username: ")
        if(username.strip().lower() == "q"):
            return
        password = input("Enter password: ")
        user = get_user(username, cursor)

        if user and verify_hash(user[1], password):
            print("Logged In successfully")
            menu(username)
            return
        else:
            print("Invalid Credentials")


        
        
        

def start():
    choice = "0"
    
    
    while True:
        print("----- Password Manager -----")
        print("1. Log In")
        print("2. Create new account")
        print("3. Exit")
        choice = input("Choose an option: ")
        if(choice == "1"):
            login()
        elif(choice == "2"):
            create_account()
        elif(choice == "3"):
            break
        else:
            print("Invalid Option")
        
        print()



def menu(username):
    choice = 0
    while True:
        print("\n----- Menu -----")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Delete Password")
        print("4. Update Password")
        print("5. Logout")
        choice = input("Choose an option: ")
        if(choice == "1"):
            add_password(username)
        elif(choice == "2"):
            get_password(username)
        elif(choice == "3"):
            delete_password_menu(username)
        elif(choice == "4"):
            update_password_screen(username)
        elif(choice == "5"):
            break
        else:
            print("Invalid Option")

def main():
    start()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()