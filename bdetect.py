#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import shutil, errno
import os
import ConfigParser
import hashlib
import funcs



#
#variables
#
count = 0
projectName = ""
whiteLst = [".project.bd"] 
config = ConfigParser.RawConfigParser()

#
#check argvs
#
if len(sys.argv) <= 1:
    funcs.help()

for arg in sys.argv:
    if arg == 'add':
        projectName = sys.argv[count + 1]
        dirSrc = sys.argv[count + 2]
        if os.path.exists('projects/' + projectName):
            print "Project name exists!: " + projectName
            exit()
        #copy source
        print "Copying..............................."
        shutil.copytree(dirSrc,'projects/' + projectName, symlinks=False, ignore=None)
        #create directory for bdetect
        print "Finishing............................."
        if not os.path.exists('projects/' + projectName + '/.bdetect'):
            os.makedirs('projects/' + projectName + '/.bdetect')
        #create file config
        config.add_section(projectName)
        config.set(projectName, 'path', os.path.abspath(dirSrc))
        config.set(projectName, 'struct', funcs.walkDir(dirSrc))
        with open('projects/' + projectName + '/.bdetect/.projects.cfg', 'wb') as configfile:
            config.write(configfile)
        print "Create a project successful: " + projectName
    if arg == 'del':
        #delete project
        projectName = sys.argv[count + 1]
        if not os.path.exists('projects/' + projectName):
            print "Project not exists!: " + projectName
            exit()
        shutil.rmtree('projects/' + projectName)
        print "Deleted project: " + projectName
    if arg == 'check':
        #check project
        projectName = sys.argv[count + 1]
        funcs.check(project)
    if arg == 'list':
        #show list projects   
        for i in os.listdir('projects'):
        	print i
    if arg == 'commit':
        print "Changing..."
        #write .history
    if arg == 'help':
        funcs.help()
  
    count += 1