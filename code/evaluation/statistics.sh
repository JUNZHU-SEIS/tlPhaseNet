# Usage: draw the histogram of the prediction performance of the 3 models 
# Author: Jun ZHU
# Date:   MAR 9 2021
# Email:  Jun__Zhu@outlook.com


gmt set MAP_TICK_LENGTH=-5p
# gmt set MAP_GRID_PEN=5p,gray


MAXERROR=52.5
TPERROR=10 # True Positives


DIR=/home/as/Work/tlPhasenet/output
GROUNDTRUTH=$DIR/test.csv
PREDICTION=$DIR/prediction
RAW=$PREDICTION/raw/picks.csv
RAWCOMPARISON=$PREDICTION/raw/result.csv
RETRAIN=$PREDICTION/retrain/picks.csv
RETRAINCOMPARISON=$PREDICTION/retrain/result.csv
PRETRAIN=$PREDICTION/pretrain/picks.csv
PRETRAINCOMPARISON=$PREDICTION/pretrain/result.csv


color_p_raw=#E3541B
color_s_raw=#0A257D
color_p_retrain=#AB7B22
color_s_retrain=#1B8515
color_p_pretrain=#A310A1
color_s_pretrain=#0A8F8D


MAXCOUNT=2700
SHADDOWERROR=10
BIN=2.5
RANGE=-$MAXERROR/$MAXERROR/0/$MAXCOUNT


cat > lines.dat << EOF
-$SHADDOWERROR $((MAXCOUNT-10))
$SHADDOWERROR $((MAXCOUNT-10))
$SHADDOWERROR $SHADDOWERROR
-$SHADDOWERROR $SHADDOWERROR
EOF


Error=../../image/statistics/error
# RawError=../../image/statistics/rawerror
# RetrainError=../../image/statistics/retrain
# PretrainError=../../image/statistics/pretrainerror


echo `head -1 $GROUNDTRUTH`,pre_itp,prob_p,pre_its,prob_s > $RAWCOMPARISON
join -1 1 -2 1 -t, <(sed 1d $GROUNDTRUTH | sort -k 1b,1) <(sed 1d $RAW | sort -k 1b,1) >> $RAWCOMPARISON
echo `head -1 $GROUNDTRUTH`,pre_itp,prob_p,pre_its,prob_s > $RETRAINCOMPARISON
join -1 1 -2 1 -t, <(sed 1d $GROUNDTRUTH | sort -k 1b,1) <(sed 1d $RETRAIN | sort -k 1b,1) >> $RETRAINCOMPARISON
echo `head -1 $GROUNDTRUTH`,pre_itp,prob_p,pre_its,prob_s > $PRETRAINCOMPARISON
join -1 1 -2 1 -t, <(sed 1d $GROUNDTRUTH | sort -k 1b,1) <(sed 1d $PRETRAIN | sort -k 1b,1) >> $PRETRAINCOMPARISON


# echo `cat $RAWCOMPARISON | wc -l` cases in total \(raw\)
# echo `awk -F',' '($5=="[]"){print $2}' $RAWCOMPARISON | wc -l` cases no P- prediction
# echo `awk -F',' '($7=="[]"){print $2}' $RAWCOMPARISON | wc -l` cases no S- prediction
# echo `awk -F',' '($7!="[]" && $5!="[]"){print $2}' $RAWCOMPARISON | wc -l` cases both P- and S- prediction
# 
# echo `cat $RETRAINCOMPARISON | wc -l` cases in total \(retrain\)
# echo `awk -F',' '($5=="[]"){print $2}' $RETRAINCOMPARISON | wc -l` cases no P- prediction
# echo `awk -F',' '($7=="[]"){print $2}' $RETRAINCOMPARISON | wc -l` cases no S- prediction
# echo `awk -F',' '($7!="[]" && $5!="[]"){print $2}' $RETRAINCOMPARISON | wc -l` cases both P- and S- prediction
# 
# echo `cat $PRETRAINCOMPARISON | wc -l` cases in total \(pretrain\)
# echo `awk -F',' '($5=="[]"){print $2}' $PRETRAINCOMPARISON | wc -l` cases no P- prediction
# echo `awk -F',' '($7=="[]"){print $2}' $PRETRAINCOMPARISON | wc -l` cases no S- prediction
# echo `awk -F',' '($7!="[]" && $5!="[]"){print $2}' $PRETRAINCOMPARISON | wc -l` cases both P- and S- prediction


