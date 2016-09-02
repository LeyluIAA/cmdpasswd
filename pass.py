import sqlite3
import base64
import sys
import getopt
import os.path

def main(argv):

    # Test if database already exist or not
    if not os.path.isfile('pass.db'):
        con = sqlite3.connect('pass.db')
        QueryCurs = con.cursor()
        createTable(QueryCurs)
    else:
        con = sqlite3.connect('pass.db')
        QueryCurs = con.cursor()

    if len(argv) > 1:
        print('password is {0}'.format(argv[1]))
    else:
        print('this script needs a password')

    # Add and save a new record
    addEntry(QueryCurs,'portail','toto',con)
    addEntry(QueryCurs,'portail2','titi',con)
    addEntry(QueryCurs,'portail3','tata',con)

    displayEntry(QueryCurs,'portail')

    displayAll(QueryCurs)

    # Close connection
    QueryCurs.close()

# Create the table if it doesn't exist
def createTable(cursor):
    cursor.execute('''CREATE TABLE credentials
    (name TEXT PRIMARY KEY, password TEXT)''')

# Add a new password
def addEntry(cursor,name,password,con):
    encodedPassword = base64.b64encode(password)
    cursor.execute('''INSERT INTO credentials (name,password)
    VALUES (?,?)''',(name,encodedPassword))
    con.commit()

# Display a select all
def displayAll(cursor):
    cursor.execute('SELECT * FROM credentials')

    for i in cursor:
        (key, name, password) = i
        print("\n{0}".format(name))
        print base64.b64decode(password)

# Display one specific password
def displayEntry(cursor, name):
	cursor.execute('''SELECT name, password FROM credentials WHERE name like (?)''',(name))

	for i in cursor:
		(key, name, password) = i
        print("\n{0}".format(name))
        print base64.b64decode(password)

# Remove an password
def removeEntry(cursor,name,con):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
