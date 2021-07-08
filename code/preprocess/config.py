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
		self.pick = os.path.join(self.pick_dir, '2014_out_dist400.txt.ok4Li')
		self.xichang = os.path.join(self.data_dir, 'xichang')
		# output dir
		self.output_dir = os.path.join('..', '..', 'output')
		self.waveform_train = os.path.join(self.output_dir, 'waveform_train')
		self.csv = os.path.join(self.output_dir, 'waveform.csv')

class Config():
	def __init__(self):
		self.nptsBeforeP = 3000 # unit: sec
		self.nptsAfterP = 6000
		self.ChannelWildcards = '*[BS]H?' # '*BH?', '*SH?', '*[BS]H?'


if __name__ == "__main__":
	Dir = Dir()
