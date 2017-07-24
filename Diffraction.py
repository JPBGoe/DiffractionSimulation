from copy import deepcopy
import math

class DiffractionException(Exception):
    pass

class Diffraction:
    """ Calalcultes the diffraction pattern of an object in a given distance: xz is the plane with the object and the wave propagetes in positive y direction"""

    def __init__(self,dist):
        self.__dist = self.setDist(dist)

    def setDist(self,dist):
        if dist <= 0:
            raise DiffractionException("Distance between object and image plain needs to be greater 0")	
        else:
            self.__dist = dist
	

    def __set_object_plain(self,shape):
        """ The center of the amplitude shape is aligned to major optical axis """
        self.__obj = shape	# 1 coord: array of array as x coord, 2 coord: array of int as z coord
		
        # Check for number of columns
        if (len(shape) - 1) % 2 != 0:
            raise DiffractionException("Input object must have an odd number of columns")

        # Check for shape being an rectangle
        zlength = -1
        for s in shape:
            if zlength > 0 and z != len(s):
                raise DiffractionException("zlength differ in shape object")
            else:
                zlength = len(s)

        if (zlength -1) % 2 != 0:
            raise DiffractionException("Input object must have an odd number of rows")

        self.__obj_xs = len(shape)
        self.__obj_zs = len(shape[0])

        
    def set_image_plain(self,x_border, z_border):
        """ xsize and ysize will be semetrically separated around the main optical axis """
        if x_border <= 0 or z_border <= 0:
            raise DiffractionException("Image Plain to small")
		
        # Create template column
        tmp = []
        for i in range(z_border*2 + 1):
            tmp.append(0 + 0 *1j)

        self.__img = []
        # Create the rows with template column deep copies
        for i in range(x_border*2 + 1):
            self.__img.append(deepcopy(tmp))

        # memorize the size of the image plane
        self.__img_xs = 2*x_border + 1
        self.__img_zs = 2*z_border + 1

    def __set_wavevec(self,k):
        # Check properties of k
        if len(k) != 3:
            raise DiffractionException("Wave vector has 3 dimensions")       

        self.k = k

    def __set_addphase(self,addphase):
        self.addphase = addphase

    def __wave(self,fromx,fromz,tox,toz): # positions relative to the centers
        """ calculates the complex amplitude at a given position from a source """
        # Distances
        rx = tox - fromx
        ry = dist
        rz = toz - fromz

        # Calculate the indices
        x_obj_ind = (self.__obj_xs - 1) / 2 + fromx 
        z_obj_ind = (self.__obj_zs - 1) / 2 + fromz
    
        # Calculate intermediates
        path_length =  self.k[0]*rx + self.k[1]*ry + self.k[2]*rz 
        phase = path_length + self.addphase[x_obj_ind][z_obj_ind]     # left out wt
        
        return (math.cos(phase) + math.sin(phase)*1j) * self.__obj[x_obj_ind][z_obj_ind]/eukl_dist
            

    def __diffract(self):
        obj_x = list(range(-((self.__obj_xs - 1) / 2), ((self.__obj_xs - 1) / 2) + 1))       
        obj_z = list(range(-((self.__obj_zs - 1) / 2), ((self.__obj_zs - 1) / 2) + 1))       
        img_x = list(range(-((self.__img_xs - 1) / 2), ((self.__img_xs - 1) / 2) + 1))       
        img_x = list(range(-((self.__img_zs - 1) / 2), ((self.__img_zs - 1) / 2) + 1)) 

        for i in img_x:
            for j in img_z:
                for k in obj_x:
                    for l in obj_z:
                        self.__img[((self.__img_xs - 1) / 2) + i][((self.__img_zs - 1) / 2) + j] += self.__wave(k,l,i,j)   

        return self.__img

    def calculate_pattern(self,obj,img_x_b,img_z_b,wavevec,init_phase):
        self.__set_object_plain(obj)
        self.__set_image_plain(img_x_b,img_z_b)
        self.__set_wavevec(wavevec)
        self.__set_addphase(init_phase)

        return self.__diffract()
