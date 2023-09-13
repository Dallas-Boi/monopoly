# Made 1-26-23
# This file handles the connections between the server and the players; Also will update the board and players

import socketio
import asyncio
from account_core import user_account

io = socketio.Client()
io.sid = user_account.get_account_id()
print(io.sid)
io.connect('https://easyGO.theweebmonkey.repl.co')
io.connect('https://easyGO.theweebmonkey.repl.co', namespaces=['/chat'])
io.emit('send_message', {'id': io.sid, 'message': 'Hello Buddy'})


@io.event
def connect():
    print("I'm connected!")

@io.event
def connect_error():
    print("The connection failed!")

@io.event
def update_message(data):
    return data

io.emit('connect_room', {'id': io.sid, 'room': 'public'})

