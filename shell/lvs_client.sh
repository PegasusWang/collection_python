#!/bin/bash
[ -f /etc/init.d/functions ] && . /etc/init.d/functions
vip=10.0.0.90
vip_netmask=10.0.0.90/32
RealServer=10.0.0.56

start() { # lo网卡上没有vip 则添加
  ip addr show | grep "$vip" &>/dev/null
  if [ "$?" -ne 0 ]; then
    ip addr add "$vip_netmask" dev lo
  fi

  echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
  echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce#检测lo是否添加上vip
  ip addr show | grep "$vip" &>/dev/null
  if [ "$?" -eq 0 ]; then
    action "ip address add vip $vip_netmask ,lvs_client start" /bin/true
  else
    action "can't add vip $vip_netmask " /bin/false
  fi
}

stop() { #lo网卡上有 vip 则删掉
  ip addr show | grep "$vip" &>/dev/null
  if [ "$?" -eq 0 ]; then
    ip addr del "$vip_netmask" dev lo
  fi

  echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
  echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce#检测删除结果
  ip addr show | grep "$vip" &>/dev/null
  if [ "$?" -ne 0 ]; then
    action "ip address del vip $vip_netmask ,lvs_client stop" /bin/true
  else
    action "can't del vip $vip_netmask " /bin/false
  fi
}

case $1 in
start)
  start
  ;;
stop)
  stop
  ;;
restart)
  stop
  sleep 1
  start
  ;;
*)
  echo "USAGE: $0 {start|stop|restart|status}"
  ;;
esac
