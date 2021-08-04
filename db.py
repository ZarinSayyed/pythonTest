import sqlite3

conn=sqlite3.connect("resource.sqlite")
cursor= conn.cursor()
#sql_query=''' drop TABLE resource'''

sql_query=''' CREATE TABLE resource(
    Service text NOT NULL PRIMARY KEY,
    Port integet   NOT NULL,
    Maintainer text NOT NULL,
    Labels text NOT NULL
)'''


cursor.execute(sql_query)

#groups text  NOT NULL,
#team  text NOT NULL