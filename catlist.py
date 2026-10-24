from common.selectable import Selectable
from tkinter import Frame,Button
from addcategorieframe import Addcategorie
from db import db

class CatlistFrame(Frame):
	"""docstring for Catlist"""
	def __init__(self, parent, **arg):
		Frame.__init__(self, parent)

		categories = db.getcategories()

		self.list = Catlist(self, categories)

		self.currentcat = None
		self.currentindex = None
		self.addbutton = Button(self, text='ajouter', command=self.processaddclick)
		self.addhandlers = []

		self.addbutton.pack(side='top')
		self.list.pack(side='top', expand=True, fill='both')

		self.list.addhandler(self.updatecurrent)

	def mount(self, side='top', fill='both', expand='true'):
		self.pack(side=side, fill=fill, expand=expand)

	def onaddpress(self, fn):
		self.addhandlers.append(fn)

	def addselecthandler(self, fn):
		self.list.addhandler(fn)

	def processaddclick(self):
		for handler in self.addhandlers:
			try:
				handler()
			except Exception as e:
				print("processaddclick error. %s" % e)

	def updatecurrent(self, index, categorie):
		self.currentcat = self.list.data[index]
		self.currentindex = index

	def addcategorie(self, categorie):
		db.addcategorie(categorie)

		categories = db.getcategories()

		self.list.data = categories

		self.list.display(self.list.data)

	def getcurrent(self):
		return self.currentcat

class Catlist(Selectable):
	def __init__(self, parent, categories, **arg):
		Selectable.__init__(self, parent, categories, name='catlist', **arg)

	def display(self, categories):
		self.delete(0,'end')

		for (index,categorie) in enumerate(categories):
			self.insert(index, categorie.upper())