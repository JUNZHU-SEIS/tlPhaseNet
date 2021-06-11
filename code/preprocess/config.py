#Purpose:  
# Usage:
# Author: Jun ZHU
# Date:   JUN 3 2021
# Email:  Jun__Zhu@outlook.com


import os
# data directory
class Dir():
	def __init__(self):
		self.data_dir = os.path.join(os.environ['HOME'], 'Data', 'tlPhasenet')
		self.pick_dir = os.path.join(self.data_dir, 'eqphas')
		self.pick = os.path.join(self.pick_dir, '2014_out_dist400.txt.ok4Li')
		self.xichang = os.path.join(self.data_dir, 'xichang')
		# print(pick)
		# output dir
		self.output_dir = os.path.join('..', '..', 'output')
		self.csv = "waveform.csv"
