import socket

s = socket.socket()
host = socket.gethostname()
port = 10000
s.bind(("0.0.0.0", port))

f = open("nodeARP.txt", "w");

#f = open('ARP.txt', 'rb')
#arp = f.read(4096)
ip = "192.168.43.92 "
mac = "60:57:18:3c:d2:fa "
portno = "10000"

imp = ip + mac + portno


f.write(imp)

f.close()

s.listen(4)


incomingPort = 0

while True:
    c, addr = s.accept()
    incoming = c.recv(4096)
    incominglist = incoming.split() #0 - ip, 1 - mac, 2 - portno
    print 'ARP Request Packet received from: ', incominglist[2]
    c.send(imp)
    f = open('nodeARP.txt', 'a')
    f.write('\n')
    f.write(incoming) #i think we have to check for the match with central server here also before updating the nodeARP cache
    f.close()

    c.close()
