'''
Space optimization (Inputs)
'''

import math
import numpy as np


def spaceOptimization(NTubes, Sq, Sl, D, layout, rectWidth, rectHeight):
	# 1) We know rectSize and tube pitchs (Sq, Sl)
	if not NTubes:
		if layout is 'InLine':
			NCols = floor(rectWidth/Sq)
			NRows = floor(rectHeight/Sl)
			


