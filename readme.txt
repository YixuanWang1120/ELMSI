程序基于python2.7，因此首先需配置python2.7环境
执行步骤
预处理：
1.用samtools将bam文件进行索引，排序（按readname）并转成sam
2.用LMSI下RemoveNameError.py将sam文件中重复和错误read去除（注意修改RemoveNameError.py中的input和outpath）
3.执行fileclass中的run.sh（注意修改其中路径python "输入文件" "输出结果文件"）