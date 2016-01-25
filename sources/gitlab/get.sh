set -x

page=$1
while :
do
    OUT="projects_${page}.html"
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT "https://gitlab.com/explore/projects?group=&page=${page}&scope=&sort=updated_desc&tag=&visibility_level="
    fi
    
    page=$((page+1))
done
