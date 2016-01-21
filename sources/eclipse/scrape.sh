
xmllint --xpath '//*[@class="collapse-header-website"]/a' --recover --html --noout projects_*.html 2> err.txt  |
    sed -e's!</a>!</a>\n!g' |
    sed -e's!href="projects!href="http://projects.eclipse.org/projects!g' 



#
#bash scrape.sh  
# @href
