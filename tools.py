from tkinter import Frame, Button,Label, Checkbutton, BooleanVar
from tkinter.ttk import Combobox
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from utils.time import Timer

class Combo(Frame):
	def __init__(self, parent, values, text, name, onselected, width=5):
		Frame.__init__(self, parent)

		self.combo = Combobox(self, values=values, width=width)
		self.label = Label(self, text=text)

		self.combo.name = name

		self.label.pack(side='left')
		self.combo.pack(side='right')

		self.combo.bind('<<ComboboxSelected>>', onselected)

	def get(self):
		return self.combo.get()

class Tools(Frame):
	"""docstring for Tools"""
	def __init__(self, parent):
		Frame.__init__(self, parent)

		colors = ['red','black','white','pink']
		fonts = [10,20,30,40,50,60,70,80]

		self.bgcombo = Combo(self, values=colors, text='bg', name='bg', width=5, onselected=self.oncombochange)
		self.fgcombo = Combo(self, values=colors, text='fg', name='fg', width=5, onselected=self.oncombochange)
		self.fontsizecombo = Combo(self, values=fonts, text='size', name='font', width=2, onselected=self.oncombochange)
		self.frameButton = Frame(self)
		self.addsongbutton = Button(self.frameButton, text='add song', command=self.onaddsong)
		self.addtosequencebutton = Button(self.frameButton, text='add to sequence', command=self.onaddtosequence)
		self.projectbutton = Button(self.frameButton, text='Projeter', command=self.onproject)
		self.sequenceVar = BooleanVar();
		self.sequenceshow = Checkbutton(self, text="Afficher sequence", command=self.onsequencechange, variable=self.sequenceVar)
		self.backgroundVar = BooleanVar()
		self.backgroundtoggler = Checkbutton(self, text="Show Background", command=self.onbackgroundtoogle, variable=self.backgroundVar)

		self.handlers = {
			'fg': [],
			'bg': [],
			'font': [],
			'addsong': [],
			'addsequence': [],
			'project': [],
			'sequence': [],
			'background':[]
		}

		self.frameButton.pack(side='bottom')
		self.bgcombo.pack(side='left')
		self.fgcombo.pack(side='left')
		self.fontsizecombo.pack(side='left')
		self.addsongbutton.pack(side='left')
		self.addtosequencebutton.pack(side='left')
		self.projectbutton.pack(side='left')
		self.sequenceshow.pack(side='bottom')
		self.backgroundtoggler.pack(side='left')

		self.grid(row=0,column=0, sticky='n')
		self.config(relief='solid', bd=3)

	def onaddsong(self):
		for handle in self.handlers['addsong']:
			try:
				handle()
			except Exception as e:
				print("addsong error %s" % e)

	def onproject(self):
		for handler in self.handlers['project']:
			try:
				handler()
			except Exception as e:
				print("onproject error. %s" % (e))

	def onsequencechange(self):
		state = self.sequenceVar.get()
		
		for handler in self.handlers['sequence']:
			try:
				handler(state)
			except Exception as e:
				print("Tools.onsequencechange error. %s" % e)

	def onbackgroundtoogle(self):
		state = self.backgroundVar.get()

		for handler in self.handlers['background']:
			try:
				handler(state)
			except Exception as e:
				print("Tools.onbackgroundtoogle. %s" % e)

	def onaddtosequence(self):
		for handler in self.handlers['addsequence']:
			try:
				handler()
			except Exception as e:
				print("Tools.onaddtosequence error. %s" % e)

	def oncombochange(self,x):
		combo = x.widget
		name = combo.name

		value = combo.get()
		handlers = self.handlers[name]

		for handler in handlers:
			try:
				handler(value)
			except Exception as e:
				print("Tools.oncombochange error.\n -- %s --" % (e))

		return "break"

	def addhandler(self, id, fn):
		self.handlers[id].append(fn)