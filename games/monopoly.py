# Started on 10-31-2022 Monday
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import json
import time
import sys
import random
import os
from colour import Color
from io import BytesIO
from PIL import Image, ImageTk

from menu import make_menu, destroy_root
from errorHandler import send_monopoly_error
from games.monopoly_addons.adv_game import commit_arson, break_their_knees, player_press_charges, maifa_or_hospital, failed_to_pay
from games.monopoly_addons.new_tab import new_frame
from games.monopoly_addons.core import Players, grid_spot, check_for_exploit, save_monopoly_V2, load_save
from games.monopoly_addons.commands import console
from games.monopoly_addons.custom_game import start_custom

global antiExploits
antiExploits = check_for_exploit(1500, 1)
# Checks if the color is valid
def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError: # The color code was not found
        return False

# Makes strike throughs on the text
def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

# Ends the game
def end_monopoly(winner = None):
    try:
        if winner != None:
            print(f'The winner is '+str(players[turn].get_player_name()))
            actLabel.config(text=f'{winner} was the winner')
            game.after(5000, game.destroy())
            game.after(1000, make_menu())
        else:
            game.after(1000, game.destroy())
            game.after(100, make_menu())
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

# Saves and ends the game (WIP)
def save_game():
    try:
        # Variables that will be set to make the data
        if action_buttons['action5']['text'] == 'End Turn':
            change_turn()
        monopoly_game_data.send_data()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# -- Start | Monopoly Game Data Handling -- #
# Loads the monopoly saved data
def load_monopoly_data(data):
    try:
        global monopoly_game_data
        global names; global colors

        monopoly_game_data = save_monopoly_V2(data['saveID'], data['game_mode'], data['turn'], data['version'], data['players'], data['cards'], data['oojUsed'], data['houses'])
        start_game('Monopoly', None, 'loading')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Updates the monopoly Data
def update_monopoly_data():
    try:
        monopoly_game_data.update_save_game(game_mode, turn, players, randomize_cards, oojUsed, [houses, hotels])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# -- End | Monopoly Game Data Handling -- #

# Player Management | Start
# Manages the bankruptcy properties
def bankrupt_props(item):
    try:
        global br_boolean
        br_boolean = True
        new_frame('auction', item, player_prop_list, br_boolean)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Banksrupts' the player
def bankrupt_player(by, player):
    try:
        global player_prop_list; global br_player; 
        # Keeps the bankrupt player ID | Changes the turn
        br_player = turn
        
        change_turn()
        # Starts an auction for all the bankrupts player items
        player_prop_list = list(players[br_player]['prop'].keys())
        #Deletes the player from the player data 
        del players[br_player]
        board.delete(br_player)

        # Checks to see if there is only one player left
        if len(players) == 1:
            end_monopoly(turn)
            return
        
        # Sees if the player bankrupt because of another player or if they did it to themself
        if by == 'player':
            for i in range(len(player_prop_list)):
                # Gives the properties from the player that went bankrupt to the player that made them go bankrupt
                players[br_player].get_player_properties()[player_prop_list[i]]['house'] = 0; players[br_player].get_players_properties()[player_prop_list[i]]['mortgage'] = False #Placed in for now will implement later
                players[player].get_player_properties()[player_prop_list[i]] = players[br_player].get_players_properties()[player_prop_list[i]]
        # If the bankrupt player went bankrupt because of themself
        elif by == 'self':
            if len(player_prop_list) >= 1:
                bankrupt_props(player_prop_list[0])

        # Makes a strike through the player
        labels[br_player].config(fg='red', text=strike(labels[br_player]['text']))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Changes the current Turn
def change_turn():
    try:
        global turn; global antiExploits
        # This is the anti-cheat check
        if turn != 'player99':
            if antiExploits.check_exploit(players[turn].get_player_cash()) == 'EXPLOIT':
                print('System has detected '+players[turn].get_player_name()+' of cheating. Their money has been set to 0\nIF this is wrongly accused please let me know.')
                players[turn].set_player_cash(0)
                update_cash_label(turn)
        
        # Everything below is to set the next turn
        turn = 'player'+str(int(turn[6:7])+1)
        rollLabel['text'] = ''
        # Action button config
        reset_action_buttons()
        action_buttons['action5'].config(text='Roll Dice', command=lambda: roll_dice(), state=NORMAL)
        action_buttons['action6'].config(text='Bankrupt', command=lambda: bankrupt_player(None, turn))
        
        shop_button.config(state=DISABLED);
        # Checks to see if the new turn is a valid player and if not then it sets the turn to player1
        list_current_players = list(players.keys())
        if turn not in list_current_players:
            turn = list_current_players[0]

        name = players[turn].get_player_name()
        actLabel.config(text=f'It is now {name} turn now!')
        # Underlines the current turn and removes the underline when it changes the turn
        for key, value in labels.items():
            labels[key].config(font=('Helvetica 10'))
        labels[turn].config(font=('Helvetica 10 underline'))
        # Disables Bankrupt until the end of the turn
        action_buttons['action6'].config(state = DISABLED, command='')

        # Updates monopoly saved data
        update_monopoly_data()
        # This handles the mafia and anti-cheat system
        antiExploits.update_before_money(players[turn].get_player_cash())
        maifa_bank_button.config(state=NORMAL)
        
        # This will check if the player has a loan
        if (players[turn].get_player_hasLoan() == True):
            players[turn].take_player_loan_payIn(1)
            if (players[turn].get_player_loan_payIn() == 0):
                print('No Payment')
                failed_to_pay(players[turn].get_player_properties(), turn)

        # Checks to see if there is only one player left
        if len(list_current_players) == 1:
            end_monopoly(turn)

        # Checks to see if the player is in jailed
        if players[turn].get_player_jail() == True:
            config_player_jailStatus('start', None)
    except Exception as e:
        7

# Moves the player
def move_player(spot, to):
    try:
        for key, value in grid.items():
            if grid[key].get_spot_name() == to:
                x, y = grid[key].get_spot_x(), grid[key].get_spot_y()
                #if int(turn[6:7]) > 3:
                board.moveto(turn, x, y)
        action_buttons['action5'].config(state=NORMAL)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Updates the players Money Labels
def update_cash_label(turn):
    try:
        if turn != "all":
            name = players[turn].get_player_name()
            labels[turn].config(text=f'{name} has: $'+str(players[turn].get_player_cash()))
        elif turn == "all":
            for player in players:
                name = players[player].get_player_name()
                labels[player].config(text=f'{name} has: $'+str(players[player].get_player_cash()))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes the end turn options (trading and editing properties)
def end_turn_part():
    try:
        # Breaking knees is only in the "Advance" Gamemode
        if thereIsShop == True:
            if players[turn].get_player_jail() == False:
                # Makes it so that people can break others knees if they are in the same spot
                item = None
                if players[turn].get_player_inventory().get('Sledge hammer') != None:
                    item = 'Sledge Hammer'
                elif players[turn].get_player_inventory().get('Bat') != None:
                    item = 'Bat'

                # Checks for people in the same spot
                for key , value in players.items():
                    if (key != turn) and (players[key].get_player_spot() == players[turn].get_player_spot()):
                        actLabel.config(text=f'Break '+players[key].get_player_name()+f'\'s Knees with a {item}\n or Continue')
                        action_buttons['action2'].config(text=f'Commit', command=lambda: break_their_knees(key, item), state=NORMAL)
                        if item == None:
                            action_buttons['action2'].config(state=DISABLED)
                        break
                # Checks if the item is None (If so disables the commit button)
        
        
        action_buttons['action3'].config(state=NORMAL, text='Edit Properties', command=lambda: new_frame('edit', None))
        action_buttons['action4'].config(state=NORMAL, text='Trade', command=lambda: new_frame('trade', None))
        action_buttons['action5'].config(state=NORMAL)
        action_buttons['action6'].config(state=NORMAL, command=lambda:bankrupt_player('self', None))
        shop_button.config(state=NORMAL, command= lambda: new_frame('shop', None))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# This gives action_buttons['action5'] button its click feature back
def action5_button_status():
    try:
        # Checks to see if the status is end_turn
        if action_buttons['action5']['text'] == 'End Turn':
            action_buttons['action5'].config(command=lambda: change_turn(), state=NORMAL)
            end_turn_part()
        elif action_buttons['action5']['text'] == 'Roll Dice':
            action_buttons['action5'].config(command=lambda: roll_dice(), state=NORMAL)
        else:
            print('Error Occured with the text. Setting action5 to "End Turn".')
            action_buttons['action5'].config(text='End Turn', command=lambda: change_turn(), state=NORMAL)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Sets all action buttons to nothing and unbinds all
def reset_action_buttons(act = None):
    try:
        if act == 'disable':
            for i in range(len(action_buttons)):
                action_buttons[f'action{i+1}'].config(state=DISABLED)
        else:
            for i in range(len(action_buttons)-2):
                action_buttons[f'action{i+1}'].config(text='', state=DISABLED, command='')
    except Exception as e:
        print(e)

# Player Management | End

# Payment Functions | Start
# Player Buys the Porperty
def buy_prop(spot, propData):
    try:
        if players[turn].get_player_cash() >= propData[spot]['cost']:
            players[turn].take_player_cash(propData[spot]['cost'])
            players[turn].add_player_properties(spot)
            board.itemconfig(f'bp_{spot}', fill=players[turn].get_player_color())
            # Functions that help complete
            prop_manage(spot, propData)
            action5_button_status()
            update_cash_label(turn)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Updates House/Hotel Labels
