'''This file contains all of the urwid custom widgets that will be used in gui.py.'''

import urwid
import os
from ..event_handler import EventHandler

#Templates

class SmartListBox(urwid.ListBox):
	'''ListBox Template'''
	def __init__(self, *args, **kwargs):
		super(SmartListBox, self).__init__(*args, **kwargs)

	def focus_next(self):
		'''Focus the next message'''
		current_focus_position = self.focus_position
		if current_focus_position == (len(self.body) - 1):
			return
		self.focus_position += 1

	def focus_prev(self):
		'''Focus the previous message'''
		current_focus_position = self.focus_position
		if current_focus_position == 0:
			return
		self.focus_position -= 1

	def focus_top(self):
		'''Focus the top widget in the listwalker'''
		self.focus_position = 0

	def focus_botton(self):
		'''Focus the botton widget in the listwalker'''
		self.focus_position = (len(self.body) - 1)

	def add_widget(self, widget):
		'''Add a widget to the listwalker, then update'''
		self.body.append(widget)
		if self.focus_position = len(self.body) - 2: #If the focus position WAS at the bottom:
			self.focus_position += 1

#Widgets

class MainScreen(urwid.Frame):
	'''Represents the main screen of the app'''
	def __init__(self, *args, **kwargs):
		super(MainScreenWidget, self).__init__(*args, **kwargs, header=urwid.Text(''), footer=urwid.Text(''))

	def set_header(self, widget):
		self.contents['header'][0] = widget
	def set_footer(self, widget):
		self.contents['footer'][0] = widget

class ScreenSplit(urwid.Columns):
	'''Represents the column that splits the sidebar from the message window'''
	def __init__(self, widget_list):
		super(ScreenSplit, self).__init__(widget_list, focus_column=1)

	def toggle_focus(self):
		if self.focus_position = 1:
			self.focus_position = 0
			return
		self.focus_position = 1

class SideBar(SmartListBox):
	'''Represents the side bar, which displays the chat channels that are available'''
	def __init__(self, listwalker):
		super(SideBar, self).__init__(listwalker)

	def keypress(self, size, key):
		if key == '': #Up arrow
			self.focus_prev()
		elif key == '': #Down arrow
			self.focus_next()
		elif key == 'tab':
			EventHandler.gui_event('screen_split-toggle-focus')
		elif key == '': #Enter
			pass

class MainWindow(urwid.Frame):
	'''Represents the message window, which contains the messages of the current chat and the text edit box to send messages from'''
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.focus_position = 'body'

	def keypress(self, size, key):
		#Propagate the keypress to both the message widget and the input widget
		# so that both can be modified by the same focus
		self.contents['body'][0].keypress(size, key)
		self.contents['footer'][0].keypress((size[0],), key)

class Messages(SmartListBox):
	'''Represents the messages of the chat'''
	def __init__(self, *args, **kwargs):
		super(Messages, self).__init__(*args, **kwargs):

	def keypress(self, size, key):
		if key == '': #Up arrow
			self.focus_prev()
		elif key == '': #Down arrow
			self.focus_next()
		elif key == 'tab':
			EventHandler.gui_event('screen_split-toggle-focus')

class TextEntry(urwid.Edit):
	'''Represents the text edit box for writing messages'''
	def __init__(self, *args, **kwargs):
		super(TextEntry, self).__init__(*args, **kwargs)

	def keypress(self, size, key):
		pass

class UserMessage(urwid.Text):
	'''Represents a message'''
	def __init__(self, *args, **kwargs):
		super(UserMessage, self).__init__(*args, **kwargs)



