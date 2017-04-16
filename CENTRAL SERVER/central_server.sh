##!/bin/bash
nmap -sP 192.168.43.* > allIP.txt;
arp > cache.txt
cat cache.txt | awk '{print $1}' > ip.txt;
