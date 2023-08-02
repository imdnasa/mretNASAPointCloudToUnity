import socket
import msvcrt
import pptk
import numpy as np
import plyfile
import time
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

rod = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 8001)) # replace with the same IP address and port number as in Unity
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            poses = []
            data = conn.recv(1024)
            if not data:
                break
            if msvcrt.kbhit():
                # Get the ASCII value of the key pressed
                key = ord(msvcrt.getch())
                # If the key pressed is 'q', break out of the loopq
                if key == ord('q'):
                    break
            print(str(data))
            print()
            #pattern = "\((-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)\)"
            position = [x for x in data.decode().strip().split(',') if x != '']
            # print(position)
            # print()
            # print()
            x = float(position[0])
            y = float(position[1])
            z = float(position[2])
            poses = [[float(x), float(y), float(z) + 47, 0, np.pi/4, 5]]
            #print(poses)
            v.play(poses, 2 * np.arange(len(poses)), repeat=False, interp='linear')
            v.capture('./rec/img' + str(rod) + '.png')
            rod = rod + 1
            time.sleep(1)

            #print(position)
