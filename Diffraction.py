import math
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


class Diffraction:
    ini_amp = []
    fin_amp = []
    pix_ini = (0.001,0.001)     # dx,dy
    pix_fin = (0.001,0.001)     # dx,dy
    wavevec = 0


    res = []

    def set_pixel(self,pix_ini=(0.001,0.001),pix_fin=(0.001,0.001)):
        self.pix_ini = pix_ini
        self.pix_fin = pix_fin 

    def sphere_wave(self,origin,at,ini_amp):    #origin =(x,y,z), at =(x,y,z) with respect to the major axis in kartesian coordinates, ini_amp complex amplitude at the origin
        if np.abs(ini_amp) == 0.0:
            return 0 + 0j

        # distancevetor
        r = ((at[0]-origin[0]),(at[1]-origin[1]))
        dist = (r[0]**2 + self.dist**2 + r[1]**2)**(0.5)

        # phase
        phase = np.angle(ini_amp) - (self.wavevec*dist % (2*math.pi)) # +wt 
        
        # output a complex number at "at" as the diffraction part of the wave starting in origin with complex ini_amp 
        return (math.cos(phase) + 1j*math.sin(phase)) * np.abs(ini_amp)/dist

    def calculate(self,ini_amp,dist,wavevec,fin_amp):
        self.ini_amp = ini_amp
        self.fin_amp = fin_amp
        self.wavevec = wavevec
        self.dist = dist

        # Create array with positions for the first array: Object in first quadrant from botom to top
        ini_pos = np.zeros((len(ini_amp),len(ini_amp[0])), dtype=(float,2))
        xpos = (-len(ini_amp)*self.pix_ini[0] + self.pix_ini[0])/2
        for i in list(range(len(ini_amp))):
            ypos = (-len(ini_amp[1])*self.pix_ini[1] + self.pix_ini[1])/2
            for j in list(range(len(ini_amp[0]))):
                ini_pos[i][j] = (xpos,ypos)
                ypos += self.pix_ini[1]
            xpos += self.pix_ini[0]

        # Create positions of the second array
        fin_pos = np.zeros((len(fin_amp),len(fin_amp[0])), dtype=(float,2))
        xpos = (-len(fin_amp)*self.pix_fin[0] + self.pix_fin[0])/2
        for i in list(range(len(fin_amp))):
            ypos = (-len(fin_amp[1])*self.pix_fin[1] + self.pix_fin[1])/2
            for j in list(range(len(fin_amp[0]))):
                fin_pos[i][j] = (xpos,ypos)
                ypos += self.pix_fin[1]
            xpos += self.pix_fin[0]

        
        # Calculate the distance
        print("Start",end="\r")
        for i in list(range(len(fin_amp))):
            print(str(100*i/len(fin_amp)) + " % finished",end="\r")
            for j in list(range(len(fin_amp[0]))):
                for k in list(range(len(ini_amp))):
                    for l in list(range(len(ini_amp[0]))):
                        self.fin_amp[i][j] += self.sphere_wave(ini_pos[k][l],fin_pos[i][j],ini_amp[k][l])
        print("                   ",end="\r")
        print("Done")


    def get_intensity(self):
        return np.abs(self.fin_amp)

    def get_phase(self):
        return np.angle(self.fin_amp)



# Create the diffraction object
obj_size = (50,50)
obj = np.zeros(obj_size,dtype=np.complex_)
for i in list(range(0,obj_size[0])):
    for j in list(range(0,obj_size[1])):
        obj[i][j] = 1000 + 1j*0

# plot the diffraction object
plt.figure(1)
plt.imshow(np.abs(obj))
plt.colorbar()
plt.show()

# Parameters
wv = 2*math.pi*10**9/600        # [wv] = 1/m
dist = 0.5                     # [dist] = m

# Create the the image plane
img_size = (100,100)
img = np.zeros(img_size,dtype=np.complex_)

# Do the calculation
diff = Diffraction()
diff.set_pixel(pix_ini=(10**(-6),10**(-6)))
diff.calculate(obj,dist,wv,img)
 
tmp = diff.get_intensity()
plt.figure(2)
plt.imshow(tmp)
plt.colorbar()
plt.show()

plt.figure(3)
plt.plot(tmp[img_size[0]//2])
plt.show()

