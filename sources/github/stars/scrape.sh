#xmllint --xpath "//*/a[starts-with(@href,'/')" --recover --html --noout projects_*.html
#xmllint --xpath "//*/a/@href" --recover --html --noout projects_*.html
xmllint --xpath "//*/a[starts-with(@href,'/')]" --recover --html --noout projects_*.html  2>er|
    sed -e's!</a>!</a>\n!g' |
    grep -v -e '\"/search' -e 'class=' |
    sed -e's!href="/!href="http://github.com/!g' 
