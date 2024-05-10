#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
# Description: Auto test download & I/O speed script
# Copyright (C) 2015 - 2016 Teddysun <i@teddysun.com>
# Thanks: LookBack <admin@dwhd.org>
# Teddysun: https://teddysun.com/444.html
# Toyo: https://doub.io
# For https://VPS.BEST
# VPS测试脚本，方便你更好地了解你的服务器
# 地址：https://github.com/ToyoDAdoubiBackup/vpstest

RED='\033[0;31m' && GREEN='\033[0;32m' && YELLOW='\033[0;33m' && PLAIN='\033[0m'
next() { printf "%-70s\n" "-" | sed 's/\s/-/g'; }
get_opsy() {
  [[ -f /etc/redhat-release ]] && awk '{print ($1,$3~/^[0-9]/?$3:$4)}' /etc/redhat-release && return
  [[ -f /etc/os-release ]] && awk -F'[= "]' '/PRETTY_NAME/{print $3,$4,$5}' /etc/os-release && return
  [[ -f /etc/lsb-release ]] && awk -F'[="]+' '/DESCRIPTION/{print $2}' /etc/lsb-release && return
}
check_sys() {
  if [[ -f /etc/redhat-release ]]; then
    release="centos"
  elif grep -q -E -i "debian" /etc/issue; then
    release="debian"
  elif grep -q -E -i "ubuntu" /etc/issue; then
    release="ubuntu"
  elif grep -q -E -i "centos|red hat|redhat" /etc/issue; then
    release="centos"
  elif grep -q -E -i "debian" /proc/version; then
    release="debian"
  elif grep -q -E -i "ubuntu" /proc/version; then
    release="ubuntu"
  elif grep -q -E -i "centos|red hat|redhat" /proc/version; then
    release="centos"
  fi
  bit=$(uname -m)
}
Installation_dependency() {
  if [[ ${release} == "centos" ]]; then
    yum update
    yum -y install mtr curl time virt-what
    [[ ${action} == "a" ]] && yum -y install make gcc gcc-c++ gdbautomake autoconf
  else
    apt-get update
    apt-get -y install curl mtr time virt-what
    [[ ${action} == "a" ]] && apt-get -y install make gcc gdb automake autoconf
  fi
}
get_info() {
  logfile="test.log"
  IP=$(curl -s myip.ipip.net | awk -F ' ' '{print $2}' | awk -F '：' '{print $2}')
  IPaddr=$(curl -s myip.ipip.net | awk -F '：' '{print $3}')
  if [[ -z "$IP" ]]; then
    IP=$(curl -s ip.cn | awk -F ' ' '{print $2}' | awk -F '：' '{print $2}')
    IPaddr=$(curl -s ip.cn | awk -F '：' '{print $3}')
  fi
  time=$(date '+%Y-%m-%d %H:%I:%S')
  backtime=$(date +%Y-%m-%d)
  vm=$(virt-what)
  [[ -z ${vm} ]] && vm="none"
  cname=$(awk -F: '/model name/ {name=$2} END {print name}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//')
  cores=$(awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo)
  freq=$(awk -F: '/cpu MHz/ {freq=$2} END {print freq}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//')
  tram=$(free -m | awk '/Mem/ {print $2}')
  uram=$(free -m | awk '/Mem/ {print $3}')
  swap=$(free -m | awk '/Swap/ {print $2}')
  uswap=$(free -m | awk '/Swap/ {print $3}')
  up=$(awk '{a=$1/86400;b=($1%86400)/3600;c=($1%3600)/60} {printf("%d days, %d hour %d min\n",a,b,c)}' /proc/uptime)
  load=$(w | head -1 | awk -F'load average:' '{print $2}' | sed 's/^[ \t]*//;s/[ \t]*$//')
  opsy=$(get_opsy)
  arch=$(uname -m)
  lbit=$(getconf LONG_BIT)
  kern=$(uname -r)
  ipv6=$(wget -qO- -t1 -T2 ipv6.icanhazip.com)
  disk_size1=("$(LANG=C df -ahPl | grep -wvE '\-|none|tmpfs|devtmpfs|by-uuid|chroot|Filesystem' | awk '{print $2}')")
  disk_size2=("$(LANG=C df -ahPl | grep -wvE '\-|none|tmpfs|devtmpfs|by-uuid|chroot|Filesystem' | awk '{print $3}')")
  disk_total_size=$(calc_disk "${disk_size1[@]}")
  disk_used_size=$(calc_disk "${disk_size2[@]}")
}
system_info() {
  clear
  echo "========== 开始记录测试信息 ==========" >$logfile
  echo "测试时间：$time" | tee -a $logfile
  next | tee -a $logfile
  echo "CPU model            : $cname" | tee -a $logfile
  echo "Number of cores      : $cores" | tee -a $logfile
  echo "CPU frequency        : $freq MHz" | tee -a $logfile
  echo "Total size of Disk   : $disk_total_size GB ($disk_used_size GB Used)" | tee -a $logfile
  echo "Total amount of Mem  : $tram MB ($uram MB Used)" | tee -a $logfile
  echo "Total amount of Swap : $swap MB ($uswap MB Used)" | tee -a $logfile
  echo "System uptime        : $up" | tee -a $logfile
  echo "Load average         : $load" | tee -a $logfile
  echo "OS                   : $opsy" | tee -a $logfile
  echo "Arch                 : $arch ($lbit Bit)" | tee -a $logfile
  echo "Kernel               : $kern" | tee -a $logfile
  echo "ip                   : $IP" | tee -a "$logfile"
  echo "ipaddr               : $IPaddr" | tee -a "$logfile"
  echo "vm                   : $vm" | tee -a "$logfile"
  next | tee -a $logfile
}
calc_disk() {
  local total_size
  local array
  total_size=0
  array=("$@")
  for size in "${array[@]}"; do
    [[ "${size}" == "0" ]] && size_t=0 || size_t=${size:0:${#size}-1}
    [[ "${size:(-1)}" == "M" ]] && size=$(awk 'BEGIN{printf "%.1f", '"$size_t"' / 1024}')
    [[ "${size:(-1)}" == "T" ]] && size=$(awk 'BEGIN{printf "%.1f", '"$size_t"' * 1024}')
    [[ "${size:(-1)}" == "G" ]] && size=${size_t}
    total_size=$(awk 'BEGIN{printf "%.1f", '"$total_size"' + '"$size"'}')
  done
  echo "${total_size}"
}
io_test_1() {
  (LANG=C dd if=/dev/zero of=test_$$ bs=64k count=4k oflag=dsync && rm -f test_$$) 2>&1 | awk -F, '{io=$NF} END { print io}' | sed 's/^[ \t]*//;s/[ \t]*$//'
}
io_test_2() {
  (LANG=C dd if=/dev/zero of=test_$$ bs=8 count=256 conv=fdatasync && rm -f test_$$) 2>&1 | awk -F, '{io=$NF} END { print io}' | sed 's/^[ \t]*//;s/[ \t]*$//'
}
io_test() {
  io1=$($1)
  echo "I/O speed(1st run)   : $io1" | tee -a $logfile
  io2=$($1)
  echo "I/O speed(2nd run)   : $io2" | tee -a $logfile
  io3=$($1)
  echo "I/O speed(3rd run)   : $io3" | tee -a $logfile
  ioraw1=$(echo "$io1" | awk 'NR==1 {print $1}')
  [[ "$(echo "$io1" | awk 'NR==1 {print $2}')" == "GB/s" ]] && ioraw1=$(awk 'BEGIN{print '"$ioraw1"' * 1024}')
  ioraw2=$(echo "$io2" | awk 'NR==1 {print $1}')
  [[ "$(echo "$io2" | awk 'NR==1 {print $2}')" == "GB/s" ]] && ioraw2=$(awk 'BEGIN{print '"$ioraw2"' * 1024}')
  ioraw3=$(echo "$io3" | awk 'NR==1 {print $1}')
  [[ "$(echo "$io3" | awk 'NR==1 {print $2}')" == "GB/s" ]] && ioraw3=$(awk 'BEGIN{print '"$ioraw3"' * 1024}')
  ioall=$(awk 'BEGIN{print '"$ioraw1"' + '"$ioraw2"' + '"$ioraw3"'}')
  ioavg=$(awk 'BEGIN{printf "%.1f", '"$ioall"' / 3}')
  echo "Average I/O speed    : $ioavg MB/s" | tee -a $logfile
  next | tee -a $logfile
}
speed_test() {
  local speedtest
  local ipaddress
  local nodeName
  speedtest=$(wget -4O /dev/null -T300 "$1" 2>&1 | awk '/\/dev\/null/ {speed=$3 $4} END {gsub(/\(|\)/,"",speed); print speed}')
  ipaddress="$(ping -c1 -n "$(awk -F'/' '{print $3}' <<<"$1")" | awk -F'[()]' '{print $2;exit}')"
  nodeName=$2
  printf "${YELLOW}%-32s${GREEN}%-24s${RED}%-14s${PLAIN}\n" "${nodeName}:" "${ipaddress}:" "${speedtest}"
}
speed() {
  printf "%-32s%-24s%-14s\n" "Node Name:" "IPv4 address:" "Download Speed"
  #    speed_test 'http://cachefly.cachefly.net/100mb.test' 'CacheFly'
  speed_test 'http://speedtest.tokyo.linode.com/100MB-tokyo.bin' 'Linode, Tokyo, JP'
  speed_test 'http://speedtest.tokyo2.linode.com/100MB-tokyo2.bin' 'Linode, Tokyo2, JP'
  speed_test 'http://speedtest.singapore.linode.com/100MB-singapore.bin' 'Linode, Singapore, SG'
  speed_test 'http://speedtest.fremont.linode.com/100MB-fremont.bin' 'Linode, Fremont, CA'
  speed_test 'http://speedtest.newark.linode.com/100MB-newark.bin' 'Linode, Newark, NJ'
  speed_test 'http://speedtest.london.linode.com/100MB-london.bin' 'Linode, London, UK'
  speed_test 'http://speedtest.frankfurt.linode.com/100MB-frankfurt.bin' 'Linode, Frankfurt, DE'
  speed_test 'http://speedtest.tok02.softlayer.com/downloads/test100.zip' 'Softlayer, Tokyo, JP'
  speed_test 'http://speedtest.sng01.softlayer.com/downloads/test100.zip' 'Softlayer, Singapore, SG'
  speed_test 'http://speedtest.sng01.softlayer.com/downloads/test100.zip' 'Softlayer, Seoul, KR'
  speed_test 'http://speedtest.hkg02.softlayer.com/downloads/test100.zip' 'Softlayer, HongKong, CN'
  speed_test 'http://speedtest.dal13.softlayer.com/downloads/test100.zip' 'Softlayer, Dallas, TX'
  speed_test 'http://speedtest.sea01.softlayer.com/downloads/test100.zip' 'Softlayer, Seattle, WA'
  speed_test 'http://speedtest.fra02.softlayer.com/downloads/test100.zip' 'Softlayer, Frankfurt, DE'
  speed_test 'http://speedtest.par01.softlayer.com/downloads/test100.zip' 'Softlayer, Paris, FR'
  speed_test 'http://mirror.hk.leaseweb.net/speedtest/100mb.bin' 'Leaseweb, HongKong, CN'
  speed_test 'http://mirror.sg.leaseweb.net/speedtest/100mb.bin' 'Leaseweb, Singapore, SG'
  speed_test 'http://chi.testfiles.ubiquityservers.com/100mb.txt' 'Leaseweb, Chicago, US'
  #	speed_test 'http://phx.testfiles.ubiquityservers.com/100mb.txt' 'Leaseweb, Phoenix, US'
  speed_test 'http://mirror.wdc1.us.leaseweb.net/speedtest/100mb.bin' 'Leaseweb, Washington D.C., US'
  speed_test 'http://chi.testfiles.ubiquityservers.com/100mb.txt' 'Leaseweb, Chicago, US'
  speed_test 'http://mirror.sfo12.us.leaseweb.net/speedtest/100mb.bin' 'Leaseweb, San Francisco, US'
  speed_test 'http://mirror.nl.leaseweb.net/speedtest/100mb.bin' 'Leaseweb, Netherlands, NL'
  speed_test 'http://proof.ovh.ca/files/100Mio.dat' 'OVH, Montreal, CA'
  speed_test 'http://183.60.137.161/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaTelecom, Dongguan, CN'
  speed_test 'http://14.29.72.152/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaTelecom, Foshan, CN'
  speed_test 'http://222.73.131.40/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaTelecom, Shanghai, CN'
  speed_test 'http://163.177.153.71/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaUnicom, Foshan, CN'
  speed_test 'http://112.90.51.172/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaUnicom, Zhongshan, CN'
  speed_test 'http://111.202.98.38/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaUnicom, Beijing, CN'
  speed_test 'http://223.82.245.41/dl.softmgr.qq.com/original/game/DuiZhanSetup1_8_4_2042_win10.exe' 'ChinaMobile, Jiangxi, CN'
  speed_test 'http://61.233.79.5/setup.exe' 'ChinaTieTong, Henan, CN'
  speed_test 'http://101.4.60.106/setup.exe' 'CERNET, Beijing, CN'
  speed_test 'http://mirrors.opencas.org/apache/ode/apache-ode-war-1.3.6.zip' 'CSTNET, Beijing, CN'
  speed_test 'http://tpdb.speed2.hinet.net/test_100m.zip' 'Hinet, Taiwan, TW'
  next | tee -a $logfile
}
speed_test_cli() {
  echo "===== 开始speedtest =====" | tee -a $logfile
  wget -q --no-check-certificate https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py &&
    python speedtest.py --share | tee -a $logfile
  echo -e "===== speedtest完成 =====" | tee -a $logfile
  rm -rf speedtest.py
  next | tee -a $logfile
}
mtrgo() {
  mtrurl=$1
  nodename=$2
  echo "===== 测试 [$nodename] 到此服务器的去程路由 =====" | tee -a $logfile
  mtrgostr=$(curl -s "$mtrurl")
  echo -e "$mtrgostr" >mtrlog.log
  mtrgostrback=$(curl -s -d @mtrlog.log "http://test.91yun.org/traceroute.php")
  rm -rf mtrlog.log
  echo -e "$mtrgostrback" | awk -F '^' '{printf("%-2s\t%-16s\t%-35s\t%-30s\t%-25s\n",$1,$2,$3,$4,$5)}' | tee -a $logfile
  echo -e "===== [$nodename] 去程路由测试结束 =====" | tee -a $logfile
}
mtrback() {
  echo "===== 测试 [$2] 的回程路由 =====" | tee -a $logfile
  mtr -r -c 10 $1 | tee -a $logfile
  echo -e "===== 回程 [$2] 路由测试结束 =====" | tee -a $logfile
}
tracetest() {
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=254&ip=$IP" "北京电信"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=275&ip=$IP" "上海电信"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=163&ip=$IP" "金华电信"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=274&ip=$IP" "广州电信"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=20&ip=$IP" "厦门电信CN2"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=7&ip=$IP" "天津联通"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=12&ip=$IP" "重庆联通"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=298&ip=$IP" "金华联通"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=339&ip=$IP" "福州联通"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=2&ip=$IP" "天津移动"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=315&ip=$IP" "镇江移动"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=160&ip=$IP" "北京教育网"
  mtrgo "http://www.ipip.net/traceroute.php?as=1&a=get&n=1&id=41&ip=$IP" "北京鹏博士"
  next | tee -a $logfile
}
backtracetest() {
  mtrback "183.60.137.161" "东莞电信"
  mtrback "14.29.72.152" "佛山电信"
  mtrback "222.73.131.40" "上海电信"
  mtrback "163.177.153.71" "佛山联通"
  mtrback "112.90.51.172" "舟山联通"
  mtrback "111.202.98.38" "北京联通"
  mtrback "223.82.245.41" "江西移动"
  mtrback "101.4.60.106" "北京科技网"
  next | tee -a $logfile
}
benchtest() {
  if ! wget -qc http://lamp.teddysun.com/files/UnixBench5.1.3.tgz; then
    echo "UnixBench 5.1.3.tgz 下载失败" && exit 1
  fi
  tar -xzf UnixBench5.1.3.tgz
  cd UnixBench/ || exit
  make
  echo "===== 开始测试CPU性能測試 =====" | tee -a ../"${logfile}"
  ./Run
  benchfile=$(ls results/ | grep -v '\.')
  cat results/"${benchfile}" >>../"${logfile}"
  echo "===== CPU性能测试结束 =====" | tee -a ../"${logfile}"
  cd ..
  rm -rf UnixBench5.1.3.tgz UnixBench
  next | tee -a $logfile
}
go() {
  check_sys
  Installation_dependency
  get_info
  system_info
  io_test "io_test_1"
  io_test "io_test_2"
  speed_test_cli
  speed
  tracetest
  backtracetest
  [[ ${action} == "a" ]] && benchtest
  echo "測試脚本执行完毕！日志文件: ${logfile}"
}
action=$1
go
