xmllint --xpath "//*/a[starts-with(@href,'/projects') and @itemprop='url']" --recover --html --noout projects_*.html 2>err |
    sed -e's!</a>!</a>\n!g' | sort -u > all_projects.txt

