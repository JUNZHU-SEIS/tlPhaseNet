# Purpose: generate input data for PhaseNet 
# Usage:
# Author: Jun ZHU
# Date:   JUN 10 2021
# Email:  Jun__Zhu@outlook.com


import os
from config import Dir
import numpy as np
from obspy import UTCDateTime, read


def GenerateData(Dir):
	with open(Dir.pick, "r") as f:
		data = [x.split() for x in f.readlines()]
		origintime = [(''.join(('-'.join(x[1:4]), 'T', ':'.join(x[4:7])))) for x in
				data if x[0]=="#"]
		row_index = np.array([i for i, x in enumerate(data) if x[0]=="#"])
		row_begin = row_index + 1
		row_end = row_index[1:]; row_end = np.append(row_end, len(data))
		manual_pick = [data[x[0]: x[1]] for x in zip(row_begin, row_end)]
	#-------------make csv file-------------------------------------------
	# UTC time = Beijing -8
	BeijingLAG = 8
	origintimeUTC = [UTCDateTime(x) - BeijingLAG * 3600  for x in origintime]
#	origintimeUTC = [UTCDateTime(x) for x in origintime]
	#-------------make npz file-------------------------------------------
	for i, t in enumerate(origintimeUTC):
		fname = "%d%d%d.%d.%d%d%d.%d"%(t.year, t.month, t.day, t.julday, t.hour,
				t.minute, t.second,	t.microsecond/1000)
		f = os.path.join(Dir.xichang, fname)
		if os.path.exists(f):
			stream = read(os.path.join(f, "*BH*"))
			print(stream)
	return


if __name__ == "__main__":
	Dir = Dir()
	GenerateData(Dir)
