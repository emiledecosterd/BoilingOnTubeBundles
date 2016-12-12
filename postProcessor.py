## 	@package postProcessor
#	Load, and save all the results 
#	
#	This class will use the PostProcess class to create plots images and text files with all
#	the data.

# Packages for the post processing
import sys,os
import time
import numpy as np
from Postprocess import *

# Qt and GUI packages
from PyQt5.QtCore import QObject, pyqtSignal
from error import Error

## 	PostProcessor
#	Data manager used at the end of each simulation to save the data
class PostProcessor(QObject):

	## 	Initialize data
	#	@param config Configuration dictionnary
	#	@param results Results diactionnary
	def __init__(self, config, results):
		self.config = config
		self.results = results

		# Save the time at initialization
		self.config['initTime'] = (time.strftime("%Y%m%H%M%S"))

		# Create the directory
		os.makedirs('figures/' + self.config['initTime'])

		# Save the plots
		self.savePlots()

		# Write data file
		self.writeFile()

	## Save the plot
	#	@param config Configuration dictionnary
	#	@param results Results diactionnary
	def savePlots(self):

		# Save the boiler plots
		plot_boiler(self.config, self.results, False)

		# Save teh xc pipe plot
		plot_xc_pipe(self.config, self.results, False)

		# Compute other calculation
		self.results = PostProcess_calc(self.config, self.results)

	## 	Write the text file
	#	@param results Results diactionnary
	def writeFile(self) :

		# Set results name lists
		names=['T_w','P_w','T_wf','P_wf','x_wf', 'eps']
		resultsNames = ['Th','Ph','Tc','Pc','xc','eps']

		# Write all the matrices in a .out file
		for key in resultsNames :
			outputFileName = './figures/' + self.config['initTime'] + '/results_'+ names[resultsNames.index(key)]+'.out'
			np.savetxt(outputFileName, self.results[key], fmt='%-7.2f', header=names[resultsNames.index(key)], newline='\r\n')

		  
		# Write general output in the results_misc
		miscNames = ['Q', 'q_avg', 'alpha_a_avg', 'alpha_i_avg']

		file = open('./figures/' + self.config['initTime'] + '/results_misc.out','w')
		for key in miscNames :
			# outputFileName = './figures/' + self.config['initTime'] + '/results_'+ names[resultsNames.index(key)]+'.out'
			value = str('%-7.2f' %(self.results[key]))
			file.write(key + '=' + value + '\n' )
		file.close()