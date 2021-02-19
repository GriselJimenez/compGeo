import math
from uncertainties import umath
from SphToCartU import SphToCartU
from CartToSphU import CartToSphU
from Pole import Pole

def AnglesU(trd1,plg1,trd2,plg2,ans0):
	'''
	AnglesU calculates the angles between two lines,
	between two planes, the line which is the intersection
	of two planes, or the plane containing two apparent dips

	AnglesU operates on two lines or planes with
	trend/plunge or strike/dip equal to trd1/plg1 and
	trd2/plg2. These angles have uncertainties

	ans0 is a character that tells the function what
	to calculate:

		ans0 = 'a' -> plane from two apparent dips
		ans0 = 'l' -> the angle between two lines

		In the above two cases, the user sends the trend
		and plunge of two lines

		ans0 = 'i' -> the intersection of two planes
		ans0 = 'p' -> the angle between two planes
 
		In the above two cases the user sends the strike
		and dip of two planes in RHR format

	NOTE: Input/Output angles are in radians and they
	have uncertainties in radians

	Angles uses functions SphToCartU, CartToSphU and Pole
	It also uses the uncertainties package from
	Eric O. Lebigot

	Based on Python function Angles
	'''
	# If planes have been entered
	if ans0 == 'i' or ans0 == 'p':
		k = 1
	# Else if lines have been entered
	elif ans0 == 'a' or ans0 == 'l':
		k = 0
	
	# Calculate the direction cosines of the lines or poles to planes
	cn1, ce1, cd1 = SphToCartU(trd1,plg1,k)
	cn2, ce2, cd2 = SphToCartU(trd2,plg2,k)
	
	# If angle between 2 lines or between the poles to 2 planes
	if ans0 == 'l' or ans0 == 'p':
		# Use dot product = Sum of the products of the direction cosines
		ans1 = umath.acos(cn1*cn2 + ce1*ce2 + cd1*cd2)
		ans2 = math.pi - ans1
	
	# If intersection of two planes or pole to a plane containing two
	# apparent dips
	if ans0 == 'a' or ans0 == 'i':
		# If the 2 planes or apparent dips are parallel return an error
		# Uncertainties are not needed for this comparison
		if trd1.n == trd2.n and plg1.n == plg2.n:
			raise ValueError('Error: lines or planes are parallel')
		# Else use cross product
		else:
			cn = ce1*cd2 - cd1*ce2
			ce = cd1*cn2 - cn1*cd2
			cd = cn1*ce2 - ce1*cn2
			# Make sure the vector points down into the lower hemisphere
			if cd < 0.0:
				cn = -cn
				ce = -ce
				cd = -cd
			# Convert vector to unit vector by dividing it by its length
			r = umath.sqrt(cn*cn+ce*ce+cd*cd)
			# Calculate line of intersection or pole to plane
			trd, plg = CartToSphU(cn/r,ce/r,cd/r)
			# If intersection of two planes
			if ans0 == 'i':
				ans1 = trd
				ans2 = plg
			# Else if plane containing two dips, calculate plane from its pole
			elif ans0 == 'a':
				ans1, ans2 = Pole(trd,plg,0)
	
	return ans1, ans2