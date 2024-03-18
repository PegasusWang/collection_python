#!/bin/bash
#Author: Stanley Wang
#mail:
#Version: 1.0
#Description: This is a script for nginx proxy health check.
#
###def vars##########
RS=(
  172.16.1.191
  172.16.1.192
)
PORT=80
html_file="/var/html/www/index.html"
declare -a RSTATUS
###main##############
function checkrs() {
  local I=0
  for ((I = 0; I < ${#RS[*]}; I++)); do
    RSTATUS[$I]=$(nmap "${RS[$I]}" -p $PORT | grep "open" | wc -l)
  done
}
function output() {
  if [ "${RSTATUS[0]}" -eq 0 ]; then
    #echo "${RS[$i]} is down!"
    sed -i '22 s/.*/<td align="center" bgcolor="red"><font size="15">Down!<\/font><\/td>/g' $html_file
  elif [ "${RSTATUS[0]}" -eq 1 ]; then
    #echo "${RS[$i]} is OK!"
    sed -i '22 s/.*/<td align="center" bgcolor="green"><font size="15">OK!<\/font><\/td>/g' $html_file
  fi
  if [ "${RSTATUS[1]}" -eq 0 ]; then
    #echo "${RS[$i]} is down!"
    sed -i '28 s/.*/<td align="center" bgcolor="red"><font size="15">Down!<\/font><\/td>/g' $html_file
  elif [ "${RSTATUS[1]}" -eq 1 ]; then
    #echo "${RS[$i]} is OK!"
    sed -i '28 s/.*/<td align="center" bgcolor="green"><font size="15">OK!<\/font><\/td>/g' $html_file
  fi
}
while true; do
  checkrs
  output
  sleep 2
done
