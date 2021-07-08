# Usage:  
# Author: Jun ZHU
# Date:   MAR 9 2021
# Email:  Jun__Zhu@outlook.com


DISTRICT_ANNOTATION=util/map_district_annotation 
STUDY_AREA=99/105/25/33
PROJECT_CENTER=102/29
SCALE_POSITION=99.7/25.3

color_land=244/243/239
color_lake=167/194/223

gmt begin CN-border-JM png
	gmt set MAP_GRID_PEN_PRIMARY 0.25p,gray,2_2
	# 绘制中国地图
	gmt coast -JM$PROJECT_CENTER/10c -R$STUDY_AREA -Ba1f1 -G$color_land -S$color_lake -BWSen
	gmt basemap -Lg$SCALE_POSITION+c17.5+w100k+f+u --FONT_ANNOT_PRIMARY=6p
	gmt plot CN-border-La.gmt -W0.1p
#	gmt grdimage @earth_relief_01m
	gmt text -F+f10p,1,black $DISTRICT_ANNOTATION 
gmt end show
