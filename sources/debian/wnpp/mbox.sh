
for x in `cat list.txt`;
do
    if [ ! -f bugs.debian.org/cgi-bin/bugreport.cgi?bug=${x} ]
       then
           wget -m --no-parent --level 1  --reject-regex=debian.org -r "https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=${x}"
           sleep 1
    else
        echo done $x
    fi
done
