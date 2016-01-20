#grep projects all_projects.txt | cut -d/ -f3 | sort -u > all_projects2.txt
for x in `cat all_projects2.txt`;
do echo $x;
   URL=http://sourceforge.net/rest/p/${x}?doap
   OUT=${x}.doap
   if [ ! -f $OUT ]
    then
        curl --output $OUT  $URL
        #wget --output-file $OUT  "http://sourceforge.net/directory/os%3Alinux/?page=${page}"
        sleep 2
   fi
done
