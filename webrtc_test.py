'''WebRTC test client'''

import websockets
import asyncio
import src.api.api as api
import json
import sys
import threading


class JSONMessage:
	'''Simple class that works with API.new_message()'''
	def __init__(self, json):
		self.json = json
	def serialize(self):
		return self.json

def main():
	username = sys.argv[1]
	password = sys.argv[2]
	server_uri = sys.argv[3]

	API = api.API(username, password, server_uri, debug=True)
	loop = asyncio.new_event_loop()
	def start_loop(loop):
		asyncio.set_event_loop(loop)
		loop.run_until_complete(API.main_loop())

	thread = threading.Thread(target=start_loop, args=(loop,))
	thread.run()
	while True:
		cmd = input('> ')
		API.new_message(JSONMessage(cmd))

main()
