import urwid
import widgets

class Gui:
	'''Manages the custom widgets'''
	def __init__(self):
		self.__messages = urwid.SimpleFocusListWalker([])
		self.__channels = urwid.SimpleFocusListWalker([])
		self.generate()

	def generate(self):
		'''Generates widgets'''
		self.text_entry = widgets.TextEntry()
		self.messages = widgets.Messages(self.__messages)
		self.main_window = widgets.MainWindow(self.messages, footer=self.text_entry)
		self.side_bar = widgets.SideBar(self.__channels)
		self.screen_split = widgets.ScreenSplit([self.side_bar, self.main_window])
		self.main_screen = widgets.MainScreen(self.screen_split)
