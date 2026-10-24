from tkinter import Entry

class SearchText(Entry):
	"""docstring for SearchText"""
	def __init__(self,parent=None):
		Entry.__init__(self, parent)

		self.bind('<Key>', self.ondata)

		self.handlers = []

		self.config(relief='solid', borderwidth=1)
		self.pack(side='top', expand='true', fill='x')


	def addhandler(self, fn):
		self.handlers.append(fn)


	def ondata(self, x):
		text = self.get()

		if len(text) > 3:
			for handler in self.handlers:
				handler(text)
