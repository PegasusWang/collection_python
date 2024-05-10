#!/bin/bash
a="the squid project provides a number of resources toassist users design,implement and support squid installations. Please browsethe documentation and support sections for more infomation"

word=/tmp/word.txt

word_sort() {
    for i in $a; do
        echo "$i" >>$word
    done
    cat $word | sort | uniq -c | sort -rn
}

letter_sort() {
    echo "$a" |
        while read -r line; do
            for i in $(seq 1 ${#line}); do
                echo "$line" | cut -c "$i" >>$word
            done
        done
    cat $word | sort | uniq -c | sort -rn
}
main() {

    [ -f $word ] && rm -f $word
    echo "word sort input 1"
    echo "letter sort input 2"
    read -r num

    case $num in
    "1")
        word_sort
        ;;
    "2")
        letter_sort
        ;;
    *)
        echo "please input 1 or 2"
        ;;
    esac
}

main
