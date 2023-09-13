import tkinter as tk
from tkinter import *
import json
import time
import sys
import random
import os
from errorHandler import send_monopoly_error

# This is only for the array of players with loans
loan_array = {}

# Commits arson on the current turn
def commit_arson(action = None, spot = None, player = None):
    from games.monopoly import action_buttons, remove_house, end_turn_part, actLabel, players, pay_player, turn, board, player_to_jail, action5_button_status
    try:
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        # If a player commits arson on someones property
        if action == 'random':
            chance_to_commit = random.randint(1, 25)
            action_buttons['action1'].unbind('<Button-1>');action_buttons['action1'].config(text='', state=DISABLED)
            action_buttons['action2'].unbind('<Button-1>');action_buttons['action2'].config(text='', state=DISABLED)
            # IF the chance was 1; It will commit arson
            if chance_to_commit == 1:
                remove_house(spot)
                actLabel.config(text=f'You set fire to {player}\'s Property...\n You do not have to pay rent!')
                end_turn_part()
            # If the chance was above 1 then it will make the player pay double and make them go to jail
            elif chance_to_commit > 1:
                actLabel.config(text=f'You failed to commit arson... After Paying $'+str(propData[spot]['rent'][players[player].get_player_properties()[spot]['house']]*2)+' you will be\nSent to jail.')
                action_buttons['action1'].config(text=f'Pay rent for $'+str(propData[spot]['rent'][players[player].get_player_properties()[spot]['house']]*2), command=lambda: pay_player(turn, player, propData[spot]['rent'][players[player].get_player_properties()[spot]['house']]*2, True), state=NORMAL)
        # If a player gets a card that sets fire to their property
        else:
            prop_list = list(players[turn].get_player_properties().keys())
            if len(prop_list) >= 1:
                randomProp = (random.randint(0, len(prop_list)-1)); randomProp -= 1
                if players[turn].get_player_properties()[prop_list[randomProp]]['house'] >= 1:
                    remove_house(prop_list[randomProp])
                else:
                    del players[turn].get_player_properties()[prop_list[randomProp]]
                    board.itemconfig(f'bp_'+str(prop_list[randomProp]), fill='#333333')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Allows for players to press charges if someone hurts them
def player_press_charges(press_player, jail_player, act):
    from games.monopoly import action_buttons, actLabel, players, board, player_to_jail, action5_button_status
    try:
        # Need to make the buttons disable, unbind, and remove the text
        if act == True:
            actLabel.config(text=f'It looks like '+players[press_player].get_player_name()+' has pressed charges on '+players[jail_player]['name'])
            board.after(3000, lambda e: player_to_jail(jail_player))
            return
        else:
            actLabel.config(text=f'It appears that '+players[jail_player].get_player_name()+' is lucky\nsince '+players[press_player]['name']+' did not press charges')
            board.after(5000, actLabel.config(text=before_act))
        action_buttons['action1'].config(text='', state=DISABLED)
        action_buttons['action2'].config(text='', state=DISABLED)
        action_buttons['action1'].after(3000, lambda: action5_button_status())
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Breaks the other players knees
def break_their_knees(player, item):
    global before_act
    from games.monopoly import action_buttons, actLabel, players, turn, config_placement
    try:
        commit_chance = -1
        if item == "Bat":
            commit_chance = random.randint(1, 1)
        elif item == 'Sledge Hammer':
            commit_chance = random.randint(1, 10)
        print(f'commit: {commit_chance} | item: {item}')
        # Makes the action5 and action6 buttons unusable
        action_buttons['action5']; action_buttons['action5']['state'] = DISABLED
        action_buttons['action6']['state'] = DISABLED
        action_buttons['action1']['state'] = NORMAL
        # If the commit chance equals 1 then it commits to breaking their knee
        before_act = actLabel['text']
        player_name = players[player].get_player_name()
        turn_name = players[turn].get_player_name()
        if commit_chance == 1:
            players[player].add_player_skipTurn(1)
            actLabel.config(text=f'Your Broke {player_name}\'s Knees.\nNow they have to skip a turn and pay hospital bills')

            # This moves the player with the broken knees to the hospital
            for key, value in players.items():
                if players[key].get_player_name() == player_name:
                    config_placement(4, key)
                    break
            
            actLabel.after(5000, actLabel.config(text=before_act))
        # If they don't succeed then it will allow the other player to place charges or not
        else:
            actLabel.config(text=f'{player_name} caught {turn_name} lacking.\n{player_name} decided to pin {turn_name} to the ground')
            actLabel.after(2000, actLabel.config(text=f'Does {player_name} want to \nPress charges or Let them go'))
            action_buttons['action1'].config(text='Press Charges', command=lambda: player_press_charges(player, turn, True))
            action_buttons['action2'].config(text='Forget about it', command=lambda: player_press_charges(player, turn, False))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# This pays the mafia or they put you in the hospital
def maifa_or_hospital(action, payment = 0):
    from games.monopoly import action_buttons, actLabel, players, turn, grid, config_placement, action5_button_status
    # If the action is payment then allows the player to continue
    if action == 'pay':
        if players[turn].get_player_cash() >= payment:
            action_buttons['action1'].config(text='', state=DISABLED, command='')
            action_buttons['action2'].config(text='', state=DISABLED, command='')
            actLabel.config(text='You decided to pay the Mafia/nThey will leave you alone now')
            action5_button_status()
        else:
            print('not enought money')
    # If the action is hospital then this puts the player in the hospital and makes them skip 2 turns
    elif action == 'hospital':
        action_buttons['action5'].config(text='End Turn')
        action5_button_status()
        actLabel.config(text=f'It appears that the mafia was not happy with you.\nYou\'re in the Hospital for the next 2 turns')
        config_placement(4, turn)
        players[turn].set_player_skipTurn(2)

