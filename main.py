classRegistry = dict()
userRegistry = dict()
maxID = 1

class course():
    def __init__(self) -> None:
        self.crn
        self.startTime
        self.endTime
        self.remainingCapacity
        self.presidingInstructor

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

    def __init__(self, fname, lname, id, schedule):
        super().__init__(fname, lname, id)
        self.schedule = schedule

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
        classRegistry.update({crs.crn : crs})

    def sysRemoveCourse(self, crn):
        classRegistry.pop(crn)

    def sysAddUser(self, user):
        userRegistry.update({user.id : user})

    def sysRemoveUser(slef, userID):
        userRegistry.pop(userID)

if __name__ == "__main__" :
    print("Welcome to this scheduling system")

    name = input("Please enter your first name and last name: ")

    name = name.split(" ", 2)

    print("1. Student")
    print("2. Instructor")
    print("3. Admin")
    userSelect = input("Enter your user from the above options selection: ")

    if (userSelect == "1"):
        newUser = student(name[0], name[1], maxID)
    elif (userSelect == "2"):
        newUser = instructor(name[0], name[1], maxID)
    elif (userSelect == "3"):
        newUser = admin(name[0], name[1], maxID)
    else: 
        newUser = None
    maxID += 1

    print(newUser)
    userRegistry.update({newUser.id : newUser})

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
        getattr(newUser, method_list[cmdNum])()
