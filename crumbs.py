from tkinter import Frame, Label

class Crumbs(Frame):
	"""docstring for Crumbs"""
	def __init__(self, parent, lines=None, **arg):
		Frame.__init__(self, parent, **arg)

		self.display(lines)
		self.handlers = []

	def display(self, lines):

		if lines:
			for child in self.winfo_children():
				child.pack_forget()

			self.after_idle(lambda : self.addnavigations(lines))

	def addhandler(self, fn):
		self.handlers.append(fn)

	def addnavigations(self, lines):
		for (index,line) in enumerate(lines):
			if index != 0:
				line = " > " + line

			label = Label(self, text=line.upper(), cursor='hand')

			label.bind('<Button-1>', lambda x,y=index,categorie=line : self.runhandlers(y,categorie))

			label.pack(side='left')

	def runhandlers(self, index, categorie):
		for handler in self.handlers:
			try:
				handler(index)
			except Exception as e:
				print("runhandlers error %s" % e)