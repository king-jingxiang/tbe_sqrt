/* Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the Apache License Version 2.0.You may not use
 * this file except in compliance with the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * Apache License for more details at
 * http://www.apache.org/licenses/LICENSE-2.0
 */

#include "gtest/gtest.h"
#include "one_in_one_out_layer.hpp"

class SQRT_ST : public testing::Test {
protected:
    static void SetUpTestCase() {
        std::cout << "SQRT_ST ST SetUp" << std::endl;
    }
    static void TearDownTestCase() {
        std::cout << "SQRT_ST ST TearDown" << std::endl;
    }
    virtual void SetUp() {}
    virtual void TearDown() {}
};
TEST_F(SQRT_ST, test_sqrt_100_100_float16) {
    std::string op_name = "sqrt";
    std::string inputSizeStr = "100_100_float16";
    uint32_t inputSize = 100*100;
    uint32_t outputSize = 100*100;

    std::string stubFunc =  "cce_sqrt_100_100_float16__kernel0";

    std::string bin_path = "./llt/ops/common/kernel_bin/sqrt/cce_sqrt_100_100_float16.o";

    std::string tilingName = "cce_sqrt_100_100_float16__kernel0";

    std::string inputArrAPath = "./llt/ops/common/data/sqrt/100_100_float16/sqrt_input_100_100_float16.data";

    std::string expectOutputDataPath = "./llt/ops/common/data/sqrt/100_100_float16/sqrt_output_100_100_float16.data";
    float ratios[2] = {0.005, 0.005};

    OneInOneOutLayer<fp16_t,fp16_t> layer{
        op_name,
        inputSizeStr,
        inputSize,
        outputSize,
        bin_path,
        tilingName,
        inputArrAPath,
        expectOutputDataPath,
        ratios,
        (void*)stubFunc.c_str()
    };

    bool ret = layer.test();

    if(!ret)
    {
        layer.writeBinaryFile((void*)layer.outputData,
        "./llt/ops/common/data/sqrt_aicore/100_100_float16/actual_sqrt_aicore_output_100_100_float16.data",
        outputSize * sizeof(fp16_t));
    }

    assert(true == ret);
}