# OBSOLETE
# formerly rami_pptk.py

import socket
import msvcrt
import pptk
import numpy as np
import plyfile
import time
import select
import re
import struct
import os
from PIL import Image

## Rachet Read Me:

#set up a conda environment with python 3.6 and the following:
# QT, TBB, Eigen, Pillow, Plyfile, pptk
#
#download a 'ply' test point cloud and name it 'points.ply' in the same directory as this code

#
#make an empty folder in the same directory with the name 'rec'
#

data = plyfile.PlyData.read('./points.ply')['vertex']
xyz = np.c_[data['x'], data['y'], data['z']]
rgb = np.c_[data['red'], data['green'], data['blue']]
n = np.c_[data['nx'], data['ny'], data['nz']]
#n = np.zeros_like(xyz)

UDP_IP = "127.0.0.1"
UDP_PORT = 8001
UDP_PORT_SEND = 8000

v = pptk.viewer(xyz, debug=True)
v.attributes(rgb / 255., 0.5 * (1 + n))
# attr1 = pptk.rand(100)     # 100 random scalars
# attr2 = pptk.rand(100, 3)  # 100 random RGB colors
# attr3 = pptk.rand(100, 4)  # 100 random RGBA colors
# attr4 = pptk.rand(1)       # 1 random scalar
# attr5 = pptk.rand(1, 3)    # 1 random RGB color
# attr6 = pptk.rand(1, 4)    # 1 random RGBA color
# v.attributes(attr1, attr2, attr3, attr4, attr5, attr6)

v.set(show_info = False, show_axis = False, show_grid = False, bg_color = [1,1,1,1])
rod = 0

send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
recv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
recv.bind((UDP_IP, UDP_PORT))

timeout = 5
readable, _, _ = select.select([recv], [], [], timeout)

#print(v.get('eye'))
while readable:

    if msvcrt.kbhit():
        # Get the ASCII value of the key pressed
        key = ord(msvcrt.getch())
        # If the key pressed is 'q', break out of the loop
        if key == ord('q'):
            break
    


    poses = []

    data, addr = recv.recvfrom(1024)

    if not data:
        break

    # decode the received binary data from Unity
    data_str = data.decode('UTF-8')
    #regex to parse (x,y,z)
    pattern = "\((-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)\)"
    result = re.findall(pattern, data_str)
    #print(result)
    if result: 
        x, y, z = result[0]
        # Extract the values
        #print(f"X: {x}, Y: {y}, Z: {z}")
        #if(rod < 5):
        #    print(poses)
        poses = [[float(x), float(y), float(z) + 48, 0, np.pi/4, 5]]
        # if (rod < 10):
        print(poses)

        v.play(poses, 2 * np.arange(len(poses)), repeat=False, interp='linear')
        
        path = r'D:\Unity\AzureKinect\Assets\PPTK Textures\img.png'

        # if (os.path.isfile(path)): #'./rec/img.png'
        #     #print("there is file")
        #     os.remove(path)
        
        with open(path, "w") as file:
            v.capture(path)
            file.flush()  # flush the buffer
            print("i create image")
            time.sleep(2)
        

        #time.sleep(0.1)
        #open the image file
        # with open('./rec/img.png', "rb") as f:
        #     image_bytes = f.read()
        # #Pack the length of the image bytes as a 4-byte integer
        # length = len(image_bytes)
        # length_bytes = struct.pack("!I", length)

        # send.sendto(image_bytes, (UDP_IP, UDP_PORT_SEND))
        #send.sendto(b"HELLO SIR", (UDP_IP, UDP_PORT_SEND))
        
        rod = rod + 1

        readable, _, _ = select.select([recv], [], [], timeout)