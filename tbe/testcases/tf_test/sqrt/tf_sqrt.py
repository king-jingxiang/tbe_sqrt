"""
Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the Apache License Version 2.0.You may not use this file
except in compliance with the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Apache License for more details at
http://www.apache.org/licenses/LICENSE-2.0

"""

import tensorflow as tf
import numpy as np
import os

from npu_bridge.estimator import npu_ops

tf.flags.DEFINE_string("local_log_dir", "output/train_logs.txt", "Log file path")
FLAGS = tf.flags.FLAGS

atol = 0.001
rtol = 0.001


def main(unused_argv):
    pass


if __name__ == "__main__":
    tf.app.run()
