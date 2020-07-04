import urwid
import os

PALETTE = [
	('my-username', 'light green', ''),
	('other-username', 'light magenta', ''),
	('current-channel', 'light magenta', ''),
	('mentions', 'light blue', ''),
	('header', '', ''),
	('footer', '', ''),
	('selected', 'standout', ''),
]

SHORTCUTS = {
	'scroll-up': 'ctrl a',
	'scroll-down': 'ctrl d',
	'scroll-top': 'ctrl f',
	'scroll-bottom': 'ctrl g'
}




#Base Classes/Traits

class Selector:
	__current_selected = None

	@classmethod
	def select(cls, widget):
		cls.__current_selected = widget

	@classmethod
	def current_selected(cls):
		return cls.__current_selected

class Constructor:
	def __init__(self):
		self.__corresponding_widget = self.construct()

	def __construct(self, *children):
		pass

	def construct(self):
		pass

	def corresponding_widget(self):
		return self.__corresponding_widget

class Listlike:
	'''Extends list functionality to classes'''
	def append(self, *args, **kwargs):
		return self.l.append(*args, **kwargs)

	def extend(self, *args, **kwargs):
		return self.l.extend(*args, **kwargs)

	def insert(self, *args, **kwargs):
		return self.l.insert(*args, **kwargs)

	def remove(self, *args, **kwargs):
		return self.l.remove(*args, **kwargs)

	def pop(self, *args, **kwargs):
		return self.l.pop(*args, **kwargs)

	def clear(self, *args, **kwargs):
		return self.l.clear(*args, **kwargs)

	def index(self, *args, **kwargs):
		return self.l.clear(*args, **kwargs)

	def count(self, *args, **kwargs):
		return self.l.clear(*args, **kwargs)

	def sort(self, *args, **kwargs):
		return self.l.clear(*args, **kwargs)

	def reverse(self, *args, **kwargs):
		return self.l.reverse(*args, **kwargs)

	def copy(self, *args, **kwargs):
		return self.l.copy(*args, **kwargs)


class UserInputHandler:
	screen = None

	@classmethod
	def set_screen(cls, screen):
		cls.screen = screen

	@classmethod
	def handle(cls, input_text, source_widget):
		if input_text.strip() == '':
			os.system('echo \a')
			return

		if input_text == ':q': #exit
			raise urwid.ExitMainLoop()
			'''
		elif input_text.startswith(':h '): #set the header
			cls.screen.set_header(input_text[3:])
		elif input_text.startswith(':f '): #set the footer
			cls.screen.set_footer(input_text[3:])
			'''

		elif input_text.startswith(':c '):
			#change the channel that most closely matches the text
			channel = input_text[3:]
			#do some work from her
		else:
			cls.screen.child.main_window.messages.append(urwid.AttrMap(UserMessage([('my-username', 'fusc: '), input_text]), None, focus_map='selected'))
			try:
				cls.screen.child.main_window.messages.corresponding_widget().original_widget.focus_next()
			except IndexError:
				pass #First message will always cause this error
		source_widget.edit_text = '' #clear the edit box

class MainScreen(Constructor):
	'''Represents the whole screen.'''
	def __init__(self):
		self.child = ScreenSplit()
		super(MainScreen, self).__init__()

	def __construct(self, child):
		class MainScreenWidget(urwid.Frame):
			def __init__(self, *args, **kwargs):
				super(MainScreenWidget, self).__init__(*args, **kwargs)
			def keypress(self2, size, key):
				self.keypress(size, key)
		return MainScreenWidget(child.corresponding_widget(), footer=urwid.Text(('footer', 'gui-test'), align='center'), header=urwid.Text(('header', 'gui-test'), align='center'))

	def construct(self):
		return self.__construct(self.child)

	def keypress(self, size, key):
		return Selector.current_selected().keypress(size, key)

	def set_header(self, text):
		self.corresponding_widget().contents['header'][0].set_text(text)

	def set_footer(self, text):
		self.corresponding_widget().contents['footer'][0].set_text(text)

