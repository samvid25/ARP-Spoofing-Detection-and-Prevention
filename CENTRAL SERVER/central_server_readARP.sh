##!/bin/bash
#gnome-terminal -x sh -c "ping $1; bash"

#python central_server.py;
while true
do
  #pkill -f central_server.py
  nmap -sP 192.168.43.*;
  arp > fail.txt;
  rm fail.txt;
  sleep 5;
  arp > actualARP.txt;
  echo "127.0.0.1" >> actualARP.txt;
  cat actualARP.txt | awk '{print $1}' > ip.txt;
  python checkOpenPorts.py
  #gnome-terminal -x sh -c "python central_server.py; bash"
  timeout 60 python central_server.py;
done
