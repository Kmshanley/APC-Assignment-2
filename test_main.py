from main import *
import sqlite3
import sys
from contextlib import contextmanager
from io import StringIO

@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig

def init_db():
    db = sqlite3.connect('database.db')
    dbCursor = db.cursor()
    return dbCursor, db

def test_admin_add_remove_course():
    dbCursor, db = init_db()
    user_under_test = admin("admin", "admin", 1243124, dbCursor)
    
    with replace_stdin(StringIO("345435\nApplied Programming\nComputer Science\n4:00-5:00pm\nMWF\nFall\n2019\n4\n")):
        user_under_test.sysAddCourse()

    db.commit()

    dbCursor.execute("""SELECT TITLE FROM COURSE WHERE CRN = ?;""", (345435,))
    res = dbCursor.fetchall()
    assert res[0][0] == "Applied Programming"

    with replace_stdin(StringIO("345435\n")):
        user_under_test.sysRemoveCourse()

    dbCursor.execute("""SELECT TITLE FROM COURSE WHERE CRN = ?;""", (345435,))
    res = dbCursor.fetchall()
    assert len(res) == 0

    db.close()

def test_admin_add_remove_user():
    dbCursor, db = init_db()
    user_under_test = admin("admin", "admin", 1243124, dbCursor)

    with replace_stdin(StringIO("Student\nTim Jankins\n32423432\ntestPassword\n")):
        user_under_test.sysAddUser()

    db.commit()

    dbCursor.execute("""SELECT FNAME,LNAME FROM STUDENT WHERE USERID = ?;""", (32423432,))
    res = dbCursor.fetchall()
    assert res[0][0] == "Tim"
    assert res[0][1] == "Jankins"

    with replace_stdin(StringIO("Student\n32423432\n")):
        user_under_test.sysRemoveUser()

    dbCursor.execute("""SELECT FNAME FROM STUDENT WHERE USERID = ?;""", (32423432,))
    res = dbCursor.fetchall()
    assert len(res) == 0

    db.close()
