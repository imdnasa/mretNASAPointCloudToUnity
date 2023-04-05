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
import io

## Rachet Read Me:

#set up a conda environment with python 3.6 and the following:
# QT, TBB, Eigen, Pillow, Plyfile, pptk
#
#download a 'ply' test point cloud and name it 'points.ply' in the same directory as this code

#
#make an empty folder in the same directory with the name 'rec'
#

#To do for next time figuring out how struct works within this method below since we're trying to capture an image here
#we want to just be able to get byte data here. 

class MRET_Viewer(pptk.viewer):
     
     def _pack_string(self, string):
        return struct.pack('Q', len(string)) + struct.pack(str(len(string)) + 's', string.encode('ascii'))

     def capture(self, filename):

        #print(os.path.abspath(filename))

        img_bytes = struct.pack('b', 11) # + self._pack_string(os.path.abspath(filename)) */
        super().__send(img_bytes)


    

data = plyfile.PlyData.read('./points.ply')['vertex']
xyz = np.c_[data['x'], data['y'], data['z']]
rgb = np.c_[data['red'], data['green'], data['blue']]
n = np.c_[data['nx'], data['ny'], data['nz']]

UDP_IP = "127.0.0.1"
UDP_PORT = 8001

v = MRET_Viewer(xyz, debug=True)
v.attributes(rgb / 255., 0.5 * (1 + n))

v.set(show_info = False, show_axis = False, show_grid = False, bg_color = [1,1,1,1])

send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
recv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
recv.bind((UDP_IP, UDP_PORT))

timeout = 120
readable, _, _ = select.select([recv], [], [], timeout)

numb_increments = 0
allDeltaTimes = 0

while readable:

    start = time.time()

    if msvcrt.kbhit():
        key = ord(msvcrt.getch())
        if key == ord('q'):
            break
    


    poses = []

    #Receive data from socket
    data, addr = recv.recvfrom(1024)

    if not data:
        break

    # decode the received binary data from Unity
    data_str = data.decode('UTF-8')
    #regex to parse (x,y,z)
    pattern = "\((-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)\)"
    result = re.findall(pattern, data_str)

    if result: 

        #Stores extracted data into poses
        x, y, z = result[0]
        poses = [[float(x), float(y), float(z) + 48, 0, np.pi/4, 5]]
        
        #For DEBUG purposes
        print(poses)

        #reorients the camera according to poses
        v.play(poses, 2 * np.arange(len(poses)), repeat=False, interp='linear')

        #new try to capture image values


        
        #Stores the file path to the image as a string
        fpath = r'D:\Unity\AzureKinect\Assets\PPTK Textures\img.png'
        imagebytes = v.capture(fpath)
        print(imagebytes)
        print(type(imagebytes))
        # image = Image.open(io.BytesIO(imagebytes))
        # image.show()
        # # Deletes old image because 'v.capture' doesn't overwrite
        # if os.path.exists(fpath):
        #     try:
        #         os.remove(fpath)
        #         print(f"The file {fpath} has been deleted.")
        #     except PermissionError:
        #         print(f"PermissionError: Could not delete the file {fpath}.")
        # else:
        #     print(f"The file {fpath} does not exist.")

        # #Saves the new image
        # with open(fpath, "w") as file:
        #     img_bytes = v.capture()
        #     # file.flush()  # flush the buffer
        #     print("i create image")

    

    readable, _, _ = select.select([recv], [], [], timeout)

    end = time.time()
    numb_increments += 1
    allDeltaTimes += (end - start)

    averageFPS = 1/(allDeltaTimes/numb_increments)

    print("AVERAGE FPS: " + str(averageFPS))
