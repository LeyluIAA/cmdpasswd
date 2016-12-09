#!/usr/bin/env python

"""
Command line password manager.
This tool let you securely store passwords and display them.
"""

import sqlite3
import base64
import sys, getopt
import os.path
import hashlib, binascii, uuid
import argparse

def main(argv):

    if os.path.isfile('pass.db'):
        # Connect to the database
        con = sqlite3.connect('pass.db')

    # Get options and args
    try:
        ap = argparse.ArgumentParser(
            description='Password manager in command line'
        )

        ap.add_argument(
            '-c',
            '--create',
            action='store_true',
            help='Create the database'
        )

        ap.add_argument(
            '-a',
            '--add',
            action='store_true',
            help='Add a new password'
        )

        ap.add_argument(
            '-l',
            '--list',
            action='store_true',
            help='List all password'
        )

        ap.add_argument(
            '-o',
            '--one',
            action='store_true',
            help='Display only one password'
        )

        ap.add_argument(
            '-r',
            '--remove',
            action='store_true',
            help='Remove a password'
        )

        ap.add_argument(
            '-u',
            '--update',
            action='store_true',
            help='Update a password'
        )

        opts = ap.parse_args(argv)

    except Exception as err:
        print(err)
        sys.exit()

    if opts.create:
        if os.path.isfile('pass.db'):
            print('==== Database already exist ====')
            quit()
        else:
            con = sqlite3.connect('pass.db')
            create_table(con)
            arg = raw_input('Enter a password to access database: ')
            add_entry(con, 'connect', 'admin', arg)
            quit()

    if opts.add:
        arg = raw_input('Please authenticate: ')
        if check_pass(con, arg):
            newname = raw_input('Enter a name for your password: ')
            identity = raw_input('Enter a id: ')
            newpassword = raw_input('Enter a password: ')
            add_entry(con, newname, identity, newpassword)
            quit()
        else:
            quit()

    if opts.list:
        arg = raw_input('Please authenticate: ')
        if check_pass(con, arg):
            display_all(con)
            quit()
        else:
            quit()

    if opts.one:
        arg = raw_input('Please authenticate: ')
        if check_pass(con, arg):
            name = raw_input('Which password do you want to display? ')
            display_entry(con, name)
            quit()
        else:
            quit()

    if opts.remove:
        arg = raw_input('Please authenticate: ')
        if check_pass(con, arg):
            oldname = raw_input(
                'Type the name of password you want to remove: '
            )
            remove_entry(con, oldname)
            quit()
        else:
            quit()

    if opts.update:
        arg = raw_input('Please authenticate: ')
        if check_pass(con, arg):
            name = raw_input(
                'Type the name of password you want to update: '
            )
            identity = raw_input(
                'Type the new id: '
            )
            newx = raw_input('Type the new password: ')
            update_entry(con, name, identity, newx)
            quit()
        else:
            quit()

def hash_password(password):
    """
    Hash a password
    :param string password: user password
    :return string hashed password:
    """

    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha512(salt.encode() + password.encod,e()).hexdigest() + ':' + salt

def check_password(con, user_password):
    """
    Check if password is correct or not
    :param string hashed_password: hashed password
    :param string user_password: user password
    :return boolean:
    """

    cursor = con.cursor()

    try:
        cursor.execute(
            '''SELECT password FROM credentials WHERE name=?''',
            ('connect',))

        for i in cursor:
            (password,) = i

        cursor.close()

        password, salt = hashed_password.split(':')
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()
    except:
        print('Impossible to check the access, is the DB correctly created ?')
        cursor.close()
        sys.exit()

def create_table(con):
    """
    Create a table.
    :param object con: connection to the database
    """

    cursor = con.cursor()

    try:
        cursor.execute('''CREATE TABLE credentials
        (name TEXT PRIMARY KEY, identity TEXT, password TEXT)''')
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

        if decodedpassword == checkpass:
            return True
        else:
            print('==== Authentication failed ====')
            return False
    except:
    	print('Impossible to check the access, is the DB correctly created ?')
    	cursor.close()
    	sys.exit()

def add_entry(con, name, identity, password):
    """
    Add a new password
    :param object con: connection to the database
    :param string name: name of the new password
    :param string password: password to add
    """

    cursor = con.cursor()

    try:
        encodedPassword = base64.b64encode(password)
        cursor.execute('''INSERT INTO credentials (name, identity, password)
        VALUES (?,?,?)''',(name, identity, encodedPassword))
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
        print('List of all passwords: \n')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        for i in cursor:
            (name, identity, password) = i
            print('{0}\n id: {1}\n password: {2}\n'.format(
                    name,
                    identity,
                    base64.b64decode(password)
                )
            )
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

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
        	'''SELECT name, identity, password FROM credentials WHERE name=?''',
        	(name,))

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        for i in cursor:
            (name, identity, password) = i
            print('{0}\n id: {1}\n password: {2}\n'.format(
                    name,
                    identity,
                    base64.b64decode(password)
                )
            )
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

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

def update_entry(con, name, identity, newpass):
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
        	'''UPDATE credentials SET password=?, identity=? WHERE name=?''',
        	(encodedPassword, identity, name))
        con.commit()
        cursor.close()
        print('Update successful')
    except:
        cursor.close()
        print('Update failed')

if __name__ == '__main__':
    main(sys.argv[1:])
