from hmac import digest
import sqlite3
import hashlib

maxID = 1
dbCursor = None #will be assigned in main

class user():
    def __init__(self, fname, lname, id):
        self.fname  = fname
        self.lname = lname
        self.id = id

    def getName(self) -> str:
        print (self.fname + " " + self.lname)
        return self.fname + " " + self.lname

    def searchClass(self):
        pass

    def __repr__(self) -> str:
        return str(self.id) + ": " + self.fname + " " + self.lname

class student(user):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname, id)
        self.schedule = list()

    def addClass(self, crn):
        self.schedule.append(crn)

    def dropClass(self, crn):
        try:
            self.schedule.remove(crn)
        except ValueError:
            print("Unable to remove class, class not found.")

    def printRegClasses(self):
        for i in self.schedule:
            print(f"{i}")

class instructor(user):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname, id)

    def __init__(self, fname, lname, id, schedule):
        super().__init__(fname, lname, id)
        self.schedule = schedule

    def getClassList(self) -> str:
        pass

class admin(user):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname, id)

    def sysAddCourse(self, crs):
        pass

    def sysRemoveCourse(self):
        crn = input("Enter crn number to delete: ")
        dbCursor.execute("""DELETE FROM COURSE WHERE CRN = ?;""", (crn))

    def sysAddUser(self, user):
        pass

    def sysRemoveUser(slef, userID):
        pass

if __name__ == "__main__" :
    db = sqlite3.connect('database.db')
    dbCursor = db.cursor()

    try:
        dbCursor.execute("""CREATE TABLE COURSE ( CRN INTEGER PRIMARY KEY, TITLE TEXT, DEPARTMENT TEXT, TIME TEXT, DAYSOFWEEK TEXT, SEMESTER TEXT, YEAR INTEGER, CREDITS INTEGER);""")
    except sqlite3.OperationalError:
        pass

    try:
        dbCursor.execute("""CREATE TABLE ADMIN ( USERID INTEGER PRIMARY KEY, FNAME TEXT, LNAME TEXT, PASSWORDHASH BLOB);""")
    except sqlite3.OperationalError:
        pass

    try:
        dbCursor.execute("""CREATE TABLE STUDENT ( USERID INTEGER PRIMARY KEY, FNAME TEXT, LNAME TEXT, PASSWORDHASH BLOB);""")
    except sqlite3.OperationalError:
        pass
        
    try:
        dbCursor.execute("""CREATE TABLE INSTRUCTOR ( USERID INTEGER PRIMARY KEY, FNAME TEXT, LNAME TEXT, PASSWORDHASH BLOB);""")
    except sqlite3.OperationalError:
        pass


    print("Welcome to this scheduling system")

    notAuth = True

    while notAuth:
        name = input("Please enter your first name and last name: ")
        name = name.split(" ", 2)

        print("1. Student")
        print("2. Instructor")
        print("3. Admin")
        userSelect = input("Enter your user from the above options selection: ")

        psdhash = hashlib.sha256()
        password = input("Enter your password: ")
        psdhash.update(bytes(password, 'utf-8'))

        if (userSelect == "1"):
            dbCursor.execute("""SELECT PASSWORDHASH, USERID FROM STUDENT WHERE FNAME = ? AND LNAME = ?;""", (name[0], name[1]))
            search = dbCursor.fetchall()

            if len(search) == 0:
                print("User does not exist in this system")
            else:
                if (search[0] == psdhash.digest()):
                    newUser = student(name[0], name[1], maxID)
                    notAuth = False #user is now authorized
                else:
                    print("Wrong password")

        elif (userSelect == "2"):
            dbCursor.execute("""SELECT PASSWORDHASH, USERID FROM INSTRUCTOR WHERE FNAME = ? AND LNAME = ?;""", (name[0], name[1]))
            search = dbCursor.fetchall()

            if len(search) == 0:
                print("User does not exist in this system")
            else:
                if (search[0] == psdhash.digest()):
                    newUser = instructor(name[0], name[1], maxID)
                    notAuth = False #user is now authorized
                else:
                    print("Wrong password")

        elif (userSelect == "3"):
            dbCursor.execute("""SELECT PASSWORDHASH, USERID FROM ADMIN WHERE FNAME = ? AND LNAME = ?;""", (name[0], name[1]))
            search = dbCursor.fetchall()

            if len(search) == 0:
                print("User does not exist in this system")
            else:
                if (search[0] == psdhash.digest()):
                    newUser = admin(name[0], name[1], maxID)
                    notAuth = False #user is now authorized
                else:
                    print("Wrong password")
        else: 
            newUser = None

    #string list of all methods in the user's chosen class
    method_list = [attribute for attribute in dir(newUser) if callable(getattr(newUser, attribute)) and attribute.startswith('__') is False]
    
    while True:
        ct = 1
        #print the method list so the user can choose which method to execute
        for i in method_list:
            print(f"{ct}. {i}")
            ct += 1

        cmdNum = input("Select a command:")
        cmdNum = int(cmdNum)
        cmdNum -= 1

        #execute chosen method
        try: 
            getattr(newUser, method_list[cmdNum])()
        except IndexError:
            print("Command Selection out of range, try again")
