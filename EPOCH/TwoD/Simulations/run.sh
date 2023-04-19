#!/bin/sh
echo "===================================================="
echo "Current Directory: $(pwd)"
echo 
echo 
for directory in $directories; do
echo "----------------------------------------------------"
echo "Going to directory $directory"
echo "----------------------------------------------------"
echo
echo
cd $directory
time pwd | mpirun -np $PBS_NTASKS epoch2d
echo
cd ..
done
echo "Task Done. Enjoy!"
echo "===================================================="
