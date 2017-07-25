import math
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

class DiffException(Exception):
    pass


class Diffraction:
    __dist = 0
    __amp_0 = []
    __phase_0 = []
    __res = []
    __wavevec = 0

    
    def __init__(self,dist):
        self.__dist = dist              # image and object plane distance

    
    def __wave(self,ori,dest):          # relative to the major optical axis in the center of __amp_0
        ori = ori                       # x component, z component
        dest = dest                     # x component, z component

        # calculate the distances
        r = [(dest[0]-ori[0]),self.__dist,(dest[1]-ori[1])]
        R = math.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
        print(str(r[0]) + " " + str(r[1]) + " "  + str(r[2]) + " " + str(R))

        # correct for relative position
        ori[0] = ori[0] + len(self.__amp_0) // 2        # x coordinate
        ori[1] = ori[1] + len(self.__amp_0[0]) // 2     # z coordinate
        dest[0] = dest[0] + len(self.__res) // 2        # x coordinate
        dest[1] = dest[1] + len(self.__res[0]) // 2     # z coordinate

        # calculate the phase for a homogenious propagation
        phase = self.__wavevec * R + self.__phase_0[ori[0]][ori[1]] # - w*t
        phase = (phase % 2* math.pi)

        # Calculate the complex amplitude at the destination
        return (math.cos(phase) + 1j* math.sin(phase))*self.__amp_0[ori[0]][ori[1]]/R
    

    def calculate(self,amp_0,phase_0,img_size,wavevec):
        self.__amp_0 = amp_0
        self.__phase_0 = phase_0
        self.__wavevec = wavevec

        # init of the image plain
        tmp = []
        for i in range(img_size[0]):
            tmp.append(0 + 1j*0)

        for j in range(img_size[1]):
            self.__res.append(deepcopy(tmp))

        # ranges
        lengthes = [len(self.__amp_0) // 2,len(self.__amp_0[0]) // 2,len(self.__res) // 2,len(self.__res[0]) // 2]
        
        # calculate
        for i in list(range(-lengthes[2],len(self.__res) - lengthes[2])):
            for j in list(range(-lengthes[3],len(self.__res[0]) - lengthes[3])):
                for k in list(range(-lengthes[1],len(self.__amp_0) - lengthes[1])):
                    for l in list(range(-lengthes[2],len(self.__amp_0) - lengthes[2])):
                        self.__res[i][j] += self.__wave([k,l],[i,j])
      

        return self.__res        
        
        
        
# Testing
tmp = []
for i in range(11):
    tmp.append(0)

ph = []
amp = []
for j in range(11):
    ph.append(deepcopy(tmp))
    amp.append(deepcopy(tmp))

amp[4][5] = 1
amp[5][5] = 1
amp[6][5] = 1

       
fsi = [21,21]

test = Diffraction(100)
result = test.calculate(amp,ph,fsi,2*math.pi*10**9/600)

I = []
for s in range(fsi[0]):
    tmp = []
    for t in range(fsi[1]):
         tmp.append(float(result[s][t]*np.conjugate(result[s][t])))
    I.append(tmp)

#print(I)

img = plt.imshow(np.real(result))
plt.show()

img2 = plt.plot(np.real(result[5]),label="Crosssection")
plt.show()

