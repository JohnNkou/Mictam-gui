from datetime import datetime
import time

class Timer:
	def __init__(self, name):
		self.name = name
	def start(self):
		self.started = datetime.now()
	def end(self):
		elapsed = datetime.now() - self.started

		print("Elapsed %s for timer %s" % (elapsed, self.name))