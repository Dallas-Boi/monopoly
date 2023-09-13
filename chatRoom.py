# Made 2-1-23 Wednesday
# This file handles all the chat room events

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import sys
import json
from errorHandler import send_monopoly_error
from games.monopoly_addons.multi_core import io

# Send the message to the server
def send_message(room, message):
    from account_core import user_account
    io.emit('send_message', {'id': user_account.get_account_id(), 'message': message, 'namespace': f'/{room}'})

# Adds the sent message to the chatBox
def update_chatBox(data):
    # Sets the messageInput to nothing
    messageInput.set('')

    # Adds the message to the chatRoom
    chatBox.status = NORMAL
    chatBox.insert('end', data['name'])
    chatBox['state'] = DISABLED


# Opens the chat room
def open_chat_window(room):
    # Root menu
    global root; global chatBox; global messageInput
    #from account_core import user_account
    root = tk.Toplevel()
    root.geometry('1000x500')
    root.title(f'ChatRoom ({room})')
    root.resizable(False, False)
    # Chatbox
    chatBox = Text(root, width=60, height=30, state=DISABLED);chatBox.place(x=0, y=0, relx=0.725, rely=0.5, anchor=CENTER)
    messageInput = Entry(root, width=60);messageInput.place(x=0, y=0, relx=0.2, rely=0.8, anchor=CENTER)
    submitButton = Button(root, text='Send Message', command=lambda: send_message(room, messageInput.get()))