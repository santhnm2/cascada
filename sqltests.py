import unittest
import sqlite3
import random

from Website import *

class TestSqlOperations(unittest.TestCase):

  def test_checkIfApproved(self):
    con = sqlite3.connect("Cascada.db")
    cur = con.cursor()
    cur.execute("INSERT INTO UserTable (Email, Password, Name, Type, Approved) VALUES (?,?,?,?,?)", ("testApproved@gmail.com", "test123", "test", "Professor", "Approved"))
    con.commit()
    con.close()
    status = checkApproved("testApproved@gmail.com")
    self.assertEqual("Approved", status[0][0])

  def test_approveProfessor(self):
    con = sqlite3.connect("Cascada.db")
    cur = con.cursor()
    cur.execute("INSERT INTO UserTable (Email, Password, Name, Type, Approved) VALUES (?,?,?,?,?)", ("test2Approved@gmail.com", "test123", "test", "Professor", "Unapproved"))
    con.commit()
    con.close()
    approveProfessor("test2Approved@gmail.com")
    status = checkApproved("test2Approved@gmail.com")
    self.assertEqual("Approved", status[0][0])

  def test_getAllClasses(self):
    classList = getAllClasses()
    self.assertTrue(len(classList) > 0)

  def test_checkTasks(self):
    taskList = getTasksForStudent("student@test.com")
    self.assertTrue(len(taskList) > 0)

  # Manually tested inserting users into the database

if __name__ == '__main__':
    unittest.main()