#!/usr/bin/env python

import secrets
import imaplib
import sqlite3
import time
from sqlite3 import Error


def checkMail():
   M = imaplib.IMAP4_SSL(secrets.MAILSERVER)
   M.login(secrets.EMAILNAME, secrets.EMAILPASS)
   M.select()
   typ, data = M.search(None, 'ALL')
   idsL = data[0].split()
   for num in data[0].split():
       typ, data = M.fetch(num, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
       if (data[0][1][:14] == 'Subject: rob! '):
#            print data[0][1]
            subject = data[0][1][14:]
            subject = subject.translate(None, '\n\r')
            writeToDB(subject)
#   print('deleting')
   for i in idsL:
       M.store(i, '+FLAGS', r'(\Deleted)')
   M.close()
   M.logout()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def writeToDB(message):
    database = "clockBase.db"

    # create a database connection
    conn = create_connection(database)

    # write to db
    cur = conn.cursor()
    sql = "INSERT INTO messages(text,source,submissionTime) VALUES('"+ message +
"', 'source test', " + str(time.time()) + ")"
    cur.execute(sql)
    conn.commit()
    conn.close()

def dumpDatabase(): # for debugging
    database = "clockBase.db"
    # create a database connection
    conn = create_connection(database)
     # show contents (for debugging)
    cur = conn.cursor()
    cur.execute("SELECT text FROM messages WHERE displayedP < 3;")
    rows = cur.fetchall()
#    print(rows)
    for row in rows:
        print(row)
    conn.close()


def checkLoop():
    while True:
        checkMail()
        time.sleep(10.0)

def main():
    checkLoop()
#   checkMail() 
#   dumpDatabase() # for debugging

if __name__ == '__main__':
    main()

