for file in $(find .. -type f -name "*.vm")
do
 python3 VMTranslator.py "$file"
done
