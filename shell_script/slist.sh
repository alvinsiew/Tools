#!/bin/bash

list_path=/tmp/serverslist.lst

rm -f $list_path

list=`cat ~/.ssh/config | grep "Host " | awk '{print $2}'`
num=1

colour=34
for line in $list
do
	sn=$num
	echo -ne "$num $line \n" >>  $list_path
	printf -- "\033[${colour}m %s %s \033[0m\n" "$num" "$line"
	num=$(($num + 1))
        if [ $colour -eq 34 ]; then
		colour=$((colour + 1))
	elif [ $colour -eq 35 ]; then
		colour=$((colour - 1))
	fi
done

echo -e "\nServer to connect:"
read cs

host=`grep "^$cs" ${list_path} | awk '{print $2}'`
ssh $host
