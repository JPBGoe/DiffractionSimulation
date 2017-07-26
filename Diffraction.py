import math
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

# the cartesian cross is centered in the input image


class Diffraction:
    dist = 0
    start_amp = []
    start_phase = []
    start_pos = []
    fin_amp = []
    fin_phase = []
    fin_pos = []
    wavevec = 1 


    res = []

    def set_input(self,ini_amp,ini_pos):
        self.start_amp = np.abs(ini_amp)
        self.start_phase = np.angle(ini_amp)
        self.start_pos = ini_pos

    def set_output(self,fin_pos):
        self.fin_pos = fin_pos

    def set_dist(self, dist):
        self.dist = dist

    def sphere_wave(self,origin,at):    #origin =(x_ind,z_ind) with respect to the image origin not the center
        # calculate the distance
        distance = math.sqrt((fin_pos[at[0]]-start_pos[origin[0]])**2 + dist**2 + (fin_pos[at[1]]-start_pos[origin[1]])**2)
        
        # calculate the object origin
        obj_ori = (len(start_amp) // 2,len(start_amp[0]) // 2)

        # phase
        phase = ( (wavevec * distance) % (math.pi*2) ) + startphase[origin(0) + obj_ori(0)][origin(1)+obj_ori(1)]
        phase = ( phase % (math.pi*2))

        # final amplitude at the place "at"
        return (math.cos(phase) + 1j*math.sin(phase)) * start_amp[origin(0) + obj_ori(0)][origin(1)+obj_ori(1)]


        


    
    def wave(self,ori,dest):          # relative to the major optical axis in the center of __amp_0
        if self.amp_0[ori[0]][ori[1]] == 0.0:
            return 0

        # calculate the distances
        r = [(dest[0]-ori[0]),self.dist,(dest[1]-ori[1])]
        R = math.sqrt(r[0]**2 + r[1]**2 + r[2]**2)

        # correct for relative position
        ori[0] = ori[0] + len(self.amp_0) // 2        # x coordinate
        ori[1] = ori[1] + len(self.amp_0[0]) // 2     # z coordinate
        dest[0] = dest[0] + len(self.res) // 2        # x coordinate
        dest[1] = dest[1] + len(self.res[0]) // 2     # z coordinate
        if not (0 <= ori[0] and ori[0] < len(self.amp_0)):
            print("ori[0]=" + str(ori[0]))
        if not (0 <= ori[1] and ori[1] < len(self.amp_0[0])):
            print("ori[0]=" + str(ori[1]))

        # calculate the phase for a homogenious propagation
        phase = self.wavevec * R + self.phase_0[ori[0]][ori[1]] # - w*t
        phase = (phase % (2*math.pi))

        # Calculate the complex amplitude at the destination
        return (math.cos(phase) + 1j* math.sin(phase))*self.amp_0[ori[0]][ori[1]]/R
    

    def calculate(self,amp_0,phase_0,img_size,wavevec):
        self.amp_0 = amp_0
        self.phase_0 = phase_0
        self.wavevec = wavevec

        # init of the image plain
        tmp = []
        for i in range(img_size[0]):
            tmp.append(0 + 1j*0)

        for j in range(img_size[1]):
            self.res.append(deepcopy(tmp))

        # calculate
        for i in list(range(len(self.res))):
            for j in list(range(len(self.res[0]))):
                for k in list(range(len(self.amp_0))):
                    for l in list(range(len(self.amp_0[0]))):
                        rel_i = i - len(self.res) // 2
                        rel_j = j - len(self.res[0]) // 2
                        rel_k = k - len(self.amp_0) // 2
                        rel_l = l - len(self.amp_0[0]) // 2
                        self.res[i][j] += self.wave([rel_k,rel_l],[rel_i,rel_j])
        return self.res        
        
        
    













    
# Testing

osi = [30,30]
fsi = [100,100]
tmp = []
for i in list(range(osi[1])):
    tmp.append(0.0)

ph = []
amp = []
for j in list(range(osi[0])):
    ph.append(deepcopy(tmp))
    amp.append(deepcopy(tmp))

for i in list(range(osi[0])):
    for j in list(range(osi[1])):
        if (i-osi[0]//2)**2 + (j-osi[1]//2)**2 <= 5**2:
            amp[i][j] = 1.0

#print(amp)


plt.figure(1)
plt.imshow(amp)
plt.colorbar()


ft = np.fft.fft2(amp)
#print(len(ft))
plt.figure(2)
plt.imshow(np.abs(ft))
plt.colorbar()

test = Diffraction()
test.set_dist(1000)
result = test.calculate(amp,ph,fsi,2*math.pi*10**9/600)


plt.figure(3)
plt.imshow(np.abs(result))
plt.colorbar()
plt.show()

