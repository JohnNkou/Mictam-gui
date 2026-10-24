import tkinter
from utils import get_dimensions, get_required_size
from constants import IMAGE_BG_COLOR
import traceback

class Message(tkinter.Frame):
	"""docstring for ClassName"""
	text = None

	def __init__(self, parent,**args):
		tkinter.Frame.__init__(self, parent, **args)

		self.default_size = 58;
		self.user_size = None
		self.canvas = tkinter.Canvas(self)
		self.fg = 'systemTextColor'
		self.tTag = 'txTag'
		self.rTag = 'rTag'
		self.pTag = 'pTag'
		self.photo = tkinter.PhotoImage(name='Fanboxy')

		self.photo.blank()

		self.grid(row=1,rowspan=8,column=0, sticky='nsew')
		self.canvas.pack(side='top', fill='both')

		self.after_idle(lambda : [
			self.canvas.create_text(0,0, tags=self.tTag, fill=self.fg, justify='center'), 
			self.canvas.create_image(0,0, image=self.photo, tags=self.pTag)
			]
		)

		self.bind("<Configure>", lambda x: [self.setcanvasdimensions(), self.checkdims()])

	def setcanvasdimensions(self):
		dims = get_dimensions(self)
		width = dims['width']
		height = dims['height']
		canvas = self.canvas

		canvas.config(width=width,height=height)

		canvas.delete(self.rTag)
		canvas.create_rectangle(0,0, width, height, tags=self.rTag)

		position = self.gettextposition(( width, height ))

		canvas.moveto(self.tTag,position['x'], position['y'])
		canvas.itemconfig(self.tTag, width=int(width / 2), font=("Arial", self.default_size, "bold"))

		canvas.update_idletasks()

		self.dims = dims

	def gettextposition(self, size):
		return { 'x': int(size[0] / 2), 'y': int(size[1] / 2) }

	def checkdims(self):
		text = self.text

		if text:
			self.display(text)

	def gettagdimension(self, tag):
		(x1,y1, x2,y2) = self.canvas.bbox(tag)

		try:
			width = int(self.canvas.itemcget(tag,'width'))
		except Exception as e:
			width = x2 - x1
		

		return { "x": x1, "y": y1, "width": width, "height": y2 - y1 }

	def ajustdimension(self, size):
		maxwidth=size['width']
		text_dimension = self.gettagdimension(self.tTag)
		textwidth = text_dimension['width']
		percent = text_dimension['height'] / size['height']

		if percent > 0.95 and maxwidth != textwidth:
			newwidth = min(maxwidth, textwidth + 10)

			self.canvas.itemconfig(self.tTag, width=newwidth)

			self.canvas.after_idle(lambda  : self.ajustdimension(size))			

	def display(self, text):
		size = self.user_size or self.default_size
		canvas = self.canvas
		dims = self.dims

		position = self.gettextposition((dims['width'], dims['height']))

		canvas.itemconfig(self.tTag,
			text=text,
			width=(int(dims['width'] / 2)),
			font=('courier', size, 'bold'),
			anchor='center'
		)
		canvas.coords(self.tTag, position['x'], position['y'])

		text_size = self.default_size
		size = get_required_size(self)

		self.canvas.after_idle(lambda : self.ajustdimension(size))
		self.text = text

	def changebackground(self, background):
		canvas = self.canvas
		
		canvas.lift(self.rTag)
		canvas.lift(self.tTag)
		canvas.itemconfig(self.rTag, fill=background)
		
		if self.photo:
			self.photo = None

	def changeforeground(self, foreground):
		self.fg = foreground
		self.canvas.itemconfig(self.tTag, fill=foreground)
	def changefilebackground(self, filename=None):
		photo = tkinter.PhotoImage(file=filename)
		canvas = self.canvas
		photowidth = photo.width()
		photoheight = photo.height()
		pwidth = self.dims['width']
		pheight = self.dims['height']
		widthdifference = photowidth - pwidth
		heightdifference = photoheight - pheight
		args = { 'shrink': True }
		xTag = 'xTag'
		imageargs = { 'anchor':'nw', 'tags': self.pTag, 'image': photo }
		imagecoords = [0,0]

		self.canvas.delete(xTag)
		
		if widthdifference < 0:
			devide = abs(int(widthdifference / 2))
			newwidth = devide + photowidth
			args['to'] = [devide,0, newwidth, photoheight]

			canvas.create_rectangle(0,0, devide, pheight, fill=IMAGE_BG_COLOR, tags=xTag)
			canvas.create_rectangle(newwidth,0,newwidth + devide, pheight, fill=IMAGE_BG_COLOR, tags=xTag)
			imagecoords[0] = devide


		if heightdifference < 0:
			devide = abs(int(heightdifference / 2))
			to = args.get('to')
			newheight = devide + photoheight
			
			if not to:
				to = [0, devide, photowidth, newheight ]
			else:
				to[1] = devide;
				to[3] = devide + photoheight

			canvas.create_rectangle(0,0, pwidth, devide, fill=IMAGE_BG_COLOR, tags=xTag)
			canvas.create_rectangle(0,newheight, pwidth, newheight + devide, fill=IMAGE_BG_COLOR, tags=xTag)

			args['to'] = to
			imagecoords[1] = devide

		canvas.itemconfig(self.pTag, image=photo)
		canvas.moveto(self.pTag, imagecoords[0], imagecoords[1])

		self.canvas.lift(self.pTag)
		self.canvas.lift(self.tTag)

		print("Image dimension box %s with image coords %s" % (self.gettagdimension(self.pTag), imagecoords))

		self.photo = photo
	def changefontsize(self, size):
		self.user_size = size
		self.canvas.itemconfig(self.tTag,font=('courier', size, 'bold'))