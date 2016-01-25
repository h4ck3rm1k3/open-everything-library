#wget https://sourceforge.net/
#grep directory index.html  | grep href | cut '-d"' -f2 | sort -u > cats.txt

for x in `cat cats.txt `;
do 
   clean=`echo $x | sed -e's![/?=]!_!g'`
   out=pages/$clean.html
   if [ ! -f ${out} ]
   then
       echo going to write to $out
       wget -c https://sourceforge.net${x}  -O ${out}
   fi
done
