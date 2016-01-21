#set -x
set -e
page=1

for page in AC 09 WZ TUV  RS  OQ  MN  KL  GJ  DF
do
    OUT="projects_${page}.html"

    if [ ! -f $OUT ]
    then
        curl --output $OUT  "http://freshcode.club/names/${page}"
        sleep 2
    fi
           
done
