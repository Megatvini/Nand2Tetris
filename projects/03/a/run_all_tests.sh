for directory in ${path}*.tst
do
    if [ -f "$directory" ] ; then  #test to see if it is a file and then executes the following commands.
		echo "$directory"
	    /mnt/c/Users/dogho/Desktop/Nand2Tetris/tools/HardwareSimulator.sh "$directory"
    fi
done