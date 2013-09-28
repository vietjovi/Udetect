#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import sys
import glob

myPath	 = sys.argv[1]
lstFile  = glob.glob(myPath + "/*.rss")

for f in lstFile:	
	feed = feedparser.parse(f)
	print f + "----" + str(len(feed["items"]))