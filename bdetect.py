#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import shutil, errno
import os
import ConfigParser
import hashlib
sys.path.insert(0, 'libs')
import funcs

#
#variables
#
count = 0
projectName = ""
whiteLst = [".project.bd"] 
config = ConfigParser.RawConfigParser()


#Determine OS type and use appropriate path seperator. 
if os.name == "posix":
    pathSep = "/"
elif os.name == "nt":
    pathSep = "\\"
else:
    print "can not detect OS!"
    exit(2)


#
#check argvs
#
if len(sys.argv) <= 1:
    funcs.help()

for arg in sys.argv:
    if arg == 'add':
        projectName = sys.argv[count + 1]
        dirSrc = sys.argv[count + 2]
        try:
            if os.path.exists('projects/' + projectName):
                print "Project name exists!: " + projectName
                exit()
            #copy source
            print "Copying..............................."
            shutil.copytree(dirSrc,'projects' + pathSep + projectName, symlinks=False, ignore=None)
            #create directory for bdetect
            print "Finishing............................."
            if not os.path.exists('projects' + pathSep + projectName + pathSep + '.bdetect'):
                os.makedirs('projects' + pathSep + projectName + pathSep + '.bdetect')
            #create file config
            config.add_section(projectName)
            config.add_section("files")
            config.add_section("directories")
            
            config.set(projectName, 'path', os.path.abspath(dirSrc))
            config.set("files", 'list', funcs.walkDir(dirSrc))
            with open('projects'+ pathSep + projectName + pathSep + '.bdetect'+ pathSep +'.config', 'wb') as configfile:
                config.write(configfile)
            print "Create a project successful: " + projectName
        except:
            funcs.delProject(projectName)
    if arg == 'del':
        #delete project
        projectName = sys.argv[count + 1]
        funcs.delProject(projectName)
        print "Deleted project: " + projectName
    if arg == 'check':
        #check project
        projectName = sys.argv[count + 1]
        funcs.check(projectName)
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