
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
