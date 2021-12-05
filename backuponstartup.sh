#!/bin/bash

# Add edited file to startup scripts for automatic backups to NFS server over SSH

logFilePath="PATH_TO_LOG_FILE"
internetCheckSite="http://google.com"
sshPort=22
sshUser="SERVER_USERNAME"
sshIP="SERVER_IP_ADRESS"
serverMountDir="DIRECTORY_TO_MOUNT_NFS_IN"
pybackupRunDir="PYBACKUP_RUN_DIRECTORY"

echo "$(date) Start sh backup script" >> $logFilePath

sleep 10
wget -q --spider $internetCheckSite
until [ $? -eq 0 ]
do
    sleep 1m
    wget -q --spider $internetCheckSite
done

sshfs -p $sshPort $sshUser@$sshIP:/ $serverMountDir

cd $pybackupRunDir
echo "$(date) Start py backup script" >> $logFilePath
python3 pybackup.py
echo "$(date) End py backup script" >> $logFilePath

fusermount -u $serverMountDir # Comment line to leave NFS server mounted after backup

echo "$(date) End sh backup script" >> $logFilePath
