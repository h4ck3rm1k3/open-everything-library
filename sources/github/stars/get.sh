#set -x
set -e
page=1
while :
do
    OUT="projects_${page}.html"
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "https://github.com/search?l=&p=${page}&q=stars%3A%3E2&ref=advsearch&type=Repositories&utf8=%E2%9C%93"
        sleep 6
    fi

    if [ $(grep -i 'triggerd abuse' $OUT -c ) -eq 1 ]
    then
        echo "abuse $OUT"
        rm $OUT
        exit
    else
        page=$((page+1))      
    fi
       
done
