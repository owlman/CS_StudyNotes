#! /bin/bash

read -p "what is your name? " name
i=0
if [ $name = "owlman" ] ;then
    echo "this not is your name."
else    
    while [ $i -le 10 ]
    do
        echo "Hello, $name"
        ((i++))
    done
fi

if [ -f "test.sh" ] ;then
    echo "yes"
fi

if [ -d "temp" ] ;then
    ls -l temp 
else
    mkdir temp
fi

expect -c "
spawn sudo apt update
expect *sudo* 
send 00000000\r
"