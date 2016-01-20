set -x

page=1
#API_KEY=c785be35f48770c7b65e39e989fd26cb495e5057396831e8e7bd59e0ab19f254
while :
do
    OUT="projects_${page}.html"
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "http://sourceforge.net/directory/os%3Alinux/?page=${page}"
    fi
    
    page=$((page+1))      
done
