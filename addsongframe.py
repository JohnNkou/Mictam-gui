from tkinter import Frame, Label, Button,Entry,Text, Scrollbar,Canvas
from utils import get_dimensions
from utils.cclass import WheelScrollable
from db import db

class Addsong(Frame):
	"""docstring for Addsong"""
	def __init__(self, parent, catid, **args):
		Frame.__init__(self, parent, **args)

		self.parentsize = get_dimensions(parent)
		self.versenumber = 1
		self.toolsframe = Frame(self)
		self.addversebutton = Button(self.toolsframe, text='ajouter verset', command=lambda : self.displayverses(len(self.verses) + 1))
		self.addbutton = Button(self.toolsframe, text='add song', command=self.addsong)
		self.closebutton = Button(self.toolsframe, text='fermer', command=lambda : self.place_forget())
		self.messageText = Label(self)
		self.titlelabel = Label(self, text='Titre', font=('',24,'normal'))
		self.titretext =  Entry(self, relief='solid', borderwidth=1, highlightthickness=1, highlightcolor='blue')
		self.verseframe = Frame(self)
		self.versescroll = Scrollbar(self.verseframe)
		self.versecanvas = Canvas(self.verseframe, borderwidth=2, highlightthickness=0)
		self.versecontent = Frame(self.versecanvas, highlightbackground=None, highlightthickness=None)
		self.catid = catid

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(3, weight=1)
		self.toolsframe.grid_columnconfigure(1,weight=1)

		self.toolsframe.grid(column=0, row=0, sticky='nwse', columnspan=4)
		self.addversebutton.grid(column=0, row=0, sticky='w')
		self.addbutton.grid(column=1, row=0, columnspan=2, sticky='w' )
		self.closebutton.grid(column=2, row=0, sticky='ew')
		self.messageText.grid(column=0, row=1, columnspan=4, sticky='nsew')
		self.titlelabel.grid(column=0, row=2, sticky='w')
		self.titretext.grid(column=1,row=2, sticky='we')
		self.verseframe.grid(column=0,row=3, columnspan=4, sticky='nsew')
		self.versecanvas.pack(side='left', fill='both', expand='true')
		self.versescroll.pack(side='right', fill='y')

		self.versecanvas.config(yscrollcommand=self.versescroll.set)
		self.versescroll.config(command=self.versecanvas.yview)
		tagid = self.versecanvas.create_window((0,0), window=self.versecontent, anchor='nw')

		self.versecontent.bind("<Configure>", lambda e: self.versecanvas.config(scrollregion=self.versecanvas.bbox('all')))

		self.versecanvas.bind('<MouseWheel>', lambda e: print("Mousewheel event %s" % e.num))

		WheelScrollable(self.versecanvas)

		self.verses = []
		self.handlers = []

		self.config(borderwidth=1, relief='solid', padx=10)
		self.place(relx=0.2, rely=0.2, relwidth=0.5, relheight=0.5)

		
		self.after_idle(lambda: self.titretext.focus_set())

	def deleteverse(self, index):
		print("Removing index %s" % index)
		verse = self.verses.pop(index)

		verse.pack_forget()

		for x in range(len(self.verses)):
			self.verses[x].updateindex(x)

	def addsong(self):
		verses = self.verses
		totalverses = len(verses)
		messages = []
		versesText = []
		titletext = self.titretext.get()

		print("Hooland damor")

		if titletext:
			titletext = titletext.strip()
			if totalverses > 0:
				for verse in verses:
					text = verse.gettext().strip()
					rtext = text.replace("\n","")

					if len(rtext) == 0:
						messages.append("Please complete all the verses")
						verse.showerror()
					else:
						verse.hideerror()
						versesText.append({'Text': text})

				if db.songexist(self.catid, titletext):
					messages.append("Le nom de ce morceaux est dejà existant")

			else:
				messages.append("Le morceaux doit au moin contenir une strophe")
		else:
			messages.append("Titre should not be empty")
			self.titlelabel.focus_set();


		if messages:
			self.messageText.config(text=str(messages), fg='red')
		else:
			self.messageText.config(text="Morceau ajouté", fg='green')
			print("Verse Text %s" % versesText)

			for handler in self.handlers:
				try:
					handler({ 'Text': titletext.upper(), 'Verses': versesText, 'catid': self.catid })
				except Exception as e:
					print("Error in addsong.\n%s" % (e))


			self.clear()

	def clear(self):
		self.titretext.delete(0,'end')
		[ verse.pack_forget() for verse in self.verses ]

	def showmessage(self, message, status='success'):
		colors = {
			'success': 'green',
			'error': 'red',
			'system': 'blue'
		}

		color = colors.get(status, colors['system'])

		if len(message) > 0:
			self.messageText.config(text=message, fg=color)
			self.messageText.grid(column=0, row=1, sticky='nsew')
		else:
			self.messageText.grid_pack()

	def displayverses(self, number):
		verselength = len(self.verses)
		iteration = number - verselength

		print("Number is %s and iteration %s" % (number,iteration))

		for x in range(iteration):
			x = x + verselength
			verse = Verse(self.versecontent, x)

			verse.pack(side='top',expand='true', fill='both')

			verse.addhandler(self.deleteverse)

			self.verses.append(verse)

		self.versecontent.update()

		print("Frame content dimensions %s. Self Frame dimension %s" % (get_dimensions(self.versecontent), get_dimensions(self)))

		if len(self.verses) == 1:
			self.verses[0].hidedelete()
		else:
			self.verses[0].showdelete()

	def addhandler(self, fn):
		self.handlers.append(fn)


class Verse(Frame):
	"""docstring for Verse"""
	def __init__(self, parent, index, **arg):
		Frame.__init__(self, parent, **arg)

		self.text = Text(self, relief='solid', height=10, borderwidth=1)
		self.button = Button(self,text='delete', command=self.ondelete)
		self.signal = Frame(self, width=2, bg='red', height=50)
		self.handlers = []
		self.index = index

		self.text.pack(side='left', expand='true', fill='both')
		self.showdelete()

		self.text.bind('<FocusIn>', lambda e: self.text.config(bd=0))
		self.text.bind('<FocusOut>', lambda e: self.text.config(bd=1))
		
	def ondelete(self):
		for handler in self.handlers:
			handler(self.index)

	def showerror(self):
		self.signal.pack(side='bottom', expand='true', anchor='w')

	def hideerror(self):
		self.signal.pack_forget()

	def updateindex(self,newindex):
		self.index = newindex

	def gettext(self):
		return self.text.get('1.0','end')

	def hidedelete(self):
		self.button.pack_forget()
	def showdelete(self):
		self.button.pack(side='right', anchor='n')

	def addhandler(self,fn):
		self.handlers.append(fn)