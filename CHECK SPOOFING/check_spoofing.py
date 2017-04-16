import os


filename = open('mac.txt','r')

ip_string = filename.read()
mac_array = ip_string.split()
filename.close()
del mac_array[0]
print mac_array

filename = open('ip.txt','r')

ip_string = filename.read()
ip_array = ip_string.split()
filename.close()
del ip_array[0]
print ip_array

def run_script():
	os.system('pkill ping')

for i in range(len(mac_array)):
	for j in range(i+1,len(mac_array)):
		if(mac_array[i] == mac_array[j]):
			run_script()
			filename = open('log.txt','w')
			filename.write('MITM Attack')



