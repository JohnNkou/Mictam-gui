from tkinter import Frame, Label, Entry, Button, Text
from db import db

class Addcategorie(Frame):
	"""docstring for Addcategorieframe"""
	def __init__(self, parent,  **arg):
		Frame.__init__(self, parent, **arg)

		self.container = Frame(self)
		self.label = Label(self.container, text='Nom')
		self.entry = Entry(self.container, borderwidth=1, highlightthickness=1)
		self.message = Label(self)
		self.addbutton = Button(self, text='ajouter', command=self.addcategorie)
		self.closebutton = Button(self, text='fermer', command=self.place_forget)
		self.handlers = []


		self.message.pack(side='top',anchor='center')
		self.container.pack(side='top')
		self.label.pack(side='left', expand=True, anchor='e')
		self.entry.pack(side='right', expand=True, anchor='w')
		self.addbutton.pack(side='left', expand=True, anchor='ne')
		self.closebutton.pack(side='right', expand=True, anchor='nw')

		self.config(borderwidth=1, relief='solid', pady=10, padx=10)
		self.place(relheight=0.2, relwidth=0.2, relx=0.4, rely=0.4)

	def addhandler(self, fn):
		self.handlers.append(fn)

	def addcategorie(self):
		value = self.entry.get()
		message = ''
		color = 'blue'

		if value:
			if db.categorieexist(value):
				message = "Cette categorie existe dejà. Veuillez entre un autre nom"
				color = 'red'
			else:
				message = 'Categorie ajoutée'
				color = 'green'
		else:
			message = 'Please provide a name for the categorie'
			color = 'red'


		if message:
			self.message.config(text=message, fg=color)

		if color == 'green':
			self.entry.delete(0,'end')
			for handler in self.handlers:
				try:
					handler({ 'Name': value, 'Songs':[] })
				except Exception as e:
					print("addcategorie error %s" % e)