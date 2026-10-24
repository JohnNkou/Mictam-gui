class WheelScrollable:
	"""docstring for WheelScrollabel"""
	def __init__(self, widget):
		self.widget = widget
		widget.bind('<MouseWheel>', self.scroll)
		
	def scroll(self, event):
		widget = self.widget
		if event.num:
			if event.num == 4:
				widget.yview_scroll(-1,'units')
			elif event.num == 5:
				widget.yview_scroll(1, 'units')
			else:
				widget.yview_scroll(event.delta * -1, "units")