#!/bin/bash
echo -n "please input a number:"
read -r a
b=$((a * 2))
for ((i = 1; i <= "${a}"; i++)); do
  printf "%-${b}s\n" "+" | sed 's/ /+/g'
done
