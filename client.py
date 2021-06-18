# Client Side
import cv2, imutils, socket
import numpy as np
import time
import base64

# Deklarasi buff size, client_socket, host_name, host_ip, port
BUFFER_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
HOST_NAME = socket.gethostname()
HOST_IP = '192.168.1.139'
print(HOST_IP)
PORT = 50036
message = b'Hello'

# Sending client_socket ke IP dan Port Server
client_socket.sendto(message,(HOST_IP,PORT))
fps,st,frames_to_count,cnt = (0,0,20,0)

# Create loop untuk stream video dari server
while True:
	packet,_ = client_socket.recvfrom(BUFFER_SIZE)
	data = base64.b64decode(packet,' /')
	npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(npdata,1)
	frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
	
	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket.close()
		break
	if cnt == frames_to_count:
		try:
			fps = round(frames_to_count/(time.time()-st))
			st=time.time()
			cnt=0
		except:
			pass
	cnt+=1
