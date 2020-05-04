#!/bin/bash

echo "Total requests: `grep -c "\- \-" $1`" > ./results_bash.txt

cat $1 | awk '{ arr[$6]++} END { for( no in arr) { print no ,"is repeated", arr[no],"times" } }' | cut -c 2- >>./results_bash.txt

echo "Top-10 requests on size:" >> results_bash.txt
cat $1 | awk '{print "url:", $7,"status_code:", $9, "size:", $10}' |sort -nrk6 | head >>./results_bash.txt

echo  "Top-10 client errors on frequency: " >>./results_bash.txt
grep "HTTP/1.1\" 4" $1 | awk '{ arr["url:" $7 " status_code:" $9]++} END { for( no in arr) { print no ,"is repeated", arr[no],"times;\n" } }' | sort -nrk5 | head  >>results_bash.txt

echo  "Top-10 client errors on size: " >>./results_bash.txt
grep "HTTP/1.1\" 4" $1 | awk '{print "ip:", $1, "url:", $7, "status_code:", $9, "size:", $10}' | sort -nrk8 | head >>./results_bash.txt
