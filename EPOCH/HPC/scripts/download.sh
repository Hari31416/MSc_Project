#!/bin/sh

#This script will zip all the sdf files in a given directory, copy(download) it to local given directory and delete the sdf files from the server.

# This is the directory where the sdf files are present on the server.
# REMOTE_DIR = "~/scratch/7run"

# This is the directory where the sdf files will be copied to on the local machine.
# LOCAL_DIR = $( pwd )

#connect to ssh

sshpass -p $HPC_PASSWORD ssh -o StrictHostKeyChecking = no $HPC_USER@$HPC_HOST

#change directory to the directory where the sdf files are present on the server.

cd "~/scratch/7run"

#zip all the sdf files in the directory

zip sdf.zip *sdf

#Save the zip directory to the local directory

ZIP_DIR = $( ls | grep sdf.zip )

#Logout from the server

exit

#Copy the zip file to the local directory

sshpass -p $HPC_PASSWORD scp -o StrictHostKeyChecking = no $HPC_USER@$HPC_HOST : $REMOTE_DIR / $ZIP_DIR .

