#Purpose:  
# Usage:
# Author: Jun ZHU
# Date:   JUN 3 2021
# Email:  Jun__Zhu@outlook.com


import os
import glob


# data directory
class Dir():
	def __init__(self):
		self.data_dir = os.path.join(os.environ['HOME'], 'Data', 'tlPhasenet')
		self.pick_dir = os.path.join(self.data_dir, 'eqphas')
		self.picklist = glob.glob(os.path.join(self.pick_dir, "*txt*"))
#		self.pick = os.path.join(self.pick_dir, '2014_out_dist400.txt.ok4Li')
		self.xichang = os.path.join(self.data_dir, 'xichang')
		# output dir
		self.output_dir = os.path.join('..', '..', 'output')
		self.waveform_train = os.path.join(self.output_dir, 'waveform_train')
		self.waveform_pred = os.path.join(self.output_dir, 'waveform_pred')
#		self.csvtrain = os.path.join(self.output_dir, 'initialtrain.csv')
#		self.csvtest = os.path.join(self.output_dir, 'test.csv')
		self.csv_eventidlog = os.path.join(self.output_dir, 'eventid_log.csv')
		self.csvtrain = os.path.join(self.output_dir, 'train.csv')
		self.csvivalid = os.path.join(self.output_dir, 'valid.csv')
		self.csvtest = os.path.join(self.output_dir, 'test.csv')
		self.image_dir = os.path.join('..', '..', 'image')
		self.seismogram = os.path.join(self.image_dir, 'seismogram')

class Config():
	def __init__(self):
		self.nptsBeforeP = 3000
		self.nptsAfterP = 6000
		self.TestOnsetInTrain = 2500 # reserve 500 npts before the P- picks
		self.nptsTest = 3000
		self.TestEndInTrain = self.TestOnsetInTrain + self.nptsTest
		self.ChannelWildcards = '*[BS]H?' # to match channel code. like '*BH?', '*SH?', '*[BS]H?'
		self.nptsSlidingRange = 1500
		self.nptsBenchmark = 3000
		self.band = {'freqmin':1, 'freqmax':15}
		self.ratio = {'train':7, 'valid':1, 'test':2}


if __name__ == "__main__":
	Dir = Dir()
	conf = Config()
	print(conf.band['freqmax'])
