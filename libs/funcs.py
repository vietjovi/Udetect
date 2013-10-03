#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import shutil, errno
import os
import ConfigParser
import hashlib
import difflib
import logging
import smtplib


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


def createProject(pName, sDir, version = 1):
    try:
        if os.path.exists('projects/' + pName):
            print "Project name exists!: " + pName
            return False
        config = ConfigParser.RawConfigParser()
        #copy source
        print "Copying..............................."
        shutil.copytree(sDir,'projects' + pathSep + pName, symlinks=False, ignore=None)
        #create directory for udetect
        print "Finishing............................."
        if not os.path.exists('projects' + pathSep + pName + pathSep + '.udetect'):
            os.makedirs('projects' + pathSep + pName + pathSep + '.udetect')
        #create file config
        config.add_section(pName)
        config.add_section("files")
        config.add_section("directories")        
        config.set(pName, 'pathS', os.path.abspath(sDir))
        config.set(pName, 'version', version)
        config.set("files", 'listS', walkDir(sDir))
        config.set("files", 'listP', walkDir('projects' + pathSep + pName))
        with open('projects'+ pathSep + pName + pathSep + '.udetect'+ pathSep +'.info', 'wb') as configfile:
            config.write(configfile)

        config = ConfigParser.RawConfigParser()
        config.readfp(open('udetect.conf'))
        if(not config.has_section(pName)):
            config.add_section(pName)
            config.set(pName, 'enable', "1")
            config.set(pName, 'white_ext', "*")
            config.set(pName, 'white_dir', "*")
            config.set(pName, 'email', "default")
            config.set(pName, 'type', "fast")
            with open('udetect.conf', 'wb') as configfile:
                config.write(configfile)

        if(version == 1):
            print "Create a project successful: " + pName
        open('projects'+ pathSep + pName + pathSep + '.udetect' + pathSep + '.change.log' , 'a').close()
    except:
        delProject(pName)
        return False

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
            print cleanStr(path + pathSep + f + " ------ " + md5Checksum(path + pathSep + f))
            dirS.append([cleanStr(path), [f, md5Checksum(path + pathSep + f)]])
    return dirS

def getListFiles(pathVar):
    fileS = []
    #print pathVar
    for path, dirs, files in os.walk(pathVar):
        for f in files:
            fileS.append(cleanStr(path + pathSep + f))
    return fileS

def getListDirs(pathVar):
    dirS = []
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

#
#delete project
#    
def delProject(pName):
    if not os.path.exists('projects' + pathSep + pName):
        print "Project not exists!: " + pName
        exit()
    shutil.rmtree('projects' + pathSep + pName)
    config = ConfigParser.RawConfigParser()
    config.readfp(open('udetect.conf'))
    config.remove_section(pName)
    with open('udetect.conf', 'wb') as configfile:
        config.write(configfile)
    return True

#
#output into a file
#
def outputToFile(fileName, resultContent):
    fileTmp = open(fileName, w)
    fileTmp.close()
    return True

#
#write events to log file
#
def logEvents(logContent):

    return True

#
#update
#
def updateProject(pName):
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.info'))
    srcDir = config.get(pName,'pathS')
    version = int(config.get(pName,'version'))
    print "version: " + str(version)
    print srcDir
    try:
        print "Backing up..............."
        os.rename("projects" + pathSep + pName, "revisions" + pathSep +  pName + "_" + str(version))
        print "Project Name:\t\t" + pName
        print "Updating................."
        createProject(pName, srcDir, str(version + 1))
    except:
        print "Failed!"
        return False
    print "Successful!"
    return True

#
#restore
#
def restoreProject(pName, version=0):
    if (version == 0):
        print "restoring..."
    else:
        print "restoring..."
    return True

#
#show info project
#
def showInfoProject(pName):
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.info'))
    srcDir = config.get(pName,'pathS')
    version = int(config.get(pName,'version'))
    print "source: " + srcDir
    print "version: " + str(version)
    f = open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.change.log', 'r')
    print f.read()
    f.close()
    return True

#
#test
#
def test(pathVar):
    dirS = []
    fileS = []
    for path, dirs, files in os.walk(pathVar):
        for f in files:
            print path + pathSep + f
            dirS.append([path])
    return dirS

#
#show help
#
def help():
    for line in open("docs" + pathSep + "help.txt", "r").readlines():
        print line.replace("\n","")
    sys.exit()

