for d in run*/
do
cd $d
echo $d
epoch1d < deck.file
cd ..
done