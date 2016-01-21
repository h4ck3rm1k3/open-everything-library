set -x

page=3
API_KEY=c785be35f48770c7b65e39e989fd26cb495e5057396831e8e7bd59e0ab19f254
while :
do
    OUT="projects_${page}.xml"
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "https://www.openhub.net/projects.xml?api_key=$API_KEY&page=${page}"
    fi
    
    page=$((page+1))      
done
