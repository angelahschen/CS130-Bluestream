import sqlite3

DB_PATH = '../db.sqlite3'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# example:
# print sqlite tables
res = c.execute('select name from sqlite_master where type="table"').fetchall()
print(res)

# print person database
res = c.execute('select * from site_ver1_person').fetchall()
print(res)

# print all from auth database
res = c.execute('select * from auth_user').fetchall()
print(res)
