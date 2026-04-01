#!/bin/bash

[ $UID -ne 0 ] && echo "please use root run" && exit 22
[ -f /etc/init.d/functions ] && . /etc/init.d/functions
vip=10.0.0.90
vip_netmask=10.0.0.90/24
RealServer=(
   10.0.0.56
   10.0.0.57
)

start() {
   ip addr show | grep "$vip" &>/dev/null
   #判断网卡上 vip 是否存在，不存在添加
   if [ "$?" -ne 0 ]; then
      ip addr add "$vip_netmask" dev ens32
      action "ip address add vip $vip_netmask" /bin/true
   else
      echo "ip address vip $vip_netmask already exists"
   fi
   #判断ipvsadm中 vip是否存在，不存在则添加
   lvs_table=$(ipvsadm -ln | grep "$vip" | wc -l)

   if [ "$lvs_table" -eq 1 ]; then
      echo "ipvsadm vip already exist"
   else
      ipvsadm -A -t "$vip":80 -s rr
      action "ipvsadm add vip $vip" /bin/true
   fi

   #判断ipvsadm中 real server是否存在，不存在则添加
   for ip in ${RealServer[*]}; do
      rs_num=$(ipvsadm -ln | grep "$ip" | wc -l)
      if [ "$rs_num" -eq 1 ]; then
         echo "real server $ip already exists"
      else
         ipvsadm -a -t "$vip":80 -r "$ip" -g
         action "ipvsadm add real server $ip" /bin/true
      fi
   done
}

stop() {
   ip addr show | grep $vip &>/dev/null
   if [ "$?" -ne 0 ]; then
      echo "ip address vip $vip is not exist"
   else
      ip addr del $vip_netmask dev ens32
      action "ip address delete vip $vip" /bin/true
   fi

   ipvsadm -C && action "clear all lvs table." /bin/true
}

case "$1" in
start)
   start
   ;;
stop)
   stop
   ;;
restart)
   stop
   sleep 2
   start
   ;;
*)
   echo "please input {start|stop|restart}"
   ;;
esac
