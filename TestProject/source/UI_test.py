from tkinter import *
from mysql.connector import connect

sql = connect(host='localhost',
              user='root',
              password='dapamaka',  # input("password: "),
              database='mdfdatabase')

cursor = sql.cursor()

cursor.execute("SELECT * FROM classes")

data = cursor.fetchall()

data.insert(0,
            (
                'id', 'code', 'name', 'credits', 'semester', 'elective', 'level',
                'aims', 'outcomes', 'syllabus', 'comments', 'reading',
                'total', 'lecture', 'tutorial', 'assignment', 'lab', 'study'
            )
            )

for i in data:
    print(i)

root = Tk()

height = len(data)
width = len(data[0])
for i in range(len(data)):  # Rows
    for j in range(len(data[i])):  # Columns
        b = Label(root, text=str(data[i][j]))
        b.grid(row=i, column=j)

mainloop()

print('\nhere')
