from tkinter import Toplevel, Frame, Message
from utils import get_screen_dimensions
from variables import songStatus
from constants import PROJECTION_TEXT_SIZE
from utils import get_dimensions, get_required_size

class Project(Toplevel):
	"""docstring for Project"""
	def __init__(self, **arg):	
		Toplevel.__init__(self, **arg)

		dims = get_screen_dimensions(self)
		(width, height) = ( int(dims['width'] * 0.5), int(dims['height'] * 0.5) )

		self.frame = Frame(self)
		self.dims = { 'width': width, 'height': height }
		
		verse = songStatus.getcurrentverse()

		self.message = Message(self.frame)

		self.frame.pack(side='left', fill='both', expand=True)
		self.message.pack(side='left', expand=True)

		self.display(verse['Text'])

		songStatus.addnewversehandler(self.update)

		self.geometry(f"{width}x{height}")

	def update(self, verse):
		self.display(verse['Text'])

	def display(self, text):
		fontsize = PROJECTION_TEXT_SIZE
		dims = self.dims

		while True:
			self.message.config(text=text, font=("Arial", fontsize, "bold"))

			self.update_idletasks()

			messagedism = get_required_size(self.message)
			pwidth = dims['width']
			pheight = dims['height']
			messagewidth = messagedism['width']
			messageheight = messagedism['height']

			if (messagewidth / pwidth) > 0.95 and (messageheight / pheight) > 0.95:
				fontsize -= 10
			else:
				break