def update_house_label():
    house_label.config(text=f'Houses Left: {houses}')
    hotel_label.config(text=f'Hotels Left: {hotels}')

# Adds a house to the property
def add_house(spot):
    try:
        global houses; global hotels
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)
        cData = players[turn]
        
        # Checks where the current spot is and places a house/hotel if can
        for key, value in grid.items():
            if grid[key].get_spot_name() == spot:
                # Adds a house to the upgraded Property
                if (houses != 0) and (players[turn].get_player_properties()[spot]['house']+1 < 5):
                    if (key >= 2) and (key <= 10):
                        board.create_rectangle((grid[key].get_spot_x()+2.5)+(cData.get_player_properties()[spot]['house']*10), grid[key].get_spot_y(), (grid[key].get_spot_x()+7.5)+(cData.get_player_properties()[spot]['house']*10), grid[key].get_spot_y()+15, fill='#4fff6c', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Left Side
                    elif (key >= 12) and (key <= 20):
                        board.create_rectangle(grid[key].get_spot_x()+60, (grid[key].get_spot_y()+2.5)+(cData.get_player_properties()[spot]['house']*10), grid[key].get_spot_x()+75, (grid[key].get_spot_y()+7.5)+(cData.get_player_properties()[spot]['house']*10), fill='#4fff6c', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Top of the Board
                    elif (key >= 22) and (key <= 30):
                        board.create_rectangle((grid[key].get_spot_x()+2.5)+(cData.get_player_properties()[spot]['house']*10), grid[key].get_spot_y()+60, (grid[key].get_spot_x()+7.5)+(cData.get_player_properties()[spot]['house']*10), grid[key].get_spot_y()+75, fill='#4fff6c', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Right Side
                    elif (key >= 32) and (key <= 40):
                        board.create_rectangle(grid[key].get_spot_x(), (grid[key].get_spot_y()+2.5)+(cData.get_player_properties()[spot]['house']*10), grid[key].get_spot_x()+15, (grid[key].get_spot_y()+7.5)+(cData.get_player_properties()[spot]['house']*10), fill='#4fff6c', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Removes a house from the total houses
                    houses -= 1
                # If the property is upgrading to a hotel
                elif (hotels != 0) and (players[turn].get_player_properties()[spot]['house']+1 == 5):
                    # Bottom of the Board
                    for i in range(5):
                        board.delete(f'{i+1}_{spot}')
                    if (key >= 2) and (key <= 10):
                        board.create_rectangle((grid[key].get_spot_x()+15), grid[key].get_spot_y(), (grid[key].get_spot_x()+25), grid[key].get_spot_y()+15, fill='#ff4f87', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Left Side
                    elif (key >= 12) and (key <= 20):
                        board.create_rectangle(grid[key].get_spot_x()+60, (grid[key].get_spot_y()+15), grid[key].get_spot_x()+75, (grid[key].get_spot_y()+25), fill='#ff4f87', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Top of the Board
                    elif (key >= 22) and (key <= 30):
                        board.create_rectangle((grid[key].get_spot_x()+15), grid[key].get_spot_y()+60, (grid[key].get_spot_x()+25), grid[key].get_spot_y()+75, fill='#ff4f87', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Right Side
                    elif (key >= 32) and (key <= 40):
                        board.create_rectangle(grid[key].get_spot_x(), (grid[key].get_spot_y()+15), grid[key].get_spot_x()+15, (grid[key].get_spot_y()+25), fill='#ff4f87', tag=str(cData.get_player_properties()[spot]['house']+1)+f'_{spot}')
                    # Removes a hotel from the total houses and adds 4 houses back to the total
                    houses += 4
                    hotels -= 1
                update_house_label()
                players[turn].set_player_property_nextHouse(spot, False)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Removes a house from the property
def remove_house(spot):
    try:
        global houses; global hotels
        # This removes a hotel from the property
        if players[turn].get_player_properties()[spot]['house'] == 5:
            board.delete(f'5_{spot}')
            hotels += 1
            players[turn].get_player_properties()[spot]['house'] = 0
            # This is a placeholder solution until I figure out how to fix the problem of
            # The game saying you have 4 houses but appears to the player that they still have their hotel
            # This will add houses to the property when the user sells their Hotel
            for key, vlaue in grid.items():
                if grid[key].get_spot_name() == spot:
                    for i in range(4):
                        if (key >= 2) and (key <= 10):
                            board.create_rectangle((grid[key].get_spot_x()+2.5)+(players[turn].get_player_properties()[spot]['house']*10), grid[key].get_spot_y(), (grid[key].get_spot_x()+7.5)+(players[turn].get_player_properties()[spot]['house']*10), grid[key].get_spot_y()+15, fill='#4fff6c', tag=str(players[turn].get_player_properties()[spot]['house']+1)+f'_{spot}')
                        # Left Side
                        elif (key >= 12) and (key <= 20):
                            board.create_rectangle(grid[key].get_spot_x()+60, (grid[key].get_spot_y()+2.5)+(players[turn].get_player_properties()[spot]['house']*10), grid[key].get_spot_x()+75, (grid[key].get_spot_y()+7.5)+(players[turn].get_player_properties()[spot]['house']*10), fill='#4fff6c', tag=str(players[turn].get_player_properties()[spot]['house']+1)+f'_{spot}')
                        # Top of the Board
                        elif (key >= 22) and (key <= 30):
                            board.create_rectangle((grid[key].get_spot_x()+2.5)+(players[turn].get_player_properties()[spot]['house']*10), grid[key].get_spot_y()+60, (grid[key].get_spot_x()+7.5)+(players[turn].get_player_properties()[spot]['house']*10), grid[key].get_spot_y()+75, fill='#4fff6c', tag=str(players[turn].get_player_properties()[spot]['house']+1)+f'_{spot}')
                        # Right Side
                        elif (key >= 32) and (key <= 40):
                            board.create_rectangle(grid[key].get_spot_x(), (grid[key].get_spot_y()+2.5)+(players[turn].get_player_properties()[spot]['house']*10), grid[key].get_spot_x()+15, (grid[key].get_spot_y()+7.5)+(players[turn].get_player_properties()[spot]['house']*10), fill='#4fff6c', tag=str(players[turn].get_player_properties()[spot]['house']+1)+f'_{spot}')
                        # Removes a house from the total houses
                        houses -= 1
                        players[turn].get_player_properties()[spot]['house'] += 1
                    break
        # This removes a house from the property
        elif players[turn].get_player_properties()[spot]['house'] < 5:
            board.delete(str(players[turn].get_player_properties()[spot]['house'])+f'_{spot}')
            houses += 1
            players[turn].get_player_properties()[spot]['house'] -= 1
        else:
            print('HOW')
        update_house_label()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Player mortgages the Property
# The Problem is that a property is not allowing a removing a house due to being false
def sell_prop(spot, mafia = False):
    try:
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)
        # Checks if the property hasn't been mortgage
        if players[turn].get_player_properties()[spot]['mortgage'] != True:
            # If the player is mortgaging their property
            if players[turn].get_player_properties()[spot]['house'] == 0:
                players[turn].set_player_property_mortgage(spot, True)
                # This will set the line through the property
                if (players[turn].get_player_spot() <= 10): # If the play is on the bottom row
                    board.create_rectangle(grid[players[turn].get_player_spot()].get_spot_x(), 440, grid[players[turn].get_player_spot()].get_spot_x()+40, 445, fill="red")
                elif (players[turn].get_player_spot() <= 20): # If the player is on the left row
                    board.create_rectangle(65, grid[players[turn].get_player_spot()].get_spot_y(), 70, grid[players[turn].get_player_spot()].get_spot_y()+40, fill="red")
                elif (players[turn].get_player_spot() <= 30): # If the player is on the Top row
                    board.create_rectangle(grid[players[turn].get_player_spot()].get_spot_x(), 65, grid[players[turn].get_player_spot()].get_spot_x()+40, 70, fill="red")
                elif (players[turn].get_player_spot() <= 40): # If the player is on the Right row
                    board.create_rectangle(440, grid[players[turn].get_player_spot()].get_spot_y(), 445, grid[players[turn].get_player_spot()].get_spot_y()+40, fill="red")
                # The button will only change if the player mortgages it
                if mafia == False:
                    action_buttons['action1'].config(text='Un-mortgage', command=lambda: buy_house(spot, int(((propData[spot]['cost']/2)*0.1)+propData[spot]['cost']/2)));
                    players[turn].add_player_cash((propData[spot]['cost'])/2)
            else:
                equal_each = []
                all_color = []
                # Puts the set of properties into a list
                for key, value in players[turn].get_player_properties().items():
                    if key[0:len(key)-1] in spot:
                        all_color.append(key)
                
                # Checks if the "removeHouse" is 7
                for i in range(len(all_color)):
                    if players[turn].get_player_properties()[all_color[i]]['removeHouse'] == players[turn].get_player_properties()[spot]['removeHouse']:
                        equal_each.append(all_color[i])

                # If the length is 1 then it will add 'DEBUG' so it won't break
                if len(equal_each) == 1:
                    equal_each.append('DEBUG')

                # Checks to see if all the properties in equal_each is False
                if len(equal_each) == 3 or ('blue' in equal_each[0] and 'blue' in equal_each[1]) or ('brown' in equal_each[0] and 'brown' in equal_each[1]):
                    for i in range(len(equal_each)):
                        players[turn].get_player_properties()[equal_each[i]]['removeHouse'] = True

                # Checks if the player can remove a house
                if players[turn].get_player_properties()[spot]['removeHouse'] == True:
                    # This makes the buy house work correctly
                    players[turn].set_player_property_removeHouse(spot, False)
                    players[turn].set_player_property_nextHouse(spot, True)
                    # Removes 'DEBUG' so error doesn't occur
                    try:
                        equal_each.remove('DEBUG')
                    except:
                        equal_each
                    # Makes the "nextHouse" equal False
                    for i in range(len(equal_each)):
                        if equal_each[i] != spot or equal_each[i] == 'DEBUG':
                            players[turn].set_player_property_nextHouse(equal_each[i], False)
                    remove_house(spot)
                    # This will occur if the mafia is taking the house
                    if mafia == True:
                        return (propData[spot]['cost'])/2
        else:
            print('Property already mortgaged')
        
        update_cash_label(turn)
        prop_manage(spot, propData)
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Player Buys a House on the Property
def buy_house(spot, cost):
    try:
        all_color = []
        same_amount = []
        equal_each = []
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        # Makes all the same properties in the same list
        for key, value in players[turn].get_player_properties().items():
            if key[0:len(key)-1] in spot:
                all_color.append(key)
        # This checks if there this only 1 item in the all_color list
        if len(all_color) == 1:
            all_color.append('DEBUG')
        
        # Checks to see if all properties of the set 'nextHouse' is equal to False
        for i in range(len(all_color)):
            if all_color[i] != 'DEBUG':
                if players[turn].get_player_properties()[all_color[i]]['nextHouse'] == False:
                    equal_each.append(all_color[i])
        print(f'equal_each: {equal_each}')
        print(f'all_color: {all_color}')
        # If all houses in the eql_each equal False, Then sets them to True
        try:
            if len(equal_each) == 3 or ('blue' in equal_each[0] and 'blue' in equal_each[1]) or ('brown' in equal_each[0] and 'brown' in equal_each[1]):
                for i in range(len(equal_each)):
                    players[turn].set_player_property_nextHouse(equal_each[i], True)
        except:
            spot

        # Checks for all 3 property Colors
        try:
            # This un-mortgages the property
            if players[turn].get_player_properties()[spot]['mortgage'] == True:
                if players[turn].get_player_cash() >= cost:
                    players[turn].take_player_cash(cost)
                    players[turn].set_player_property_mortgage(spot, False)
                    update_cash_label(turn)
            elif len(all_color) == 3 or ('blue' in all_color[0] and 'blue' in all_color[1]) or ('brown' in all_color[0] and 'brown' in all_color[1]):
                # Better Housing update | Checks if the next house can be placed on that property
                if players[turn].get_player_properties()[spot]['nextHouse'] == False:
                    print('You need to place the same amount of house on each property\nBefore placing here')
                    prop_manage(spot, propData)
                    return

                # Checks for hotels
                if players[turn].get_player_properties()[spot]['house'] == 5:
                    print('You already have a Hotel Here')
                    return
                if players[turn].get_player_cash() >= cost:
                    add_house(spot)
                    players[turn].take_player_cash(cost)
                    players[turn].add_player_property_house(spot)
                    if players[turn].get_player_properties()[spot]['house'] == 5:
                        action_buttons['action1'].config(text='Hotel Already Owned', state=DISABLED)
                    else:
                        action_buttons['action1'].config(state=NORMAL)
                    update_cash_label(turn)
                else:
                    print('Not enough money')
                    return
            
            else:
                print('You can not buy a house on this property since you do not have the set')
        except ValueError:
            print('You can not buy a house on this property since you do not have the set')
        prop_manage(spot, propData)
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Player Pays another Player
def pay_player(fromP, toP = None, amount = 0, goJail = None, to_all = None):
    try:
        if toP != None:
            if players[fromP].get_player_cash() >= amount:
                players[fromP].take_player_cash(amount)
                players[toP].add_player_cash(amount)
                print(f'{fromP} gave ${amount} to {toP}')
                print(f'{fromP} cash: $'+str(players[fromP].get_player_cash()))
                print(f'{toP} cash: $'+str(players[toP].get_player_cash()))
                action_buttons['action1'].config(state=DISABLED, text='', command='')
                update_cash_label(toP)
                update_cash_label(turn)

                # This will just disable the "set arson" button
                if action_buttons['action2']['text'] == 'Set Fire (Arson)':
                    action_buttons['action2'].config(text='', state=DISABLED, command='')

                # Checks to see if the player is paying all players
                if to_all != None:
                    spot
                    return
                # Checks if the player is going to jail
                if goJail != None:
                    player_to_jail(turn)
                else:
                    action5_button_status()
            else:
                print(f'You do not have ${amount}')
            return
        else:            
            if to_all == 'all':
                for key, value in players.items():
                    if key != fromP:
                        pay_player(fromP, key, amount, None, 'all')
            elif to_all == 'from':
                for key, value in players.items():
                    if key != fromP:
                        print(key)
                        pay_player(key, turn, amount, None, 'all')
            action5_button_status()
            update_cash_label('all')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

#Pays the Bank | WIP
def pay_bank(amount):
    try:
        if players[turn].get_player_cash() >= amount:
            players[turn].take_player_cash(amount)
            update_cash_label(turn)
            action5_button_status()
        else:
            actLabel.config(text='You do not have enough Money')
            time.sleep(3)
            actLabel.config(text=f'You have to pay ${amount}')
            return
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# When the player lands on a spot that is taxed
# Update code to make it universal
def pay_tax(payment):
    try:
        global free_parking
        if players[turn].get_player_cash() >= int(payment):
            players[turn].take_player_cash(int(payment))
            free_parking += int(payment)
            update_cash_label(turn)
        else:
            actLabel.config(text='You do not have enough Money')
            game.after(3000, actLabel.config(text=f'You have to pay ${payment}'))
            return

        action_buttons['action1'].config(state=DISABLED, text='', command='')
        action5_button_status()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Gives the player all the money in free parking
def get_free_parking(propData):
    try:
        global free_parking
        players[turn].add_player_cash(free_parking)
        name = players[turn].get_player_name()
        actLabel.config(text=f'{name} has gained ${free_parking}')
        antiExploits.add_real_money(free_parking)
        free_parking = 200
        update_cash_label(turn)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# When the player passes go
def pass_go(on_go = False):
    # on_go: if the player is on go and needs to disable the buttom
    if on_go == True:
        action_buttons['action2'].config(state=DISABLED)
    # 
    actLabel.config(text=players[turn].get_player_name()+f' gained $200 for passing/landing on "Go"')
    players[turn].add_player_cash(200)
    update_cash_label(turn)
    action5_button_status()

# Payment Functions | End

# Plays the card the player got
def use_card(card, cardID):     
    try:
        with open('gameData/cards.json', 'r') as cd:
            cardData = json.load(cd)

        actLabel.config(text=cardID['details'])    
        # This checks if the "ooj" card has been taken or not
        if cardID['id'] == f'ooj_{card}':
            if f'ooj_{card}' in oojUsed:
                get_card(spot)

        # Checks to see if the card is disabled 
        if cardID['id'] in disabled_cards:
            get_card(spot)
            return  
        
        #If the card is a get out of jail
        if 'ooj' in cardID['id']:
            players[turn].add_player_ooj(cardID['id'])
            oojUsed.append(cardID['id'])
            action5_button_status()
        # If the player pays all players
        elif 'to_all' in cardID['id']:
            reset_action_buttons('disabled')
            action_buttons['action1'].config(text='Pay all payers $50', command=lambda: pay_player(turn, None, 50, None, 'all'), state=NORMAL)
        # Has the player pay all their houses and hotels
        elif 'Street_Repairs' in cardID['id'] :
            amount = 0
            for key, value in players[turn].get_player_properties().items():
                if players[turn].get_player_properties()[key]['house'] == 5:
                    amount += cardData[card][randomize_cards[card][0]]['pay'][1]
                elif players[turn].get_player_properties()[key]['house'] >= 1:
                    amount += cardData[card][randomize_cards[card][0]]['pay'][0]
            if amount == 0:
                end_turn_part()
            else:
                action_buttons['action1'].config(text=f'Pay ${amount}', command=lambda: pay_bank(amount), state=NORMAL)
        # Makes all players pay the player $50 
        # Gives the other players $50 instead of the one player
        elif 'from_all' in cardID['id'] :
                reset_action_buttons('disabled')
                pay_player(turn, None, 50, None, 'from')
        # Allows the player to advance to the given place
        elif "advance" in cardID['id']:
            for key, value in grid.items():
                if grid[key].get_spot_name() == cardData[card][randomize_cards[card][0]]['to']:
                    board.update()
                    board.after(2000, config_placement(key, turn))
                    players[turn].set_player_spot(key)
                    check_property(grid[key].get_spot_name())
                    break
        # Sends the player to jail
        elif "jail" in cardID['id']:
            board.update()
            action_buttons['action1'].after(2000, player_to_jail(turn))
        # Sets one of the players' house on fire (removes)
        elif "arson" in cardID['id']:
            props_house = []
            # This will randomize the players properties to commit arson on
            for key, value in players[turn].get_player_properties().items():
                # Adds the property to the "props_house" if it has a house and house can be removed
                if (players[turn].get_player_properties()[key]['house'] > 0) and (players[turn].get_player_properties()[key]['removeHouse'] == True) and (players[turn].get_player_properties()[key]['mortgage'] == False):
                    props_house.append(key)

            # Randomizes the prop
            if len(props_house) > 0:
                prop_gone = random.randint(0, len(props_house))
            action5_button_status()
        # This makes a player pay tax
        elif "pay_tax" in cardID['id']:
            # Current Error Key Error: 'pay
            action_buttons['action1'].config(command=lambda: pay_tax(cardData[card][randomize_cards[card][len(randomize_cards[card])-1]]['pay']), state=NORMAL, text=f'Pay $'+str(cardData[card][randomize_cards[card][0]]['pay']))
        # This occurs when the mafia comes to get your money
        elif "mafia_comes" in cardID['id']:
            payment = cardID['pay']
            action_buttons['action1'].config(state=NORMAL, text=f'Pay the mafia ${payment}', command=lambda: maifa_or_hospital('pay', payment))
            action_buttons['action2'].config(state=NORMAL, text=f'Don\'t pay the mafia', command=lambda: maifa_or_hospital('hospital', 0))

        # Puts the current card at the end of the list
        randomize_cards[card].append(randomize_cards[card][0])
        randomize_cards[card].remove(randomize_cards[card][0])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Chest / Chance Cards Functions
def get_card(spot):
    try:
        with open('gameData/cards.json', 'r') as cd:
            cardData = json.load(cd)

        # Gets the spot the player is at and gets a random card from that spot
        card = spot[0:len(spot)-1]

        # Gets a random card from their spot
        cardID = cardData[card][randomize_cards[card][0]]
        use_card(card, cardID)   
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# This puts the player in jail
def player_to_jail(player):
    try:
        # Checks to see if anyone else is in jail
        amount = 0
        for key, value in players.items():
            if players[key].get_player_jail() == True:
                amount += 1

        # Moves the player to the correct spot based on whos in jail
        # Base: x = 25, y = 435
        if amount == 0:
            board.moveto(player, 26, 436)
        elif amount == 1:
            board.moveto(player, 56, 436)
        elif amount == 2:
            board.moveto(player, 26, 466)
        elif amount == 3:
            board.moveto(player, 56, 466)

        # Sets the player to the "isJailed" State
        players[turn].set_player_jail(True)
        config_player_jailStatus('new_prison')
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# This allows for the player to go to jail, buy out of jail, or use a free Card
def config_player_jailStatus(act, opt = None):
    try:
        # Removes the configurations of action_buttons['action1'], 2, and 5
        reset_action_buttons()
        # Sets up the options for the player in Jail
        if act == 'start':
            actLabel.config(text='Pick an Option')
            # Allows the player to pay $50
            action_buttons['action2'].config(text='Pay $50', command=lambda: config_player_jailStatus('end', 'pay'), state=NORMAL)
            # Allows the player to roll doubles
            action_buttons['action5'].config(text='Roll Doubles', command=lambda: config_player_jailStatus('end', 'roll'), state=NORMAL)
            maifa_bank_button.config(state=DISABLED)
            # Allows the player to use a "Get out of Jail" Card
            if (len(players[turn].get_player_ooj())) > 0:
                action_buttons['action1'].config(text='Use a "Get out Of Jail" Free card', command=lambda: config_player_jailStatus('end', 'card'), state=NORMAL)
            else:
                action_buttons['action1'].config(text='No "Get out of Jail" Free card', state=DISABLED)
        # When the player picks an Option
        elif act == "end":
            # If the option is "Pay $50"
            if opt == 'pay':
                if players[turn].get_player_cash() >= 50:
                    players[turn].take_player_cash(50)
                    actLabel.config(text='Roll Dice to Move')
                    players[turn].set_player_jail(False)
                    action_buttons['action5'].config(text='Roll Dice', command=lambda: roll_dice(), state=NORMAL)
                else:
                    actLabel.config(text='Not Enough Money')
                    config_player_jailStatus('start', None)
                    return
            # If the option is "Roll Doubles"
            elif opt == 'roll':
                # RNG between 1-6
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                # Checks if the player rolled a double
                if dice1 == dice2:
                    actLabel.config(text='You Rolled a Double!\nRoll Dice to Move')
                    players[turn].set_player_jail(False)
                    action_buttons['action5'].config(text='Roll Dice', command=lambda: roll_dice(), state=NORMAL)
                else:
                    actLabel.config(text='You Did Not Roll a Double.')
                    action_buttons['action5'].config(text='End Turn', command=lambda: change_turn(), state=NORMAL);
                    return
            # If the option is "Use Get out of Jail Free Card"
            elif opt == 'card':
                actLabel.config(text='You Used a "Get out of Jail" Card.\nRoll Dice to Move')
                players[turn].set_player_jail(False)
                players[turn].remove_player_ooj()
                action_buttons['action5'].config(text='Roll Dice', command=lambda: roll_dice(), state=NORMAL)
            maifa_bank_button.config(state=NORMAL)
            update_cash_label(turn)
        # This occurs when the player is new in jail
        elif act == 'new_prison':
            action_buttons['action5'].config(text='End Turn')
            action5_button_status()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes sure that the player is in the correct place
def config_placement(moveTo, turn):
    global next_to_player
    next_to_player = False
    try:
        #Checks for other players at the spot
        x, y = 0, 0
        num = 0
        for key, value in players.items():
            if key != turn:
                if players[key].get_player_spot() == players[turn].get_player_spot():
                    num += 1
        # If the Player is on the Bottom
        if (moveTo >= 2) and (moveTo <=10):
            if num == 0:
                x, y = int(grid.get(moveTo, {}).get_spot_x()), int(grid.get(moveTo, {}).get_spot_y())+15
            elif num == 1:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+24, int(grid.get(moveTo, {}).get_spot_y())+15
            elif num == 2:
                x, y = int(grid.get(moveTo, {}).get_spot_x()), int(grid.get(moveTo, {}).get_spot_y())+35
            elif num == 3:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+24, int(grid.get(moveTo, {}).get_spot_y())+35
        # If the player is on the Left Side
        elif (moveTo >= 12) and (moveTo <= 20):
            #if moveTo == 
                if num == 0:
                    x, y = int(grid.get(moveTo, {}).get_spot_x())+44, int(grid.get(moveTo, {}).get_spot_y())
                elif num == 1:
                    x, y = int(grid.get(moveTo, {}).get_spot_x())+44, int(grid.get(moveTo, {}).get_spot_y())+20
                elif num == 2:
                    x, y = int(grid.get(moveTo, {}).get_spot_x())+19, int(grid.get(moveTo, {}).get_spot_y())
                elif num == 3:
                    x, y = int(grid.get(moveTo, {}).get_spot_x())+19, int(grid.get(moveTo, {}).get_spot_y())+20
        # If te player is on the top of the board
        elif (moveTo >= 22) and (moveTo <= 30):
            if num == 0:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+24, int(grid.get(moveTo, {}).get_spot_y())+44
            elif num == 1:
                x, y = int(grid.get(moveTo, {}).get_spot_x()), int(grid.get(moveTo, {}).get_spot_y())+44
            elif num == 2:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+24, int(grid.get(moveTo, {}).get_spot_y())+24
            elif num == 3:
                x, y = int(grid.get(moveTo, {}).get_spot_x()), int(grid.get(moveTo, {}).get_spot_y())+24
        # If the player is on the right side
        elif (moveTo >= 32) and (moveTo <= 40):
            if num == 0:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+15, int(grid.get(moveTo, {}).get_spot_y())+24
            elif num == 1:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+15, int(grid.get(moveTo, {}).get_spot_y())
            elif num == 2:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+39, int(grid.get(moveTo, {}).get_spot_y())+24
            elif num == 3:
                x, y = int(grid.get(moveTo, {}).get_spot_x())+39, int(grid.get(moveTo, {}).get_spot_y())
        # If the player lands on "go"
        elif (moveTo == 1):
            # Base: 435, 435
            if num == 0:
                x, y = 450, 450
            elif num == 1:
                x, y = 450, 480
            elif num == 2:
                x, y = 480, 450
            elif num == 3:
                x, y = 480, 480
        # If the player lands on "visiting_jail"
        elif moveTo == 11:
            # Base: 'x':0, 'y':435
            if num == 0:
                x, y = 3, 436
            elif num == 1:
                x, y = 3, 465
            elif num == 2:
                x, y = 3, 491
            elif num == 3:
                x, y = 33, 491
        # if the player lands on "free_parking"
        elif moveTo == 21:
            # Base: 435, 435
            if num == 0:
                x, y = 45, 45
            elif num == 1:
                x, y = 45, 15
            elif num == 2:
                x, y = 15, 45
            elif num == 3:
                x, y = 15, 15
        # if the player lands on "toJail"
        elif moveTo == 31:
            x, y = 450, 45
        
        # Moves the player
        board.moveto(turn, x, y)
        # This is to check if there is another player in the spot
        if num == 2:
            next_to_player = True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Property Management
def prop_manage(spot, propData):
    try:
        actLabel.config(text=f'Manage '+propData[spot]['name'])
        if ('railroad' in spot) or ('electrical' in spot) or ('water' in spot):
            payment = int(propData[spot]['cost'])
            if players[turn].get_player_properties()[spot]['mortgage'] == False:
                action_buttons['action1'].config(state=DISABLED, text='', command='')
                action_buttons['action2'].config(state=NORMAL, text=f'Mortgage for ${payment/2}')
            else:
                payment = int(((propData[spot]['cost']/2)*0.1)+propData[spot]['cost']/2)
                action_buttons['action1'].config(state=NORMAL, text=f'Un-Mortgage for ${payment}', command=lambda: buy_house(spot, payment))
                action_buttons['action2'].config(state=DISABLED, text='Property is Mortgage')
        else:
            payment = int(propData[spot]['price'])
            # Checks to see if the text needs to be house or hotel
            if players[turn].get_player_properties()[spot]['house'] > 0 or players[turn].get_player_properties()[spot]['house'] < 4:
                action_buttons['action1'].config(state=NORMAL, text=f'Buy a House for ${payment}', command=lambda: buy_house(spot, payment))
            elif players[turn].get_player_properties()[spot]['house'] == 4:
                action_buttons['action1'].config(state=NORMAL, text=f'Buy a Hotel for ${payment}', command=lambda: buy_house(spot, payment))
            elif players[turn].get_player_properties()[spot]['house'] == 5:
                action_buttons['action1'].config(state=DISABLED, text='You already have A Hotel')
            # If the property is mortgage this allows for un-mortgaging
            if players[turn].get_player_properties()[spot]['mortgage'] == True:
                payment = int(((propData[spot]['cost']/2)*0.1)+propData[spot]['cost']/2)
                action_buttons['action1'].config(state=NORMAL, text=f'Un-Mortgage for ${payment}', command=lambda: buy_house(spot, payment))
            
            # Checks if the property has been mortgage if not then it lets the player to sell their house/hotel
            if players[turn].get_player_properties()[spot]['mortgage'] != True:
                if players[turn].get_player_properties().get(spot, {}).get('house') > 0:
                    if players[turn].get_player_properties()[spot]['house'] < 5:
                        action_buttons['action2'].config(state=NORMAL, text=f'Sell a House for ${payment}')
                    elif players[turn].get_player_properties()[spot]['house'] == 5:
                        action_buttons['action2'].config(state=NORMAL, text=f'Sell a Hotel for ${payment}')
                # Checks to see if the property is able to be mortgage
                elif players[turn].get_player_properties().get(spot, {}).get('house') == 0:
                    action_buttons['action2'].config(state=NORMAL, text=f'Mortgage for ${payment/2}')
            else:
                action_buttons['action2'].config(text='Property is mortgage', state=DISABLED)
        # This Checks if the amount of total houses/hotels is 0 and Disables the button if it is
        if houses == 0:
            if players[turn].get_player_properties().get(spot, {}).get('house') > 4 or players[turn].get_player_properties().get(spot, {}).get('house') < 4:
                action_buttons['action1'].config(text='No Available Houses', state=DISABLED)
        else:
            if players[turn].get_player_properties().get(spot, {}).get('house') == 4:
                action5_button_status['action1'].config(text='No Available Motels', state=DISABLED)
        check_set_color = []
        # Adds the set to a list
        for key, value in players[turn].get_player_properties().items():
            if key[0:len(key)-1] in spot:
                check_set_color.append(key)
        if len(check_set_color) == 1: # Put in place to make sure there is no index Error
            check_set_color.append('DEBUG')
        # Disables the house button if they can not add houses
        #if players[turn].get_player_properties()[spot]['mortgage'] == False: # This is put in place to make sure they can un-Mortgage the property
                #if len(check_set_color) == 3 or ('blue' in check_set_color[0] and 'blue' in check_set_color[1]) or ('brown' in check_set_color[0] and 'brown' in check_set_color[1]):
                    #action_buttons['action1'].config(state=DISABLED, text='You need the\nSet to buy houses')

        # IF the player is in the edit_property tab this will occur so that it won't enabled the main buttons
        if edit_prop == True:
            reset_action_buttons('Disable')
        else:
            # Updates actions and text
            action_buttons['action2'].config(command=lambda: sell_prop(spot))
            update_cash_label(turn)
            end_turn_part()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Checks the Property to See if it is Bought
def check_property(spot):
    try:
        action_buttons['action5'].config(state=DISABLED)
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        # Checks to see if the property was bought
        for key, value in players.items():
            if (players[key].get_player_properties().get(spot, {}) != {}) and (players[key].get_player_properties().get(spot, {}).get('mortgage') == False):
                # Makes Sure that the key is not the current turn
                if key != turn:
                    # Checks if the property is Electrical Company or Water Works
                    if spot in ['electrical', 'water']:
                        # Checks to see if the player has both Electric Company or Water Works
                        if players[key].get_player_properties().get('electrical') != False and players[key].get_player_properties().get('water') != False:
                            payment = movement*10
                        else:
                            payment = movement*4
                    # Checks to see if the the owner has any other railroads
                    elif 'railroad' in spot:
                        payment = 25
                        for i in range(4):
                            if players[key].get_player_properties().get(f'railroad{i}') != False and players[key].get_player_properties().get(f'railroad{i}', {}).get('mortgage') == False:
                                if f'railroad{i}' == key:
                                    payment *= 2
                    else:
                        payment = propData[spot]['rent'][players[key].get_player_properties()[spot]['house']]
                        if game_mode == 'Advance':
                            action_buttons['action2'].config(text='Set Fire (Arson)', state=NORMAL, command=lambda: commit_arson('random', spot, key))
                    actLabel.config(text=f'You have to pay '+players[key].get_player_name()+f' ${payment}')
                    action_buttons['action1'].config(state=NORMAL, text=f'Pay rent for ${payment}', command=lambda: pay_player(turn, key, payment))
                    action_buttons['action6'].config(command=lambda: bankrupt_player('player', key))
                    return
                else:  
                    prop_manage(spot, propData)
                    action5_button_status()
                    return
            # If the property is mortgage then this will make is so the player does not have to pay
            elif players[key].get_player_properties().get(spot, {}).get('mortgage') == True:
                actLabel.config(text='This property is mortgage, No Need to pay')
                end_turn_part()
                return
        
        # This is for checking what property the player move to
        if ('chest' in spot) or ('chance' in spot):
            get_card(spot)
        elif 'inTax' in spot:
            actLabel.config(text='You have to pay $100')
            action_buttons['action1'].config(state=NORMAL, text='Pay $100', command=lambda: pay_tax(100))
            action_buttons['action6'].config(state=NORMAL, command=lambda: bankrupt_player('self', turn));action_buttons['action3'].config(state=NORMAL, text='Edit Properties')
        elif 'LTax' in spot:
            actLabel.config(text='You have to pay $200')
            action_buttons['action6'].config(state=NORMAL, command=lambda: bankrupt_player('self', turn));action_buttons['action3'].config(state=NORMAL, text='Edit Properties')
            action_buttons['action1'].config(state=NORMAL, text='Pay $200', command=lambda: pay_tax(200))
        elif 'hospital' in spot:
            actLabel.config(text='You have to pay $25 parking fees')
            action_buttons['action1'].config(state=NORMAL, text='Pay $25', command=lambda: pay_tax(25))
        elif 'jail' in spot:
            actLabel['text'] = 'Your fine because your just visiting!'
            action5_button_status()
        elif 'toJail' in spot:
            board.update()
            actLabel.config(text='You been caught for having bad luck. Go to Jail')
            board.after(2000, player_to_jail(turn))
            action_buttons['action5'].config(state=NORMAL, text='End Turn', command=lambda: change_turn())
        elif 'free' in spot:
            get_free_parking(propData)
            action_buttons['action5'].config(state=NORMAL)
            action5_button_status()
        # If the player lands on go they can either choose to go to the casino or just get $200
        elif 'go' in spot:
            #action_buttons["action1"].config(text='Go to Casino (Fee $50)', state=DISABLED, command=lambda: new_frame('casino'))
            action_buttons["action2"].config(state=DISABLED)
        else:
            actLabel.config(text=f'Do you want to Buy \n'+propData[spot]['name']+' for $'+str(propData[spot]['cost']))
            if players[turn].get_player_cash() < propData[spot]['cost']:
                action_buttons['action1'].config(state=DISABLED, text=f'Not Enough Money')
            else:
                action_buttons['action1'].config(state=NORMAL, text=f'Buy for $'+str(propData[spot]['cost']), command=lambda: buy_prop(spot, propData))
            action_buttons['action2'].config(state=NORMAL, text='Auction Property', command=lambda: new_frame('auction', spot))
        update_monopoly_data()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# When a player clicks a property it will execute this
def property_details(event):
    try:
        # This checks if the given click is a valid canvas item
        # If the click was a valid canvas item it continues, if not it stops the function
        try:
            prop = board.gettags('current')[0]
        except Exception as e:
            print(e)
            return
        prop = prop.lower()
        no_props_list = ['player', 'chance', 'inTax', 'chest', 'bp', 'free', 'go', 'jail', 'hospital']
        # Checks to see if the given prop was a valid property
        if (prop in no_props_list) == False:
            new_frame('propDetails')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Rolls The Dice to move the player
def roll_dice():
    try:
        global spotID; global moveTo; global spot; global rollD; global movement
        # Checks if the player is Jailed
        if players[turn].get_player_jail() == True:
            config_player_jailStatus('start', None)
            return

        # Rolls a number between 1 and 6 (twice)
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        rollLabel['text'] = f'You rolled a {dice1} and a {dice2}'
        movement = dice1+dice2
        
        spotID = players[turn].get_player_spot()
        moveTo = spotID + movement
        
        # This will not allow the player to click the "roll dice" again
        action_buttons['action5'].config(state=DISABLED) 

        # This shows the player moving spot to spot
        i = 0
        while i < movement: 
            i+=1
            # Checks if the player passes boardwalk | Resets the while statement
            if players[turn].get_player_spot() > len(grid)-1: 
                movement = (spotID+movement) - len(grid)
                i = 1
                spotID = 0

            # Sets the player spot and Moves the player
            players[turn].set_player_spot(spotID+i)
            board.after(250, config_placement(spotID+i, turn))
            board.update()
            # If the player passes go
            if players[turn].get_player_spot() == 1:
                pass_go(False)
                update_cash_label(turn)

        # The id of the spot the player is on
        spot = grid.get(players[turn].get_player_spot(), {}).get_spot_name()
        
        # This makes the buttons "action3" and "action4" DIsabled when rolling
        action_buttons['action3'].config(text='', state=DISABLED, command='')
        action_buttons['action4'].config(text='', state=DISABLED, command='')

        #Sets the action_buttons['action5'] button to "End Turn"
        if dice1 != dice2:
            rollD = 0
            action_buttons['action5'].config(state=DISABLED, text='End Turn')
        # Checks for doubles
        elif dice1 == dice2:
            rollD += 1
        
        check_property(spot) # Checks the property if the player has landed on a free or owned property
        
        # Checks to see if the player rolled 3 doubles
        if rollD == 3:
            rollD = 0
            print('Rolled 3 doubles')
            actLabel.config(text='You Rolled 3 Doubles. Time to Serve Your Sentence')
            player_to_jail(turn)
    # Error Handler
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes the Board and Players
def make_board(loading_data):
    try:
        global grid; global board; global actLabel; global players; global labels; global house_label; global hotel_label; global rollLabel
        global action_buttons; global jailSpace; global players_out; global shop_button
        global bottomP; global leftP; global topP; global rightP
        global bottomB; global leftB; global topB; global rightB; 
        global name_list; global color_list; global maifa_bank_button; global con_output; global monopoly_game_data
        global thereIsMafia; global thereIsShop
        board = Canvas(game, width=525, height=525);board.place(x=100, y=0)
        grid = {}
        players = {}
        players_out = []
        labels = {}
        action_buttons = {}
        num = 1
    
        board_color = 'light blue'

        # Makes the save game and return to menu button
        saveGame_button = Button(game, text='Save Game');saveGame_button.place(x=50, y=20, anchor=CENTER);saveGame_button.bind('<Button-1>', lambda e: save_game());
        return_menu = Button(game, text='Main Menu');return_menu.place(x=50, y=50, anchor=CENTER);return_menu.bind('<Button-1>', lambda e: end_monopoly())
        shop_button = Button(game, text='Open Shop', state=DISABLED);
        maifa_bank_button = Button(game, text='Get Loan', command=lambda: new_frame('mafia'));

        # Actions the player can do
        actLabel = Label(game, text='', font=('Helvetica 10'));actLabel.place(x=825, y=150, relx=0.0, rely=0.0, anchor=CENTER)
        rollLabel = Label(game, text='', font=('Helvetica 10'));rollLabel.place(x=825, y=300, relx=0.0, rely=0.0, anchor=CENTER)

        # Makes the action Buttons
        for y in range(3):
            for x in range(2):
                action_buttons[f'action{num}'] = Button(game, text='', state=DISABLED)
                action_buttons[f'action{num}'].place(x=750+((x)*150), y=205+((y)*30), relx=0.0, rely=0.0, anchor=CENTER)
                num += 1
        
        action_buttons['action5'].config(text='Roll Dice', state=NORMAL, command=lambda: roll_dice())
        action_buttons['action6'].config(text='Bankrupt')

        # Chance: #FF0080
        # Chest: #138CA2
        bottomP = ['light_Blue3', 'light_Blue2', 'chance1', 'light_Blue1', 'railroad1', 'inTax', 'brown2', 'chest1', 'brown1']
        bottomB = ['#C6F6FF', '#C6F6FF', '#FF0080', '#C6F6FF', '#000000', "grey", '#5C1F1F', '#138CA2', '#5C1F1F']

        leftP = ['orange3', 'orange2', 'chest2', 'orange1', 'railroad2', 'pink3', 'pink2', 'electrical', 'pink1']
        leftB = ['#FF7400', '#FF7400', '#138CA2', '#FF7400', '#000000', '#EC73FF', '#EC73FF', '#ffffff', '#EC73FF']

        topP = ['red1', 'chance2', 'red2', 'red3', 'railroad3', 'yellow1', 'yellow2', 'water', 'yellow3']
        topB = ['#FF0000', '#FF0080', '#FF0000', '#FF0000', '#000000', '#FFFF00', '#FFFF00', '#ffffff', '#FFFF00']

        rightP = ['green1', 'green2', 'chest3', 'green3', 'railroad4', 'chance3', 'blue1', 'LTax', 'blue2']
        rightB = ['#127305', '#127305', '#138CA2', '#127305', '#000000', '#FF0080', '#0000FF', "grey", '#0000FF']

        # This will enable the "advance" gamemode addons
        if game_mode == 'Advance':
            # Replaces the spot "inTax" to "hospital"
            thereIsMafia = True
            thereIsShop = True

        # Places the loan butto
        if thereIsMafia:
            maifa_bank_button.place(x=50, y=110, anchor=CENTER)
            bottomP[5] = "hospital";bottomB[5] = '#00F0FF'
        
        # Places the shop Button
        if thereIsShop:
            shop_button.place(x=50, y=80, anchor=CENTER);
            
        # Bottom Spots
        bottom = board.create_rectangle(435, 435, 510, 510, fill=board_color, tag='go')
        grid[bottom] = grid_spot(bottom, 'go', None ,435, 510)
        for i in range(0, 9):
            bottom = board.create_rectangle(395-((i)*40), 435, 475-((i+1)*40), 510, fill=board_color, tag=f'{bottomP[(len(bottomP)-1)-i]}')
            grid[bottom] = grid_spot(bottom, bottomP[(len(bottomP)-1)-i], bottomB[(len(bottomB)-1)-i], 395-((i)*40), 435)

        # Left Side
        left = board.create_rectangle(0, 435, 75, 510, fill=board_color, tag='visit_jail')
        grid[left] = grid_spot(left, 'visit_jail', None ,0, 435)
        for i in range(0, 9):
            left = board.create_rectangle(0, 395-((i)*40), 75, 475-((i+1)*40), fill=board_color, tag=f'{leftP[(len(leftP)-1)-i]}')
            grid[left] = grid_spot(left, leftP[(len(leftP)-1)-i], leftB[(len(leftB)-1)-i] ,0, 395-((i)*40))
    
        # Top Spots
        top = board.create_rectangle(0, 0, 75, 75, fill=board_color, tag='free')
        grid[top] = grid_spot(top, 'free', None,0, 0)
        for i in range(0, 9):
            top = board.create_rectangle((i)*40+75, 0, (i+1)*40+75, 75, fill=board_color, tag=f'{topP[i]}')
            grid[top] = grid_spot(top, topP[i], topB[i],(i)*40+75, 0)
            
        # Right Side
        right = board.create_rectangle(435, 0, 510, 75, fill=board_color, tag='toJail')
        grid[right] = grid_spot(right, 'toJail', None, 435, 0)
        for i in range(0, 9):
            right = board.create_rectangle(435, (i)*40+75, 510, (i+1)*40+75, fill=board_color, tag=f'{rightP[i]}')
            grid[right] = grid_spot(right, rightP[i], rightB[i], 435, (i)*40+75)

        # Makes the property Boarders
        # Future Note: This is made from right to left
        # Bottom Properties
        for i in range(len(bottomB)):
            board.create_rectangle(395-((i)*40), 435, 475-((i+1)*40), 450, fill=bottomB[(len(bottomB)-1)-i], tag=f'{bottomP[(len(bottomP)-1)-i]}')
            board.create_rectangle(405-((i)*40) ,428, 425-((i)*40), 433, fill='#333333', tag=f'bp_{bottomP[(len(bottomP)-1)-i]}')
        # Left Properties
        for i in range(len(leftB)):
            board.create_rectangle(60, 395-((i)*40), 75, 475-((i+1)*40), fill=leftB[(len(leftB)-1)-i], tag=f'{leftP[(len(leftP)-1)-i]}')
            board.create_rectangle(77, 405-((i)*40), 82, 425-((i)*40), fill='#333333', tag=f'bp_{leftP[(len(leftP)-1)-i]}')
        # Top Properties
        for i in range(len(topB)):
            board.create_rectangle((i)*40+75, 60, (i+1)*40+75, 75, fill=topB[i], tag=f'{topP[i]}')
            board.create_rectangle(405-((i)*40), 77, 425-((i)*40), 82, fill='#333333', tag=f'bp_{topP[(len(topP)-1)-i]}')
        # Right Properties
        for i in range(len(rightB)):
            board.create_rectangle(435, (i)*40+75, 450, (i+1)*40+75, fill=rightB[i], tag=f'{rightP[i]}')
            board.create_rectangle(428, 405-((i)*40), 433, 425-((i)*40), fill='#333333', tag=f'bp_{rightP[(len(rightP)-1)-i]}')

        # Removes all bp for properties that don't need them
        remove_bp = ['inTax', 'LTax', 'chance1', 'chance2', 'chance3', 'chest1', 'chest2', 'chest3', 'hospital']
        for i in range(len(remove_bp)):
            try:
                board.delete('bp_'+remove_bp[i])
            except:
                continue

        # Makes the Jail space
        jailSpace = board.create_rectangle(25, 435, 75, 485, fill='orange', tag='in_jail')

        # House/Hotel Labels
        house_label = Label(game, text=f'Houses Left: {houses}', font=('Helvetica 10'));house_label.place(x=800, y=25)
        hotel_label = Label(game, text=f'Hotels Left: {hotels}', font=('Helvetica 10'));hotel_label.place(x=800, y=50)

        # This allows players to look at the property Details
        board.bind('<Button-1>', lambda e: property_details('place'))

        # Makes the name_list and color_list
        if loading_data != None:
            name_list = []
            color_list = []
            for key, value in monopoly_game_data.get_save_players().items():
                name_list.append(monopoly_game_data.get_save_players()[key]['name'])
                color_list.append(monopoly_game_data.get_save_players()[key]['color'])
    
        # Makes the Player Dictionary
        for i in range(len(name_list)):
            # Player Pieces
            board.create_rectangle(450, 450+(i*25), 465, 465+(i*25), fill=color_list[i], tag=f'player{i+1}')
            players[f'player{i+1}'] = Players(name_list[i], color_list[i], 1, 2000, 0, False, {}, {}, [], False, 0, 0)
            #players[f'player{i+1}'] = {"spot": 1, "name":name_list[i], "color":color_list[i],"prop": {}, "cash": 2000, "getOut": [], "inventory": {}, "skipTurn": 0, "loans": {"hasLoan": False, "loanAmount": 0, "payIn": 0} , "isJailed": False}
            config_placement(1, f'player{i+1}')
            #Cash Labels
            labels[f'player{i+1}'] = Label(game, text=players[f'player{i+1}'].get_player_name()+' has: $'+str(players[f'player{i+1}'].get_player_cash()))
            labels[f'player{i+1}'].place(x=625, y=25*(i+1))
        
        # This makes a on screen output
        con_output = Text(game, width=35, height=28);con_output.place(x=1000, y=30)
        #con_output = Text(game, width=55, height=10);con_output.place(x=850, y=0, relx=0, rely=0.7, anchor=CENTER)
        # This allows for commands
        command_input = Entry(game, width=35);command_input.place(x=1000, y=500)
        command_submit = Button(game, text='Submit', state=NORMAL, command=lambda: console(command_input.get()));command_submit.place(x=1250, y=510, anchor=CENTER)

        # Checks for loading saved game data
        # Checks to see if the players loaded their data
        if loading_data != None:
            print('Loading Save')
            # Player Names
            plyers = list(monopoly_game_data.get_save_players().keys())
            for i in range(len(plyers)):
                players[f'player{i+1}'] = Players(
                    monopoly_game_data.get_save_players()[f'player{i+1}']['name'], 
                    monopoly_game_data.get_save_players()[f'player{i+1}']['color'], 
                    monopoly_game_data.get_save_players()[f'player{i+1}']['spot'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['cash'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['skipTurn'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['jailStatus'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['prop'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['inventory'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['ooj'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['loans']['hasLoan'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['loans']['loanAmount'],
                    monopoly_game_data.get_save_players()[f'player{i+1}']['loans']['payIn']
                )

            update_cash_label(turn)
            for key, value in monopoly_game_data.get_save_players().items():
                config_placement(monopoly_game_data.get_save_players()[key]['spot'], key)
                update_cash_label(key)

            # Makes sure that it shows that they own the property
            playing_players = list(monopoly_game_data.get_save_players().keys())
            for i in range(len(playing_players)):
                for key, value in monopoly_game_data.get_save_players()[playing_players[i]]['prop'].items():
                    board.itemconfig(f'bp_{key}', fill=monopoly_game_data.get_save_players()[playing_players[i]]['color'])
        else:
            saveid = ''
            for i in range(6):
                num = random.randint(0, 9)
                saveid = saveid + str(num)
            monopoly_game_data = save_monopoly_V2(saveid, game_mode, turn, game_version, players, randomize_cards, oojUsed, [houses, hotels])
            change_turn()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes the Window for player customization
def start_game(gameName, gamemode = None, data = None, version = None):
    global game; global debug; global turn; global free_parking; global houses; global hotels
    global rollD; global oojUsed; global randomize_cards; global game_mode
    global monopoly_game_data; global edit_prop; global debug_mode
    global disabled_cards; global disabled_items
    global thereIsShop; global thereIsMafia
    debug = True

    # This checks if it was given a gamemode
    if gamemode == None:
        gamemode = monopoly_game_data.get_save_game_mode()

    game = tk.Toplevel()
    game.geometry('1300x525')
    game.title(f'{gameName} ({gamemode})')
    game.resizable(False, False)
    game_mode = gamemode

    # Needed Items
    turn = 'player99'
    free_parking = 200
    houses = 32
    hotels = 12
    edit_prop = False
    names = []
    colors = []
    oojUsed = []
    randomize_cards = {"chance": [], "chest": []}
    rollD = 0
    given_data = None
    debug_mode = False

    with open('gameData/cards.json', 'r') as cd:
        cardData = json.load(cd)

    with open('gameData/shopItems.json', 'r') as idb:
        items = json.load(idb)

    # Randomizes the chance cards
    chanceCards_raw = cardData['chance']
    chanceCards = []
    for key, value in chanceCards_raw.items():
        if (chanceCards_raw[key]['id'] != "") and (chanceCards_raw[key]['gamemode'] in [game_mode, 'Normal']) and (chanceCards_raw[key]['id'] not in disabled_cards):
            chanceCards.append(key)
    random.shuffle(chanceCards)
    randomize_cards['chance'] = chanceCards

    # Randomizes the chest cards
    chestCards_raw = cardData['chest']
    chestCards = []
    for key, value in chestCards_raw.items():
        if (chestCards_raw[key]['id'] != "") and (chestCards_raw[key]['gamemode'] in [game_mode, 'Normal']) and (chestCards_raw[key]['id'] not in disabled_cards):
            chestCards.append(key)
    random.shuffle(chestCards)
    randomize_cards['chest'] = chestCards

    # This will enable all the cards that the user selects
    if gamemode == 'Custom':
        from games.monopoly_addons.custom_game import check_buttons_cards, moreBx, check_buttons_items, check_buttons_others
        moreBx.destroy()
        # Disables all chest cards (Advance only)
        for i in range(len(randomize_cards['chest'])):
            disabled_cards.append(cardData['chest'][str(i+1)]['id'])
        
        # Disables all chance cards (Advance only)
        for i in range(len(randomize_cards['chance'])):
            disabled_cards.append(cardData['chance'][str(i+1)]['id'])
        
        # This will remove all selected items from the custom gamemode CHEST
        for key, value in cardData['chest'].items():
            # Checks if it was selected
            if cardData['chest'][key]['id'] != '':
                if (check_buttons_cards[cardData['chest'][key]['id']+' (Chest)']['var'].get() != '') and (check_buttons_cards[cardData['chest'][key]['id']+' (Chest)']['var'].get() == cardData['chest'][key]['id']):
                    disabled_cards.remove(key)

        # This will remove all selected items from the custom gamemode CHANCE
        for key, value in cardData['chance'].items():
            # Checks if it was selected
            if cardData['chance'][key]['id'] != '':
                if (check_buttons_cards[cardData['chance'][key]['id']+' (Chance)']['var'].get() != '') and (check_buttons_cards[cardData['chance'][key]['id']+' (Chance)']['var'].get() == cardData['chance'][key]['id']):
                    disabled_cards.remove(key)

        # Disables all Player items
        for key, value in check_buttons_items.items():
            disabled_items['Player Shop'].append(check_buttons_items[key]['var'].get())

        # Enables selected Player items
        for key, value in check_buttons_items.items():
            # This checks if the item was selected
            if check_buttons_items[key]['var'].get() != '':
                disabled_items['Player Shop'].remove(check_buttons_items[key]['var'].get())
        
        # Enables Selected Other Items
        for key, value in check_buttons_others.items():
            # This checks if the item was selected
            print(check_buttons_others[key]['var'].get())
            if check_buttons_others[key]['var'].get() == 'Mafia':
                thereIsMafia = True
            elif check_buttons_others[key]['var'].get() == 'Player Shop':
                print('Player Shop Enabled')
                thereIsShop = True
    
    # Checks if the user loaded a saved game | If they did it will set the data to the saved data
    if data == 'dev':
        global name_list; global color_list; global game_version
        game_version = version
        name_list = ['Dallas', 'test']
        color_list = ['red', 'blue']
        gameMode_win.destroy()
    # This gets the save from the player
    elif data != None:
        destroy_root()
        given_data = True
        turn = monopoly_game_data.get_save_turn()
        randomize_cards = monopoly_game_data.get_save_cards()
        houses = monopoly_game_data.get_save_houses()[0]
        hotels = monopoly_game_data.get_save_houses()[1]
    
    make_board(given_data)
    
    game.mainloop()

# Checks the Inputs before Starting
def check_players(moreBx, gameName, gamemode):
    # Checks each input if its empty
    global name_list; global color_list
    name_list_raw = []
    color_list_raw = []
    name_list = []
    color_list = []
    lower_case_letters = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    index = 1
    # Gets the values for all Player Names
    for name in player_name:
        # Makes the first letter of the name uppercase
        first_let = name.get()[0:1]
        add_name = name.get()
        if first_let in lower_case_letters:
            add_name = f'{name.get()}'.title()

        # appends the name to the unorganized list
        name_list_raw.append(add_name)
    
    # Gets the values for all Player Names
    for color in player_color:
        color_list_raw.append(color.get())

    # Checks for repeated Names
    for name in name_list_raw:
        if (name not in name_list) and (name != ""):
            name_list.append(name)
        else:
            try:
                index = name_list_raw.index(name,index+1, len(name_list_raw))
            except:
                index +=1
            name_list.append(f'{name}_{index}')
    
    # Checks for repeated Colors
    for color in color_list_raw:
        if (color not in color_list) and (color != ""):
            if check_color(color) == True:
                color_list.append(color)
            else:
                print('Not a valid Color')
                error_label = Label(moreBx, text=f'"{color}" is not a valid Color.');error_label.place(x=0, y=-40, relx=0.5, rely=0.9, anchor=CENTER)
                return
        else:
            print('Repeated color')
            error_label = Label(moreBx, text='You can not have 2 of the same color.');error_label.place(x=0, y=-40, relx=0.5, rely=0.9, anchor=CENTER)
            return

    moreBx.destroy()
    start_game(gameName, gamemode)

# Add players to the game
def add_player_tag(moreBx):
    remove_player_button.bind('<Button-1>', lambda e: remove_player_tag(moreBx));remove_player_button.config(state=NORMAL, text='Remove Player')
    player_name.append(Entry(moreBx))
    player_name[len(player_name)-1].place(x=65, y=35+((len(player_name)-1)*40), relx=0.1, rely=0.1, anchor=CENTER)
    player_color.append(Entry(moreBx))
    player_color[len(player_name)-1].place(x=220, y=35+((len(player_name)-1)*40), relx=0.2, rely=0.1, anchor=CENTER)
    add_player_button.place(y=75+((len(player_name)-1)*40))
    remove_player_button.place(y=75+((len(player_name)-1)*40))
    # Disables the add_player_button if the player amount is 4
    if len(player_name) == 4:
        add_player_button.unbind('<Button-1>');add_player_button.config(state=DISABLED, text='You can not have\nmore than 4 players')
        return

# Removes players from the game
def remove_player_tag(moreBx):
    add_player_button.bind('<Button-1>', lambda e: add_player_tag(moreBx));add_player_button.config(state=NORMAL, text='Add Player')
    # Destroys and deletes the player
    player_name[len(player_name)-1].destroy()
    player_color[len(player_color)-1].destroy()
    del player_name[len(player_name)-1]
    del player_color[len(player_color)-1]

    # Moves the Add and Remove Buttons
    add_player_button.place(y=75+((len(player_name)-1)*40))
    remove_player_button.place(y=75+((len(player_name)-1)*40))

    if len(player_name) == 2:
        remove_player_button.unbind('<Button-1>');remove_player_button.config(state=DISABLED, text='You must have\nat least 2 players')
        return

#This will allow the player to go back to the main menu
def back_menu(level, back = None, gameName = None, version = None):
    level.destroy()
    if back == None:
        make_menu() 
    else:
        start(gameName, version)

# Starts the gmae
def start_players(gameName, gamemode):
    global add_player_button; global remove_player_button; global player_name; global player_color

    # This will just destroy the custom gamemode window if the gamemode is custom
    if gamemode == 'custom':
        from games.monopoly_addons.custom_game import moreBx
        moreBx.destroy()

    moreBx = tk.Toplevel()
    moreBx.title('Player Customization')
    moreBx.resizable(False, False)
    moreBx.geometry("400x500")
    moreBx.geometry("+5+5")
    player_name = []
    player_color = []
    name_label = Label(moreBx, text='Name', font=('Helvetica 10 underline'));name_label.place(x=65, y=25, relx=0.1, rely=0.0, anchor=CENTER)
    color_label = Label(moreBx, text='Color \n(Basic Color Name \nor Hex Code)', font=('Helvetica 10 underline'));color_label.place(x=220, y=25, relx=0.2, rely=0.0, anchor=CENTER)

    #Destroys the gamemode window
    gameMode_win.destroy()

    # Adds Entries for player_name and player_color
    for i in range(2):
        player_name.append(Entry(moreBx))
        player_name[i].place(x=65, y=35+(i*40), relx=0.1, rely=0.1, anchor=CENTER)
        player_color.append(Entry(moreBx))
        player_color[i].place(x=220, y=35+(i*40), relx=0.2, rely=0.1, anchor=CENTER)
    
    add_player_button = Button(moreBx, text='Add Player');add_player_button.place(x=65, y=110, relx=0.1, rely=0.1, anchor=CENTER)
    add_player_button.bind('<Button-1>', lambda e: add_player_tag(moreBx))
    remove_player_button = Button(moreBx, text='Remove Player');remove_player_button.place(x=220, y=120, relx=0.2, rely=0.1, anchor=CENTER)
    remove_player_button.config(state=DISABLED, text='You must have\nat least 2 players')

    # Final Parts
    try:
        import dev_file
        dev_button = Button(moreBx, text='Start Dev Mode', command=lambda: start_game(f'Monopoly {game_version}', gamemode, 'dev', game_version));dev_button.place(x=0, y=0, relx=0.5, rely=0.9, anchor=CENTER)
    except:
        # Just a place holder
        player_name

    confirm_button = Button(moreBx, text='Play Monopoly');confirm_button.place(x=0, y=0, relx=0.5, rely=0.8, anchor=CENTER)
    confirm_button.bind('<Button-1>', lambda e: check_players(moreBx, gameName, gamemode))

    # This makes the button to either go back to the gamemode selection or main menu
    back_to_main = Button(moreBx, text='Go Back to Main Menu', command=lambda: back_menu(moreBx));back_to_main.place(x=-15, y=0, relx=0.3, rely=0.9, anchor=CENTER)
    back_to_mode = Button(moreBx, text='Go Back to Gamemodes', command=lambda: back_menu(moreBx, 'mode', gameName, game_version));back_to_mode.place(x=15, y=0, relx=0.7, rely=0.9, anchor=CENTER)
    moreBx.mainloop()

# Loads a saved game from code
def loadGame(version):
    save_key = input('Please Enter your Save key (you can paste):\n')
    load_save(save_key, version)

# Starts the gamemode selection
def start(gameName, version):
    global gameMode_win; global game_version; global disabled_items; global disabled_shop; global disabled_cards
    global thereIsMafia; global thereIsShop
    game_version = version
    gameMode_win = tk.Toplevel()
    gameMode_win.title('Select a Gamemode')
    gameMode_win.resizable(False, False)
    gameMode_win.geometry("400x500")

    # Disables Items
    disabled_cards = []
    disabled_items = {"Player Shop": []}
    disabled_shop = []

    thereIsMafia = False
    thereIsShop = False
    
    normal_Button = Button(gameMode_win, text='Normal Monopoly');normal_Button.place(x=0, y=20, relx=0.2, rely=0.0, anchor=CENTER);normal_Button.bind('<Button-1>', lambda e:start_players(gameName, NORMAL))
    advance_Button = Button(gameMode_win, text='Advance Monopoly');advance_Button.place(x=0, y=20, relx=0.8, rely=0.0, anchor=CENTER);advance_Button.bind('<Button-1>', lambda e: start_players(gameName, 'Advance'))
    custom_Button = Button(gameMode_win, text='Custom Monopoly');custom_Button.place(x=0, y=80, relx=0.2, rely=0.0, anchor=CENTER);custom_Button.bind('<Button-1>', lambda e: start_custom())
    
    # Save Data Button 
    loadData_m = Button(gameMode_win, text='Load Monopoly Save');loadData_m.place(x=0, y=80, relx=0.8, rely=0.0, anchor=CENTER);loadData_m.bind('<Button-1>', lambda e :loadGame(version))
    back_to_menu = Button(gameMode_win, text='Go Back', command=lambda: back_menu(gameMode_win));back_to_menu.place(x=0, y=0, relx=0.5, rely=0.9, anchor=CENTER)
    destroy_root()

    # Nothing can below .mainloop() or it will not be runned
    gameMode_win.mainloop()
    