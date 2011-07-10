import os, time

class Logger:
	def __init__(self, logfile=os.devnull):
		try:
			self.log = open(logfile, 'a')
		except IOError:
			self.log = open(os.devnull, 'w')
	
	def close(self):
		self.log.close()
	
	def timestr(self):
		return time.strftime('%c')
	
	def info(self, msg):
		logstr = "[%s] I: %s" % (self.timestr(), msg)
		print logstr
		self.log.write(logstr + "\n")
	
	def warning(self, msg):
		logstr = "[%s] W: %s" % (self.timestr(), msg)
		print logstr
		self.log.write(logstr + "\n")
	
	def error(self, msg, fatal=False):
		fatalstr = ""
		if fatal:
			fatalstr = "[Fatal] "
		
		logstr = "[%s] E: %s %s" % (fatalstr, self.timestr(), msg)
		print "--- SERVER ERROR ---"
		print logstr
		print "--- SERVER ERROR ---"
		self.log.write(logstr + "\n")
