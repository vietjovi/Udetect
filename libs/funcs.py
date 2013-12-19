#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import shutil, errno
import os
import ConfigParser
import hashlib
import difflib
import logging
import logging.handlers
import smtplib
import datetime

LOG_FILENAME = 'udetect.log'
LOG_MAXSIZE = 10*1024 #10 MB

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
        config.set("directories",'listD', getListDirectories(sDir))        
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
        #open('log' + pathSep + LOG_FILENAME , 'a').close()
    except:
        #raise
        delProject(pName)
        return False

    return True

def getListDirectories(pathVar):
    arrTmp = []
    for x in os.walk(pathVar):
        arrTmp.append(x[0])
    return arrTmp

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
            #print cleanStr(path + pathSep + f + " ------ " + md5Checksum(path + pathSep + f))
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
    for x in os.walk(pathVar):
        dirS.append(x[0])
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

def historyProject(pName):
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
    # version = int(config.get(pName,'version'))
    print "source: " + srcDir
    # print "version: " + str(version)
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
#get extension, directory, file name
#
def getExtension(fileName):
    return os.path.splitext(fileName)[1]

def getDirectory(fileName):
    return os.path.split(fileName)[0]

def getFileName(fileName):
    return os.path.split(fileName)[1]

#
#check project
#
def checkProject(pName, type="fast", white_dir = '*', white_ext = '*'):
    msg = ''
    msgTmp = ''
    lstDirsOrg = []
    lstFilesOld = []
    lstFilesOldSum = []
    lstFilesNew = []
    lstFilesNewSum = []
    lstDirsNew = []
    fName = 'log' + pathSep + LOG_FILENAME
    #open('output' + pathSep + pName + '.html', 'w').close()
    logging.basicConfig(filename=fName, level=logging.DEBUG, format='%(asctime)s %(message)s')
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=LOG_MAXSIZE, backupCount=5)
    # logging.debug('minion')
    # logging.info('banana')
    # logging.warning(potato')
    if white_dir == "*":
        white_dir = []
    else:
        white_dir = white_dir.split(' ')     

    if white_ext == "*":
        white_ext = []
    else:
        white_ext = white_ext.split(' ')
    white_ext
    white_dir.append('.udetect')
    diffCount = 0

    print "Project Name:\t\t" + pName
    config = ConfigParser.ConfigParser()
    config.readfp(open('projects' + pathSep + pName + pathSep + '.udetect' + pathSep + '.info'))
    srcDir = config.get(pName,'pathS')

    print "Path:        \t\t" + srcDir
    lstOrg = eval(config.get('files','listS'))
    lstOrgDir = eval(config.get('directories','listD'))

#create list files, dirs org
    for i in lstOrgDir:
        if checkWhiteList(white_dir, white_ext, i):
            lstDirsOrg.append(cleanStr(i + pathSep))

    for i in lstOrg:
        fileTmp = i[0] + pathSep + i[1][0]
        if checkWhiteList(white_dir, white_ext, fileTmp):
            arrTmp = [cleanStr(fileTmp), i[1][1]]
            lstFilesOldSum.append(arrTmp)
            lstFilesOld.append(cleanStr(fileTmp))

#create list files, dirs new
    for path, dirs, files in os.walk(srcDir):
        for f in files:
            if checkWhiteList(white_dir, white_ext, path + pathSep + f):
                lstFilesNew.append(cleanStr(path + pathSep + f))

    for x in os.walk(srcDir):
        if checkWhiteList(white_dir, white_ext, x[0]):
            lstDirsNew.append(cleanStr(x[0] +  pathSep))

#start check
    for x in lstFilesNew:
        if x not in lstFilesOld:
            msgTmp = cleanStr(x + "\t ---- New")
            msg += msgTmp + "\n"
            logging.warning(msgTmp)
            diffCount += 1

    for x in lstFilesOld:
        if x not in lstFilesNew:
            msgTmp = cleanStr(x + "\t ---- Deleted")
            msg += msgTmp + "\n"
            logging.warning(msgTmp)
            diffCount += 1
        else:
            arrTmp = [x, md5Checksum(x)]
            if arrTmp not in lstFilesOldSum: # file modified
                msgTmp = cleanStr(x + "\t ---- Modified")
                msg += msgTmp + "\n"
                logging.warning(msgTmp)
                diffCount += 1
                if type == 'full':
                    try:
                        f = open('output' + pathSep + pName + "_" + str(datetime.date.today()) + '.html', 'a')
                        strTmp = '<hr>'
                        f.write(strTmp)
                        f.write(x)
                        f.write(compareFiles(x.replace(srcDir,"projects" + pathSep + pName), x))
                        f.close()
                    except:
                        print "Can't create file in directory 'output'"
                        pass

    #Check Directories
    for x in lstDirsOrg:
        if x not in lstDirsNew:
            msgTmp = cleanStr(x + "\t ---- Deleted")
            msg += msgTmp + "\n"
            logging.warning(msgTmp)
            diffCount += 1

    for x in lstDirsNew:
        if x not in lstDirsOrg:
            msgTmp = cleanStr(x + "\t ---- New")
            msg += msgTmp + "\n"
            logging.warning(msgTmp)
            diffCount += 1

    if diffCount < 1:
        return False
    updateProject(pName, srcDir)
    return msg

#
#Compare files
#
def compareFiles(f1, f2):
    msg = ''
    text1Lines = open(f1, "r").readlines()
    text2Lines = open(f2, "r").readlines()
    diffLst = list(diffC.compare(text1Lines, text2Lines))
    # for line in diffLst:
    #     if line[0] == '-':
    #         print line
    #sys.stdout.writelines(diffLst)
    # logging.warning(diffLst)
    msg = difflib.HtmlDiff().make_file(text1Lines, text2Lines)
    return msg
#
#update checksum of files
#
def updateProject(pName, sDir):
    config = ConfigParser.RawConfigParser()
    #copy source
    print "Updating..............................."
    shutil.rmtree('projects' + pathSep + pName)
    #exit()
    createProject(pName, sDir)
    # shutil.copytree(sDir,'projects' + pathSep + pName, symlinks=False, ignore=None)
    # #create directory for udetect
    # print "Finishing............................."
    # if not os.path.exists('projects' + pathSep + pName + pathSep + '.udetect'):
    #     os.makedirs('projects' + pathSep + pName + pathSep + '.udetect')
    # #create file config
    # config.add_section(pName)
    # config.add_section("files")
    # config.add_section("directories")        
    # config.set(pName, 'pathS', os.path.abspath(sDir))
    # #config.set(pName, 'version', version)
    # config.set("files", 'listS', walkDir(sDir))
    # config.set("files", 'listP', walkDir('projects' + pathSep + pName))
    # with open('projects'+ pathSep + pName + pathSep + '.udetect'+ pathSep +'.info', 'wb') as configfile:
    #     config.write(configfile)
    return True


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

    subject = subject
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


def checkWhiteList(lstDir, lstExt, fileName):
    #print fileName
    if(os.path.isfile(fileName)):
        if getExtension(fileName) in lstExt:
            return False
    for l in lstDir:
        if l in fileName:
            return False
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
                        #print result
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
