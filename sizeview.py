from tkinter import Frame, Label

class SizeView(Frame):
	def __init__(self, parent, **args):
		Frame.__init__(self, parent, **args)

		self.label = Label(self,text='waiting')

		self.pack(side='top', expand='false', fill='x')
		self.label.pack(side='top', expand='true', fill='both')

		self.bind('<Configure>', self.update)

	def getsize(self):
		return self.winfo_toplevel().winfo_geometry()

	def update(self,event):
		text = self.getsize()

		self.label.config(text=text)