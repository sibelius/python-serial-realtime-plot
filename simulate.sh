#!/bin/bash

rand() {
    if [ "$#" -ne 1 ];
    then
        echo $(( ( RANDOM % 100 )  + 1 ))
    else
        echo $(( ( RANDOM % $1 )  + 1 ))
    fi
}

gen_tripa() {
    echo "c00000000$(rand)i00000000$(rand)t$(rand).$(rand)p$(rand).$(rand)s00$(rand)e."
}

if [ "$#" -ne 1 ]; 
then
    echo "Usage: $0 /dev/ttys00X"
else 
    while true
    do
        tripa=$(gen_tripa)
        echo $tripa
        echo $tripa > $1
        sleep 0.05
    done
fi
