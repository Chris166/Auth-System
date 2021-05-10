import sqlite3
import time
import sys
from colorama import Fore


def login():
    while True:
        username = input(f"{Fore.WHITE}Enter your username:")
        password = input(f"{Fore.WHITE}Enter your password:")
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM info WHERE username = ? AND password = ?")
        cursor.execute(find_user, [username, password])
        results = cursor.fetchall()

        if results:
            for i in results:
                print(f"{Fore.BLUE}Welcome " + i[2])
            break

        else:
            print(f"[{Fore.RED}-{Fore.WHITE}]Username and password not recognised")
            again = input(f"{Fore.WHITE}Do you want to try again (y/n): ")
            if again.lower() == "n":
                print(f"{Fore.WHITE}[{Fore.RED}-{Fore.WHITE}]Goodbye")
                time.sleep(1)
                # return(exit)
                break


def newUser():
    found = 0
    while found == 0:
        username = input(f"{Fore.WHITE}Please enter a username: ")
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
        findUser = "SELECT * FROM info WHERE username = ?"
        cursor.execute(findUser, [username])

        if cursor.fetchall():
            print(f"{Fore.WHITE}[{Fore.RED}-{Fore.WHITE}]Username Taken, please try again with another.")
        else:
            found = 1

        firstName = input(f"{Fore.WHITE}Enter your first name: ")
        surname = input(f"{Fore.WHITE}Enter your surname: ")
        password = input(f"{Fore.WHITE}Enter your password: ")
        password1 = input(f"{Fore.WHITE}Please reenter your password: ")
        while password != password1:
            print(f"{Fore.RED}[-]{Fore.WHITE}Your passwords didn't match, please try again.")
            password = input(f"{Fore.WHITE}Enter your password: ")
            password1 = input(f"{Fore.WHITE}Please reenter your password: ")
        insertData = '''INSERT INTO info(username,firstname,surname,password)
        VALUES(?,?,?,?)'''
        cursor.execute(insertData, [username, firstName, surname, password])
        db.commit()


def menu():
    while True:
        print(f"{Fore.WHITE}Welcome to my system")
        Menu = ('''
        1 = Create new User
        2 = Login to system
        3 = Exit\n''')

        userChoice = input(Menu)

        if userChoice == "1":
            newUser()
        elif userChoice == "2":
            login()
        elif userChoice == "3":
            print(f"{Fore.RED}Goodbye")
            sys.exit()
        else:
            print(f"{Fore.RED}[-]{Fore.WHITE}Command not recognised")


menu()
