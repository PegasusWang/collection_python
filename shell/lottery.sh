#!/bin/bash

######
# 需要一个抓阄的程序：

# 要求：

# 1、执行脚本后，想去的同学输入英文名字全拼，产生随机数01-99之间的数字，数字越大就去参加项目实践，前面已经抓到的数字，下次不能在出现相同数字。

# 2、第一个输入名字后，屏幕输出信息，并将名字和数字记录到文件里，程序不能退出继续等待别的学生输入。
#####
namelist=/tmp/name.txt
#判断数字是否重复
judgeNum() {
    if grep -w "$1" $namelist; then
        a=1
    else
        a=0
    fi
}

while read -rp "please input your name:" name; do
    a=1
    while [ $a -eq 1 ]; do #数字不重复就跳出第二个while ，重复就再生成一个
        num=$((RANDOM % 100 + 1))
        judgeNum $num
    done
    echo "$name:$num" | tee -a $namelist #结果显示到屏幕 并 追加到文件中
done
