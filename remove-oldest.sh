#!/usr/bin/env bash

max=$1
dir=$2

echo "Removing all but $max most recent files in $dir"

cd $dir
while :
do
	count=`ls | wc -l`
	if [ $count -lt $max ]; then
		echo "Less than $max files, exiting."
		exit
	fi
	oldest=`ls -tr | head -n1`
	echo "There are $count files. Deleting the oldest $oldest"
	rm -rf $oldest
done
