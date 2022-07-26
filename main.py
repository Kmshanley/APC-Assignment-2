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
        print ("------Name-----")
        print (self.fname + " " + self.lname)
        print ("----------------")
        return self.fname + " " + self.lname

    def searchClass(self):
        param = input("Enter parameter to search on: ")
        param = param.upper()
        val = input("Enter value for parameter: ")

        dbCursor.execute("""SELECT CRN, TITLE FROM COURSE WHERE ? = ?;""", (param, val))

        results = dbCursor.fetchall()

        for i in results:
            print(i)

        if len(results) == 0:
            print("No results found!")

    def Log_out(self):
        db.commit()
        db.close()
        quit() #just end the program    

    def __repr__(self) -> str:
        return str(self.id) + ": " + self.fname + " " + self.lname

class student(user):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname, id)
        self.schedule = list()

    def __init__(self, fname, lname, id, schedule):
        super().__init__(fname, lname, id)
        self.schedule = schedule

    def addClass(self):
        crn = input("Enter crn: ")
        self.schedule.append(crn)

    def dropClass(self):
        crn = input("Enter crn: ")
        try:
            self.schedule.remove(crn)
        except ValueError:
            print("Unable to remove class, class not found.")

    def Print_Registered_Classes(self):
        for i in self.schedule:
            print(f"{i}")

class instructor(user):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname, id)
        self.roster = list()

    def __init__(self, fname, lname, id, roster):
        super().__init__(fname, lname, id)
        self.roster = roster

    def addClass(self):
        crn = input("Enter crn: ")
        self.roster.append(crn)

    def dropClass(self):
        crn = input("Enter crn: ")
        try:
            self.roster.remove(crn)
        except ValueError:
            print("Unable to remove class, class not found.")

    def Print_Roster(self):
        for i in self.roster:
            print(f"{i}")

class admin(user):
    def __init__(self, fname, lname, id):
        super().__init__(fname, lname, id)

    def sysAddCourse(self):
        crn = input("Enter Crn: ")
        title = input("Enter title: ")
        dept = input("Enter Department: ")
        time = input("Enter Time: ")
        dayofweek = input("Enter Days of the week: ")
        semester = input("Enter semester: ")
        try:
            year = int(input("Enter Year: "))
        except ValueError:
            print("Invalid Input")
            year = 0
        try:
            credits = int(input("Enter Credits: "))
        except ValueError:
            print("Invalid Input")
            credits = 0

        dbCursor.execute("""INSERT INTO COURSE VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", (crn, title, dept, time, dayofweek, semester, year, credits))
            
    def sysRemoveCourse(self):
        crn = input("Enter crn number to delete: ")
        dbCursor.execute("""DELETE FROM COURSE WHERE CRN = ?;""", (crn,))

    def sysAddUser(self):
        select = input("Enter user type (Student, Admin, Instructor): ")

        name = input("Enter first name and last name: ")
        name.split(" ", 2)
        id = input("Enter user ID: ")
        psd = input("Enter user password: ")

        psdhash = hashlib.sha256()
        psdhash.update(bytes(psd, 'utf-8')) #generate hash of password

        if select == "Student":
            dbCursor.execute("""INSERT INTO STUDENT VALUES (?, ?, ?, ?);""", (id, name[0], name[0], psdhash.digest()))
        elif select == "Admin":
            dbCursor.execute("""INSERT INTO ADMIN VALUES (?, ?, ?, ?);""", (id, name[0], name[0], psdhash.digest()))
        elif select == "Instructor":
            dbCursor.execute("""INSERT INTO INSTRUCTOR VALUES (?, ?, ?, ?);""", (id, name[0], name[0], psdhash.digest()))
        else:
            print("Invalid Input")

    def sysRemoveUser(slef):
        select = input("Enter user type (Student, Admin, Instructor): ")
        id = input("Enter ID of user to remove: ")

        if select == "Student":
            dbCursor.execute("""DELETE FROM STUDENT WHERE USERID = ?;""", (id,))
        elif select == "Admin":
            dbCursor.execute("""DELETE FROM ADMIN WHERE USERID = ?;""", (id,))
        elif select == "Instructor":
            dbCursor.execute("""DELETE FROM INSTRUCTOR WHERE USERID = ?;""", (id,))
        else:
            print("Invalid Input")

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
        dbCursor.execute("""CREATE TABLE STUDENT ( USERID INTEGER PRIMARY KEY, FNAME TEXT, LNAME TEXT, PASSWORDHASH BLOB, ENROLLEDCLASSES BLOB);""")
    except sqlite3.OperationalError:
        pass
        
    try:
        dbCursor.execute("""CREATE TABLE INSTRUCTOR ( USERID INTEGER PRIMARY KEY, FNAME TEXT, LNAME TEXT, PASSWORDHASH BLOB, );""")
    except sqlite3.OperationalError:
        pass

    try: #add default admin
        dbCursor.execute("""INSERT INTO ADMIN VALUES (00000, "admin", "admin", ?);""", (b'\x8civ\xe5\xb5A\x04\x15\xbd\xe9\x08\xbdM\xee\x15\xdf\xb1g\xa9\xc8s\xfcK\xb8\xa8\x1fo*\xb4H\xa9\x18',))
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
                if (search[0][0] == psdhash.digest()):
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
                if (search[0][0] == psdhash.digest()):
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
                if (search[0][0] == psdhash.digest()):
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
            try:
                getattr(newUser, method_list[cmdNum])()
            except:
                print("Error executing command")
        except IndexError:
            print("Command Selection out of range, try again")

    db.commit()
    db.close()
