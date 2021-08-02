# Purpose: Divide the data into 'train' 'validation' & 'test' datasets
# Author: Jun ZHU
# Date:   %Month% %Day% 2021
# Email:  Jun__Zhu@outlook.com


import numpy as np
import pandas as pd
from config import Config, Dir


def Divide(
		dircsv,
		ratio={'train':1, 'valid':1, 'test':1}):
	"""divide the data into 'train', 'validation' & 'test'"""


	TVTratio = np.array([ratio['train'], ratio['valid'], ratio['test']])
	df = pd.read_csv(dircsv['log'])
	evid = np.array([x for x in df['evid']])
#	nrec = len(evid)
	UniqID, counts = np.unique(evid, return_counts=True)
#	nevent = len(UniqID)
	divergence = len(evid) * np.cumsum(TVTratio) / np.sum(TVTratio)
	div1 = np.argmin(np.abs(np.cumsum(counts) - divergence[0]))
	div2 = np.argmin(np.abs(np.cumsum(counts) - divergence[1]))
#	print(divergence, div1, div2, UniqID[div1], UniqID[div2])
	trainidx = np.concatenate([np.where(evid==x)[0] for x in UniqID[:div1+1]])
	valididx = np.concatenate([np.where(evid==x)[0] for x in UniqID[div1+1: div2+1]])
	testidx = np.concatenate([np.where(evid==x)[0] for x in UniqID[div2+1:]])
#	print(train, valid, test)
	header = ['fname', 'itp', 'its', 'channels']
	df.iloc[trainidx, [0, 3, 4, 7]].to_csv(dircsv['train'], index=False, header=header)
	df.iloc[valididx, [0, 3, 4, 7]].to_csv(dircsv['valid'], index=False, header=header)
	df.iloc[testidx, [0, 3, 4, 7]].to_csv(dircsv['test'], index=False, header=header)
	print(len(evid), 'recordings in total; ', len(UniqID), 'events in total')
	return


if __name__ == "__main__":
	conf = Config(); Dir = Dir()
	Dir = {'log': Dir.csv_eventidlog, 'train': Dir.csvtrain,
			'valid':Dir.csvivalid, 'test':Dir.csvtest}
	Divide(Dir, conf.ratio)