# Updates the get loan button
def change_loan_button(moreBx):
    from games.monopoly import players, turn
    amount = selected_loan.get()[1:len(selected_loan.get())]
    inTurns = 0
    # Updates the output label
    if int(amount) >= 1000:
        output_label.config(text=f'THATS a big loan... Make sure you pay it back!')
        inTurns = 7
    else:
        output_label.config(text=f'Alright.... Just make sure to pay me back!')
        inTurns = 2
    # Updates the get loan Button
    get_loan.config(text=f'Get a {selected_loan.get()} loan', state=NORMAL, command=lambda: player_add_loan(amount, inTurns, moreBx))

# Adds the loan to the player
def player_add_loan(amount, turns, moreBx):
    # Imports from other files
    from games.monopoly import players, turn, antiExploits
    from games.monopoly import update_cash_label
    from games.monopoly_addons.new_tab import destroy_moreBx
    from games.monopoly_addons.core import check_for_exploit
    # Updates the players database
    players[turn].set_player_hasLoan(True)
    players[turn].set_player_loanAmount(int(amount))
    players[turn].set_player_loan_payIn(turns)
    players[turn].add_player_cash(int(amount))
    update_cash_label(turn)
    # Updates the before money in the anti Cheat (This is so that the anti cheat does do a false positive)
    antiExploits.add_real_money(int(amount))
    # Updates the output label and closes the menu
    output_label.config(text=f'Alright you have {turns-1} turns to pay this back')
    get_loan.config(state=DISABLED)
    # This updates the mafia_property class

    # This closes the tab
    moreBx.after(3000, lambda: destroy_moreBx())

# Makes the loan menu for the mafia
def maifa_bank_menu(moreBx):
    from games.monopoly import players, turn
    from games.monopoly_addons.new_tab import destroy_moreBx
    global get_loan; global selected_loan; global output_label;
    moreBx.geometry('500x300')
    moreBx.title('Mafia Loans')
    # The Back Button
    done_loan = Button(moreBx, text='Go Back', command=lambda: destroy_moreBx());done_loan.place(x=0, y=20, relx=0.5, rely=0.0, anchor=CENTER);

    # The output labels
    output_label = Label(moreBx, text=f'Here to get some loans? You have to pay them back of course\nIf you don\'t pay them back, then it\'s not gonna be pretty.');
    output_label.place(x=0, y=50, relx=0.5, rely=0.0, anchor=CENTER)

    # The drop down menu for loans
    if players[turn].get_player_hasLoan() == False:
        # Makes the loan dropdown menu
        all_loans = ['$1500', '$1000', '$500', '$250']
        selected_loan = StringVar() 
        selected_loan.set('')
        selected_loan.trace("w", lambda name, index, mode, sv=selected_loan: change_loan_button(moreBx))
        ownedList = OptionMenu(moreBx, selected_loan, *all_loans);ownedList.place(x=0, y=90, relx=0.5, rely=0.0, anchor=CENTER)
        # Makes the get loan button
        get_loan = Button(moreBx, text='');get_loan.place(x=0, y=130, relx=0.5, rely=0.0, anchor=CENTER)

# This class allows for the mafia to take back their money if the player does not have enough money then they take their property

# This will occur if the player fails to pay their loan back
def failed_to_pay(cur_props, turn):
    from games.monopoly import players, sell_prop, update_cash_label
    try:
        # Opens the propData
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)    
        
        # This is the amount the player owns
        amount = int(players[turn].get_player_loanAmount())+100

        # Turns the propData keys into an array
        propList_raw = list(propData.keys())
        propList_raw.reverse()
        propList = {}

        # This makes the properties into an nested array
        for i in range(len(propList_raw)):
            # This makes the array in the JSON array
            if propList.get(propList_raw[i][0:len(propList_raw[i])-1]) == None:
                propList[propList_raw[i][0:len(propList_raw[i])-1]] = []
            # Appends the property in that object
            propList[propList_raw[i][0:len(propList_raw[i])-1]].append(propList_raw[i])
        
        # This takes the players money and pays back the loan
        amount -= players[turn].get_player_cash()
        players[turn].set_player_cash(0)
        # This gives the player their money back if they paid the loan with just their money and paid more than needed
        if amount < 0:
            players[turn].take_player_cash(amount)
            amount = 0

        # This will stop the function if the amount is 0
        if amount == 0:
            return

        # Goes through each property and sells each house until the loan is payed
        for key, value in propList.items():
            for i in range(len(propList[key])):
                # Checks if the player has the property
                if players[turn].get_player_properties().get(propList[key][i]) != None:
                    while (players[turn].get_player_properties()[propList[key][i]]['mortgage'] == False):
                        print(f'Removed house from '+str(propList[key][i]))
                        sell_prop(propList[key][i], True)
                        amount -= propData[propList[key][i]]['price']
                        # This will give the player their money back if the mafia took to much
                        if amount < 0:
                            players[turn].get_player_cash(amount)
                            amount = 0
                        # This will break the while loop once the loan is payed back
                        if amount == 0:
                            break
        update_cash_label(turn)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)
