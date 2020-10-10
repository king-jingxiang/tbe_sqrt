# Copyright (c) Huawei Technologies Co., Ltd. 2020. All rights reserved.

cmake_minimum_required(VERSION 3.5.1)

message(STATUS "CMAKE_CURRENT_BINARY_DIR=${CMAKE_CURRENT_BINARY_DIR}")
message(STATUS "CMAKE_CURRENT_SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}")

set(CMAKE_C_COMPILER "gcc")
if ("x$ENV{CMAKE_CXX_COMPILER}" STREQUAL "x")
    set(CMAKE_CXX_COMPILER "g++")
else()
    set(CMAKE_CXX_COMPILER $ENV{CMAKE_CXX_COMPILER})
endif()

project(tbe)

if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/cmake/config.cmake)
    include(${CMAKE_CURRENT_BINARY_DIR}/cmake/config.cmake)
else()
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.cmake)
        include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.cmake)
    endif()
endif()

execute_process(COMMAND rm -rf ./makepkg)

message(STATUS "OP_COMMON_INC=${OP_COMMON_INC}")

add_subdirectory(framework)
add_subdirectory(op_proto)
add_subdirectory(tbe)

message(STATUS "operation system is ${CMAKE_HOST_SYSTEM_NAME}")

set(ALL_MODULES ${OP_PROTO_TARGET} config_json)
if(IS_DIRECTORY "${CMAKE_SOURCE_DIR}/framework/caffe_plugin")
    set(ALL_MODULES ${ALL_MODULES} ${CAFFE_PLUGIN_TARGET})
endif()
if(IS_DIRECTORY "${CMAKE_SOURCE_DIR}/framework/tf_plugin")
    set(ALL_MODULES ${ALL_MODULES} ${TF_PLUGIN_TARGET})
endif()

message(STATUS "ALL_MODULES=${ALL_MODULES}")
add_custom_target(${RUN_TARGET} ALL DEPENDS ${ALL_MODULES})

add_custom_command(TARGET ${RUN_TARGET}
        PRE_BUILD
        COMMAND mkdir -p ./makepkg/packages/fusion_rules/${PROJECT_DIR}/
        COMMAND mkdir -p ./makepkg/packages/op_impl/${PROJECT_DIR}/ai_core/tbe/custom_impl
        COMMAND mkdir -p ./makepkg/packages/op_impl/${PROJECT_DIR}/vector_core/tbe/custom_impl
        COMMAND cp -r ${CMAKE_SOURCE_DIR}/tbe/impl/*.py ./makepkg/packages/op_impl/${PROJECT_DIR}/ai_core/tbe/custom_impl
        COMMAND cp -r ${CMAKE_SOURCE_DIR}/tbe/impl/*.py ./makepkg/packages/op_impl/${PROJECT_DIR}/vector_core/tbe/custom_impl
        COMMAND cp ${CMAKE_SOURCE_DIR}/scripts/install.sh ./makepkg/
        COMMAND cp ${CMAKE_SOURCE_DIR}/scripts/upgrade.sh ./makepkg/
        COMMAND cp ${CMAKE_SOURCE_DIR}/scripts/uninstall.sh ./makepkg/
        COMMAND cp ${CMAKE_SOURCE_DIR}/scripts/help.sh ./makepkg/
        COMMAND ${CMAKE_SOURCE_DIR}/cmake/util/makeself/makeself.sh --gzip --complevel 4 --nomd5 --sha256 ./makepkg ${RUN_TARGET} "version:1.0" ./install.sh
        )
