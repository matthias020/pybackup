import os
import shutil
from time import sleep, time
from filecmp import cmp as compare

toIgnore = []


def pybackup():
    allInRunDir = os.listdir("./")
    if "origin.path" not in allInRunDir:
        firstRun()
        exit()
    
    originPath, destinationPath = importPaths()

    destinationPathWithDate, newBackupStamp = pathDateFormat(destinationPath)
    oldBackupStamp = getOldBackupStamp(destinationPath)
    oldDestinationPathWithDate = destinationPath + "/" + str(oldBackupStamp)

    os.system("clear")

    print("Backing up ...")
    fullBackup(allFiles, originPath, destinationPathWithDate)
    print("Cleaning old latest backup ...")
    cleanOldBackup(oldDestinationPathWithDate, destinationPathWithDate, str(oldBackupStamp), str(newBackupStamp))
    print("Done!")

# pybackup()
def firstRun():
    os.system("clear")

    originPath = input("Path to directory to backup: ")
    destinationPath = input("Path to directory to backup to (will be overwritten when exists): ")
    writePathFiles(originPath, destinationPath)
    destinationPath, newBackupStamp = pathDateFormat(destinationPath)

    os.system("clear")

    print("Backing up for the first time ...")
    fullBackup(allFiles, originPath, destinationPath)
    print("Done!")

# firstRun()
def writePathFiles(originPath, destinationPath):
    originPathFile = open("origin.path", "x")
    originPathFile.write(originPath)
    originPathFile.close()

    destinationPathFile = open("destination.path", "x")
    destinationPathFile.write(destinationPath)
    destinationPathFile.close()

# pybackup(), firstRun()
def pathDateFormat(path):
    date = int(time())
    pathWithDate = path + "/" + str(date)

    return pathWithDate, date

# pybackup(), firstRun()
def fullBackup(fileList, originPath, destinationPath):
    listFiles(originPath, 0)
    copyFiles(fileList, originPath, destinationPath)

# fullBackup(), selectListFilesMode(), cleanOldBackup()
allFiles = []
allFilesOld = []
allFilesNew = []
def listFiles(path, mode):
    allInDir = os.listdir(path)

    n = 0
    for name in allInDir:
        nameWithPath = path + "/" + name
        allInDir[n] = nameWithPath
        
        n = n + 1
    
    filesInDir = []
    foldersInDir = []
    for path in allInDir:
        ignorePath = False
        for ignore in toIgnore:
            if path == ignore:
                ignorePath = True

        if ignorePath == False:
            isFile = os.path.isfile(path)
            if isFile == True:
                filesInDir.append(path)
            else:
                foldersInDir.append(path)
    
    selectListFilesMode(mode, filesInDir, foldersInDir)

# listFiles()
def selectListFilesMode(mode, filesInDir, foldersInDir):
    if mode == 0:
        for file in filesInDir:
            allFiles.append(file)
        for folder in foldersInDir:
            listFiles(folder, 0)

    elif mode == 1:
        for file in filesInDir:
            allFilesOld.append(file)
        for folder in foldersInDir:
            listFiles(folder, 1)

    else:
        for file in filesInDir:
            allFilesNew.append(file)
        for folder in foldersInDir:
            listFiles(folder, 2)

# fullBackup()
def copyFiles(fileList, originPath, destinationPath):
    for originFilePath in fileList:
        destinationFilePath = str.replace(originFilePath, originPath, destinationPath)

        os.makedirs(os.path.dirname(destinationFilePath), exist_ok=True)
        shutil.copyfile(originFilePath, destinationFilePath)

# pybackup()
def importPaths():
    originPathFile = open("./origin.path", "r")
    originPath = originPathFile.readline()
    originPathFile.close()

    destinationPathFile = open("./destination.path", "r")
    destinationPath = destinationPathFile.readline()
    destinationPathFile.close()

    return originPath, destinationPath

# pybackup()
def getOldBackupStamp(path):
    allInDir = os.listdir(path)

    oldBackupStamp = 0
    for folder in allInDir:
        if int(folder) > oldBackupStamp:
            oldBackupStamp = int(folder)

    return oldBackupStamp

# pybackup()
def cleanOldBackup(path, newPath, oldBackupStamp, newBackupStamp):
    listFiles(path, 1)
    listFiles(newPath, 2)
    allFilesOldForCompare, allFilesNewForCompare = makeFilesComparable(allFilesOld, allFilesNew, oldBackupStamp, newBackupStamp)
    
    n = 0
    for partialPath in allFilesOldForCompare:
        if partialPath in allFilesNewForCompare:
            fullPathOld = allFilesOld[n]
            indexNew = allFilesNewForCompare.index(partialPath)
            fullPathNew = allFilesNew[indexNew]
            
            isSame = compare(fullPathOld, fullPathNew)
            if isSame == True:
                os.remove(fullPathOld)

        n = n + 1

# cleanOldBackup()
def makeFilesComparable(allFilesOld, allFilesNew, oldBackupStamp, newBackupStamp):
    allFilesOldForCompare = []
    for file in allFilesOld:
        fileToCompare = file.split(oldBackupStamp + "/", 1)[1]
        allFilesOldForCompare.append(fileToCompare)
    
    allFilesNewForCompare = []
    for file in allFilesNew:
        fileToCompare = file.split(newBackupStamp + "/", 1)[1]
        allFilesNewForCompare.append(fileToCompare)
    
    return allFilesOldForCompare, allFilesNewForCompare


pybackup()