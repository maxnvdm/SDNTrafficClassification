#!/bin/bash


printf "Real-time Classification"
printf "Enter the number of iterations you would like to run or 0 to quit\n"
read run
for ((i=1;i<=run;i++)); do
	sudo bash snortprocess.sh $i
done
