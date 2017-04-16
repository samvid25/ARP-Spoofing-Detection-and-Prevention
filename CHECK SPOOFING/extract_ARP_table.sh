##!/bin/bash
gnome-terminal -x sh -c "ping $1; bash"
while true
do
	arp > cache.txt;
	cat cache.txt | awk '{print $1}' > ip.txt;
	cat cache.txt | awk '{print $3}' > mac.txt;
	python check_spoofing.py;
	sleep 3;
done
