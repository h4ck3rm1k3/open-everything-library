
#set -x
set -e

URL="https://rubygems.org/api/v1/gems/"
URL_SUFFIX=".json"

D=ruby
if [ ! -d $D ]
then
   mkdir -p $D
fi


for page in `cut '-d ' -f1  ruby/all.txt`;
do
 #   echo $page;
   
    OUT="ruby/gem_${page}.json"
    
    if [ ! -f $OUT ]
    then
	echo getting $page
        curl --output $OUT  "${URL}${page}${URL_SUFFIX}"
        sleep 2
    fi
    
done

   
