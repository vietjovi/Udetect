#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import sys
import glob

def fixStr(inputStr):
  strTmp = inputStr
  return eval(str(strTmp[0]))['value']

feedOld = feedOld = feedparser.parse('/var/www/atom/trung-quoc.rss')
numFeedOld = len(feedOld["items"])

for i in range(0,len(feedOld["items"])):
	print i
	print feedOld["items"][i]
	try:
		content = fixStr(feedOld["items"][i]["content"])
	except:
		content = feedOld["items"][i]["title"]
	print content
	#raw_input()