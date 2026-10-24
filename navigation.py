from tkinter import Frame, Button
from utils import get_dimensions

class Navigation(Frame):
	"""docstring for Navigation"""
	def __init__(self, parent):
		Frame.__init__(self,parent)

		self.next = Button(self,text='next', command=lambda : self.goTo(1))
		self.prev = Button(self,text='prev', command=lambda : self.goTo(-1))
		self.position = 0;
		self.handlers = []
		
		self.grid(row=10,column=0)

	def setverse(self, verses):
		self.versesLength = len(verses)
		self.position = 0;

		self.goTo(self.position)

	def goTo(self, incr):
		newposition = self.position + incr

		if newposition > 0:
			self.prev.pack(side='left')
		else:
			self.prev.pack_forget()

		if (newposition + 1) < self.versesLength:
			self.next.pack(side='right')
		else:
			self.next.pack_forget()

		self.position = newposition

		for handle in self.handlers:
			handle(newposition)

	def addhandler(self, fn):
		self.handlers.append(fn)