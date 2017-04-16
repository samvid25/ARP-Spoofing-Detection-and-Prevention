import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

f = open('ip.txt', 'r')
arptxt = open('ARP.txt', 'w')
ips = f.read(4096)
list_ips = ips.split('\n')
print list_ips

ip = "192.168.43.255 "
mac = "ff:ff:ff:ff:ff:ff "
portno = "15000"

imp = ip + mac + portno

for i in list_ips[1:-1]:
    for ports in range (10000, 10011):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((i, ports))
        print i, ports, result
        if result == 0:
            print 'conneced'
            s.send(imp + " central")
            recv_data = s.recv(4096)
            arptxt.write(recv_data + '\n')
            s.close()
arptxt.close()
