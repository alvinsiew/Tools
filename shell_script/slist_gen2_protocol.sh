#!/bin/bash
#
# Version	Author		Remarks
# 1.1		Alvin		Make script more robust to wrong entries
# 2.0		Alvin		Revamp script to be able to do filtering
###################################################################################################

clear

list_path=/tmp/serverslist.lst

list=`cat ~/.ssh/config | grep "Host " | awk '{print $2}'`


filter() {
	rm -f $ft_list_path
	printf "\n\n\e[3;4;36mEnter filter:\n\e[0m"
	read ft
	clear
	colour=34
		
	cat $list_path | grep "${ft}" | while read line
        do
                printf -- "\033[${colour}m %s %s \033[0m\n" "$line"
                if [ $colour -eq 34 ]; then
                        colour=$((colour + 1))
                elif [ $colour -eq 35 ]; then
                        colour=$((colour - 1))
                fi
        done

	echo -e "\n<Hit \"Enter\" to filter>"
	printf "\e[3;4;33mServer to connect:\n\e[0m"
	read cs

        if [[ -z $cs ]]; then
		top
                filter
        fi

        if [[ $cs == *[a-zA-Z]* ]]; then
		clear
                echo "Not a number"
                main
        fi

        num=$(($num - 1))

        if [ $cs -gt $num ]; then
		clear
                echo "Number of out of range"
                main
        fi
	host=`grep "^$cs " ${list_path} | awk '{print $2}'`
	ssh $host
	exit
}

top() {
	clear
	rm -f $list_path
	num=1
	colour=34
	for line in $list
	do
		echo -ne "$num $line \n" >>  $list_path
		printf -- "\033[${colour}m %s %s \033[0m\n" "$num"")""$line"
		num=$(($num + 1))
        	if [ $colour -eq 34 ]; then
			colour=$((colour + 1))
		elif [ $colour -eq 35 ]; then
			colour=$((colour - 1))
		fi
	done
}

main() {
	top
	echo -e "\n<Hit \"Enter\" to filter>"
	printf "\e[3;4;33mServer to connect:\n\e[0m"
	read cs

        if [[ -z $cs ]]; then
		top
                filter
        fi

        if [[ $cs == *[a-zA-Z]* ]]; then
		clear
                echo "Not a number"
                main
        fi

        num=$(($num - 1))

        if [ $cs -gt $num ]; then
		clear
                echo "Number of out of range"
                main
        fi

	host=`grep "^$cs " ${list_path} | awk '{print $2}'`
	ssh $host
	exit
}

main
