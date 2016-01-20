#set -x
set -e
page=1

URL="http://mvnrepository.com/open-source?p="
D=mvnrepository
if [ ! -d $D ]
then
   mkdir -p $D
fi
   
while :
do
    OUT="mvnrepository/projects_${page}.html"
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "${URL}${page}"
        sleep 6
    fi

    page=$((page+1))      

       
done
