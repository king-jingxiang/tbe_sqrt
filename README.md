# tbe_sqrt
基于昇腾AI处理器的算子开发
通过Mind Studio图形化界面，体验端到端的算子开发流程，包括算子工程创建，算子代码实现、测试代码实现以及测试。
1. 工程配置
1.1. 启动Mind Studio
【实验操作桌面】双击图标“Xfce 终端”打开命令行界面，输入以下命令启动“Mind Studio”。

拷贝代码
sh MindStudio-ubuntu/bin/MindStudio.sh
启动成功，保持当前命令行开启，请勿关闭。

在成功启动“Mind Studio”的界面点击“Create new project”如下图所示：


1.2. 创建算子工程
在弹出的创建新项目的界面，配置如下：
Name：sqrt(算子项目名称)；
其他保持默认，

点击“Next”，如下图所示：


配置参数如下：
Plugin Framework：默认，
Compute Unit：点击下拉菜单并全选，
Operator Type：sqrt

如下图所示：


点击“Finish”，项目创建成功，如下图所示：


2. 关键代码补充
2.1. 设置环境变量
在MindStudio顶部的菜单栏点击“File” -> “Project Structure…”，如下图所示：


弹出的配置窗口中点击“New...”按钮，选择“Python SDK”项，如下图所示：


在“Add Python Interpreter”界面，选择“Virtualenv Environment” -> “Existing environment”，点击“...”按钮，如下如所示：


在“Select Python Interpreter”界面的列表中，找到Python执行文件（路径/usr/bin/python3.7），如下图所示：


逐层点击“OK”进行确认，最终“Project Structure”配置界面如下图所示：


点击“Apply” -> “OK”，完成环境配置。

2.2. 编写算子实现代码
算子实现代码是指“sqrt/tbe/impl”目录下的“sqrt.py”。
复制以下代码，在MindStudio的左侧栏找到源文件“sqrt.py”双击打开，找到文件第46行的【"""】后回车下一行，添加如下代码：

拷贝代码
    
    dtype = input_x.dtype
    date = input_x
    if dtype == "float16":
        date = te.lang.cce.cast_to(input_x, "float32")
    log_val = te.lang.cce.vlog(date)
    const_val = tvm.const(0.5, "float32")
    mul_val = te.lang.cce.vmuls(log_val, const_val)
    res = te.lang.cce.vexp(mul_val)
    if dtype == "float16":
        res = te.lang.cce.cast_to(res, "float16")
    return res
结果如下图所示：

注意：python脚本代码一定要与下图所示缩进格式一致，否则会运行失败。


按键“Ctrl+S”保存文件。

2.3. 编写测试数据生成代码
测试数据生成代码是指“/home/user/AscendProjects/sqrt/tbe/testcases/st/sqrt”目录下的“sqrt_datagen.py”。
复制以下代码，在MindStudio的左侧栏找到源文件“sqrt_datagen.py”双击打开，找到文件第26行的【"""】后回车下一行，添加如下代码：

拷贝代码
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
找到文件第56行，将“pass”替换为如下代码：

拷贝代码
sqrt("sqrt", (100,100), "float16")
结果如下图所示：


按键“Ctrl+S”保存文件。

2.4. 编写调用算子代码
调用算子的代码是指“/home/user/AscendProjects/sqrt/tbe/testcases/st/sqrt”目录下的“test_sqrt_st.py”。
复制以下代码，在MindStudio的左侧栏找到源文件“test_sqrt_st.py”双击打开，找到文件第25行的【"all": {}】后，在“{}”中添加如下代码：

拷贝代码
"test_sqrt_100_100_float16": ((100, 100), "float16", "cce_sqrt_100_100_float16")
结果如下图所示：


按键“Ctrl+S”保存文件。

2.5. 编写测试用例代码
测试用例代码是指“/home/user/AscendProjects/sqrt/tbe/testcases/st/sqrt”目录下的“sqrt_st.cc”。
复制以下代码，在MindStudio的左侧栏找到源文件“sqrt_st.cc”双击打开，找到文件第28行回车后，添加如下代码：

拷贝代码
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
结果如下图所示：


按键“Ctrl+S”保存文件。

3. 运行测试生成结果
3.1. 运行项目代码
添加完关键代码后，在Mind Studio左侧栏“/home/user/AscendProjects/sqrt/tbe/testcases/st”,下的“sqrt”文件夹上右键，选择“Run Tbe Operator ‘sqrt’ST with coverage”，如下图所示：


在弹出的窗口中，配置参数如下：
SoC Version：Ascend910，
AI Core Num：32，
其他参数默认，

如下图所示


点击“Run”运行代码。
在Mind Studio下方窗口中可查看结果，出现[ PASSED ] 1 test.说明测试结果正确，如下图所示：


至此实验结束。
