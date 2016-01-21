#set -x
set -e

URL="https://bitbucket.org/api/2.0/repositories/"
page=1
while :
do
    OUT="projects_${page}.html"

    if [ -z $OUT ]
    then
        rm $OUT
        echo crash $OUT
    fi

    if [ ! -f $OUT ]
    then
        wget -O $OUT  $URL       
        sleep 6
    fi
    
    if [ ! -f $OUT ]
    then
        echo crash $OUT
    fi
    
    if [ -z $OUT ]
    then
        rm $OUT
        echo crash $OUT
    else
        URL=`jq .next $OUT -r`
        echo got next $URL    
        page=$((page+1))
    fi    

done
