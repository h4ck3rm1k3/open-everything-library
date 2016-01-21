set -e

if [ !  -f projects_urls.txt ]
then
    exit
fi

if [ !  -d details ]
then
   mkdir details
fi

BASE=https://www.openhub.net

for page in `cat projects_urls.txt`
do
    pagename=`echo $page | cut -d/ -f3`
    OUT="details/${pagename}.html"
    URL="${BASE}${page}"
    echo url $URL
    
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
     #exit
     
done
