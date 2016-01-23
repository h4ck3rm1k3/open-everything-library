#set -x
set -e
page=$1
: ${page:=1}
# max was 67156

while :
do
    OUT="projects_${page}.html"

    if [ ! -f $OUT ]
    then
        if [ $(grep 'A 500 Error has Occurred' $OUT -c ) -eq 1 ]
        then
            echo "removing $OUT"
            rm $OUT
        fi        
    fi       
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "https://www.openhub.net/p?page=${page}&query=&ref=explore_project"
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
