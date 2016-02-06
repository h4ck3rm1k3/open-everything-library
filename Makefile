create_item:
	python3 create_request.py 'https://www.wikidata.org/w/api.php?maxlag=5&format=json&bot=1&summary=Bot%3A+New+item+with+sitelink+from+%5B%5Bwikipedia%3Aen%3AThe+Audience+Engine%5D%5D&assert=user&action=wbeditentity&new=item&data=%7B%22labels%22%3A+%7B%22en%22%3A+%7B%22value%22%3A+%22The+Audience+Engine%22%2C+%22language%22%3A+%22en%22%7D%7D%2C+%22sitelinks%22%3A+%7B%22enwiki%22%3A+%7B%22site%22%3A+%22enwiki%22%2C+%22title%22%3A+%22The+Audience+Engine%22%7D%7D%7D&token=25e4d8bd369df40f89963679e983758a56b48fbd%2B%5C'

testwd2 :
	python3 load_cat_pages_into_wikidata.py
testwd :
	python3 create_request.py 'https://www.wikidata.org/w/api.php?action=wbcreateclaim&entity={{{2}}}&property=P31&snaktype=value&value=Q4167836'


import_git:
#	max id:	repositories.50342805.json
	./import_gh2.py

test123:
	python openhub_extract.py

parse:
	chmod +x extract_html.py
	./extract_html.py sources/data2/python/pypi.python.org/example2.html

wnpp:
	chmod +x ./wnpp.py
	./wnpp.py

links3:
	chmod +x ./Opencontent_netloc.py
	./Opencontent_netloc.py

links2:
	./Opencontent_retry.py

links:
	./Opencontent_links.py

Opencontent:
	python3 Opencontent.py

process_mongo:
	python process_pages_mongo.py

merge_mongo:
	python merge_mongo.py

transfermongo:
	python transfermg.py allcats.txt

cats4:
	python cats.py allcats.txt

cats3:
	python cats.py opencat2.txt

cats2:
	python process_cats.py

cats:
	python cats.py opencat.txt

test3:
	python search_terms.py open_source_list.txt
	#todo.txt

test2:
	python search.py

test:
	python parse.py

*.md : *.org
	pandoc -i %< -o %>

cats5:
	python cats.py opencat4.txt
