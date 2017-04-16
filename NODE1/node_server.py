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

    #FIRST CHECK OUT IF IT ALREADY EXISTS IN THE ARP

    file = open('nodeARP.txt','r')
    acceptance = True
    if incominglist[-1] != "central":
        data2 = incominglist
        data = file.read(4096)
        data_list = data.split('\n')[:-1]
        valid = 'False'
        not_found = True
        ip_only_found = False
        rewrite_ip = ''
        for x in data_list:
            print "Checking if ARP data exists in local arp cache..."
            if x[0] == data2[0] and x[1] == data2[1]:
                not_found = False
                valid  = 'True'
                break
            elif x[0] == data2[0]:
                ip_only_found = True
                rewrite_ip = x[0]
                not_found = False
                valid = 'False'
                break

        #SEND DATA TO CENTRAL SERVER AND CHECKa IF DATA EXISTS
        if not_found == True or valid == 'False':
            print "ARP data not matching in local arp cache..."
            print "Asking Central Server to Validate New Connection..."
            c_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c_ip = '192.168.43.92'
            c_port = 15000
            c_s.connect((c_ip,c_port))
            c_s.send(incoming)
            c_r_data = c_s.recv(4096).split()
            valid = c_r_data[0]

        if ip_only_found == True:
            #If IP and MAC both exist in local but only IP Matches
            #Replace the existing entry
            i = 0
            combined_string = ''
            for x in data_list:
                if x[0] == rewrite_ip:
                    data_list[i][1] = c_r_data[2]
                if x[0] != data_list[-1]:
                    combined_string += data_list[i][0] + '   ' + data_list[i][1] + '\n'
                else:
                    combined_string += data_list[i][0] + '   ' + data_list[i][1]
                i = i + 1
            file = open('nodeARP.txt','w')
            file.write(combined_string)
            file.close()
        elif valid == 'True' and not_found == True:
            #If IP and MAC both exist in Central server but not in local arp
            print 'Connection Accepted and Local Cache Updated'
            file = open('nodeARP.txt','a')
            file.write('\n');
            file.write(incoming)
            file.close()
        elif valid == 'False':
            #If either local or central server say false
            print "New Connection Not Valid", "Connection Refused"
            acceptance = False

    if acceptance:
        c.send(imp)
    else:
        c.send('refused')
    c.close()
