#!/bin/bash
#Program
#	This Program copy the num of bmp
#History
#2015/10/04 Joseph First release
i=0
F=$(echo "$1" | sed 's/\..*$//g')
K=$(echo "$1" | sed 's/^.*\.//g')
if [[ ! -e "$1" ]]; then
	echo "The filename you input is not exist!" && exit 0
	#statements
else
	echo "processing"
	while [ $i -le $2 ]
		do
   		cp -vf "$1" $F$i.$K
   		let i+=1
	done
fi
# echo "$K"
# echo "$F"