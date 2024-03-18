#!/bin/bash

# 定义rsync服务器的IP地址和源文件夹
RSYNC_SERVER="rsync://192.168.98.129"
SOURCE_FOLDER="/mirrors/"

# 定义要同步的目标文件夹
DEST_FOLDER="/opt/mirrors/"

# 定义日志文件的路径
LOG_FILE="/tmp/logfile.log"

# 同步操作
rsync -avzp --delete  "$RSYNC_SERVER:$DEST_FOLDER" "$SOURCE_FOLDER">> $LOG_FILE

# 检查rsync命令的返回状态
if [ $? -eq 0 ]; then
    echo "同步成功！"
else
    echo "同步失败，请检查日志文件 $LOG_FILE 以获取更多详细信息。"
fi
