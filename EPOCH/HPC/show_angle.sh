for dir in ./*/;
do
echo $dir
cat "$dir/input.deck" | grep -i "lambda = ";
cat "$dir/input.deck" | grep -i "upper_theta = ";
echo
echo
# echo $dir
done