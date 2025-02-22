#!/bin/bash

clear
tput civis
while true; do
    tput cup 0 0

    hyfetch --ascii ~/miku.txt
    read -t 1 -n 1 input && break
done
tput cnorm
