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
maxEntry = 10
urlRoot = "/var/www/atom/"
daySub = 10
langArray = [['Trung Quoc','zh-CN'], ['German','de'], ['French','fr']]
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

#
#main
#
db = MySQLdb.connect(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT), charset='utf8')
cursor = db.cursor()
cursor.connection.autocommit(True)
query = "select id, title from ttrss_feed_categories;"
cursor.execute(query)
lstCat = cursor.fetchall()
print datetime.datetime.utcnow()
for i in lstCat:
  query = "SELECT ttrss_feed_categories.id, ttrss_feeds.feed_url, ttrss_entries.title, ttrss_entries.link, ttrss_entries.guid, ttrss_entries.content, ttrss_entries.updated, ttrss_entries.id, ttrss_entries.author FROM ttrss_user_entries, ttrss_entries, ttrss_feeds, ttrss_feed_categories WHERE ttrss_entries.id = ttrss_user_entries.ref_id AND ttrss_user_entries.feed_id=ttrss_feeds.id AND ttrss_feeds.cat_id = ttrss_feed_categories.id AND ttrss_feeds.cat_id = %s AND ttrss_user_entries.unread = 1 AND ttrss_entries.date_updated > DATE_SUB(now(), INTERVAL %d DAY) ORDER BY ttrss_entries.id DESC LIMIT 0, %d;" % (i[0], daySub, maxEntry) 
  #print query
  cursor.execute(query)
  lstRss = cursor.fetchall()
  item = []
  lstIdToMarkRead = []
  cat = i[1]
  lang = "en"
  for la in langArray:
    if cat == la[0]:
      lang = la[1]
  print cat + " -- Language: " + lang
  fname = string.lower(cat.replace(' ','-')) + ".rss"
  if not os.path.isfile(fname):
    open(fname, 'w').close() 
  feedA = AtomFeed(title=cat,
                subtitle="My Feeds",
                feed_url="http://172.16.69.162/atom/"+string.lower(cat.replace(' ','-')) + ".rss",
                url="http://172.16.69.162/",
                author="XXX")
  if len(lstRss) > 0:
    print "You have %s feeds!" % (str(len(lstRss)))
    rssUrl = urlRoot + fname    
    feed = feedparser.parse(rssUrl)
    for rss in lstRss:
      title = cleanStr(rss[2]).decode('unicode-escape')
      link = rss[3].replace('"','')
      author = rss[8]
      dateUpdated = rss[6]
      lstIdToMarkRead.append(str(rss[7]))
      if not (lang == "en"):
        title = trans(title, lang[1], "en")
        link = "http://translate.google.com.vn/translate?sl=" + lang[1] + "&tl=en&prev=_t&hl=en&ie=UTF-8&eotf=1&u=" + urllib.quote_plus(link)
      log = str(rss[7]) + " || " + str(rss[6]) + " || " + title
      try:
        subprocess.check_output('echo "%s" >> %s' % (log.replace("\"","\\\""), logFile), shell=True)
      except:
        pass

      feedA.add(title=title,
         content=rss[5],
         content_type="html",
         author=author,
         url=link,
         updated=dateUpdated)

    numFeedOrg = len(feed["items"])
    numFeedA  = len(feedparser.parse(feedA.to_string())["items"])
    if (numFeedA < maxEntry) and numFeedOrg > 0:
      for itemTmp in feed["items"]:
        #print itemTmp['updated']
        try:      
          content = itemTmp["content"]
        except:
          content = ""
        dateUpdated = datetime.datetime.strptime(itemTmp['updated'],'%Y-%m-%dT%H:%M:%SZ')
        #print dateUpdated
        feedA.add(
           title=itemTmp["title"],
           content=content,
           content_type="html",
           author=itemTmp["author"],
           url=itemTmp["link"],
           updated=dateUpdated)
        if len(feedparser.parse(feedA.to_string())["items"]) <= maxEntry:
          break
    ff = open(urlRoot + fname, 'w')
    ff.write(feedA.to_string())
    ff.close()
    print str(date.today()) + " || " + "Generated "+ rssUrl +"\n"
  #Mark read
  for int_id in lstIdToMarkRead:
    query = "UPDATE `ttrss_user_entries` SET `unread` = 0 WHERE ref_id =" + str(int_id)
    cursor.execute(query)