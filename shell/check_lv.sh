#!/bin/bash
[ $UID -ne 0 ] && echo "please use root run" && exit 22
[ -f /etc/init.d/functions ] && . /etc/init.d/functions
#定义 vip 和real server ip
vip=10.0.0.90
vip_netmask=10.0.0.90/24
RealServer=(
  10.0.0.56
  10.0.0.57
)

status_del() {
  for Rs_ip in ${RealServer[*]}; do
    error=0 #定义检测失败次数
    #进行两次检测
    for ((i = 1; i <= 2; i++)); do
      x=$(nmap -p 80 "$Rs_ip" | grep 'open' | wc -l)
      if [ "$x" -eq 0 ]; then
        let error+=1
      fi
      sleep 2
    done
    #检查real主机ip 是否在 ipvsadm列表中
    vs_ip=$(ipvsadm -ln | grep $Rs_ip | wc -l) #两次检测失败，而且real ip存在ipvsadm列表中，执行向ipvsadm中添加命令
    if [ $error -eq 2 -a "$vs_ip" -ne 0 ]; then
      ipvsadm -d -t "$vip":80 -r "$Rs_ip":80
      echo "Real server $Rs_ip is down,delete it" #两次检测失败，而且不存在ipvsadm列表中，输出 down
    elif [ $error -eq 2 -a "$vs_ip" -eq 0 ]; then
      echo "Real server $Rs_ip is down" #检测失败次数为0或者1，列表中存在，输出 running
    elif [ $error -ne 2 -a "$vs_ip" -ne 0 ]; then
      echo "Real server $Rs_ip is running"
    fi
  done
}

status_add() {
  for Rs_ip in ${RealServer[*]}; do
    bingo=0
    for ((i = 1; i <= 2; i++)); do
      x=$(nmap -p 80 "$Rs_ip" | grep 'open' | wc -l)
      if [ "$x" -eq 1 ]; then
        let bingo+=1
      fi
      sleep 2
    done
    vs_ip=$(ipvsadm -ln | grep $Rs_ip | wc -l) #两次检测成功，real ip不在ipvsadm中，执行向ipvsadm 添加ip 命令
    if [ $bingo -eq 2 -a "$vs_ip" -eq 0 ]; then
      ipvsadm -a -t "$vip":80 -r "$Rs_ip":80
      echo "Real server $Rs_ip is recover,add it"
    fi
  done
}

main() {
  while true; do
    status_del
    sleep 10
    status_add
    sleep 10
  done
}

main
