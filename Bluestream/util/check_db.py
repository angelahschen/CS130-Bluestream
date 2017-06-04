import sqlite3

####### Usage:
#           - modify TEST_NUMBERS
#             to include indeces of select_strings
#
#           - add sqlite3 select statementsto select_strings
#

TEST_NUMBERS = [6]

DB_PATH = '../db.sqlite3'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# example:
select_strings = [
        # (0) print sqlite tables
        'select name from sqlite_master where type="table"',

        # (1) print person database
        'select * from site_ver1_person',

        # (2) print all from auth database
        'select * from auth_user',

        # (3) print all from session database
        'select * from django_session',

        # (4) print all from section4 database
        'select * from site_ver1_formsection4 where id>=3',

        # (5) drop all values from section4 database
        'delete from site_ver1_formsection4 where id>=1',

        # (6) print all from section5 database
        'select * from site_ver1_formsection5 where id>=3',
        ]

for i in TEST_NUMBERS:
    res = c.execute(select_strings[i]).fetchall()
    print(res)
    print('\n')

c.close()
conn.commit()
conn.close()
