# requires database to be already active

import mysql.connector as con

sql = con.connect(host='localhost',
                  user='root',
                  password='dapamaka',
                  database='mdfdatabase')

cursor = sql.cursor()

cursor.execute("SELECT this_class_id, required_class_id FROM pre_requisites")

output = cursor.fetchall()

for i in range(len(output)):
    active = output[i]
    # print(active)
    q = "SELECT class_code, level FROM classes WHERE class_id = %s;"
    cursor.execute(q, (active[0],))

    this = cursor.fetchone()

    # print(this)

    q = "SELECT class_code FROM classes WHERE class_id = %s"
    cursor.execute(q, (active[1],))
    output[i] = {'class': this[0], 'level': this[1], 'otherclass': cursor.fetchone()[0]}

# output.sort(key=(lambda x: -1 * int(x['level'])))


def relies_on(code, os):
    out = []
    i = 0
    while i < len(os):
        if os[i]['class'] == code:
            o = os.pop(i)
            out += [relies_on(o['otherclass'], os)]
            os.insert(i, o)
        i += 1
    return code, out


def print_tree(tree):
    out = ['|-->' + str(tree[0])]
    out += ['\t' + l for t in tree[1] for l in print_tree(t) if l is not '']
    return out


p = relies_on('AB501', output)
# print(output)
t = print_tree(p)

for l in t:
    print(l)
