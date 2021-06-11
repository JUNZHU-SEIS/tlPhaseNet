# Purpose:  
# Usage:
# Author: Jun ZHU
# Date:   MAR 9 2021
# Email:  Jun__Zhu@outlook.com


import tensorflow as tf
tf.compat.v1.enable_eager_execution()

with tf.compat.v1.Session() as sess:
    latest_check_point = tf.train.latest_checkpoint('../direct/model/190703-214543/')
