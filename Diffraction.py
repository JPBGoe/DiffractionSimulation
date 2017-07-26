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
        #print(str(r[0]) + " " + str(r[1]) + " "  + str(r[2]) + " " + str(R))

        # correct for relative position
        ori[0] = ori[0] + len(self.__amp_0) // 2        # x coordinate
        ori[1] = ori[1] + len(self.__amp_0[0]) // 2     # z coordinate
        dest[0] = dest[0] + len(self.__res) // 2        # x coordinate
        dest[1] = dest[1] + len(self.__res[0]) // 2     # z coordinate
        if not (0 <= ori[0] and ori[0] < len(self.__amp_0)):
            print("ori[0]=" + str(ori[0]))
        if not (0 <= ori[1] and ori[1] < len(self.__amp_0[0])):
            print("ori[0]=" + str(ori[1]))

        # calculate the phase for a homogenious propagation
        phase = self.__wavevec * R + self.__phase_0[ori[0]][ori[1]] # - w*t
        phase = (phase % (2*math.pi))

        # Calculate the complex amplitude at the destination
        return (math.cos(phase) + 1j* math.sin(phase))*self.__amp_0[ori[0]][ori[1]]
    

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

        # calculate
        for i in list(range(len(self.__res))):
            for j in list(range(len(self.__res[0]))):
                for k in list(range(len(self.__amp_0))):
                    for l in list(range(len(self.__amp_0[0]))):
                        rel_i = i - len(self.__res) // 2
                        rel_j = j - len(self.__res[0]) // 2
                        rel_k = k - len(self.__amp_0) // 2
                        rel_l = l - len(self.__amp_0[0]) // 2
                        self.__res[i][j] += self.__wave([rel_k,rel_l],[rel_i,rel_j])
      

        return self.__res        
        
        
        
# Testing

osi = [21,21]
fsi = [40,40]
tmp = []
for i in list(range(osi[1])):
    tmp.append(1.0)

ph = []
amp = []
for j in list(range(osi[0])):
    ph.append(deepcopy(tmp))
    amp.append(deepcopy(tmp))


ft = np.fft.fft2(amp)
plt.figure(0)
plt.imshow(np.abs(ft))
plt.colorbar()

test = Diffraction(10000)
result = test.calculate(amp,ph,fsi,2*math.pi*10**9/600)


plt.figure(1)
plt.imshow(np.abs(result))
plt.colorbar()
plt.show()

