#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import shutil, errno
import os
import ConfigParser
import hashlib

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

def walkDir(pathVar):
    dirS = []
    fileS = []
    for path, dirs, files in os.walk(pathVar):
        for f in files:
            print path + f + "------" + md5Checksum(path+f)
            dirS.append([path, [f, md5Checksum(path+f)]])
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

def help():
    print 'Bdetect v1.0 (c)2012 by S3K4 team - a very fast logon Joomla Cracker - support all version'
    print 'Website: http://www.uns.vn'
    print 'Mail   : contact@uns.vn'
    print ''
    print 'Options:'
    print 'add project_name source_directory - create a new project'
    print 'list - show all projects'
    print 'del project_name - delete a project'
    sys.exit()