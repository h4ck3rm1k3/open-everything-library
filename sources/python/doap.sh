set -e

if [ !  -f projects.txt ]
then
    cut "-d\"" -f2  pypi.python.org/pypi/doaps.txt | sed -e 's!\&amp\;!\&!g'  | cut "-d&" -f1-2  | sort -u > projects.txt
fi

BASE=https://pypi.python.org

for page in `cat projects.txt`
do

    pagename=`echo $page | cut -d= -f3`
    OUT="doaps/doap_${pagename}.rdf"
    URL="${BASE}${page}"
    echo url $URL
    #exit
    if [ -f $OUT ]
    then
        echo check $OUT
        
        if [ $(grep 'A 500 Error has Occurred' $OUT -c ) -eq 1 ]
        then
            echo "removing $OUT"
            rm $OUT
            #exit
        fi
        
        if [ ! -s $OUT ]
         then
             rm $OUT
             echo crash $OUT
             #exit
         fi

    fi       
    # if [ $(grep "Oh snap! We can\'t process this request." $OUT -c ) -eq 1 ]
    # then
    #     echo "removing $OUT"
    #     rm $OUT
    # fi
    # gi
    
     if [ ! -f $OUT ]
     then
         echo get $OUT
         #exit
         curl --output $OUT  "$URL"
         sleep 2  
     fi

     if [ ! -s $OUT ]
     then
         rm $OUT
         echo crashd2 $OUT
         exit
     fi
  
    
    # if [ $(grep 'A 500 Error has Occurred' $OUT -c ) -eq 1 ]
    # then
    #     echo "removing $OUT again"
    #     rm $OUT
    # else
    #     page=$((page+1))      
    # fi

     
done
