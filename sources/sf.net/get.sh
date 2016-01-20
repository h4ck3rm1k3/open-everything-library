#set -x
set -e
page=$1
: ${page:=1}

#API_KEY=c785be35f48770c7b65e39e989fd26cb495e5057396831e8e7bd59e0ab19f254
while :
do
    OUT="projects_${page}.html"

    if [ -f $OUT ]
    then
        if [ $(grep 'A 500 Error has Occurred' $OUT -c ) -eq 1 ]
        then
            echo "removing $OUT"
            rm $OUT
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
        curl --output $OUT  "http://sourceforge.net/directory/os%3Alinux/?page=${page}"
        #wget --output-file $OUT  "http://sourceforge.net/directory/os%3Alinux/?page=${page}"
        sleep 2
    fi
    
    if [ $(grep 'A 500 Error has Occurred' $OUT -c ) -eq 1 ]
    then
        echo "removing $OUT again"
        rm $OUT
    else
        page=$((page+1))      
    fi
       
done