# tail -n +2 $PRETRAINCOMPARISON | awk -F',' '($5!="[]"){print $2, $5}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1, "["$0"]"}}}' x=$TPERROR > pretrainP
# tail -n +2 $RAWCOMPARISON | awk -F',' '($5!="[]"){print $2, $5}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1, "["$0"]"}}}' x=$TPERROR > rawP
# tail -n +2 $RAWCOMPARISON | awk -F',' '($7!="[]"){print $3, $7}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field, $1, "["$0"]"}}}' x=$TPERROR > rawS

# true positive picks
tail -n +2 $RAWCOMPARISON | awk -F',' '($5!="[]"){print $2, $5}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1}}}' x=$MAXERROR > error_p_raw
tail -n +2 $RAWCOMPARISON | awk -F',' '($7!="[]"){print $3, $7}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1}}}' x=$MAXERROR > error_s_raw
tail -n +2 $RETRAINCOMPARISON | awk -F',' '($5!="[]"){print $2, $5}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1}}}' x=$MAXERROR > error_p_retrain
tail -n +2 $RETRAINCOMPARISON | awk -F',' '($7!="[]"){print $3, $7}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1}}}' x=$MAXERROR > error_s_retrain
tail -n +2 $PRETRAINCOMPARISON | awk -F',' '($5!="[]"){print $2, $5}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1}}}' x=$MAXERROR > error_p_pretrain
tail -n +2 $PRETRAINCOMPARISON | awk -F',' '($7!="[]"){print $3, $7}' | sed 's/\[\(.*\)\]/\1/g' | awk '{for (field=2; field<=NF; field++) {if ($field-$1<x && $field-$1>-x){print $field-$1}}}' x=$MAXERROR > error_s_pretrain


# distribution of error
gmt begin $Error png
	gmt subplot begin 1x2 -Fs20c/20c -A
		gmt subplot set 0,0
			gmt basemap -R$RANGE -Bxaf+l"Error"+u" pts" -Byaf+l"Counts" -BWSen+t"Distribution of P Pick Error"+glightgray
			gmt plot lines.dat -Ggray@25 -L
			gmt histogram error_p_retrain -T$BIN -i0 -Z0 -N2 -IO | gmt plot -l"re-train" -W3p,$color_p_retrain
			gmt histogram error_p_raw -T$BIN -i0 -Z0 -N2 -IO | gmt plot -l"raw" -W3p,$color_p_raw
			gmt histogram error_p_pretrain -T$BIN -i0 -Z0 -N2 -IO | gmt plot -l"pre-train" -W3p,$color_p_pretrain
#			gmt histogram error_p_retrain -T$BIN -i0 -Z0 -N2 -IO -R-20/20/0/5000 > distribution_error_p_retrain 
#			gmt histogram error_p_raw -T$BIN -i0 -Z0 -N2 -IO -R-20/20/0/5000 > distribution_error_p_raw 
#			gmt histogram error_p_pretrain -T$BIN -i0 -Z0 -N2 -IO -R-20/20/0/5000 > distribution_error_p_pretrain 
		gmt subplot set 0,1
			gmt basemap -R$RANGE -Bxaf+l"Error"+u" pts" -Byaf -BWSen+t"Distribution of S Pick Error"+glightgray
			gmt plot lines.dat -Ggray@25 -L
			gmt histogram error_s_retrain -T$BIN -i0 -Z0 -N2 -IO | gmt plot -l"re-train" -W3p,$color_s_retrain
			gmt histogram error_s_raw -T$BIN -i0 -Z0 -N2 -IO | gmt plot -l"raw" -W3p,$color_s_raw
			gmt histogram error_s_pretrain -T$BIN -i0 -Z0 -N2 -IO | gmt plot -l"pre-train" -W3p,$color_s_pretrain
#			gmt histogram error_s_retrain -T$BIN -i0 -Z0 -N2 -IO -R-20/20/0/5000 
	gmt subplot end
gmt end show


rm -rf lines.dat
mv error_* error/
