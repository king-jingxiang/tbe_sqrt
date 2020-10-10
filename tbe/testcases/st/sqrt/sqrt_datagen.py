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

import numpy as np
import sys
from dataFormat import *


def sqrt(name, shape, src_type):
    sys.stdout.write("Info: writing input for %s...\n" % name)
    """
    TODO:
    write codes for generating data.
    """
    input_shape = shape

    shape_str = ""
    for dim in shape:
        shape_str += str(dim) + "_"
    feature_name = shape_str + src_type

    inputArr = np.random.uniform(0, 10, input_shape).astype(src_type)
    dumpData(inputArr, name + "_input_" + feature_name + ".data",
             fmt="binary", data_type=src_type,
             path="../data/" + name + "/" + feature_name)
    sys.stdout.write("Info: writing input for %s done!!!\n" % name)

    if src_type == "float16":
        inputArr = inputArr.astype(np.float32)

    compute_input = inputArr
    outputArr = np.sqrt(compute_input).astype(src_type)

    if src_type == "float16":
        outputArr = outputArr.astype(np.float16)

    dumpData(outputArr, name + "_output_" + feature_name + ".data",
             fmt="binary", data_type=src_type,
             path="../data/" + name + "/" + feature_name)
    sys.stdout.write("Info: writing output for %s done!!!\n" % name)


def gen_sqrt_data(isBBIT=False):
    sqrt("sqrt", (100,100), "float16")


if __name__ == "__main__":
    gen_sqrt_data()
