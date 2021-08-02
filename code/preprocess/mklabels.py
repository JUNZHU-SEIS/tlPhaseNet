# Purpose: generate input data for the file eqphas & xichang/ 
# Author: Jun ZHU
# Date:   JUN 10 2021
# Email:  Jun__Zhu@outlook.com


import os
from config import Dir, Config
import numpy as np
from obspy import UTCDateTime, read, Stream
import matplotlib.pyplot as plt


def FilterPicks(UTCday, eventpick):
	"""Extract the direct phases from the event pick, i.e. ['PG', 'SG']
		Note: there are some event outputs no picks under the given criteria
	"""


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


def RoutineSeismicProcess(stream, band={'freqmin':1, 'freqmax':15}):
	"""routine process of the seismic data"""


	stream.detrend()
	stream.taper(max_percentage=0.05)
	stream.filter('bandpass', freqmin=band['freqmin'], freqmax=band['freqmax'], zerophase=True, corners=2)
	return


def Plot(data, itp, its, fname, folder, dpi=600):
	"""plot the 3-c waveform data with the P- and S- picks"""


	wf = np.transpose(data)
	fig, ax = plt.subplots(3,1, sharex=True)

	ax[0].plot(wf[0], color='k', lw=0.5, label='E')
	ax[0].axvline(x=itp, color='b', lw=0.4)
	ax[0].axvline(x=its, color='r', lw=0.4)
	ax[0].legend(loc='upper right')

	ax[1].plot(wf[1], color='k', lw=0.5, label='N')
	ax[1].axvline(x=itp, color='b', lw=0.4)
	ax[1].axvline(x=its, color='r', lw=0.4)
	ax[1].legend(loc='upper right')

	ax[2].plot(wf[2], color='k', lw=0.5, label='Z')
	ax[2].axvline(x=itp, color='b', lw=0.4)
	ax[2].axvline(x=its, color='r', lw=0.4)
	ax[2].legend(loc='upper right')

	xticks = ax[2].set_xticks([itp, its])
	ax[2].set_xticklabels([str(itp), str(its)], Rotation=90)

	ax[0].set_title(fname)

	plt.savefig(os.path.join(folder, fname+'.png'), dpi=dpi)
	plt.show()
	return


