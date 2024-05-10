#!/bin/bash

echo -n "please input a number:"
read -r a
for ((i = 1; i <= "$a"; i++)); do
    printf "%-${i}s\n" "+" | sed 's/ /+/g'
done
