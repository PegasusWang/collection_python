#!/bin/bash

echo "please a number"
read -r num

sum=$((num * 2 + 1))

for ((a = 1; a <= num; a++)); do

    for ((b = 1; b <= $(((sum - 2 * a - 1) / 2)); b++)); do
        echo -n " "
    done

    for ((b = 1; b <= $((2 * a - 1)); b++)); do
        echo -n "+"
    done

    for ((b = 1; b <= $(((sum - 2 * a - 1) / 2)); b++)); do
        echo -n " "
    done

    echo -e "\n"
done
