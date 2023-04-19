import os

# This script will zip all the sdf files in a given directory, copy(download) it to local given directory and delete the sdf files from the server.

# This script will be run on local machine.

HOST = "hpc.iitd.ac.in"
USER = "username"
PASSWORD = "password"

# This is the directory where the sdf files are present on the server.
REMOTE_DIR = "~/scratch/7run"

# This is the directory where the sdf files will be downloaded on the local machine.
LOCAL_DIR = os.path.join(os.getcwd(), "data")
