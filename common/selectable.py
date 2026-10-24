from tkinter import Listbox
from utils.time import Timer

class Selectable(Listbox):
	"""docstring for Selectable"""
	def __init__(self, parent, data,name, **args):
		Listbox.__init__(self, parent, args)

		self.data = data
		self.handlers = []

		self.bind('<<ListboxSelect>>', self.onselect)

		self.display(data)

	def update(self, newdata):
		self.data = newdata

	def addhandler(self, fn):
		self.handlers.append(fn)

	def onselect(self,x):
		curselection = self.curselection()
		if curselection:
			index = curselection[0]
			payload = self.data[index]

			for handle in self.handlers:
				handle(index,payload)
				