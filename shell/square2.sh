#!/bin/bash

echo "input a number"
read -r num

num2=$(( num * 2 ))
for ((a = 1; a <= "$num"; a++)); do
  echo -e "\n"
  for ((b = 1; b <= "$num2"; b++)); do
    echo -n +
  done
done
