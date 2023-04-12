#!/bin/bash

second=3;
SystemPrint=$(echo -e "\nSystem will restart after ${second}s\n");

while true
do
    npm start;
    echo "${SystemPrint#-e}";
    sleep $second;
done
