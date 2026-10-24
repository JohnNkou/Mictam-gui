from tkinter import Tk,Button,Frame,Listbox,Entry
import os
import json
import tkinter
from searchresult import SearchResult
from searchText import SearchText
from catlist import CatlistFrame
from songlist import SongList
from navigation import Navigation
from message import Message
from tools import Tools
from sizeview import SizeView
from addsongframe import Addsong
from addcategorieframe import Addcategorie
from crumbs import Crumbs
from sequence import Sequence
from background import Background
from variables import songStatus
from project import Project
from utils.time import Timer
from db import db

HOME = os.environ['HOME']
root = Tk()


nextPackConfig = { 'side': tkinter.RIGHT, 'anchor': tkinter.SW }
prevPackConfig = { 'side': tkinter.LEFT, 'anchor': tkinter.SW }
rootGeometry = "%sx%s+-1164+0" % (1180, root.winfo_vrootheight())


root.title('Song Viewer')
root.geometry(rootGeometry)

listFrame = Frame(root, width=400)
songFrame = Frame(root)
searchFrame = Frame(listFrame)
tool = Tools(songFrame)
message = Message(songFrame)
navigation = Navigation(songFrame)
searchText = SearchText(searchFrame)
crumbs = Crumbs(listFrame)
catList = CatlistFrame(listFrame)
songList = SongList(listFrame)
sequence = Sequence(listFrame)
background = Background(songFrame)
searchResult = SearchResult(parent=root, entrywidget=searchText)

listFrame.pack_propagate(False)

listFrame.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
searchFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
searchText.pack(side=tkinter.TOP, expand=tkinter.TRUE, fill=tkinter.X)
crumbs.pack(side=tkinter.TOP, expand='false', anchor='nw')
catList.mount()

songFrame.pack(side=tkinter.RIGHT, expand=tkinter.TRUE, fill=tkinter.BOTH)
songFrame.rowconfigure(1,weight=1)
songFrame.columnconfigure(0,weight=1)
songFrame.columnconfigure(1,weight=1)

crumbs.addhandler(lambda index: index == 0 and [
	songList.pack_forget(),
	catList.mount(),
	catList.update_idletasks(),
	crumbs.display([ catList.getcurrent() ])
	]
)

catList.addselecthandler(lambda index, categorie: crumbs.display([catList.getcurrent()]))
catList.addselecthandler(lambda index, categorie: [ 
	catList.pack_forget(),
	listFrame.after_idle(lambda: songList.mount()),
	songList.display(db.getcategories(index)['Songs']),
	songList.update_idletasks()
])
catList.onaddpress(lambda : Addcategorie(root).addhandler(catList.addcategorie))


searchText.addhandler(lambda text : searchResult.displayResult(songs, text))
navigation.addhandler(lambda position: songStatus.updateindex(position))
songList.addhandler(lambda index,song: songStatus.setsong(db.getsongs(catList.currentindex, index)))
sequence.addhandler(lambda index, item: [
	catList.updatecurrent(item['catid'], db.getcategories(item['catid'])),
	print("Item is %s" % item),
	songStatus.setsong(db.getsongs(item['catid'], item['songid']))
	] 
)
searchResult.addhandler(lambda song: songStatus.setsong(song))

songStatus.addnewsonghandler(lambda song: crumbs.display([ catList.getcurrent(), songList.getcurrent() ]))
songStatus.addnewsonghandler(lambda song: navigation.setverse(song['Verses']))
songStatus.addnewversehandler(lambda verse: message.display(verse['Text']))

background.addhandler(lambda filename: message.changefilebackground(filename))

tool.addhandler('bg',lambda color: message.changebackground(color))
tool.addhandler('fg',lambda color: message.changeforeground(color))
tool.addhandler('font', lambda fontsize: message.changefontsize(fontsize))
tool.addhandler('addsong', lambda : Addsong(root, catList.currentindex).addhandler(songList.addsong))
tool.addhandler('project', lambda : Project().mainloop())
tool.addhandler('sequence', lambda state: [sequence.pack(side='top', expand=True, fill='both'), sequence.update_idletasks()] if state else sequence.pack_forget())
tool.addhandler('addsequence', lambda : sequence.additem({ "Text": songStatus.currentSong['Text'], "catid": catList.currentindex, "songid": songList.currentindex }))
tool.addhandler('background', lambda state: [background.grid(row=0, rowspan=2, column=1, columnspan=3, sticky='nsew'), background.update_idletasks()] if state else background.grid_forget())

root.bind('<Button>', lambda x : searchResult.place_forget())

#root.bind("<Configure>", lambda x : print(root.geometry()))

root.focus_force()

root.mainloop()