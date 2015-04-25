echo ""
echo "# Table of Contents"
echo ""
files=`ls [0-9a-z]*.py | grep -v "ok.py"`
for f in $files; do
   awk ' gsub(/^# /,"") {
         name=$0
	 file=FILENAME
         gsub(/.py$/,".md",file)
         print "+ ["$0"](__PRE/doc/"file")"; 
         exit}' $f
done
echo ""   
