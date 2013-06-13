#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import shutil, errno
import os
import ConfigParser

#
#functions
#
def copyAll(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

#bdetect add path

#
#variables
#
count = 0
projectName = ""
config = ConfigParser.RawConfigParser()

#
#check argvs
#
for arg in sys.argv:
    if arg == 'add':
        projectName = sys.argv[count + 1]
        path = sys.argv[count + 2]
        #copy source
        shutil.copytree(path,'projects/' + projectName, symlinks=False, ignore=None)
        #create file config
        config.add_section(projectName)
        config.set(projectName, 'path', path)
        with open('projects.cfg', 'wb') as configfile:
            config.write(configfile)
    if arg == 'del':
        projectName = sys.argv[count + 1]
        shutil.rmtree('projects/' + projectName)
        #delete project
    if arg == 'check':
        projectName = sys.argv[count + 1]
        #check project
        #read file config
        config.read("projects.cfg")
        src = config.get(projectName, 'path')
    if arg == 'list':
        #show list projects   
        for i in os.listdir('projects'):
        	print i
    count += 1