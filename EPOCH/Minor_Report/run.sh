for d in D*5/
do
cd $d
echo $d
epoch1d < deck.file
cd ..
done

for d in D*2/
do
cd $d
echo $d
epoch1d < deck.file
cd ..
done