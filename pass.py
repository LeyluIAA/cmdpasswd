import sqlite3
import base64
import sys
import getopt

def main(argv):

    con = sqlite3.connect('pass.db')

    try:
        opts, args = getopt.getopt(argv, 'hlcp:o:an:m:rux:')
    except Exception as err:
        print err
        sys.exit()

    newx = ''

    if len(opts) is 0 and len(args) is 0:
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ('-h'):
            usage()
        if opt == '-l':
            for opt, arg in opts:
                if opt == '-p':
                    if checkPass(con,arg):
                        displayAll(con)
        if opt == '-o':
            name = arg
            for opt, arg in opts:
                if opt == '-p':
                    if checkPass(con,arg):
                        displayEntry(con,name)
        if opt == '-c':
            for opt, arg in opts:
                if opt == '-p':
                    createTable(con)
                    addEntry(con,'connect',arg)
        if opt == '-a':
            for opt, arg in opts:
                if opt == '-p':
                    if checkPass(con,arg):
                        for opt, arg in opts:
                            if opt == '-n':
                                newname = arg
                            elif opt == '-m':
                                newpassword = arg
                    try:
                        addEntry(con,newname,newpassword)
                    except:
                        print('missing arguments')
        if opt == '-r':
            for opt, arg in opts:
                if opt == '-p':
                    if checkPass(con,arg):
                        for opt, arg in opts:
                            if opt == '-n':
                                oldname = arg
                    try:
                        removeEntry(con,oldname)
                    except:
                        print('missing arguments')
        if opt == '-u':
            for opt, arg in opts:
                if opt == '-p':
                    if checkPass(con,arg):
                        for opt, arg in opts:
                            if opt == '-n':
                                name = arg
                            if opt == '-x':
                                newx = arg
                    try:
                        updateEntry(con,name,newx)
                    except:
                        print('missing arguments')

def usage():
    print('usage: python {0} -h --help for help'.format(sys.argv[0]))

# Create the table if it doesn't exist
def createTable(con):

    cursor = con.cursor()

    try:
        cursor.execute('''CREATE TABLE credentials
        (name TEXT PRIMARY KEY, password TEXT)''')
        con.commit()
        cursor.close()
        print('database successfully created')
        return True

    except:
        cursor.close()
        return False

# Check if the given password is correct
def checkPass(con,checkpass):

    cursor = con.cursor()

    cursor.execute('''SELECT password FROM credentials WHERE name=?''',('connect',))

    for i in cursor:
        (password,) = i
        decodedpassword = base64.b64decode(password)

    cursor.close()
    return decodedpassword == checkpass

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
        print('this name already exist in database')
        return False

# Display a select all
def displayAll(con):

    cursor = con.cursor()
    try:
        cursor.execute('SELECT * FROM credentials')

        for i in cursor:
            (name, password) = i
            print('\n{0}'.format(name))
            print base64.b64decode(password)

        cursor.close()
    except:
        cursor.close()
        print('Display failed. Probably because the database does not exist.')

# Display one specific password
def displayEntry(con, name):

    cursor = con.cursor()

    try:
        cursor.execute('''SELECT name, password FROM credentials WHERE name=?''',(name,))

        for i in cursor:
            (name, password) = i
            print("\n{0}".format(name))
            print base64.b64decode(password)
        cursor.close()
    except:
        cursor.close()
        print('this name does not exist in database')
        sys.exit()

# Remove an password
def removeEntry(con,name):

    cursor = con.cursor()

    cursor.execute('''DELETE FROM credentials WHERE name=?''',(name,))
    con.commit()

    print('password successfully removed')
    cursor.close()

def updateEntry(con,name,newpass):
    cursor = con.cursor()

    encodedPassword = base64.b64encode(newpass)

    try:
        cursor.execute('''UPDATE credentials SET password=? WHERE name=?''',(encodedPassword,name))
        con.commit()
        cursor.close()
        print('Update successful')
        return True
    except:
        cursor.close()
        print('Update failed')
        return False

if __name__ == '__main__':
    main(sys.argv[1:])
