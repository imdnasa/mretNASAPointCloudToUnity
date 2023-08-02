import pptk
import numpy as np
import plyfile
import socket
import time
import msvcrt
import select
import re
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

v = pptk.viewer(xyz)
v.attributes(rgb / 255., 0.5 * (1 + n))

#UDP Socket
UDP_IP = "127.0.0.1"
UDP_PORT = 8001
UDP_PORT_SEND = 8000


MESSAGE = b"HI UNITY"
    
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))
v.set(show_info = False, show_axis = False, show_grid = False, bg_color = [1,1,1,1])

timeout = 5
rot = 0
readable, _, _ = select.select([sock], [], [], timeout)
while True:
    poses = []
    data, addr = sock.recvfrom(1024)
    print(data)
    data_str = data.decode("utf-8")
    pattern = "\((-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)\)"
    result = re.findall(pattern, data_str)
    if result: 
        x, y, z = result[0]
        #print(result[0])
        #print(x,y,z)
        poses = [[float(x), float(y), float(z) + 47, 0, np.pi/4, 5]]
        #print(poses[0], '\n')
        v.play(poses, 2 * np.arange(len(poses)), repeat=False, interp='linear')
        v.capture('./rec/img' + str(rot) + '.png')
        rot = rot + 1
        time.sleep(1)
        sock2.sendto(MESSAGE, (UDP_IP, UDP_PORT_SEND))
        readable, _, _ = select.select([sock], [], [], timeout)
    if msvcrt.kbhit():
        # Get the ASCII value of the key pressed
        key = ord(msvcrt.getch())
        # If the key pressed is 'q', break out of the loopq
        if key == ord('q'):
            break
    


# poses.append([x, y, z, 1 * np.pi/2, np.pi/4, 5])
# poses.append([0, 0, 47, 2 * np.pi/2, np.pi/4, 5])
# poses.append([0, 0, 47, 3 * np.pi/2, np.pi/4, 5])
# poses.append([0, 0, 47, 4 * np.pi/2, np.pi/4, 5])



#v.play(poses,2 * np.arange(len(poses)), tlim= 3, repeat=False, interp='linear')
#v.play(poses, 2 * np.arange(len(poses)), repeat=True, interp='linear')
#v.set(r = 0) distance from lookat
#
#v.record('./rec', poses, 2 * np.arange(len(poses)), interp='linear', fps = 1, prefix = 'img_', ext='png')

###################################################################

#takes screenshot of current view and saves as png (NOT TRANSPARENT)
#v.capture('./rec/img.png')

###################################################################
# Load the captured image with Pillow and convert the white background to transparent
# image = Image.open('./rec/img_1.png')
# image = image.convert('RGBA')
# data = image.getdata()
# new_data = []
# for item in data:
#     if item[0] == 255 and item[1] == 255 and item[2] == 255:
#         new_data.append((255, 255, 255, 0))
#     else:
#         new_data.append(item)
# image.putdata(new_data)

# # # Save the image with a transparent background
# image.save('image_transparent.png')