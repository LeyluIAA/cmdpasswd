import sqlite3
import base64
import sys
import getopt

def main(argv):

    con = sqlite3.connect('pass.db')
    createTable(con)

    if len(argv) > 1:
        print('password is {0}'.format(argv[1]))
    else:
        print('this script needs a password')

    # Add and save a new record
    addEntry(con,'portail','toto')
    addEntry(con,'facebook','titi')
    addEntry(con,'twitter','tata')

    displayAll(con)
    #removeEntry(con,'eurk')
    displayAll(con)

# Create the table if it doesn't exist
def createTable(con):

    cursor = con.cursor()

    try:
        cursor.execute('''CREATE TABLE credentials
        (name TEXT PRIMARY KEY, password TEXT)''')
        con.commit()
        cursor.close()
        print("database successfully created")
        return True

    except:
        cursor.close()
        return False

# Add a new password
def addEntry(con, name,password):

    cursor = con.cursor()

    try:
        encodedPassword = base64.b64encode(password)
        cursor.execute('''INSERT INTO credentials (name,password)
        VALUES (?,?)''',(name,encodedPassword))
        con.commit()
        cursor.close()
        print('password successfully inserted')
        return True
    except:
        cursor.close()
        print("this name already exist in database")
        return False

# Display a select all
def displayAll(con):

    cursor = con.cursor()
    cursor.execute('SELECT * FROM credentials')

    for i in cursor:
        (name, password) = i
        print("\n{0}".format(name))
        print base64.b64decode(password)

    cursor.close()

# Display one specific password
def displayEntry(con, name):

    cursor = con.cursor()
    cursor.execute('''SELECT name, password FROM credentials WHERE name=?''',(name,))

    for i in cursor:
        (name, password) = i
        print("\n{0}".format(name))
        print base64.b64decode(password)

    cursor.close()

# Remove an password
def removeEntry(con,name):

    cursor = con.cursor()

    cursor.execute('''DELETE FROM credentials WHERE name=?''',(name,))
    con.commit()

    cursor.close()

def updateEntry(con,name):
    pass

if __name__ == "__main__":
    main(sys.argv[1:])
