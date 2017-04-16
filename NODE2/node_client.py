import socket

ip_addr = '192.168.43.15'
mac_addr = '60:57:89:AF:9c:34'
port_no = '10001'
send_data = ip_addr + " " + mac_addr + " " + port_no

file = open('arp.txt','w')
file.write(send_data)
# First line is basically the client's own data
file.close()

command = 'ex'

while command != 'exit':
    command = raw_input('>>>')
    clist = command.split()
    if clist[0] == 'ping':
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_ip = clist[1]
        port = int(clist[2])
        s.connect((server_ip,port))
        print 'error'
        s.send(send_data)
        print "ARP Request Sent to (Node)" + server_ip

        recv_data = s.recv(4096)
        print "ARP Reply Received from (Node)" + server_ip
        #FIRST CHECK OUT IF IT ALREADY EXISTS IN THE ARP
        if recv_data == 'refused':
            print "Client IP and MAC Don't Match"
            print "Connection Refused"
            s.close()
            continue

        file = open('arp.txt','r')
        data2 = recv_data.split()
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
            c_s.send(recv_data)
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
            file = open('arp.txt','w')
            file.write(combined_string)
            file.close()
        elif valid == 'True' and not_found == True:
            #If IP and MAC both exist in Central server but not in local arp
            print 'Connection Accepted and Local Cache Updated'
            file = open('arp.txt','a')
            file.write('\n');
            file.write(recv_data)
            file.close()
        elif valid == 'False':
            #If either local or central server say false
            print "New Connection Not Valid", "Connection Refused"
    elif clist[0] == 'arp':
        file = open('arp.txt','r')
        arp = file.read(4096)
        print arp
        file.close()
