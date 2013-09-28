#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb


#http://172.16.69.158/rss/Trung-Quoc.rss

#
#variables
#
DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_NAME = "tinyrss"
DATABASE_PASSWD = "871804"
DATABASE_PORT = 3306

db = MySQLdb.connect(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT), charset='utf8')
cursor = db.cursor()
cursor.connection.autocommit(True)

query = "UPDATE ttrss_user_entries SET unread = 1;"
cursor.execute(query)
print "done"