# Purpose: transfer learning application to PhaseNet model, developed by W. Zhu
# Author: Jun ZHU
# Date:   JUL 16 2021
# Email:  Jun__Zhu@outlook.com


import numpy as np
import obspy
from obspy import read
import matplotlib.pyplot as plt
from model import Model
from data_reader import Config, DataReader, DataReader_test, DataReader_pred, DataReader_mseed
from run import read_args, set_config
import tensorflow as tf


def TransferLearning(model):
	print(model.logits)


	return


if __name__ == "__main__":
	args = read_args()
#	print(data_reader)
	coord = tf.train.Coordinator()
	data_reader = DataReader_pred(
		data_dir=args.data_dir,
		data_list='./dataset/train.csv', # temporary
		queue_size=args.batch_size*10,
		coord=coord,
		input_length=args.input_length)
	config = set_config(args, data_reader)
	print(config.pool_size, '\n\n\n\n-----------\n\n\n')
	model = Model(config)
	TransferLearning(model)
