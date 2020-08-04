import json
import websockets
from hashlib import sha256
import pprint

class API:
	def __init__(self, username, password, server_uri, debug=False):
		self.methods = {}
		self.subscriptions = {}
		self.queue = []

		self.username = username
		self.passhash = sha256(password.encode('ascii')).hexdigest() #hash the password
		self.server_uri = server_uri
		self.debug = debug
		self.id = 0
		self.token = None

		self.connect()
		self.login()

	async def main_loop(self):
		'''The main loop that is run in an event loop.
		The main jobs of the loop are:
		1. Receive messages from the server and broadcast them
		2. Check the queue for messages to send to the server'''
		async with websockets.connect(self.server_uri) as websocket:
			while True:
				try:
					# Send all messages in the queue
					while self.queue:
						item = self.queue.pop(0)
						await self.send(websocket, item)

					# Receive a message and handle it
					await self.handle_result(await websocket.recv())
				except websockets.exceptions.ConnectionClosed:
					break

	async def send(self, websocket, item):
		'''Sends a message. Used internally.'''
		item_json = item.serialize()
		if isinstance(item, Method):
			self.methods[item.id] = item
		elif isinstance(item, Subscription):
			self.subscription[item.id] = item
		await websocket.send(item_json)

	async def handle_result(self, result):
		'''Called when the API receives a result. Used internally.'''
		dict = json.loads(result)
		if self.debug:
			print('Result: ')
			pprint.pprint(dict) #temporary, for testing purposes
		if dict.get('msg') == 'ping':
			self.new_message(Message({'msg': 'pong'}))

		if dict.get('msg') and dict.get('id'):
			result = Result.from_dict(dict)
			method = self.methods[result.id]
			del self.methods[result.id]
			method.set_result(result)

	def new_message(self, message):
		'''Adds a message to the queue. Used in conjunction to the gui & event handler.'''
		self.queue.append(message)


	def new_id(self):
		'''Generates a new id to use when sending messages'''
		self.id += 1
		return self.id

	def _method(function):
		'''Decorator for methods'''
		def decorator(self, *args, **kwargs):
			method, params = function(self, *args, **kwargs)
			id = str(self.new_id())
			msg = 'method'
			self.new_message(Method(msg, id, method, params=params))
		return decorator

	def connect(self):
		'''You have to send this request first or else the request will not go through'''
		self.new_message(Connect)


	@_method
	def archive(self, room_id):
		'''Archiving a room marks it as read only and then removes it from the channel list on the left.'''
		return ('archiveRoom', [str(room_id)])


	@_method
	def get_public_settings(self):
		'''Returns the public settings of the server'''
		method = 'public-settings/get'
		return (method, None)

	@_method
	def get_rooms(self, date=0):
		'''Returns the rooms of the server (update and remove)'''
		return ('rooms/get', [{'$date': date}])

	@_method
	def login(self):
		'''Sends a login method.'''
		method = 'login'
		if self.token:
			params = [{'resume': 'auth-token'}]
		else:
			params = [
				{
					'user': {'username': self.username},
					'password': {
						'digest': self.passhash,
						'algorithm': 'sha256'
					}
				}
			]
		return (method, params)







class Message:
	'''Generic message type'''
	def __init__(self, data):
		self.result = None
		self.data = data
		self.on_result_func = None
		self.on_error_func = None

	def serialize(self):
		'''Return a json string'''
		return json.dumps(self.data)

	def set_result(self, result):
		'''Sets a result'''
		self.result = result
		if isinstance(self.result, Error):
			if self.on_error_func:
				self.on_error_func(self, result)
		elif isinstance(self.result, Result):
			if self.on_result_func:
				self.on_result_func(self, result)

	def on_result(self):
		'''Returns a decorator to call a function on result.
		   The function in question should accept two arguments: the original message and the result.'''
		def on_result_inner(function):
			self.on_result_func = function
			return function
		return on_result_inner

	def on_error(self):
		'''Returns a decorator to call a function on error.
		   The function in question should accept two arguments: the original message and the error.'''
		def on_error_inner(function):
			self.on_error_func = function
			return function
		return on_error_inner




class Method(Message):
	'''Real-time API Method object'''
	def __init__(self, msg, id, method, params=[]):
		self.msg = msg
		self.id = id
		self.method = method
		self.params = params
		self.result = self.on_result_func = self.on_error_func = None

	def serialize(self):
		d = {
			'msg': self.msg,
			'id': self.id,
			'method': self.method
		}
		if self.params:
			d['params'] = self.params
		return json.dumps(d)


class Subscription(Message):
	'''Real-time API Subscription object'''
	def __init__(self, msg, id, name, params=[]):
		self.msg = msg
		self.id = id
		self.name = name
		self.params = params
		self.result = self.on_result_func = self.on_error_func = None

	def serialize(self):
		return json.dumps({
			'msg': self.msg,
			'id': self.id,
			'name': self.name,
			'params': self.params
		})

	def unsub(self, api):
		'''Unsubscribes from the subscription'''
		class Unsub(Message):
			'''Unsubscribe message'''
			def __init__(self2, id):
				self2.msg = 'unsub'
				self2.id = id
			def serialize(self2):
				return json.dumps({
					'msg': self2.msg,
					'id': self2.id
				})
		unsub = Unsub(self.id)
		api.send_message(unsub)

class Connect:
	'''Connect request'''
	@staticmethod
	def serialize():
		return json.dumps({
			'msg': 'connect',
			'version': '1',
			'support': ['1']
		})


class Result:
	'''Result object'''
	def __init__(self, msg, id, result):
		self.msg = msg
		self.id = id
		self.result = result

	@classmethod
	def from_dict(cls, dict):
		if dict.get('error'):
			#it's an error type
			return Error(dict['msg'], dict['id'], dict['error'])
		return Result(dict['msg'], dict['id'], dict['result'])


class Error(Result):
	'''result error object'''
	def __init__(self, msg, id, error):
		self.msg = msg
		self.id = id
		self.error = error
