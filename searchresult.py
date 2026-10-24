from tkinter import Listbox, Frame, Label

def sizeSearchResult():
	sr = searchText
	dims = ( sr.winfo_x(), sr.winfo_y(), sr.winfo_width(), sr.winfo_height() )
	(x,y,width,height) = dims
	print("Dimensions are %s" % (str(dims)))

	searchResult.place(x=x,y=y + height,width=width,height=height)

class SearchResult(Frame):
	"""docstring for SearchResult"""
	def __init__(self, entrywidget,parent=None,**args):
		Frame.__init__(self, parent,**args)

		

		self.dims = None

		self.handlers = []
		self.conf = {
			'bg':'red',
		}

		self.result = []
		self.entrywidget = entrywidget
		self.listbox = Listbox(self)

		self.listbox.pack(side='left', expand='true', fill='both')
		self.listbox.bind('<<ListboxSelect>>', self.onselect)
		self.bind('<Button>', lambda x : "break")

		self.config(**self.conf)

	def show(self):

		self.place(**self.dims)

	def hide(self):
		self.place_forget()

	def addhandler(self, fn):
		self.handlers.append(fn)

	def onselect(self, x):
		index = self.listbox.curselection()[0]
		song = self.result[index][1]

		print("SearchResult selected song is %s" % (song))

		for handle in self.handlers:
			handle(song)

		return "break"

	def get_dimensions(self, entrywidget):
		ew = entrywidget

		return { 'x': ew.winfo_x(), 'y': ew.winfo_y(), 'width': ew.winfo_width(), 'height': ew.winfo_height() }

	def displayResult(self, lists, text):
		self.result = [ ( index, x ) for (index, x) in enumerate(lists) if text.lower() in x['Text'].lower() ]

		self.listbox.delete(0, 'end')

		print("Listbox size is %s" % (self.listbox.size()))

		for (index, song) in self.result:
			self.listbox.insert(index,song['Text'])

		if len(self.result) == 0:
			Label(self,text='Aucun resulat trouvé')
			print("Aucun resultat trouvé")
		else:
			print("Resultat trouvé")

		if self.dims == None:
			self.dims = self.get_dimensions(self.entrywidget)
			self.dims['y'] = self.dims['y'] = self.dims['height'];
			self.dims['height'] = self.dims['height'] + 300
			print("New dimension are %s" % (self.dims))

		print("Dimensions %s" % (str(self.dims)))

		self.place(**self.dims)

		self.update_idletasks();