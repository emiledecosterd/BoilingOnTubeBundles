## 	@package postProcessor
#	Load, and save all the results 
#	
#	This class will use the PostProcess class to create plots images and text files with all
#	the data.

# Packages for the post processing
import sys,os
import time
import numpy as np
from postProcess import *

# Qt and GUI packages
from PyQt5.QtCore import QObject, pyqtSignal
from error import Error

## 	PostProcessor
#	Data manager used at the end of each simulation to save the data
class PostProcessor(QObject):

	## 	Initialize data
	#	@param config Configuration dictionnary
	#	@param results Results diactionnary
	def __init__(self, config, results, show):
		self.config = config
		self.results = results
		self.show = show

		# Create the directory

		if not (os.path.isdir(self.config['filename'] + 'data')):
			os.makedirs(self.config['filename'] + 'data')
			os.makedirs(self.config['filename'] + 'mplt')
			os.makedirs(self.config['filename'] + 'images')

		# Save the plots
		self.savePlots()

		# Write data file
		self.writeFile()

	## Save the plot
	#	@param config Configuration dictionnary
	#	@param results Results diactionnary
	def savePlots(self):

		try:
			# Save the boiler plots
			plot_boiler(self.config, self.results, self.show)
		except Exception as e:
			raise Error('PostProcessor.savePlots.plot_boiler', e)

		try:
			# Save teh xc pipe plot
			plot_xc_pipe(self.config, self.results, self.show)
		except Exception as e:
			raise Error('PostProcessor.savePlots.plot_xc_pipe', e)

		try:
			# Compute other calculation
			self.results = PostProcess_calc(self.config, self.results)
		except Exception as e:
			raise Error('PostProcessor.savePlots.PostProcess_calc', e)

		# try:
		# 	plotFlowPatternMap(self.config, self.results, self.show)
		# except Exception as e:
		# 	raise Error('PostProcessor.savePlots.plotFlowPatternMap', e)

	## 	Write the text file
	#	@param results Results diactionnary
	def writeFile(self) :

		# Set results name lists
		names=['T_w','P_w','T_wf','P_wf','x_wf', 'eps']
		resultsNames = ['Th','Ph','Tc','Pc','xc','eps']

		# Write all the matrices in a .out file
		for key in resultsNames :
			outputFileName = self.config['filename'] + 'data/results_'+ names[resultsNames.index(key)]+'.out'
			np.savetxt(outputFileName, self.results[key], fmt='%-7.2f', header=names[resultsNames.index(key)], newline='\r\n')

		  
		# Write general output in the results_misc
		miscNames = ['Q', 'q_avg', 'alpha_a_avg', 'alpha_i_avg']

		file = open(self.config['filename'] + 'data' + '/results_misc.out','w')
		for key in miscNames :
			# outputFileName = './figures/' + self.config['initTime'] + '/results_'+ names[resultsNames.index(key)]+'.out'
			value = str('%-7.2f' %(self.results[key]))
			file.write(key + '=' + value + '\n' )
		file.close()