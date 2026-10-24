def goTo(songStatus,verseNumber, message):
	currentSong = songStatus.getsong()
	currentVerse = songStatus['currentVerse']

	verses = currentSong['Verses']
	length = len(verses)
	nextVerse = currentVerse + verseNumber
	verse = verses[nextVerse]['Text']

	if nextVerse == (length - 1):
		Next.pack_forget()
	else:
		Next.pack(**nextPackConfig)


	if nextVerse == 0:
		Prev.pack_forget()
	else:
		Prev.pack(**prevPackConfig)

	songStatus['currentVerse'] = nextVerse

	message.display(nextVerse)

def get_dimensions(widget):
	return {
		'x': widget.winfo_x(), 'y': widget.winfo_y(),
		'width': widget.winfo_width(), 'height': widget.winfo_height()
	}

def get_screen_dimensions(root):
	return {
		'width': root.winfo_screenwidth(),
		'height': root.winfo_screenheight()
	}

def get_required_size(widget):
	return {
		'width': widget.winfo_reqwidth(),
		'height': widget.winfo_reqheight()
	}