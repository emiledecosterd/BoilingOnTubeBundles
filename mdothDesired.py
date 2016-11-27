'''
Guess Water Mass Flow Rate (kg/m²s)
'''
import math
import numpy as np
from properties import get_properties
from CoolProp.CoolProp import PropsSI

# Estimate mass flow rate

def guessMassFlow(opCond, geom, Th_in, Th_outGuess, qGuess):
	# qguess in [W/m²]
	# All temperature in [K]

	cp = PropsSI('C','T',(Th_in+Th_outGuess)/2,'Q',0.0,'Water')
	Di = geom['D']-2*geom['t']
	mdot_h = (qGuess*math.pi*Di*geom['L'])/(cp*abs(Th_outGuess-Th_in)) # [kg/s]
	mdot_h = mdot_h/(geom['N']*math.pi*Di**2/4) # [kg/m²s]

	return mdot_h
