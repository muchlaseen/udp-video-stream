# Server Side
import cv2, imutils, socket
import numpy as np
import time
import base64

# Deklarasi buff size, server_socket, host_name, host_ip, port
BUFFER_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
HOST_NAME = socket.gethostname()
HOST_IP= '192.168.1.139'
print(HOST_IP)
PORT = 50036

# Binding server_socket dengan IP Address dan Port
socket_address = (HOST_IP,PORT)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

# Attach video untuk ditransmit ke Client 
vid = cv2.VideoCapture('sunset.mp4') 
fps,st,frames_to_count,cnt = (0,0,20,0)

# Create loop untuk open dan transmit video serta menghitung fps dari video tsb
while True:
	msg,client_addr = server_socket.recvfrom(BUFFER_SIZE)
	print('GOT connection from ',client_addr)
	WIDTH=400
	while(vid.isOpened()):
		_,frame = vid.read()
		frame = imutils.resize(frame,width=WIDTH)
		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		message = base64.b64encode(buffer)
		server_socket.sendto(message,client_addr)
		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
		cv2.imshow('TRANSMITTING VIDEO',frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			server_socket.close()
			break
		if cnt == frames_to_count:
			try:
				fps = round(frames_to_count/(time.time()-st))
				st=time.time()
				cnt=0
			except:
				pass
		cnt+=1