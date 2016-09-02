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
    addEntry(QueryCurs,'portail','toto')
    addEntry(QueryCurs,'portail2','titi')
    con.commit()


    # Display a select all
    QueryCurs.execute('SELECT * FROM credentials')

    for i in QueryCurs:
        (key, name, password) = i
        print("\n{0}".format(name))
        print base64.b64decode(password)

    # Close connection
    QueryCurs.close()

# Create the table if it doesn't exist
def createTable(cursor):
    cursor.execute('''CREATE TABLE credentials
    (id INTEGER PRIMARY KEY, name TEXT, password TEXT)''')

# Add a new password
def addEntry(cursor,name,password):
    encodedPassword = base64.b64encode(password)
    cursor.execute('''INSERT INTO credentials (name,password)
    VALUES (?,?)''',(name,encodedPassword))

def removeEntry(cursor,name):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
