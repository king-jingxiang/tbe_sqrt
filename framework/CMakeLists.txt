#
# Copyright (c) Huawei Technologies Co., Ltd. 2020. All rights reserved.
#

# add operator subdirectory
if(IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/caffe_plugin")
    add_subdirectory(caffe_plugin)
endif()
if(IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/tf_plugin")
    add_subdirectory(tf_plugin)
endif()
