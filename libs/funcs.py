#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import shutil, errno
import os
import ConfigParser
import hashlib
import difflib

#
#varialble
#
diffC = difflib.Differ()

if os.name == "posix":
    pathSep = "/"
elif os.name == "nt":
    pathSep = "\\"
else:
    print "can not detect OS!"
    exit(2)
#
#functions
#  

def check(pName):
    print pName
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.bdetect' + pathSep + '.config'))
    #config.read(open('projects' + pathSep + pName + pathSep + '.bdetect' + pathSep + '.config'))
    srcDir = config.get(pName,'pathS')
    print srcDir
    lstOrg = eval(config.get('files','listS'))
    lstSrc = eval(config.get('files','listS'))
    for i in lstOrg:
        fileTmp = i[0] + pathSep + i[1][0]
        if os.path.exists(fileTmp):
            print fileTmp
            if not (md5Checksum(fileTmp) == i[1][1]):
                #print "changed"
                # create a list of lines in text1
                fileOrg =  fileTmp.replace(srcDir,"projects" + pathSep + pName)
                text1Lines = open(fileOrg, "r").readlines()

                # dito for text2
                text2Lines = open(fileTmp, "r").readlines()
                print
                diffLst = list(diffC.compare(text1Lines, text2Lines))
                print "Lines different in " + i[1][0] + ":"
                for line in diffLst:
                    if line[0] == '-':
                        print line,
                print
        else:
            print fileTmp + "---- Not found"  

    return True

def copyAll(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def walkDir(pathVar):
    dirS = []
    fileS = []
    for path, dirs, files in os.walk(pathVar):
        for f in files:
            print path + pathSep + f + " ------ " + md5Checksum(path + pathSep + f)
            dirS.append([path, [f, md5Checksum(path + pathSep + f)]])
    return dirS

def countFiles(Barr):
    for files in os.walk(path):
        print files
    return 0

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def checkProject(pName):
    print "Checking................."

#
#delete project
#    
def delProject(pName):
    if not os.path.exists('projects' + pathSep + pName):
        print "Project not exists!: " + pName
        exit()
    shutil.rmtree('projects' + pathSep + pName)
    return True

def help():
    print 'Bdetect v1.0 (c)2012 by S3K4 team - detect change of files, directories'
    print 'Website: http://www.uns.vn'
    print 'Mail   : contact@uns.vn'
    print ''
    print 'Options:'
    print 'add project_name source_directory - create a new project'
    print 'list - show all projects'
    print 'check project_name - check a project'
    print 'del project_name - delete a project'
    sys.exit()