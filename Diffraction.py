class DiffractionException(Exception):
	pass

class Diffraction:
	""" Calalcultes the diffraction pattern of an object in a given distance: xz is the plane with the object and the wave propagetes in positive y direction"""
	
	__slot__ = []

	def __init__(self,dist):
		self.__dist = self.setDist(dist)

	def setDist(self,dist):
		if dist <= 0:
			raise DiffractionException("Distance between object and image plain needs to be greater 0")	
		else:
			self.__dist = dist
	

	def input_object(self,centerx,centerz,shape):
		self.__obj_xc = centerx
		self.__obj_zc = centerz
		self.__obj_shape = shape	# 1 coord: array of array as x coord, 2 coord: array of int as z coord
		
		# Check if they fit
		if not(centerx in range(len(shape))):
			raise DiffractionException("Center of the object in x direction is outside the shape of the object")
		
		# Check if for each x the numbers of z are equal
		zlength = -1
		for s in shape:
			if zlength > 0 and z != len(s):
				raise DiffractionException("zlength differ in shape object")
			else:
				zlength = len(s)
		
