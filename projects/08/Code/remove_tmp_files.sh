for file in $(find .. -type f -name "*.asm")
do
 echo "$file"
done

for file in $(find .. -type f -name "*.asm")
do
 rm "$file"
done

for file in $(find .. -type f -name "*.out")
do
 rm "$file"
done
