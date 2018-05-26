#!/bin/bash

list_path=/tmp/serverslist.lst

rm -f $list_path

list=`cat ~/.ssh/config | grep "Host " | awk '{print $2}'`
num=1

for line in $list
do
	sn=$num
	echo -ne "$num $line \n" | tee -a $list_path
	num=$(($num + 1))
done

echo -e "\nServer to connect:"
read cs

host=`grep "^$cs" ${list_path} | awk '{print $2}'`
ssh $host
