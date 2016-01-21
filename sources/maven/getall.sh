wget  -m -U "Mozilla/5.0 (compatible; Konqueror/3.2; Linux)"   \
      -e robots=off -l4  -r  \
      --no-parent https://repo1.maven.org/maven2/ \
      -A maven-metadata.xml,index.html,pom.xml,.pom
