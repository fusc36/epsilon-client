'''Just handles events'''

class EventHandler:
	'''Handles events'''
	@classmethod
	def setup(cls, gui, api):
		cls.gui = gui
		cls.api = api

	@classmethod
	def gui_api_event(cls, event: str, *args, **kwargs):
		'''Called when the gui wants to interact with the api'''
		pass

	@classmethod
	def api_gui_event(cls, event: str, *args, **kwargs):
		'''Called when the api wants to interact with the gui'''
		pass

	@classmethod
	def gui_event(cls, event: str, *args, **kwargs):
		'''Called when the gui wants to interact with itself'''
		if event == 'screen_split-toggle-focus':
			cls.gui.screen_split.toggle_focus()

		elif event == '':
			pass
