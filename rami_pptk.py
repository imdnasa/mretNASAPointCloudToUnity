import socket
import msvcrt
import pptk
import numpy as np
import plyfile
import time
import select
import re
import struct
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

rec_port = 8001
send_port = 8000

v = pptk.viewer(xyz)
v.attributes(rgb / 255., 0.5 * (1 + n))

v.set(show_info = False, show_axis = False, show_grid = False, bg_color = [1,1,1,1])
rod = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', rec_port)) # replace with the same IP address and port number as in Unity
    s.listen()
    conn, addr = s.accept()
    with conn:                
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_out:
            s_out.bind(('localhost', send_port)) 
            while True:
                poses = []
                data = conn.recv(1024)
                if not data:
                    break
                if msvcrt.kbhit():
                    # Get the ASCII value of the key pressed
                    key = ord(msvcrt.getch())
                    # If the key pressed is 'q', break out of the loop
                    if key == ord('q'):
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
                    poses = [[float(x), float(y), float(z), 0, np.pi/4, 5]]
                    print(poses)
                    v.play(poses, 2 * np.arange(len(poses)), repeat=False, interp='linear')
                    v.capture('./rec/img' + str(rod) + '.png')
                    #open the image file
                    with open('./rec/img' + str(rod) + '.png', "rb") as f:
                        image_bytes = f.read()
                    # Pack the length of the image bytes as a 4-byte integer
                    length = len(image_bytes)
                    length_bytes = struct.pack("!I", length)
                    # Send the length of the image bytes first
                    s_out.sendto(length_bytes, ("localhost", send_port))

                    # Send the image bytes
                    s_out.sendto(image_bytes, ("localhost", send_port))
                    rod = rod + 1
                    time.sleep(0.5)