def cleanStr(strInput):
    strTmp = strInput.replace("\\\\","\\")
    strTmp = strInput.replace("//","/")
    return strTmp

#
#update Udetect
#
def update():
    return True

#
#check project
#
def checkProject(pName, type="fast", white_dir = '*', white_ext = '*'):
    msg = ''
    msgTmp = ''
    fName = 'projects' + pathSep + pName + pathSep + '.udetect/.change.log'
    logging.basicConfig(filename=fName, level=logging.DEBUG, format='%(asctime)s %(message)s')
    # logging.debug('minion')
    # logging.info('banana')
    # logging.warning(potato')
    if white_dir == '*':
        white_dir = None
    else:
        white_dir = white_dir.split(' ')
        print white_dir
    diffCount = 0 
    print "Project Name:\t\t" + pName
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.info'))
    srcDir = config.get(pName,'pathS')
    listFilesOld = []
    print "Path:        \t\t" + srcDir
    lstOrg = eval(config.get('files','listS'))

    for i in lstOrg:
        fileTmp = i[0] + pathSep + i[1][0]
        listFilesOld.append(cleanStr(fileTmp))
        if os.path.exists(fileTmp):
            if (md5Checksum(fileTmp) != i[1][1]):
                if type == "fast":
                    msgTmp = "Lines different in " + i[1][0] + ":"                    
                    logging.warning(msgTmp)
                    msg += msgTmp + "\n"
                    
                elif type == "all":
                    # create a list of lines in text1
                    fileOrg =  fileTmp.replace(srcDir,"projects" + pathSep + pName)
                    text1Lines = open(fileOrg, "r").readlines()

                    # dito for text2
                    text2Lines = open(fileTmp, "r").readlines()
                    diffLst = list(diffC.compare(text1Lines, text2Lines))
                    for line in diffLst:
                        if line[0] == '-':
                            print line
                            logging.warning(line)
                    sys.stdout.writelines(diffLst)
                    logging.warning(diffLst)
                diffCount += 1
        else:
            msgTmp = cleanStr(fileTmp + "\tNot found")
            msg += msgTmp + "\n"
            logging.warning(msgTmp)
            diffCount += 1    
    #find new files
    listFilesNew = getListFiles(srcDir)
    for fileTmp in listFilesNew:
        if fileTmp not in listFilesOld:
            msgTmp = cleanStr(fileTmp + "\t ---- New")
            msg += msgTmp + "\n"
            logging.warning(msgTmp)
            diffCount += 1
    if diffCount < 1:
        return False
    return msg

#
#send mail
#
def sendMail(email, subject, msg=""):
    config = ConfigParser.RawConfigParser()
    config.readfp(open('udetect.conf'))
    mailFrm = config.get('main_config','email')
    smtpServer = config.get('main_config', 'smtp_server')
    smtpPort = config.get('main_config', 'smtp_port')
    smtpPass = config.get('main_config', 'smtp_pass')

    subject = 'Gmail SMTP Test'
    body = 'blah blah blah'
     
    "Sends an e-mail to the specified recipient."
     
    body = "" + msg + ""
     
    headers = ["From: " + mailFrm,
               "Subject: " + subject,
               "To: " + email,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(smtpServer, smtpPort)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(mailFrm, smtpPass)
     
    session.sendmail(mailFrm, email, headers + "\r\n\r\n" + body)
    session.quit()

    return True

#
#start
# 
def start():
    config = ConfigParser.RawConfigParser()
    config.readfp(open('udetect.conf'))
    defaultEmail = config.get('main_config','email_default')
    for pName in config.sections():
        if(pName != 'main_config'):
            #print pName
            if(config.get(pName,'enable') == '1'):
                result = checkProject(pName, config.get(pName, "type"), config.get(pName, "white_dir"), config.get(pName, "white_ext"))
                if result:                    
                    try:
                        print result
                        email = config.get(pName,'email')
                        if email == 'default':
                            email = defaultEmail
                        sendMail(email, '[UDETECT] report for ' + pName, '<pre>' + result + '</pre>')
                        #print result
                        pass
                    except Exception, e:
                        print "Can not send mail!"
                        print "Please check setting, connection, v.v."
                        pass
                else:
                    print "no change"
    print "done"
    return True
