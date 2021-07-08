# Purpose: generate input data for the file eqphas & xichang/ 
# Usage:
# Author: Jun ZHU
# Date:   JUN 10 2021
# Email:  Jun__Zhu@outlook.com


import os
from config import Dir, Config
import numpy as np
from obspy import UTCDateTime, read, Stream


def FilterPicks(UTCday, eventpick):
	"""extract the direct phases from the event pick, i.e. ['PG', 'SG']"""


	# print(eventpick)
	DesiredPhaseList = ["PG", "SG"]
	phases = [x[3] for x in eventpick if x[3] in DesiredPhaseList]
	arrivals = [x[5] for x in eventpick if x[3] in DesiredPhaseList]
	nameset = ['*'.join((x[0], x[-1][:-1])) + '?'  for x in eventpick
			if x[3] in DesiredPhaseList]
	# print(nameset)
	availablepick = []
	for x in set(nameset):
		idx = np.where(np.array(nameset)==x)[0]
		phaselist = np.array(phases)[idx]
		arrivallist = np.array(arrivals)[idx]
		# check if all desired phases co-exist
		if (DesiredPhaseList[0] in phaselist) and (DesiredPhaseList[1] in phaselist):
			# discard the repeating picks: np.where(...)[...][0]
			PGidx = np.where(phaselist==DesiredPhaseList[0])[0][0]
			SGidx = np.where(phaselist==DesiredPhaseList[1])[0][0]
			phaseidx = np.array([PGidx, SGidx])
			availablepick.append({
				'name':x,
				'PG': UTCDateTime(UTCday+arrivallist[PGidx]),
				'SG': UTCDateTime(UTCday+arrivallist[SGidx])
				})
	return availablepick


def GenerateData(Dir, conf):
	with open(Dir.csv, 'w') as f:
		f.write('fname,itp,its,channels\n')
	for year in Dir.picklist:
		# with open(Dir.pick, "r") as f:
		with open(year, "r") as f:
			data = [x.split() for x in f.readlines()]
			# the origintime (UTC+8, Beijing) of all the picks
			origintime = [(''.join(('-'.join(x[1:4]), 'T', ':'.join(x[4:7]))))
					for	x in data if x[0]=="#"]
			# print(origintime)
			# the line number of each pick
			row_index = np.array([i for i, x in enumerate(data) if x[0]=="#"])
			row_begin = row_index + 1
			row_end = row_index[1:]; row_end = np.append(row_end, len(data))
			# get available picks, origintime[i][:11] denote the date
			FilteredPicks = [FilterPicks(origintime[i][:11], data[x[0]: x[1]])
					for i, x in enumerate(zip(row_begin, row_end))]
			# print(FilteredPicks)
		# UTC+8 Beijing to UTC+0
		LAG = 8
		UTC = [UTCDateTime(x) - LAG * 3600  for x in origintime]

		# discard the empty pick under the given criterion
		available = [i for i,x in enumerate(FilteredPicks) if len(x)>0]
		AvailableOrigintime = [UTC[i] for i in available]
		AvailablePick = [FilteredPicks[i] for i in available]

		if not os.path.exists(Dir.waveform_train):
			os.makedirs(Dir.waveform_train)
		for pick,t in zip(AvailablePick, AvailableOrigintime):
			eventfolder = "%4d%02d%02d.%03d.%02d%02d%02d.%03d"%(
				t.year, t.month, t.day, t.julday,
				t.hour, t.minute, t.second, t.microsecond/1e3)
			fpath = os.path.join(Dir.xichang, eventfolder)
			pickedstation = [x['name'] for x in pick]
			if not os.path.exists(fpath):
				# if the folder is empty, delete it in advance,
				continue
			# match desired channel codes
			st = read(os.path.join(fpath, conf.ChannelWildcards))
			tracestation = [(tr.stats.station + tr.stats.network + "*" +
				tr.stats.channel[:-1] + "?") for tr in st]
			matched_index = [i for i,x in enumerate(pickedstation) if x in tracestation]
			if len(matched_index) == 0:
				# check if there exists matched picked station in the folder
				continue
			event = [{'path':fpath, 'picks':pick[j]} for j in matched_index]
			for rec in event:
				rec_stream = Stream([st[i] for i,x in enumerate(tracestation)
					if x==rec['picks']['name']])
				all_sample_rate = np.array([x.stats.sampling_rate for x in
					rec_stream])
				rate, counts = np.unique(all_sample_rate, return_counts=True)
				if len(rate) > 1:
					continue
				if counts[0] != 3:
					continue
				all_channels = np.array([rec_trace.stats.channel for rec_trace
					in rec_stream])
				channel, counts = np.unique(all_channels, return_counts=True)
#				if np.any(counts > 1):
#					continue
				channels = '_'.join(all_channels)
				commonrate = rate[0]
				# UTC+8 to UTC+0
				pick_p = rec['picks']['PG'] - LAG*3600
				pick_s = rec['picks']['SG'] - LAG*3600
				UTC_p = '%4d%02d%02d%02d%02d%02d'%(pick_p.year, pick_p.month,
						pick_p.day, pick_p.hour, pick_p.minute, pick_p.second)
				maxstart = max([x.stats.starttime for x in rec_stream])
				minend = min([x.stats.endtime for x in rec_stream])
				onset = pick_p - conf.nptsBeforeP / commonrate
				end = pick_p + conf.nptsAfterP / commonrate
				if not ((onset > maxstart) and (end < minend) and
						(onset < pick_s) and (end > pick_s)):
					# check if can be cut on all seismograms & 
					# check if both P- and S- can be involved
					continue
				rec_stream.trim(starttime=onset, endtime=end)
				# transpose the data of 3 cut traces, for reshaping to: (npts, 3)
				npz_data = np.transpose(np.vstack([x.data for x in rec_stream]))
				itp = int((pick_p - rec_stream[0].stats.starttime) * rec_stream[0].stats.sampling_rate)
				its = int((pick_s - rec_stream[0].stats.starttime) * rec_stream[0].stats.sampling_rate)
				fname = '_'.join((rec_stream[0].stats.network, rec_stream[0].stats.station, UTC_p))+'.npz'
				np.savez(os.path.join(Dir.waveform_train, fname), data=npz_data, itp=itp, its=its, channels=channels)
				f = open(Dir.csv, 'a')
				f.write(','.join((fname, str(itp), str(its), channels))+'\n')
				f.close()
	return


if __name__ == "__main__":
	Dir = Dir(); conf = Config()
	GenerateData(Dir, conf)
