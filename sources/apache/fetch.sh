set -e
D=doap
if [ ! -d $D ]
then
   mkdir -p $D
fi

for prj in `grep location projects.apache.org/data/projects.xml | cut '-d>' -f2 | cut '-d<' -f1 | sort -u`;
do
    #echo $prj
    slug=`echo $prj | \
        sed -e's!https://!!g' | \
        sed -e's!http://!!g' | \
        sed -e's!svn.apache.org/repos/asf/!!g' | \
        sed -e's!/trunk/!!g' | \
        sed -e's!/site/!_!g' | \
        sed -e's!/site_content/!_!g' | \
        sed -e's!doap!!g' |  \
        sed -e's!\.(rdf|git|xml)!!g' |  \
        sed -e's!git-wip-us.apache.org/repos/asf?p=!!g' | \
        sed -e's!.git;a=blob_plain;f=doap_!!g'  | \
        sed -e's!;hb=HEAD!!g' | \
        sed -e's![\s\/=;]!_!g' 
`

    echo $slug
    
    OUT="${D}/${slug}.doap"
    echo $OUT
    if [ $(grep 'Service Temporarily Unavailable' $OUT -c ) -eq 1 ]
    then
        echo "removing $OUT again"
        rm $OUT
    fi
    
    if [ ! -f $OUT ]
    then
        curl --output $OUT  "${prj}"
        sleep 3
    fi     

done
