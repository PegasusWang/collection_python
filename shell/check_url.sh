#!/bin/bash

[ -f /etc/init.d/functions ] && source /etc/init.d/functions

array=(
    http://www.163.com
    http://www.taobao.com
    http://oldboy.blog.51cto.com
    http://10.0.0.7
)

wait() {
    echo -n "wait"
    for ((a = 1; a <= 3; a++)); do
        echo -n "."
        sleep 1
    done
}

check_url() {
    wget -T 5 -t 2 --spider "$1" &>/dev/null
    RETVAL=$?
    if [ $RETVAL -eq 0 ]; then
        action "check $1" /bin/true
    else
        action "check $1" /bin/false
    fi
    return $RETVAL
}

main() {
    for ((i = 0; i < ${#array[*]}; i++)); do
        wait
        check_url "${array[i]}"
    done
}

main
