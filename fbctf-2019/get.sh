#/bin/bash

	

# hash="$(go run pow.go $1)"

# echo "${hash}"

curl -s "http://challenges.fbctf.com:8082/report_bugs" -X GET --cookie-jar cookies.txt --cookie cookies.txt > out.txt;

sed '50q;d' out.txt | grep -oE ' [[:alnum:]]{5} ' | head -1 |  sed -e 's/^[[:space:]]*//';


