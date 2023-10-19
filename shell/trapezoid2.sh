#!/bin/bash

echo "input a number"
read -r num

#let num2=num*2
for ((a = 1; a <= "$num"; a++)); do
    for ((b = 1; b <= a; b++)); do
        echo -n "+"
    done
    echo -e "\n"
done
