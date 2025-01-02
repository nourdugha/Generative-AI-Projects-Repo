import sqlite3

## connect to database
connection = sqlite3.connect("student.db") 
cursor = connection.cursor()

## create table
table = """
create table STUDENT(NAME VARCHAR(22), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""
cursor.execute(table)

## insert data to the table
cursor.execute('''Insert INTO STUDENT values ('Nour','Data science', 'A', 100)''')
cursor.execute('''Insert INTO STUDENT values ('Ahmad','Data science', 'B', 80)''')
cursor.execute('''Insert INTO STUDENT values ('Dugha','Data science', 'C', 55)''')
cursor.execute('''Insert INTO STUDENT values ('Mazen','Devops', 'A', 90)''')
cursor.execute('''Insert INTO STUDENT values ('Abd','Devops', 'A', 100)''')

## fetch all data from the table
data = cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

## commit the changes and close the connection
connection.commit()
connection.close()