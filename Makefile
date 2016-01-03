*.md : *.org
	pandoc -i %< -o %>