class ScreenSplit(Constructor):
	def __init__(self):
		self.sidebar = SideBar()
		self.main_window = MainWindow()
		super(ScreenSplit, self).__init__()

	def __construct(self, sidebar, main_window):
		class ScreenSplitWidget(urwid.Columns):
			def __init__(self, *args, **kwargs):
				super(ScreenSplitWidget, self).__init__(*args, **kwargs)

		return ScreenSplitWidget([(20, sidebar.corresponding_widget()), main_window.corresponding_widget()]) #the sidebar should be 20 chars

	def construct(self):
		return self.__construct(self.sidebar, self.main_window)


class SideBar(Constructor, Listlike):
	def __init__(self):
		self.channels = urwid.SimpleFocusListWalker([])
		self.l = self.channels #alias for Listlike inheritance
		super(SideBar, self).__init__()

	def __construct(self, channels):
		class SideBarWidget(urwid.ListBox):
			def __init__(self, *args, **kwargs):
				super(SideBarWidget, self).__init__(*args, **kwargs)

		return urwid.LineBox(SideBarWidget(channels))

	def construct(self):
		return self.__construct(self.channels)

class MainWindow(Constructor):
	def __init__(self):
		self.messages = Messages()
		self.text_entry = TextEntry()
		super(MainWindow, self).__init__()

	def __construct(self, messages, text_entry):
		class MainWindowWidget(urwid.Frame):
			def __init__(self, *args, **kwargs):
				super(MainWindowWidget, self).__init__(*args, **kwargs)

		return urwid.LineBox(MainWindowWidget(messages.corresponding_widget(), footer=text_entry.corresponding_widget()))

	def construct(self):
		return self.__construct(self.messages, self.text_entry)



class Messages(Constructor, Listlike):
	def __init__(self):
		self.messages = urwid.SimpleFocusListWalker([])
		self.l = self.messages #alias for Listlike inheritance
		super(Messages, self).__init__()

	def __construct(self, messages):
		class MessagesWidget(urwid.ListBox):
			def __init__(self, *args, **kwargs):
				super(MessagesWidget, self).__init__(*args, **kwargs)

			def focus_next(self):
				current_position = self.get_focus()[1]
				self.set_focus(current_position + 1, coming_from='above')

			def focus_prev(self):
				current_position = self.get_focus()[1]
				self.set_focus(current_position - 1, coming_from='below')

			def focus_top(self):
				self.set_focus(0)

			def focus_bottom(self):
				self.set_focus(len(self.body) - 1)

		return urwid.LineBox(MessagesWidget(messages))

	def construct(self):
		return self.__construct(self.messages)

class TextEntry(Constructor):
	def __init__(self):
		super(TextEntry, self).__init__()

	def __construct(self):
		class TextEntryWidget(urwid.Edit):
			def __init__(self, *args, **kwargs):
				super(TextEntryWidget, self).__init__(*args, **kwargs)

			def keypress(self, size, key):
				UserInputHandler.screen.set_header(str(key))
				super(TextEntryWidget, self).keypress((size[0],), key)

				if key == SHORTCUTS['scroll-up']:
					#scroll up
					try:
						UserInputHandler.screen.child.main_window.messages.corresponding_widget().original_widget.focus_prev()
					except Exception as e:
						os.system('echo \a') #BEEP!
						#UserInputHandler.screen.set_footer(str(e))

				elif key == SHORTCUTS['scroll-down']: #Scroll Down
					try:
						UserInputHandler.screen.child.main_window.messages.corresponding_widget().original_widget.focus_next()
					except Exception as e:
						os.system('echo \a') #BEEP!
						#UserInputHandler.screen.set_footer(str(e))

				elif key == SHORTCUTS['scroll-top']:
					try:
						UserInputHandler.screen.child.main_window.messages.corresponding_widget().original_widget.focus_top()
					except:
						os.system('echo \a') #BEEP!

				elif key == SHORTCUTS['scroll-bottom']:
					try:
						UserInputHandler.screen.child.main_window.messages.corresponding_widget().original_widget.focus_bottom()
					except:
						os.system('echo \a') #BEEP!

				elif key == 'enter':
					#TODO: send message
					UserInputHandler.handle(self.get_edit_text(), self)
				return key

		return urwid.LineBox(TextEntryWidget())

	def construct(self):
		return self.__construct()

	def keypress(self, size, keypress):
		self.corresponding_widget().keypress(size, keypress)

class UserMessage(urwid.Text):
	def __init__(self, *args, **kwargs):
		super(UserMessage, self).__init__(*args, **kwargs)
