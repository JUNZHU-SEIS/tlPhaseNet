# Purpose:	Read check point 
# Author:	Jun ZHU
# Date:		AUG 23 2021
# Email:	Jun__Zhu@outlook.com


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def train(load=True):
	saver = tf.train.Saver()

	saver.restore(sess, '190703-214543/')


if __name__ == "__main__":
	pass

