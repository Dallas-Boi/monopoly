# Made 1-12-23 Thursday
# This will only really be for debugging purposes

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import json


# Makes console functional
def console(con_input):
    from games.monopoly import players, con_output, turn, board, grid, monopoly_game_data, config_placement, check_property, update_cash_label, player_to_jail, use_card
    from games import monopoly
    # This seperates each word into a list
    input_list = con_input.split(" ")
    returned_text = ''
    # This checks if the input has an entry
    if con_input != '':
        # These are the built in command for the console
        if '/' in input_list[0]:
            try:
                # Commands will only work if debug_mode is True
                if monopoly.debug_mode == True:
                    # This adds money to the given player
                    if 'add' in input_list[0]:
                        players[input_list[1]]['cash'] += int(input_list[2])
                        update_cash_label(input_list[1])
                        returned_text = f'{input_list[1]} was given {input_list[2]}'
                    # Moves the player to the given spot
                    elif 'move' in input_list[0]:
                         for key, value in grid.items():
                            if grid[key]['place'] == input_list[1]:
                                coords = board.coords(turn)
                                spotID = board.find_overlapping(coords[0], coords[1], coords[2], coords[3])[0]
                                players[turn].set_player_spot(key)
                                config_placement(key, turn)
                                check_property(input_list[1])
                                returned_text = f'{turn} was moved to {input_list[1]}'
                    # Buys a given property
                    elif 'buy' in input_list[0]:
                        from games.monopoly import buy_prop
                        with open('gameData/propertyDetails.json', 'r') as pd:
                            propData = json.load(pd)
                        buy_prop(input_list[1], propData)
                    # Jails the given player
                    elif 'jail' in input_list[0]:
                        player_to_jail(turn)
                        returned_text = f'{input_list[1]} has been Jailed'
                    # This will allow the testing of cards
                    elif 'card' in input_list[0]:
                        use_card(input_list[1], input_list[2])
                    # This is to see the that is being stored
                    elif 'print' in input_list[0]:
                        # This prints the save data
                        if 'save' in input_list[1]:
                            returned_text = monopoly_game_data
                        # This prints the given player
                        elif 'player' in input_list[1]:
                            print_player(input_list[1])
                    # This occurs when the user does not use a valid command
                    else:
                        returned_text = f'"{con_input}" is not a valid command'
                 # This will turn on/off the debug mode
                elif 'debug' in input_list[0]:
                    if monopoly.debug_mode == False:
                        monopoly.debug_mode = True
                        returned_text = 'Debug Mode has been turned on'
                    else:
                        monopoly.debug_mode = False
                        returned_text = 'Debug Mode has been turned Off'
                con_output.delete(1.0, END)
            except Exception as e:
                returned_text = f'The command was entered wrong: {e}'

    # The if statement checks to see if "returned_text" has something so it isn't all seperated
    if returned_text != '':
        # This adds the output of the command to the console
        con_output['state'] = NORMAL
        con_output.insert('end', f'{returned_text}\n')
        con_output['state'] = DISABLED

# This will print the player into the console
def print_player(user):
    from games.monopoly import players, con_output, grid

    returned_text = f'Name: '+players[user].get_player_name()
    returned_text += f'\nColor: '+players[user].get_player_color()
    returned_text += f'\nCash: '+str(players[user].get_player_cash())
    returned_text += f'\nSpotID: '+str(players[user].get_player_spot())
    returned_text += f'\nSpot: "'+str(grid[players[user].get_player_spot()]['place'])+'"'
    returned_text += f'\nJailed: '+str(players[user].get_player_jail())
    returned_text += f'\nInventory: '+str(players[user].get_player_inventory())
    returned_text += f'\nProperties: '+str(players[user].get_player_properties())
    returned_text += f'\nhasLoan: '+str(players[user].get_player_hasLoan())
    returned_text += f'\nloanAmount: '+str(players[user].get_player_loanAmount())
    returned_text += f'\nLoan PayIn: '+str(players[user].get_player_loan_payIn())

    # This adds the output of the command to the console
    con_output['state'] = NORMAL
    con_output.insert('end', f'{returned_text}\n')
    con_output['state'] = DISABLED
