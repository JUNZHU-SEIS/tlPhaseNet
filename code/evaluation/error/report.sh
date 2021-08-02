# Usage: write a report about the  prediction performance of various models
# Author: Jun ZHU
# Date:   JUL 30 2021
# Email:  Jun__Zhu@outlook.com


DIR=/home/as/Work/tlPhasenet/output
GROUNDTRUTH=$DIR/testlog.csv


INTERVALS=(0 1 2 3 4 5 6 7 8 9 10 15 25 35 45 50) # true positives
OUTPUT=PerformanceReport


echo -e "`tail -n +2 $GROUNDTRUTH | wc -l` test recordings\n" > $OUTPUT


ls error_* > tmp


# for INTERVAL in 0 1 2 3 4 5 6 7 8 9 10 20 30 40 50
for INTERVAL in ${INTERVALS[@]}
	do
		echo -e "\nUse residual <= $INTERVAL sample points as the TP (True Positives)" >> $OUTPUT
		ls error_* | awk -vx=$INTERVAL -vy="'" '{printf "awk %s($1>=-%s && $1<=%s){print}%s %s | wc -l\n", y,x,x,y,$1}' | sh > tmpp
		paste -d "," tmp tmpp >> $OUTPUT
	done


rm tmp*
