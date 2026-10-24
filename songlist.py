from tkinter import Listbox, Label
from common.selectable import Selectable
from db import db

class SongList(Selectable):
	"""docstring for SongList"""
	def __init__(self, parent,  **args):

		Selectable.__init__(self, parent, [], name='songlist', **args)

		self.addhandler(self.updatecurrent)

		self.currentsong = None

	def display(self, songs):
		maxTextLength = 0;
		sText = None

		self.delete(0,'end')

		for (index,song) in enumerate(songs):
			songText = song['Text']
			songLength = len(songText.strip())

			if songLength > maxTextLength:
				sText = songText
				maxTextLength = songLength

			self.insert(index, songText)

		self.config(width=(maxTextLength-10))

		self.data = songs

	def mount(self, side='top', fill='both', expand=True):
		self.pack(side=side, fill=fill, expand=expand)

	def updatecurrent(self, index, song):
		self.currentsong = song['Text']
		self.currentindex = index

	def getcurrent(self):
		return self.currentsong

	def addsong(self, song):
		catid = song['catid']

		del song['catid']

		db.addsong(catid, song)

		self.data = db.getsongs(catid)

		self.display(self.data)