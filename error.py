##	@package error
#	A generic error to be used throughout the code

##	Error
#
#	Generic error that can be used from everywhere throughout the code
class Error(Exception):

	##	The constructor
	#	@param	functionName	The name of the function in which the error occured
	#	@param	message			The error message to give more details about the error
	functionName=''
	message=''

	def __init__(self, functionName, message):
		self.functionName = functionName
		self.message = message;
