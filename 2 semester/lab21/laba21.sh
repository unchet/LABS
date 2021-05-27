#!/bin/bash
if [ -n "$1" ]
	then 
	length=$1
	else
	echo "Какая длина должна быть у файлов?"
	read length
fi

read -p "Ваш слуга не посмеет без вашего разрешения изменить имена файлов. Вы дозволяете? (y/n)?" choice

case "$choice" in 
	y|Y ) echo "Ваше желание услышано, Господин. Всё будет сделано в лучшем виде.";;
	* )   echo -e "\nВаш покорный слуга не будет ничего делать с файлами Господина.  (｡╯︵╰｡)"
		  exit;;
esac

cd lab21

FILES=$(find ./ -type f)
for file in $FILES
do
	name=$(basename $file)
	diff=$(($length - ${#name}))
	if (("$diff" <= "0"))
	then
		continue	
	fi
	while (("$diff">"0"))
	do
		name=${name}"^"
		diff=$(($diff-1))
	done
	dir=$(dirname $file)
	mv $file ${dir}/${name}
done

echo -e "\nМиссия выполнена, Господин!  (๑˃ᴗ˂)ﻭ"

