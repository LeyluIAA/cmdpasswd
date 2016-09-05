#!/usr/bin/env python

"""
Command line password manager.
This tool let you securely store passwords and display them.
"""

import sqlite3
import base64
import sys
import getopt

def main(argv):
	# Connect to the database
    con = sqlite3.connect('pass.db')

    # Get options and args
    try:
        opts, args = getopt.getopt(argv, 'hlc:p:o:a:r:u:x:')
    except Exception as err:
        print err
        sys.exit()

    newx = ''

    # If no options, print help
    if len(opts) is 0 and len(args) is 0:
        usage()
        sys.exit()

    # Do specific actions depends on options
    for opt, arg in opts:
    	# Display help
        if opt in ('-h'):
            usage()
        # Display all passwords
        if opt == '-l':
            for opt, arg in opts:
                if opt == '-p':
                    if check_pass(con, arg):
                        display_all(con)
                    else:
                    	print('wrong password')
        # Display a specific password
        if opt == '-o':
            name = arg
            count = 0
            for opt, arg in opts:
                if opt == '-p':
                    count += 1
                    if check_pass(con, arg):
                        display_entry(con, name)
                    else:
                    	print('wrong password')
            if not count:
            	print('missing arguments')
        # Create the database
        if opt == '-c':
            create_table(con)
            add_entry(con,'connect',arg)
        # Add a password
        if opt == '-a':
            newname = arg
            count = 0
            for opt, arg in opts:
                if opt == '-p':
                    count += 1
                    if check_pass(con, arg):
                        for opt, arg in opts:
                            if opt == '-x':
                                newpassword = arg
                    else:
                        print('wrong password')
                    try:
                        add_entry(con, newname, newpassword)
                    except:
                        print('missing arguments')
            if not count:
                print('missing arguments')
        # Remove a password
        if opt == '-r':
            oldname = arg
            count = 0
            for opt, arg in opts:
                if opt == '-p':
                	count += 1
                    if check_pass(con, arg):
                        try:
                            remove_entry(con, oldname)
                        except:
                            print('Wrong password')
            if not count:
                print('missing arguments')
        # Update a password
        if opt == '-u':
            name = arg
            count = 0
            for opt, arg in opts:
                if opt == '-p':
                    count += 1
                    if check_pass(con, arg):
                        for opt, arg in opts:
                            if opt == '-x':
                                count += 2
                                newx = arg
                                try:
                                    update_entry(con, name, newx)
                                except:
                                    print('missing arguments')
                        if count < 2:
                            print('missing arguments')
            if not count:
                print('missing arguments')

def usage():
	"""
	Give the usage to the user
    """

	print('''\
    	usage: python {0} [options] [arguments]
            -h --help for help
            -c password : Create the database
            -l -p password : List all passwords
            -o name -p password : Display a password
            -a name -p password -x password-to-add : Add a password
            -r oldname -p password : Remove a password
            -u name -p password -x newpassword : Update a password\
            '''.format(sys.argv[0]))

def create_table(con):
    """
    Create a table.
    :param object con: connection to the database
    """

    cursor = con.cursor()

    try:
        cursor.execute('''CREATE TABLE credentials
        (name TEXT PRIMARY KEY, password TEXT)''')
        con.commit()
        cursor.close()
        print('database successfully created')
    except:
    	print('Impossible to create the database')
        cursor.close()

def check_pass(con, checkpass):
    """
    Check if the auth password is correct
    :param object con: connection to the database
    :param string checkpass: user password to authenticate him on the app
    :return type boolean:
    """

    cursor = con.cursor()

    try:
        cursor.execute(
    	    '''SELECT password FROM credentials WHERE name=?''',
    	    ('connect',))

        for i in cursor:
            (password,) = i
            decodedpassword = base64.b64decode(password)

        cursor.close()
        return decodedpassword == checkpass
    except:
    	print('Impossible to check the access, is the DB correctly created ?')
    	cursor.close()
    	sys.exit()

def add_entry(con, name, password):
    """
    Add a new password
    :param object con: connection to the database
    :param string name: name of the new password
    :param string password: password to add
    """

    cursor = con.cursor()

    try:
        encodedPassword = base64.b64encode(password)
        cursor.execute('''INSERT INTO credentials (name,password)
        VALUES (?,?)''',(name, encodedPassword))
        con.commit()
        cursor.close()
        print('password successfully inserted')
    except:
        cursor.close()
        print('this name already exist in database')

def display_all(con):
    """
    Display all passwords
    :param object con: connection to the database
    """

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

def display_entry(con, name):
    """
    Display a specific password
    :param object con: connection to the database
    :param string name: password name to display
    """

    cursor = con.cursor()

    try:
        cursor.execute(
        	'''SELECT name, password FROM credentials WHERE name=?''',
        	(name,))

        for i in cursor:
            (name, password) = i
            print("\n{0}".format(name))
            print base64.b64decode(password)
        cursor.close()
    except:
        cursor.close()
        print('this name does not exist in database')
        sys.exit()

def remove_entry(con, name):
    """
    Remove a password
    :param object con: connection to the database
    :param string name: password name to remove
    """

    cursor = con.cursor()

    cursor.execute('''DELETE FROM credentials WHERE name=?''',(name,))
    con.commit()

    print('password successfully removed')
    cursor.close()

def update_entry(con, name, newpass):
    """
    Update a password
    :param object con: connection to the database
    :param string name: password name to update
    :param string newpass: new password to set
    """

    cursor = con.cursor()

    encodedPassword = base64.b64encode(newpass)

    try:
        cursor.execute(
        	'''UPDATE credentials SET password=? WHERE name=?''',
        	(encodedPassword, name))
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