def GenerateData(Dir, conf):
	if not os.path.exists(Dir.waveform_train):
		os.makedirs(Dir.waveform_train)
	if not os.path.exists(Dir.waveform_pred):
		os.makedirs(Dir.waveform_pred)

	HeaderText = 'fname,itp,its,channels\n'
	with open(Dir.csvtrain, 'w') as f:
		f.write(HeaderText)
	with open(Dir.csvtest, 'w') as f:
		f.write(HeaderText)
	HeaderEventIdLog = 'fname,UTC_p,fpath,itp_train,its_train,itp_test,its_test,channels,evid\n'
	with open(Dir.csv_eventidlog, 'w') as f:
		f.write(HeaderEventIdLog)
	evid = 0
	for year in Dir.picklist:
		# with open(Dir.pick, "r") as f:
		with open(year, "r") as f:
			data = [x.split() for x in f.readlines()]
			# the origintime (in UTC+8) of all the picks
			origintime = [(''.join(('-'.join(x[1:4]), 'T', ':'.join(x[4:7]))))
					for	x in data if x[0]=="#"]
			# the line index of each pick in the phase list file
			row_index = np.array([i for i, x in enumerate(data) if x[0]=="#"])
			row_begin = row_index + 1
			row_end = row_index[1:]; row_end = np.append(row_end, len(data))
			# origintime[i][:11] denote the date, like yyyy-mm-dd
			FilteredPicks = [FilterPicks(origintime[i][:11], data[x[0]: x[1]])
					for i, x in enumerate(zip(row_begin, row_end))]
			# print(FilteredPicks)
		# UTC+8 to UTC+0
		LAG = 8
		UTC = [UTCDateTime(x) - LAG*3600  for x in origintime]

		# discard the empty pick
		available = [i for i,x in enumerate(FilteredPicks) if len(x)>0]
		AvailableOrigintime = [UTC[i] for i in available]
		AvailablePick = [FilteredPicks[i] for i in available]

		for pick,t in zip(AvailablePick, AvailableOrigintime):
			eventfolder = "%4d%02d%02d.%03d.%02d%02d%02d.%03d"%(
				t.year, t.month, t.day, t.julday,
				t.hour, t.minute, t.second, t.microsecond/1e3)
			fpath = os.path.join(Dir.xichang, eventfolder)
			pickedstation = [x['name'] for x in pick]
			if not os.path.exists(fpath):
				# if the folder is empty, please delete it in advance,
				continue

			# match the desired channel code
			st = read(os.path.join(fpath, conf.ChannelWildcards))
			tracestation = [(tr.stats.station + tr.stats.network + "*" +
				tr.stats.channel[:-1] + "?") for tr in st] # store trace names
			matched_index = [i for i,x in enumerate(pickedstation) if x in tracestation]
			if len(matched_index) == 0:
				# if no matched trace is found, just skip
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
#				print(pick_p, pick_s) # pick of P- and S- wave in UTC
				UTC_p = '%4d%02d%02d%02d%02d%02d'%(pick_p.year, pick_p.month,
						pick_p.day, pick_p.hour, pick_p.minute, pick_p.second)
				maxstart = max([x.stats.starttime for x in rec_stream])
				minend = min([x.stats.endtime for x in rec_stream])
				# skip the recording which DOES NOT involve the training picks
				train_onset = pick_p - conf.nptsBeforeP / commonrate
				train_end = pick_p + conf.nptsAfterP / commonrate
				# skip the recording which DOES NOT involve the test picks
				test_end = train_onset + conf.TestEndInTrain / commonrate
				if not ((train_onset > maxstart) and (train_end < minend) and
						(train_onset < pick_s) and (train_end > pick_s)	and
						(test_end > pick_s)):
					# check if can be cut on all seismograms
					# check if both P- and S- picks are involved in both 'train' & 'test' dataset
					continue
#				rec_stream.plot()
				RoutineSeismicProcess(rec_stream, conf.band)
				rec_stream.trim(starttime=train_onset, endtime=train_end)
#				rec_stream.plot()

				# transpose the data of 3 cut traces, for reshaping to: (npts, 3)
				# store the train dataset
				npz_train = np.transpose(np.vstack([x.data for x in rec_stream]))
				itp_train = int((pick_p - rec_stream[0].stats.starttime) * rec_stream[0].stats.sampling_rate)
				its_train = int((pick_s - rec_stream[0].stats.starttime) * rec_stream[0].stats.sampling_rate)
				fname = '_'.join((rec_stream[0].stats.network, rec_stream[0].stats.station, UTC_p))+'.npz'
#				Plot(npz_train, itp_train, its_train, fname, Dir.seismogram, dpi=600)
				np.savez(os.path.join(Dir.waveform_train, fname),
						data=npz_train, itp=itp_train, its=its_train, channels=channels)
#				f = open(Dir.csvtrain, 'a')
#				f.write(','.join((fname, str(itp_train), str(its_train), channels))+'\n')
#				f.close()

				npz_test = npz_train[conf.TestOnsetInTrain:conf.TestEndInTrain, :]
				itp_test = itp_train - conf.TestOnsetInTrain
				its_test = its_train - conf.TestOnsetInTrain
#				Plot(npz_test, itp_test, its_test, fname, Dir.seismogram, dpi=600)
				np.savez(os.path.join(Dir.waveform_pred, fname),
						data=npz_test, itp=itp_test, its=its_test, channels=channels)
#				f = open(Dir.csvtest, 'a')
#				f.write(','.join((fname, str(itp_test), str(its_test), channels))+'\n')
#				f.close()

				# log the sample waveform
				f = open(Dir.csv_eventidlog, 'a')
				f.write(','.join((fname, UTC_p, fpath, str(itp_train),
					str(its_train), str(itp_test), str(its_test),
					channels, str(evid)))+'\n')
				f.close()
			evid += 1
	return


if __name__ == "__main__":
	Dir = Dir(); conf = Config()
	GenerateData(Dir, conf)
