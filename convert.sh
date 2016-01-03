for x in *.org;
do echo $x;
   export y=`echo $x | sed -e's!.org!.md!g'`
   pandoc -i "$x" -o "$y";
done
