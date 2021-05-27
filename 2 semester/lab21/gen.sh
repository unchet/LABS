#!/bin/bash
echo "Сколько файлов сгенерировать?"
read quality 
cd lab21
while (("$quality">"0"))
do
	temp=$(</dev/urandom tr -dc A-Z-a-z-0-9 | head -c ${1:-$((2 + RANDOM % 10))})
	touch ${temp}
	quality=$(($quality-1))
done
