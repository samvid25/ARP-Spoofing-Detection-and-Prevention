import socket

s = socket.socket()
host = socket.gethostname()
port = 15000
s.bind(("0.0.0.0", port))

flag = 0

ip = "192.168.43.255 "
mac = "ff:ff:ff:ff:ff:ff "
portno = "15000"

imp = ip + mac + portno


s.listen(4)

while True:
    c, addr = s.accept()
    incoming = c.recv(4096)
    incominglist = incoming.split()
    print 'ARP Validation request received from ', addr
    f = open('ARP.txt', 'rb');
    arp = f.read(4096);
    lines = arp.split('\n')

    #print lines


    lists = []
    for l in lines:
        lists.append(l.split())

    print lists

    for i in lists[:-1]:
        if (i[0] == incominglist[0]) and (i[1] == incominglist[1]):
            print 'True'
            c.send('True ' + i[0] + " " + i[1])
            flag = 1

    if flag == 0:
        print 'False'
        c.send('False ' + i[0] + " " + i[1])
    f.close()
    c.close()
