import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import sys
import json
from errorHandler import send_monopoly_error

# When a game ends or the players return
def make_menu():
    # Root menu
    global root
    root = tk.Toplevel()
    root.geometry('1000x500')
    root.title('Main Menu')
    root.resizable(False, False)
    mainMenu()

def destroy_root():
    root.destroy()

# Plays the given gameType
def play(gameType):
    global monopoly
    if 'monopoly' in gameType:
        from games.monopoly import start
        start('Monopoly', monopV)
    elif 'offCheck' in gameType:
        from games.checkersOn import start
        start('Local Checkers')
    elif 'Connect' in gameType:
        from games.connect import start
        connect.config(state='disabled')
        start('Connect')

# This changes the Version of the change logs
def change_version(version):
    # Opens the JSON Change Log
    global output_logs
    with open('infoLogs/changelog_mon.json', 'r') as ch:
        cLogs = json.load(ch)

    date = cLogs[version].get('Date')
    changelog = ''
    # This will add everything to the output
    output_logs['state'] = NORMAL
    output_logs.delete("1.0","end")
    # Checks if log has "Date"
    if date != None:
        changelog = f'Release Date: {date} \n'
    
    if cLogs[version].get('Future Updates'):
        changelog = f'Future Updates\n-----------\n'
        for i in range(len(cLogs[version]['Future Updates'])):
            changelog = changelog + '• ' +cLogs[version]['Future Updates'][i]+'\n'

    # Checks if log has "Release"
    if cLogs[version].get('Release') != None:
        changelog = changelog + f'Released:\n-----------\n'+cLogs[version]['Release']+'\n'

    # Checks if the log has "Name"
    if cLogs[version].get('Name') != None:
        changelog = changelog + f'Update Name: '+cLogs[version]['Name']+'\n'

    # Checks if log has "Added"
    if cLogs[version].get('Added') != None:
        changelog = changelog + f'-\nAdded:\n-----------\n'
        for i in range(len(cLogs[version]['Added'])):
            changelog = changelog + f'• '+cLogs[version]['Added'][i]+'\n'

    # Checks if log has "Removed"
    if cLogs[version].get('Removed') != None:
        changelog = changelog + f'-\nRemoved:\n-----------\n'
        for i in range(len(cLogs[version]['Removed'])):
            changelog = changelog + f'• '+cLogs[version]['Removed'][i]+'\n'

    # Checks if log has "Reworked"
    if cLogs[version].get('Reworked') != None:
        changelog = changelog + f'-\nReworked:\n-----------\n'
        for i in range(len(cLogs[version]['Reworked'])):
            changelog = changelog + f'• '+cLogs[version]['Reworked'][i]+'\n'

    # Checks if log has "Changes"
    if cLogs[version].get('Changes') != None:
        changelog = changelog + f'-\nChanges:\n-----------\n'
        for i in range(len(cLogs[version]['Changes'])):
            changelog = changelog + f'• '+cLogs[version]['Changes'][i]+'\n'
    
    # Checks if log has "Fixes"
    if cLogs[version].get('Fixes') != None:
        changelog = changelog + f'-\nFixes:\n-----------\n'
        for i in range(len(cLogs[version]['Fixes'])):
            changelog = changelog + f'• '+cLogs[version]['Fixes'][i]+'\n'

    # Prints the log to the output
    output_logs.insert('end', f'{changelog}')
    output_logs['state'] = DISABLED
      
# Main Menu (First thing that pops up)
def mainMenu():
    global monopV
    # Versions and Modes
    monopV = "V 0.6"

    # Makes the Main Menu
    global monopoly; global checkOff; global connect; global debugP; global debugLabel
    global sub; global betaTesterP; global betaMode; global save_key
    global usernameEntry; global passwordEntry; global output_logs
    debug = True
    betaMode = False
    save_key = ''

    # Labels
    header = ttk.Label(root, text="Pick a Game!")
    header.place(x=0, y=10, relx=0.5, anchor=CENTER)

    # Game Buttons
    monopoly = ttk.Button(root, text=f'Monopoly {monopV}');monopoly.place(x=0, y=40, relx=0.5, anchor=CENTER);monopoly.bind('<Button-1>', lambda e: play('monopoly'))
    checkOff = ttk.Button(root, text="Local Checkers");checkOff.place(x=-94, y=40, relx=0.5, anchor=CENTER);checkOff.bind('<Button-1>', lambda e: play('offCheck'))
    connect = ttk.Button(root, text="4 in a line");connect.place(x=88, y=40, relx=0.5, anchor=CENTER);connect.bind('<Button-1>', lambda e: play('Connect'))

    # Change Log Handling
    with open('infoLogs/changelog_mon.json', 'r') as ch:
        cLogs = json.load(ch)

    version_list = list(cLogs.keys())
    selected = StringVar()
    selected.set('')
    selected.trace("w", lambda name, index, mode, sv=selected: change_version(selected.get()))
    ownedList = OptionMenu(root, selected, *version_list);ownedList.place(x=0, y=10, relx=0.5, rely=0.2, anchor=CENTER)

    # This makes the output box for the change logs
    output_logs = Text(root, width=110, height=20, state=DISABLED);output_logs.place(x=0, y=0, relx=0.5, rely=0.6, anchor=CENTER)
    
    root.mainloop()