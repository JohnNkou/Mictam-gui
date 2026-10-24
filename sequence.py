from tkinter import Frame, Label
from common.selectable import Selectable

class Sequence(Frame):
	"""docstring for Sequence"""
	def __init__(self, parent,  **arg):
		Frame.__init__(self, parent)

		self.list = SequenceList(self, [])
		self.label = Label(self, text='Sequence', font=("Arial",24,"bold"))

		self.label.pack(side='top')
		self.list.pack(side='top', expand=True, fill='both')



	def additem(self, item):
		self.list.data.append(item)

		lastindex = self.list.size()

		self.list.insert(lastindex, item['Text'])

	def removeitem(self, index):
		self.list.data.remove(index)

		self.list.delete(index)

	def addhandler(self, fn):
		self.list.addhandler(fn)

class SequenceList(Selectable):
	"""docstring for SequenceList"""
	def __init__(self, parent, sequences, **args):
		Selectable.__init__(self, parent, [], name="Sequence", **args)

	def display(self, sequences):
		for (index,item) in enumerate(sequences):
			self.insert(index, item['Text'])