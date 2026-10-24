class SongStatus:
	currentSong = None
	handlers = {
		'new': [],
		'verse': []
	}

	def setsong(self, song):
		self.currentSong = song
		self.index = 0

		self.onupdate()

	def getsong(self):
		return self.currentSong

	def updateindex(self, newindex):
		try:
			if newindex != self.index:
				self.currentSong['Verses'][newindex]
				self.index = newindex

				self.onverseupdate()
		except Exception as e:
			print("Error in SongStatus update index. %e" % e)

	def getcurrentverse(self):
		return self.currentSong['Verses'][self.index]

	def onupdate(self):
		if self.currentSong:
			for listes in self.handlers:
				for handler in self.handlers[listes]:
					try:
						data = self.currentSong if listes == "new" else self.getcurrentverse()
						handler(data)
					except Exception as e:
						print("SongStatus.onupdate error %e" % e)

	def onverseupdate(self):
		if self.currentSong:
			for handler in self.handlers['verse']:
				try:
					handler(self.getcurrentverse())
				except Exception as e:
					print("SongStatus.onverseupdate error %e" % e)

	def addnewsonghandler(self, fn):
		self.handlers['new'].append(fn)
	def addnewversehandler(self, fn):
		self.handlers['verse'].append(fn)