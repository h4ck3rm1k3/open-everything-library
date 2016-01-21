#set -x
set -e
page=1
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
        curl --output $OUT  "http://projects.eclipse.org/search/projects?page=${page}"
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
