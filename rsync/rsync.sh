#!/bin/bash
#this script for start|stop rsync daemon service

# 指定rsyncd.conf文件的路径
RSYNC_CONF="/etc/rsyncd.conf"
RSYNC_PID_FILE="/var/run/rsyncd.pid" # rsync服务器进程ID文件路径

check_status() {
  STATUS=$(ps -ef | egrep -q "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
}
start() {
  if [ "${STATUS}X" == "X" ]; then
    rm -f $RSYNC_PID_FILE
    # 启动rsync服务器
    rsync --daemon --config=$RSYNC_CONF
    check_status
    if [ "${STATUS}X" != "X" ]; then
      echo "rsync service start.......OK"
    fi
  else
    echo "rsync service is running !"
  fi

}

stop() {
  # 停止rsync服务器
  if [ "${STATUS}X" != "X" ]; then
    kill -9 "$(cat $RSYNC_PID_FILE)" #读取并结束 进程 pid号
    check_status
    if [ "${STATUS}X" == "X" ]; then
      echo "rsync service stop.......OK"
    fi
  else
    echo "rsync service is not running !"
  fi
}

restart() {
  # 重启rsync服务器
  stop
  start
}

status() {
  # 检查rsync服务器的状态
  if [ "${STATUS}X" != "X" ]; then
    echo "rsync service is running !"
  else
    echo "rsync service is not running !"
  fi
}

main() {

  if ! grep "rsync --daemon" /etc/rc.local; then
    echo "rsync --daemon --config=$RSYNC_CONF" >>/etc/rc.local #加入开机自启动
  fi
  check_status
  case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    restart
    ;;
  status)
    status
    ;;
  *)
    echo "使用方法: $0 {start|stop|restart|status}"
    exit 1
    ;;
  esac

}

main "$@"
