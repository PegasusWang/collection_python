#!/bin/bash
#this script for start|stop rsync daemon service

# status1=$(ps -ef | egrep "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
# 指定rsyncd.conf文件的路径
RSYNC_CONF="/etc/rsyncd.conf"
RSYNC_PID_FILE="/var/run/rsyncd.pid" # rsync服务器进程ID文件路径
START_RSYNC="rsync --daemon --config=$RSYNC_CONF"

start() {
  status1=$(ps -ef | grep -E "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
  if [ "${status1}X" == "X" ]; then
    rm -f $RSYNC_PID_FILE
    # 启动rsync服务器
    ${START_RSYNC}
    # rsync --daemon --config=$RSYNC_CONF
    status2=$(ps -ef | grep -E "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
    if [ "${status2}X" != "X" ]; then
      echo "rsync service start.......OK"
    fi
  else
    echo "rsync service is running !"
  fi

}

stop() {
  # 停止rsync服务器
  status1=$(ps -ef | grep -E "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
  if [ "${status1}X" != "X" ]; then
    kill -9 "$(cat $RSYNC_PID_FILE)" #读取并结束 进程 pid号
    status2=$(ps -ef | grep -E "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
    if [ "${status2}X" == "X" ]; then
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
  status1=$(ps -ef | grep -E "rsync --daemon.*rsyncd.conf" | grep -v 'grep')
  if [ "${status1}X" != "X" ]; then
    echo "rsync service is running !"
  else
    echo "rsync service is not running !"
  fi
}

add_boot_up() {
  # 加入开机自启动
  if ! grep -E "rsync --daemon" /etc/rc.local >/dev/null; then
    echo "rsync --daemon --config=$RSYNC_CONF" >>/etc/rc.local #加入开机自启动
  fi
}

main() {
  add_boot_up
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
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
  esac

}

main "$@"
