import sqlite3

conn = sqlite3.connect('students.db')
c = conn.cursor()

for row in c.execute("SELECT * FROM student"):
    print(row)
conn.execute("")
conn.close()
