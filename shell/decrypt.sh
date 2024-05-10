#!/bin/bash

array=(21029299 f2b61ccf a3da1677 1f6d12dd 8721469a)
count=0

for i in $(seq 0 32767); do
  variable=$(echo $i | md5sum | cut -c 1-8)
  if [[ ${array[*]} =~ $variable ]]; then
    let count++
    echo "$count: $i ==>> $variable"
  fi
  [ $count -eq 5 ] && exit
done
