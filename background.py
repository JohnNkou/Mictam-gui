from tkinter import Frame, Label, Button, PhotoImage
from tkinter.filedialog import askopenfilename
from math import floor
from db import db
import traceback

class PhotoLabel(Frame):
	"""docstring for PhotoLabel"""
	def __init__(self, parent, image, text, width=100, height=None, **arg):
		Frame.__init__(self, parent, padx=2, pady=2, **arg)

		self.label = Label(self, text=text, image=image)

		self.image = image
		self.width = width
		self.height = height or width
		self.isbackground = True

		self.bind('<Configure>', self.changesize)
		#self.label.bind('<Button-1>', lambda x: self.label.focus_set())

		self.label.pack(side='left', fill='both')

		self.config(highlightthickness=1, highlightcolor="blue")


	def changesize(self, dimensions):
		image = self.image
		width = self.width
		height = self.height
		wratio = int(image.width() / width)
		hratio = int(image.height() / height)

		self.image = image.subsample(max(1, wratio), max(1, hratio))

		self.label.config(image=self.image)

class Background(Frame):
	"""docstring for Background"""
	def __init__(self, parent, iconwidth=100, **arg):
		Frame.__init__(self, parent, **arg)

		label = Label(self, text='Background')

		self.toolFrame = Frame(self)
		self.addbutton = Button(self.toolFrame, text='Ajouter', command=self.getfilename)
		self.listFrame = Frame(self)
		self.maxcol = None
		self.iconwidth = iconwidth
		self.row = 0
		self.col = 0
		self.photos = []
		self.currentFrame = None
		self.pad = 10
		self.firstdisplay = False
		self.handlers = []

		label.pack(side='top')
		self.toolFrame.pack(side='top', fill='x')
		self.addbutton.pack(side='left')
		self.listFrame.pack(side='top', expand=True, fill='both')
		self.listFrame.bind('<Configure>', self.setmaxcol)
		self.bind("<Button-1>", self.choosebackground)

	def choosebackground(self, x):
		(x,y) = self.winfo_pointerxy()

		widget = self.winfo_containing(x,y)

		if widget:
			text = None
			try:
				filename = widget.cget('text')

				if filename:
					widget.focus_set()

					for handler in self.handlers:
						try:
							handler(filename)
						except Exception as e:
							print(e)
			except Exception as e:
				print(f"{e}. {traceback.print(e.__traceback__)}")

	def setmaxcol(self, dim):
		self.maxcol = max(1,floor((dim.width - (self.pad * 2)) / self.iconwidth))

		if not self.firstdisplay:
			backgrounds = db.getbackgrounds()
			length = len(backgrounds)

			self.firstdisplay = True
			self.row = floor(length / self.maxcol)
			self.col = length % self.maxcol

			self.display(backgrounds)

	def display(self, backgrounds):
		for background in backgrounds:
			self.addbackground(background['path'])


	def addbackground(self, filename):
		if self.col == 0:
			self.currentFrame = Frame(self.listFrame)
			self.currentFrame.pack(side='top', fill='x', anchor='nw')

		photo = PhotoImage(file=filename)
		photolabel = PhotoLabel(self.currentFrame, image=photo, text=filename)
		photolabel.isbackground = True
		tags = photolabel.label.bindtags()

		photolabel.pack(side='left')
		photolabel.label.bindtags(( tags[0], str(self) ) + tags[1:])

		self.col = (self.col + 1) % self.maxcol

		if self.col == 0:
			self.row += 1

		self.photos.append((photo, photolabel))

	def getfilename(self):
		filename = askopenfilename()

		if filename:
			self.addbackground(filename)

			db.addbackground({ 'path': filename, 'default':False })
	def addhandler(self,fn):
		self.handlers.append(fn)