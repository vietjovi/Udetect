#!/usr/bin/python
import smtplib
import os
 
dirS = []
fileS = []
for path, dirs, files in os.walk('/home/vietjovi/atom/'):
    for f in files:
		print path + '/' + f
