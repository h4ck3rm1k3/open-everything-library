
#set -x
set -e
page=1

URL="http://go-search.org/search?q=&p="

D=golang
if [ ! -d $D ]
then
   mkdir -p $D
fi


while :
do
   
    OUT="${D}/index_${page}.html"

    if [ $(grep 'Service Temporarily Unavailable' $OUT -c ) -eq 1 ]
    then
        echo "removing $OUT again"
        rm $OUT
    fi

        
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "${URL}${page}"
        sleep 3
    fi

    
    
    page=$((page+1))
    
done

   
