#requires database to be already active

import mysql.connector as con


sql = con.connect(host='localhost',
                  user='root',
                  password=input("password: "),
                  database='mdfdatabase')

cursor = sql.cursor()

cursor.execute("SELECT this_class_id, required_class_id FROM pre_requisites")

output = cursor.fetchall()

for line in output:
    id0, id1 = line
    q = "SELECT class_code FROM classes WHERE class_id = %s"

    cursor.execute(q, (id0,))
    this = cursor.fetchone()[0]
    cursor.execute(q, (id1,))
    req = cursor.fetchone()[0]

    print("%s <- %s" % (this, req))
