import sqlite3
import time


def login():
    while True:
        username = input("Enter your username:")
        password = input("Enter your password:")
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM info WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
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
                # return(exit)
                break


def newUser():
    found = 0
    while found == 0:
        username = input("Please enter a username: ")
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM info WHERE username = ?")
        cursor.execute(findUser,[(username)])

        if cursor.fetchall():
            print("Username Taken, please try again with another.")
        else:
            found = 1

        firstName = input("Enter your first name: ")
        surname = input("Enter your surname: ")
        password = input("Enter your password: ")
        password1 = input("Please reenter your password: ")
        while password != password1:
            print("Your passwords didn't match, please try again.")
            password = input("Enter your password: ")
            password1 = input("Please reenter your password: ")
        insertData = '''INSERT INTO info(username,firstname,surname,password)
        VALUES(?,?,?,?)'''
        cursor.execute(insertData,[(username),(firstname),(surname),(password)])
        db.commit()

newUser()