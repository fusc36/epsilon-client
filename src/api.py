from rocketchat_API.rocketchat import RocketChat
import requests

class API:
	def __init__(self, *args, **kwargs):
		self.rocket = RocketChat(*args, **kwargs)

	def get_channels(self):
		channels = self.rocket.channels_list()
		if channels.status_code == 200:
			channels_list = []
			for channel in channels.json()['channels']:
				channels_list.append(Room.construct(channel))
			return channels_list
		return None

	def get_messages(self, *args, **kwargs):
		history = self.rocket.channels_history(*args, **kwargs)
		if history.status_code == 200:
			messages_list = []
			for message in history.json()['messages']:
				messages_list.append(Message(message))
			return messages_list
		return

	def send_message(self, *args, **kwargs):
		message_sent = self.rocket.chat_post_message(*args, **kwargs)
		if message_sent.status_code == 200:
			return True
		return False

	def sort_messages(self, li):
		'''Sorts the messages in li by sent time'''
		li.sort(lambda message: message.timestamp)

class Room:
	def __init__(self, dict):
		self.id = dict.get('_id')
		self.type = dict.get('t')

	@staticmethod
	def construct(dict):
		if dict.get('t'):
			if dict.get('t') == 'd':
				return DirectChat(dict)
			elif dict.get('t') == 'c':
				return Chat(dict)
			elif dict.get('t') == 'p':
				return PrivateChat(dict)

		return None

class DirectChat(Room):
	'''DirectChat class'''
	pass		#Empty because it is basically the base class

class Chat(Room):
	def __init__(self, dict):
		self.name = dict.get('name')
		self.user = User(dict.get('u'))	#Room creator
		self.topic = dict.get('topic')
		super(Chat, self).__init__(dict)

class PrivateChat(Chat):
	def __init__(self, dict):
		self.read_only = dict.get('ro')
		super(PrivateChat, self).__init__(dict)

class Message:
	def __init__(self, dict):
		self.id = dict.get('_id')
		self.type = dict.get('t')
		self.timestamp = jsontime_to_datetime(dict.get('ts'))
		self.room_id = dict.get('rid')
		self.message = dict.get('msg')
		self.url = dict.get('url')			#list
		self.expires_at = jsontime_to_datetime(dict.get('expireAt'))
		self.mentions = dict.get('mentions')		#list
		self.user = User.from_dict(dict.get('u'))	#User()
		self.groupable = dict.get('groupable')
		self.updated_at = jsontime_to_datetime(dict.get('_updatedAt'))

class User:
	def __init__(self, dict):
		self.username = dict.get('username')
		self.id = dict.get('_id')

	@classmethod
	def from_dict(cls, dict):
		'''Returns a User() object if dict is not None'''
		if dict:
			return cls(dict)
		return None


def jsontime_to_datetime(string):
	return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')
