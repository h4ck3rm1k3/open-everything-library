grep -h Package: /var/lib/apt/lists/*_Sources | sort  | cut -d: -f2 | sort -u
