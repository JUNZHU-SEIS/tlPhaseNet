# Purpose:  
# Usage:
# Author: Jun ZHU
# Date:   %Month% %Day% 2021
# Email:  Jun__Zhu@outlook.com


import numpy as np
from config import Config, Dir
import os
import pandas as pd
import random
import matplotlib.pyplot as plt


def Plot(wf, pick):
	fig, ax = plt.subplots(3, 1, sharex=True)
	ax[0].plot(wf[:,0], color='gray', lw=0.8)
	ax[0].axvline(x=pick[0], color='blue')
	ax[0].axvline(x=pick[1], color='red')
	ax[1].plot(wf[:,1], color='gray', lw=0.8)
	ax[1].axvline(x=pick[0], color='blue')
	ax[1].axvline(x=pick[1], color='red')
	ax[2].plot(wf[:,2], color='gray', lw=0.8)
	ax[2].axvline(x=pick[0], color='blue')
	ax[2].axvline(x=pick[1], color='red')
	plt.show()
	return


def GenerateBenchmark(Dir, conf):
	if not os.path.exists(Dir.waveform_pred):
		os.mkdir(Dir.waveform_pred)
	data = pd.read_csv(Dir.csv)
	fname, itp, its = [], [], []
	for x,z in zip(data['fname'], data['its']):
#	for x,z in zip(data['fname'][:10], data['its'][:10]):
		if z <= conf.nptsBeforeP:
			# skip the waveform whose S- pick earlier than the P- pick
			continue
		wf = np.load(os.path.join(Dir.waveform_train, x))['data']
		SlidingOnset = random.randint(conf.nptsBeforeP - conf.nptsSlidingRange, conf.nptsBeforeP)
		benchmark_wf = wf[SlidingOnset: SlidingOnset+conf.nptsBenchmark, :]
		new_itp, new_its = conf.nptsBeforeP-SlidingOnset, z-SlidingOnset

#		Plot(benchmark_wf, (new_itp, new_its)
		fname.append(x); itp.append(new_itp); its.append(new_its)
		np.savez(os.path.join(Dir.waveform_pred, x), data=benchmark_wf)
	df_log = pd.DataFrame({'fname': fname, 'itp': itp, 'its': its})
	df_fname = pd.DataFrame({'fname': fname})
	df_log.to_csv(Dir.csvpredictlog, index=False)
	df_fname.to_csv(Dir.csvpredictfname, index=False)
	return


if __name__ == "__main__":
	Dir = Dir(); conf = Config()
	GenerateBenchmark(Dir, conf)
