import os
import json

home = os.environ['HOME']
filename = "songs.json"
file = open(f"{filename}").read()
data = json.loads(file)

class Db(object):
	"""docstring for Db"""
	data = data
	def __init__(self):
		self.data = data

		data['Categories'].sort(key=self.catkey)

		for cat in data['Categories']:
			cat['Songs'].sort(key=self.songkey)

	def catkey(self, cat):
		return cat['Name']
	def songkey(self, song):
		return song['Text']

	def getcategories(self, id=None):
		if id != None:
			categorie = self.data['Categories'][id]

			return categorie
		else:
			return list(map(lambda x: x['Name'], self.data['Categories']))

	def categorieexist(self, name):
		return all(( x for x in self.data['Categories'] if x['Name'].lower() != name.lower() ))

	def songexist(self, catid, name):
		categorie = self.data['Categories'][catid]

		return any((x for x in categorie['Songs'] if x['Text'].lower() == name.lower()))

	def dump(self):
		with open(filename, 'w') as file:
			file.write(json.dumps(self.data))

	def addcategorie(self, categorie):
		self.data['Categories'].append(categorie)

		self.data['Categories'].sort(key=self.catkey)

		self.dump()

	def getbackgrounds(self, index=None):
		background = self.data.get("backgrounds")

		if background == None:
			background = []
			self.data['backgrounds'] = background

			self.dump()
		else:
			if index:
				background = backgroud[index]

		return background

	def addbackground(self, background):
		self.data['backgrounds'].append(background)

		self.dump()

	def getsongs(self, catid, songid=None):
		songs = self.data['Categories'][catid]['Songs']

		if songid == None:
			return songs

		return songs[songid]

	def addsong(self, catid, song):
		songs = self.data['Categories'][catid]['Songs'];

		songs.append(song)

		songs.sort(key=self.songkey)
		self.dump()

db = Db()