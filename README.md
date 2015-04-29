# open-everything-library
Open Everything, for for the library

Processed from impress, saved to HTML.

Converted to markdown.

    for x in *.html; do html2markdown $x > `echo $x |sed -e's/.html/.md/g'`;  done

Edited the markdown.

Install Remark Compiled version :

    wget http://gnab.github.io/remark/downloads/remark-latest.min.js -O remark/remark-latest.min.js

Create the slideshow :

    python remark.py > index.html
