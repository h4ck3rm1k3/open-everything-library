
for x in `cat names.txt`;
do echo $x;
   wget https://packages.qa.debian.org/common/RDF.html?srcrdf=$x
done;
