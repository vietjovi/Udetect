#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
from pyatom import AtomFeed
import feedparser
import MySQLdb
from xml.sax.saxutils import unescape
import subprocess
import os.path
import string
from datetime import date
import re
import urllib
#import PyRSS2Gen

reload(sys)
sys.setdefaultencoding("utf8")

#
#variables
#
DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_NAME = "tinyrss"
DATABASE_PASSWD = "871804"
DATABASE_PORT = 3306
maxEntry = 100
urlRoot = "/var/www/atom/"
feedUrl = "http://172.16.69.162/atom/"
#daySub = 10

#{ten_file:{ten_category:[keywork]}}
langArray = {'file1':{'Trung Quoc':['5000']}, 'file2': {'The loai 1':['khủng','bố']}, 'file3':{'The Loai 2':['Sony','399']}}

rssUrl = ""
logFile = "./rss.log"
log = ""
#query = "SELECT ttrss_feed_categories.id, ttrss_feeds.feed_url, ttrss_entries.title, ttrss_entries.link, ttrss_entries.guid, ttrss_entries.content, ttrss_entries.updated, ttrss_entries.id FROM ttrss_user_entries, ttrss_entries, ttrss_feeds, ttrss_feed_categories WHERE ttrss_entries.id = ttrss_user_entries.ref_id AND ttrss_user_entries.feed_id=ttrss_feeds.id AND ttrss_feeds.cat_id = ttrss_feed_categories.id AND ttrss_feeds.cat_id = %s AND ttrss_user_entries.unread = 1; " % (i[0]) 
#ttrss_user_entries, ttrss_feeds, ttrss_entries


#
#function
#
def cleanStr(inputStr):
  return inputStr.replace("&#039;","'")

def trans(strInput, frLang, toLang):
  return subprocess.check_output('translate -t %s -f %s "%s"' % (toLang, frLang, strInput.replace("\"","\\\"")), shell=True)

def fixStr(inputStr):
  strTmp = inputStr
  return eval(str(strTmp[0]))['value']

#
#main
#
db = MySQLdb.connect(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT), charset='utf8')
cursor = db.cursor()
cursor.connection.autocommit(True)

for x in langArray:
  for y in langArray[x]:
    query = "select id, title from ttrss_feed_categories WHERE title = '%s';"%(y)
    cursor.execute(query)
    lstCat = cursor.fetchall()
    print datetime.datetime.utcnow()
    for i in lstCat:
      clause = ""
      cat = i[1]
      #print langArray[x][y]
      #fname = string.lower(cat.replace(' ','-')) + ".rss"
      fname = x + ".rss"
      try:
        for h in langArray[x][y]:
          clause += " ttrss_entries.title like '%"+h+"%' AND "
      except:
        pass

      query = "SELECT ttrss_feed_categories.id, ttrss_feeds.feed_url, ttrss_entries.title, ttrss_entries.link, ttrss_entries.guid, ttrss_entries.content, ttrss_entries.updated, ttrss_entries.id, ttrss_entries.author FROM ttrss_user_entries, ttrss_entries, ttrss_feeds, ttrss_feed_categories WHERE %s ttrss_entries.id = ttrss_user_entries.ref_id AND ttrss_user_entries.feed_id=ttrss_feeds.id AND ttrss_feeds.cat_id = ttrss_feed_categories.id AND ttrss_feeds.cat_id = %s AND ttrss_user_entries.unread = 1 ORDER BY ttrss_entries.id DESC LIMIT 0, %d;" % (clause, i[0], maxEntry)
      #print query
      cursor.execute(query)
      lstRss = cursor.fetchall()
      item = []
      lstIdToMarkRead = []
      
      lang = "en"
      for la in langArray:
        if cat == la[0]:
          lang = la[1]
      print cat + " -- Language: " + lang
      
      if not os.path.isfile(fname):
        open(fname, 'w').close() 
      feedNew = AtomFeed(title=cat,
                    subtitle="My Feeds",
                    feed_url=feedUrl+string.lower(cat.replace(' ','-')) + ".rss",
                    url=feedUrl.split("/")[0] + "//" + feedUrl.split("/")[2] + "/",
                    author="")
      if len(lstRss) > 0:
        print "You have %s feeds!" % (str(len(lstRss)))
        rssUrl = urlRoot + fname    
        feedOld = feedparser.parse(rssUrl) #lay feed cu tu file

        for rss in lstRss:
          title = cleanStr(rss[2])
          link = rss[3].replace('"','')
          author = rss[8]
          dateUpdated = rss[6]
          content = rss[5]
          lstIdToMarkRead.append(str(rss[7]))
          log = str(rss[7]) + " || " + str(rss[6]) + " || " + title
          try:
            subprocess.check_output('echo "%s" >> %s' % (log.replace("\"","\\\""), logFile), shell=True)
          except:
            pass

          feedNew.add(title=title,
             content=content,
             content_type="html",
             author=author,
             url=link,
             updated=dateUpdated)

        numFeedOld = len(feedOld["items"])
        numFeedNew  = len(feedparser.parse(feedNew.to_string())["items"])
        for i in range(0,maxEntry - numFeedNew):
          try:
            content = fixStr(feedOld["items"][i]["content"])
            dateUpdated = datetime.datetime.strptime(feedOld["items"][i]['updated'],'%Y-%m-%dT%H:%M:%SZ')
            feedNew.add(
               title=feedOld["items"][i]["title"],
               content=content,
               content_type="html",
               author=feedOld["items"][i]["author"],
               url=feedOld["items"][i]["link"],
               updated=dateUpdated)
          except:
            break
        #ghi file rss    
        ff = open(urlRoot + fname, 'w')
        ff.write(feedNew.to_string())
        ff.close()
        print str(date.today()) + " || " + "Generated "+ rssUrl +"\n"
      #Mark read
      for int_id in lstIdToMarkRead:
        query = "UPDATE `ttrss_user_entries` SET `unread` = 0 WHERE ref_id =" + str(int_id)
        cursor.execute(query)