while :
do 
	echo  parse
	#bash ./parse.sh
        grep directory pages/*  | grep href | grep \/directory | cut '-d"' -f2 |  grep -e'^\/directory' | sed -e's!/$!!g' | sort -u  > cats.txt
	echo get
	bash ./get1.sh
	echo next
done
	
