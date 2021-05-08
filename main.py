import sqlite3
import time

def login():
    while True:
        username = input("Enter your username:")
        password = input("Enter your password:")
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM info WHERE username = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Welcome "+i[2])
            break

        else:
            print("Username and password not recognised")
            again = input("Do you want to try again (y/n): ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                #return(exit)
                break
login()