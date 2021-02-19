import numpy as np
import matplotlib.pyplot as plt
from Pole import Pole
from GeogrToView import GeogrToView
from SmallCircle import SmallCircle
from GreatCircle import GreatCircle

def Stereonet(trdv,plgv,intrad,sttype):
	'''
	Stereonet plots an equal angle or equal area stereonet
	of unit radius in any view direction
	
	trdv = trend of view direction
	plgv = plunge of view direction
	intrad = interval in radians between great or small circles
	sttype = type of stereonet. 0 = equal angle, 1 = equal area
	
	NOTE: All angles should be entered in radians
	
	Stereonet uses functions Pole, GeogrToView,
	SmallCircle and GreatCircle
	
	Python function translated from the Matlab function
	Stereonet in Allmendinger et al. (2012)
	'''
	pi = np.pi
	# some constants
	east = pi/2.0
	west = 3.0*east
	
	# Plot stereonet reference circle
	r = 1.0 # radius pf stereonet
	TH = np.arange(0,360,1)*pi/180
	X = r * np.cos(TH)
	Y = r * np.sin(TH)
	
	# Make a larger figure
	plt.rcParams['figure.figsize'] = [15, 7.5]
	plt.plot(X,Y, 'k')
	plt.axis ([-1, 1, -1, 1])
	plt.axis ('equal')
	plt.axis('off')
	
	# Number of small circles
	nCircles = int(pi/(intrad*2.0))
	
	# small circles, start at North
	trd, plg = 0.0, 0.0
	
	# If view direction is not the default (trdv=0,plgv=90)
	# transform line to view direction
	if trdv != 0.0 or plgv != east:
		trd, plg = GeogrToView(trd,plg,trdv,plgv)
	
	# Plot small circles
	for i in range(1,nCircles+1):
		coneAngle = i*intrad
		path1, path2, np1, np2 = SmallCircle(trd,plg,coneAngle,sttype)
		plt.plot(path1[np.arange(0,np1),0], path1[np.arange(0,np1),1], color='gray',linewidth=0.5)
		if np2 > 0:
			plt.plot(path2[np.arange(0,np2),0], path2[np.arange(0,np2),1], color='gray', linewidth=0.5)
	
	# Great circles
	for i in range(0,nCircles*2+1):
		# Western half
		if i <= nCircles:
			# Pole of great circle
			trd = west
			plg = i*intrad
			# Eastern half
		else:
			# Pole of great circle
			trd = east
			plg = (i-nCircles)*intrad
		# If pole is vertical shift it a little bit
		if plg == east:
			plg = plg * 0.9999
		# If view direction is not the default 
		# (trdv = 0,plgv = 90)
		# transform line to view direction
		if trdv != 0.0 or plgv != east:
			trd, plg = GeogrToView(trd,plg,trdv,plgv)
		# Compute plane from pole
		strike, dip = Pole(trd,plg,0)
		# Plot great circle
		path = GreatCircle(strike,dip,sttype)
		plt.plot(path[:,0],path[:,1],color='gray',linewidth=0.5)