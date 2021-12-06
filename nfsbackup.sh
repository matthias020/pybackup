#!/bin/bash

# Add edited file to startup scripts for automatic backups to NFS server over SSH

logFilePath="PATH_TO_LOG_FILE"
internetCheckSite="http://google.com"
sshPort=22
sshUser="SERVER_USERNAME"
sshIP="SERVER_IP_ADRESS"
serverMountDir="DIRECTORY_TO_MOUNT_NFS_IN"
pybackupRunDir="PYBACKUP_RUN_DIRECTORY"

printf "$(date) Start sh backup script\n" >> $logFilePath

sleep 10
wget -q --spider $internetCheckSite
until [ $? -eq 0 ]
do
    sleep 1m
    wget -q --spider $internetCheckSite
done

sshfs -p $sshPort $sshUser@$sshIP:/ $serverMountDir

cd $pybackupRunDir
printf "$(date) Start py backup script\n" >> $logFilePath
python3 pybackup.py
printf "$(date) End py backup script\n" >> $logFilePath

fusermount -u $serverMountDir # Comment line to leave NFS server mounted after backup

printf "$(date) End sh backup script\n\n" >> $logFilePath
