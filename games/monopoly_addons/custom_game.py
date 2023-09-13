# Made 1-26-23 Thursday
# This file allows for custom Game modes

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import json
import time
import sys
import random
import os

moreBx = ''

# Cards List
check_buttons_cards = {}
customs_cards = []

# Items List
check_buttons_items = {}
customs_items = []

# other List
check_buttons_others = {'Mafia': {}, 'Player Shop': {}}
customs_others = ['Mafia', 'Player Shop']

mafia_cards = ['mafia_comes']

# Makes the UI for the customize Items
def start_custom():
    from games.monopoly import gameMode_win, start_players, disabled_cards, disabled_items, back_menu
    global moreBx; global check_values; global check_buttons
    gameMode_win.destroy()
    moreBx = tk.Toplevel()
    moreBx.title('Customizing Monopoly')
    moreBx.geometry("500x700")

    with open('gameData/cards.json', 'r') as cdb:
        cards = json.load(cdb)

    with open('gameData/shopItems.json', 'r') as idb:
        items = json.load(idb)

    # Makes the labels
    card_label = Label(moreBx, text='Cards', font=('Helvetica 15 underline'));card_label.place(x=0, y=20, relx=0.2, rely=0, anchor=CENTER)
    item_label = Label(moreBx, text='Items', font=('Helvetica 15 underline'));item_label.place(x=0, y=20, relx=0.5, rely=0, anchor=CENTER)
    other_label = Label(moreBx, text='Others', font=('Helvetica 15 underline'));other_label.place(x=0, y=20, relx=0.8, rely=0, anchor=CENTER)

    # This adds all advance Chest items to the customs_cards list
    for key, value in cards['chest'].items():
        # Checks if the card is in the advance gamemode
        if ((cards['chest'][key]['id'] in disabled_cards) == False) and (cards['chest'][key]['id'] != ''):
            customs_cards.append(cards['chest'][key]['id']+' (Chest)')
            check_buttons_cards[cards['chest'][key]['id']+' (Chest)'] = {}

    # This adds all advance Chance items to the customs_cards list
    for key, value in cards['chance'].items():
        # Checks if the card is in the advance gamemode
        if ((cards['chance'][key]['id'] in disabled_cards) == False) and (cards['chance'][key]['id'] != ''):
            customs_cards.append(cards['chance'][key]['id']+' (Chance)')
            check_buttons_cards[cards['chance'][key]['id']+' (Chance)'] = {}

    # This adds all advance items to the customs_items list
    for key, value in items['Player Shop'].items():
        # Checks if the card is in the advance gamemode
        if (key in disabled_items['Player Shop']) == False :
            customs_items.append(key)
            check_buttons_items[key] = {}

    # This adds all the values to check_value_cards
    for i in range(len(customs_cards)):
        var = tk.StringVar()
        check_buttons_cards[customs_cards[i]]['var'] = var

    # This adds all the values to check_value_items
    for i in range(len(customs_items)):
        var = tk.StringVar()
        check_buttons_items[customs_items[i]]['var'] = var

    # This adds all the values to check_value_others
    for i in range(len(customs_others)):
        var = tk.StringVar()
        check_buttons_others[customs_others[i]]['var'] = var

    # Makes the list of customizable cards
    for i in range(len(customs_cards)):
        check_buttons_cards[customs_cards[i]]['button'] = Checkbutton(moreBx, text=customs_cards[i], variable=check_buttons_cards[customs_cards[i]]['var'], onvalue=customs_cards[i], offvalue='')
        check_buttons_cards[customs_cards[i]]['button'].place(x=0, y=50+(i*30), relx=0.2, anchor=CENTER)

    # Disables Mafia Items
    check_buttons_cards['mafia_comes (Chest)']['button'].config(state=DISABLED)

    # Makes the list of customizable items
    for i in range(len(customs_items)):
        check_buttons_items[customs_items[i]]['button'] = Checkbutton(moreBx, text=customs_items[i], variable=check_buttons_items[customs_items[i]]['var'], onvalue=customs_items[i], offvalue='', state=DISABLED)
        check_buttons_items[customs_items[i]]['button'].place(x=0, y=50+(i*30), relx=0.5, anchor=CENTER)

    # Makes the list of customizable others
    for i in range(len(customs_others)):
        check_buttons_others[customs_others[i]]['button'] = Checkbutton(moreBx, text=customs_others[i], variable=check_buttons_others[customs_others[i]]['var'], onvalue=customs_others[i], offvalue=f'', command=lambda: others_update())
        check_buttons_others[customs_others[i]]['button'].place(x=0, y=50+(i*30), relx=0.8, anchor=CENTER)

    # End Buttons
    start_button = Button(moreBx, text='Start Game', command=lambda: start_players('Monopoly', 'Custom'));start_button.place(x=0, y=50+(len(customs_items)*30), relx=0.5, rely=0, anchor=CENTER)
    back_button = Button(moreBx, text='Back to Gamemodes', command=lambda: back_menu(moreBx, 'menu')); back_button.place(x=0, y=0, relx=0.2, rely=0.8, anchor=CENTER)

# This executes when the "PLayer Shop" is selected
def others_update():
    with open('gameData/cards.json', 'r') as cdb:
        cards = json.load(cdb)

    # Updates all check_buttons_items to state=NORMAL
    # If the player Shop was enabled
    if check_buttons_others['Player Shop']['var'].get() == 'Player Shop':
        for key, value in check_buttons_items.items():
            check_buttons_items[key]['button'].config(state=NORMAL)
    # If the player shop was disabled
    elif check_buttons_others['Player Shop']['var'].get() == '':
        for key, value in check_buttons_items.items():
            check_buttons_items[key]['button'].config(state=DISABLED)
            check_buttons_items[key]['var'].set('')

    # If the player enables the Mafia
    if check_buttons_others['Mafia']['var'].get() == 'Mafia':
        for i in range(len(check_buttons_cards)):
            if cards['chest'][str(i+1)]['id'] in mafia_cards:
                check_buttons_cards[cards['chest'][str(i+1)]['id']+' (Chest)']['button'].config(state=NORMAL)
    # If "Mafia" was Disabled
    elif check_buttons_others['Mafia']['var'].get() == '':
        for i in range(len(check_buttons_cards)):
            if cards['chest'][str(i+1)]['id'] in mafia_cards:
                check_buttons_cards[cards['chest'][str(i+1)]['id']+' (Chest)']['button'].config(state=DISABLED)
                check_buttons_cards[cards['chest'][str(i+1)]['id']+' (Chest)']['var'].set('')