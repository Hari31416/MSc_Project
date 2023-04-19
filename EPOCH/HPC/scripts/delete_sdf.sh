#!/bin/sh
for d in */;do
cd $d
echo "Deleting sdf files from $d"
rm *sdf
cd ..
echo 
done