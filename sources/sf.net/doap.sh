
if [ ! -d pages ]
then
    mkdir pages
fi

function getpage()
{
    URL=$1
    OUT=$2    
    if [ ! -f $OUT ]
    then
        echo $URL
        curl --output $OUT  $URL
        sleep 2
    fi
    if [ -f $OUT ]
    then
        if [ $(grep 'A 404 Error has Occurred' $OUT -c ) -eq 1 ]
        then
            echo "removing $OUT"            
            rm $OUT
            return 1

            # now lets try the second one
            #getpage $URL2 $OUT2
        else
            return 0
        fi
   else
       echo "failed $OUT"
       return 2
   fi
}

function sfp()
{    
    x=$1    
    URL="http://sourceforge.net/rest/p/${x}?doap"
    x=`echo $1 | sed -e's!/!_!g'`    
    OUT="doap/${x}.doap"
    getpage $URL $OUT
    return $?
    
}

function sf2()
{
    x=$1
    y=$2
    URL="http://sourceforge.net/rest/${x}/${y}?doap"
    OUT="doap/${x}_${y}.doap"
    getpage $URL $OUT
    return $?
}

for x in `cat all_projects2.txt`;
do
    sfp $x
    if [ $? -ne 0 ]
    then
        y=`echo $x | cut -d. -f1`
        z=`echo $x | cut -d. -f2`
        sf2 $z $y
    fi    
done
