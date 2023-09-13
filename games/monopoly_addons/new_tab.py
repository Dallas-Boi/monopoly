# Create 1-6-23 Friday
# This is used for the moreBx (Used for the shop, auction, etc...)
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import json
import time
import sys
import random
import os

from errorHandler import send_monopoly_error
from games.monopoly_addons.adv_game import maifa_bank_menu, failed_to_pay

# Destorys the moreBx level
def destroy_moreBx():
    from games.monopoly import action_buttons
    try:
        global edit_prop
        action_buttons['action1'].config(state=NORMAL)
        action_buttons['action2'].config(state=NORMAL)
        action_buttons['action3'].config(state=NORMAL)
        action_buttons['action4'].config(state=NORMAL)
        action_buttons['action5'].config(state=NORMAL)
        action_buttons['action6'].config(state=NORMAL)
        edit_prop = False
        
        moreBx.destroy()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Casino 
# -------
# This opens the casino
def open_casino():
    from games.monopoly import players, turn, update_cash_label
    try:
        moreBx.geometry('500x500')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Auctions 
# ---------
# Ends the auction
def end_auction():
    from games.monopoly import action_buttons, actLabel, bankrupt_props, action5_button_status
    try:
        global br_boolean
        destroy_moreBx()
        # If the auction is auctioning normally
        if br_boolean == False:
            action_buttons['action1'].config(state=DISABLED, text='', command='')
            action_buttons['action2'].config(state=DISABLED, text='', command='')
            action5_button_status()
            actLabel['text'] = 'Welp the property was auctioned off'
        # If the auction is doing bankruptcy
        elif br_boolean == True:
            del player_prop_list[0]
            br_boolean = False
            if len(player_prop_list) >= 1:
                bankrupt_props(player_prop_list[0])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Binds the add buttons
def bind_add_button():
    try:
        add1.bind('<Button-1>', lambda e: add_totalMoney(1));add1['state'] = NORMAL
        add10.bind('<Button-1>', lambda e: add_totalMoney(10));add10['state'] = NORMAL
        add50.bind('<Button-1>', lambda e: add_totalMoney(50));add50['state'] = NORMAL
        add100.bind('<Button-1>', lambda e: add_totalMoney(100));add100['state'] = NORMAL
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Changes the auctions current Turn
def change_auction_turn():
    from games.monopoly import action_buttons, players
    try:
        global auction_turn; global auction_turn_raw
        # Changes the auction_turn
        auction_turn_raw = 'player'+str(int(auction_turn_raw[6:7])+1)
        if auction_turn_raw not in current_players:
            auction_turn_raw = current_players[0]

        # Changes the turn text
        auction_turn = players[auction_turn_raw]['name']
        currentLabel['text'] = f'{auction_turn}\'s turn to bid.'

        bind_add_button()
        # Checks the players money so they can not go negative Dylan
        if players[auction_turn_raw]['cash']-totalValue < 1:
            add1.unbind('<Button-1>');add1['state'] = DISABLED
            add10.unbind('<Button-1>');add10['state'] = DISABLED
            add50.unbind('<Button-1>');add50['state'] = DISABLED
            add100.unbind('<Button-1>');add100['state'] = DISABLED
        elif players[auction_turn_raw]['cash']-totalValue < 10:
            add10.unbind('<Button-1>');add10['state'] = DISABLED
            add50.unbind('<Button-1>');add50['state'] = DISABLED
            add100.unbind('<Button-1>');add100['state'] = DISABLED
        elif players[auction_turn_raw]['cash']-totalValue < 50:
            add50.unbind('<Button-1>');add50['state'] = DISABLED
            add100.unbind('<Button-1>');add100['state'] = DISABLED
        elif players[auction_turn_raw]['cash']-totalValue < 100:
            add100.unbind('<Button-1>');add100['state'] = DISABLED
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Takes the user out of the auction
def remove_auctionPlayer():
    from games.monopoly import action_buttons, players, board, update_cash_label
    try:
        # Removes the user from the current_players
        current_players.remove(auction_turn_raw)
        change_auction_turn()

        # This only executes when there is only one player left in the auction
        # This gives the winner the property 
        if len(current_players) == 1:
            players[auction_turn_raw]['cash'] -= totalValue
            players[auction_turn_raw]['prop'][auction_property] = {'house': 0, 'mortgage': False}
            board.itemconfig(f'bp_{auction_property}', fill=players[auction_turn_raw]['color'])
            update_cash_label(auction_turn_raw)
            end_auction()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Adds money to the auction
def add_totalMoney(amount):
    try:
        global totalValue
        # Logs the added amount
        auctionLog.config(state=NORMAL)
        auctionLog.insert(END, f'{auction_turn} added ${amount}\n')
        auctionLog.config(state=DISABLED)

        # Changes the total amount
        totalValue += amount
        totalLabel['text'] = f'Total Cost: ${totalValue}'

        change_auction_turn()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Allows auctions for properties
def auction_item(item):
    from games.monopoly import action_buttons, players, turn
    try:
        # Auctions Stuff
        global current_players; global auction_turn; global auction_turn_raw; global totalValue; global auctionLog; 
        global currentLabel; global totalLabel; global auction_property
        global add1; global add10; global add50; global add100
        global totalValue; global br_boolean

        #Opens the propertyDetails Json File
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)


        br_boolean = False
        current_players = []
        auction_property = item
        auction_turn_raw = turn
        auction_turn = players[turn].get_player_name()
        moreBx.geometry("500x500")
        moreBx.geometry("+5+5")
        totalValue = 0

        # Adds the players into the list of current players
        for key, value in players.items():
            current_players.append(key)
        
        # Widgets
        # Auction Payment log
        auctionLog = Text(moreBx, width=50, height=20, bg='red');auctionLog.place(x=0, y=30, relx=0.5, rely=0.3, anchor=CENTER)
        auctionLog.config(state=DISABLED)

        # Auction Labels
        currentLabel = Label(moreBx, text=f'{auction_turn}\'s turn to bid.', font=('Helvetica 10 underline'));currentLabel.place(x=0, y=80, relx=0.25, rely=0.6, anchor=CENTER)
        totalLabel = Label(moreBx, text=f'Total Cost: ${totalValue}.', font=('Helvetica 10 underline'));totalLabel.place(x=0, y=120, relx=0.25, rely=0.6, anchor=CENTER)
        propertyLabel = Label(moreBx, text=f'Auctioning off '+str(propData[auction_property]['name']), font=('Helvetica 10 underline'));propertyLabel.place(x=0, y=80, relx=0.75, rely=0.6, anchor=CENTER)
        property_value_label = Label(moreBx, text=f'Property Value $'+str(propData[auction_property]['cost']), font=('Helvetica 10 underline'));property_value_label.place(x=0, y=120, relx=0.75, rely=0.6, anchor=CENTER)

        # Auction money Buttons
        
        add1 = Button(moreBx, text='Add $1');add1.place(x=5, y=0, relx=0.1, rely=0.9, anchor=CENTER);
        add10 = Button(moreBx, text='Add $10');add10.place(x=90, y=0, relx=0.1, rely=0.9, anchor=CENTER);
        add50 = Button(moreBx, text='Add $50');add50.place(x=180, y=0, relx=0.1, rely=0.9, anchor=CENTER);
        add100 = Button(moreBx, text='Add $100');add100.place(x=275, y=0, relx=0.1, rely=0.9, anchor=CENTER);
        callOut = Button(moreBx, text='Stop Bidding');callOut.place(x=385, y=0, relx=0.1, rely=0.9, anchor=CENTER);callOut.bind('<Button-1>', lambda e: remove_auctionPlayer())
        bind_add_button()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)
# -- END | AUCTIONS -- #

# Just to all 2 functions when Selling a house in edit prop
def actButton_click(action, prop, price, select, propData):
    from games.monopoly import action_buttons, players, buy_house, sell_prop
    try:
        #Price: Price of action | Action: the given action | prop: 
        if action == 'buy':
            buy_house(prop, price)
        elif action == 'sell':
            sell_prop(prop)
        change_prop(select, propData)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Changes the property to the selected one
def change_prop(select, propData):
    from games.monopoly import action_buttons, players, turn
    try:
        if select == ("" or "No Properties"):
            return

        for key, value in propData.items():
            if propData[key]['name'] == select:
                # Buy Button
                prop = key

                if ('railroad' in key) or ('electrical' in key) or ('water' in key):
                    if players[turn].get_player_properties()[key]['mortgage'] == False:
                        price = propData[key]['cost']/2
                        actButton1.config(text=f'Mortgage for $'+str(propData[key]['cost']/2), command=lambda: actButton_click('sell', prop, price, select, propData))
                    else:
                        price = int(((propData[key]['cost']/2)*0.1)+propData[key]['cost']/2)
                        actButton1.config(text=f'Un-Mortgage for $'+str(price), command=lambda: actButton_click('buy', prop, price, select, propData))
                    return

                # Checks for houses            
                if players[turn].get_player_properties()[key]['house'] == 4:
                    price = propData[key]['price']
                    actButton1.config(text='Buy Motel for $'+str(price))
                elif players[turn].get_player_properties()[key]['mortgage'] != True:
                    price = propData[key]['price']
                    actButton1.config(text='Buy House for $'+str(price))
                elif players[turn].get_player_properties()[key]['mortgage'] == True:
                    price = int(((propData[key]['cost']/2)*0.1)+propData[key]['cost']/2)
                    actButton1.config(text='Un-Mortgage property $'+str(price))
                if players[turn].get_player_properties()[key]['house'] == 5:
                    actButton1.config(state=DISABLED, text='You already have a Hotel')
                else:
                    actButton1.config(state=NORMAL)

                # Sell Button
                if players[turn].get_player_properties()[key]['house'] == 5: 
                    price = propData[key]['price']
                    actButton2.config(text='Sell Motel for $'+str(price))
                elif players[turn].get_player_properties()[key]['house'] > 0:
                    price = propData[key]['price']
                    actButton2.config(text='Sell House for $'+str(price))
                elif players[turn].get_player_properties()[key]['mortgage'] == False:                    
                    price = propData[key]['cost']/2
                    actButton2.config(state=NORMAL,text='Mortgage for $'+str(price))
                if players[turn].get_player_properties()[key]['mortgage'] == True:
                    actButton2.config(state=DISABLED, text='This property is already mortgaged', command='')
                
            actButton1.config(command=lambda: actButton_click('buy', prop, price, select, propData))
            actButton2.config(command=lambda: actButton_click('sell', prop, price, select, propData))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes the property edit window
def edit_property():
    from games.monopoly import action_buttons, players, turn
    try:
        global selected; global actButton1; global actButton2
        moreBx.geometry('200x500')
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd) 
        propertiesList = ['No Properties']   

        # Adds all the players properties to a list
        for key, value in players[turn].get_player_properties().items():
            propertiesList.append(propData[key]['name'])

        # Removes the "No Properties" if the list is greater than 2
        if len(propertiesList) >= 2:
            propertiesList.remove('No Properties')

        done_edit = Button(moreBx, text='Go Back');done_edit.place(x=0, y=20, relx=0.5, rely=0.0, anchor=CENTER);
        done_edit.bind("<Button-1>", lambda e: destroy_moreBx())

        selected = StringVar()
        selected.set('')
        selected.trace("w", lambda name, index, mode, sv=selected: change_prop(selected.get(), propData))
        ownedList = OptionMenu(moreBx, selected, *propertiesList);ownedList.place(x=0, y=50, relx=0.5, rely=0.0, anchor=CENTER)

        actButton1 = Button(moreBx);actButton1.place(x=0, y=80, relx=0.5, rely=0.0, anchor=CENTER)
        actButton2 = Button(moreBx);actButton2.place(x=0, y=110, relx=0.5, rely=0.0, anchor=CENTER)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# -- Start | Player Shop -- #
# Updates the shop list
def update_shop_items(shop, item):
    del shopItems[item]
    #itemList.config(values=shopItems)

# Adds the item to to the player
def add_bought_item(shop, item):
    from games.monopoly import action_buttons, players, turn, update_cash_label
    try:
        with open('gameData/shopItems.json', 'r') as sd:
            shopData = json.load(sd)
        if players[turn].get_player_inventory().get(item) == None:
            # Checks if the user has enough money
            print(f'Buying {item}')
            if players[turn].get_player_cash() >= shopData[shop][item]['price']:
                players[turn].take_player_cash(shopData[shop][item]['price'])
                if shop == 'Player Shop':
                    print(f'Bought {item}')
                    players[turn].get_player_inventory()[item] = 0
                elif shop == 'Property Shop':
                    print('Developing')
            else:
                detailsLabel.config(text='You do not have enough money.')
                
                return
            update_cash_label(turn)
            load_item(shop, item)
        else:
            detailsLabel.config(text='You already own this item')
            detailsLabel.after(3000, detailsLabel.config(text=shopData[shop][item]['details']))
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Loads the item
def load_item(shop, item, start = None):
    from games.monopoly import action_buttons, players, turn
    global player_actButton1; 
    try:
        with open('gameData/shopItems.json', 'r') as sd:
            shopData = json.load(sd)
        # Checks if the Item is "No Items Available" so that they can not buy it
        if item == "No Items Available":
            player_actButton1.config(state=DISABLED, text='Not Buyable')
            detailsLabel.config(text='Not a Buyable Item')
            return

        item_cost = shopData[shop][item]['price']
        detailsLabel.config(text=shopData[shop][item]['details'])
        player_actButton1.place(x=0, y=160, relx=0.5, rely=0.0, anchor=CENTER)
        # Checks to see if the player owns the item
        if players[turn].get_player_inventory().get(item) == None:
            player_actButton1.config(text=f'Buy Item for ${item_cost}', command=lambda: add_bought_item(shop, item), state=NORMAL)
        elif players[turn].get_player_cash() < item_cost:
            player_actButton1.config(text='You do not have enough money to buy this', state=DISABLED)
        else:
            player_actButton1.config(text='You already own This Item', state=DISABLED)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Allows the player to buy person Items
def load_shop(shop):
    from games.monopoly import action_buttons, players, turn, disabled_items
    try:
        global player_actButton1; global detailsLabel; global selected_item; global itemList; global shopItems
        with open('gameData/shopItems.json', 'r') as sd:
            shopData = json.load(sd) 
        selected_item = StringVar()
        selected_item.set('')
        # If the selected shop is "Player Shop"
        shopItems = list(shopData[shop].keys())
        for i in range(len(shopItems)):
            if players[turn].get_player_inventory().get(shopItems[i]) == True:
                shopItems.remove(shopItems[i])

        # Removes any disabled shop
        for i in range(len(disabled_items[shop])):
            shopItems.remove(disabled_items[shop][i])

        # Checks if the shopItems list is empty
        if len(shopItems) < 1:
            shopItems.append('No Items Available')
        if shop == 'Player Shop':
            player_actButton1 = Button(moreBx);
        selected_item.trace("w", lambda name, index, mode, sv=selected_item: load_item(shop, selected_item.get()))
        itemList = OptionMenu(moreBx, selected_item, *shopItems);itemList.place(x=0, y=80, relx=0.5, rely=0.0, anchor=CENTER)
        detailsLabel = Label(moreBx);detailsLabel.place(x=0, y=110, relx=0.5, rely=0.0, anchor=CENTER)
        #player_actButton2 = Button(moreBx);player_actButton2.place(x=0, y=110, relx=0.5, rely=0.0, anchor=CENTER)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes the item shop
def make_player_shop():
    from games.monopoly import action_buttons, players, turn, disabled_shop
    try:
        global selected_shop; global actButton1; global actButton2
        moreBx.geometry('500x300')
        with open('gameData/shopItems.json', 'r') as sd:
            shopData = json.load(sd) 
        current_shops = list(shopData.keys())

        done_shop = Button(moreBx, text='Go Back');done_shop.place(x=0, y=20, relx=0.5, rely=0.0, anchor=CENTER);
        done_shop.bind("<Button-1>", lambda e: destroy_moreBx())

        # Removes any disabled shop
        for i in range(len(disabled_shop)):
            current_shops.remove(disabled_shop[i])

        selected_shop = StringVar() 
        selected_shop.set('')
        selected_shop.trace("w", lambda name, index, mode, sv=selected_shop: load_shop(selected_shop.get()))
        ownedList = OptionMenu(moreBx, selected_shop, *current_shops);ownedList.place(x=0, y=50, relx=0.5, rely=0.0, anchor=CENTER)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Trading | Start

# Updates all property Colors
def update_property_colors(player):
    from games.monopoly import action_buttons, players, turn, board
    try:
        for key, value in players[player].get_player_properties().items():
            board.itemconfig(f'bp_{key}', fill=players[player].get_player_color())
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Confirms the Current Trade
def confirm_trade(player):
    from games.monopoly import action_buttons, players, turn, update_cash_label
    
    try:
        global they_confirm, your_confirm, your_givingList, their_givingList
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        print('Confirming Trade')
        # Confirms the trade between the two players
        if player == turn:
            your_confirm = True
            print(f'{player} confirmed')
        else:
            they_confirm = True
            print(f'{player} confirmed')
        # When both players confirm
        if they_confirm and your_confirm == True:
            print('Trade Confirm')
            your_confirm = False
            they_confirm = False

            # Changes the selected player name into their ID
            for key, value in players.items():
                if turn != key:
                    if players[key].get_player_name() == select_player.get():
                        other = key
                        break

            # This gives both players the traded properties
            print(players[turn].get_player_properties())
            givingProps = your_givingList
            receivingProps = their_givingList

            your_givingList = receivingProps
            their_givingList = givingProps
            trade_props = False # When this is true it will disable the action1 and action2 buttons
            # Adds the prop to the other player and removes from the current player
            for item in your_givingList:
                players[other].add_player_properties(your_propList_raw[your_givingList.index(item)])
                players[turn].take_player_properties(your_propList_raw[your_givingList.index(item)])
                trade_props = True
        
            # Adds the prop to the current player and removes from the other player
            for item in their_givingList:
                players[turn].add_player_properties(their_propList_raw[their_givingList.index(item)])
                players[other].take_player_properties(their_propList_raw[their_givingList.index(item)])
            
            #Gives the trader the traded cash
            players[turn].add_player_cash(their_givingMoney - your_givingMoney)
            players[other].add_player_cash(your_givingMoney - their_givingMoney)
            #Disables Action1 and action2
            if trade_props == True:
                action_buttons['action1'].config(state=DISABLED)
                action_buttons['action2'].config(state=DISABLED)
            # Updates the property colors of the trade properties
            update_property_colors(turn)
            update_property_colors(other)
            # Updates the cash text
            update_cash_label(turn)
            update_cash_label(other)
            # Destroys the Trade menu
            destroy_moreBx()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

#Checks to see if the trade can be confirmed
def check_confirm():
    try:
        # Checks to see if each list has an item to give
        if (len(their_givingList) and len(your_givingList) >= 1) or (your_givingMoney and their_givingMoney >= 1):
            your_complete.config(state=NORMAL)
            their_complete.config(state=NORMAL)
        else:
            your_complete.config(state=DISABLED)
            their_complete.config(state=DISABLED)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Adds money to the trade
def trade_money_manage(giving_money, player, aOs, value):
    from games.monopoly import action_buttons, players, turn
    try:
        global your_givingMoney; global their_givingMoney; global your_totalValue; global their_totalValue
        # This checks to see if the given value is a interger
        if value == '':
            return
        
        try:
            value = int(value)
        except:
            print(f'{value} is not a valid Number')
            return

        # This allows for money to giving to the other player
        if giving_money == True:
            if player == turn:
                if aOs == "add":
                    your_givingMoney += value
                elif aOs == "sub":
                    your_givingMoney -= value
                your_givingLabel.config(text=players[turn].get_player_name()+f' Giving: ${your_givingMoney}')
                your_moneyEntry.delete(0, END)
            else:
                if aOs == "add":
                    their_givingMoney += value
                elif aOs == "sub":
                    their_givingMoney -= value
                their_givingLabel.config(text=players[turn].get_player_name()+f' Giving: ${their_givingMoney}')
                their_moneyEntry.delete(0, END)
            giving_money = False

        # Updates the total Value for each persons trade
        if giving_money == False:
            if player == turn:
                if aOs == "add":
                    your_totalValue += value
                elif aOs == "sub":
                    your_totalValue -= value
                your_totalLabel['text'] = players[turn].get_player_name()+f' Total Value: ${your_totalValue}'
            else:
                if aOs == "add":
                    their_totalValue += value
                elif aOs == "sub":
                    their_totalValue -= value
                their_totalLabel['text'] = players[turn].get_player_name()+f' Total Value: ${their_totalValue}'
        check_confirm()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Adds the property to the list 
def add_property_list(item, player):
    from games.monopoly import turn
    try:
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        # Checks if the selected property is a valid 
        test_for_fake = 0
        for key, value in propData.items():
            if propData[key]['name'] == item:
                test_for_fake += 1 
        if test_for_fake == 0:
            print('Selected property does not exist')
            return    

        if player == turn: # If the property being added is the players
            if (item in your_givingList) == False:
                your_givingList.append(item)
                your_giving.config(state=NORMAL)
                for key, value in propData.items():
                    if propData[key]['name'] == item:
                        trade_money_manage(False, player, "add", propData[key]['cost'])
                your_giving.insert(END, f'{item}, ')
                your_giving.config(state=DISABLED)
        else: # If the property being added is the other playering being traded
            if (item in their_givingList) == False: # Adds the item to the list if it is not in the list
                their_givingList.append(item)
                their_giving.config(state=NORMAL)
                for key, value in propData.items():
                    if propData[key]['name'] == item:
                        trade_money_manage(False, player, "add", propData[key]['cost'])
                their_giving.insert(END, f'{item}, ')
                their_giving.config(state=DISABLED)
        check_confirm()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Removes the property from the list
def remove_property_list(item, player):
    from games.monopoly import turn
    try:
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        if player == turn: # If the player is editing themself
            if (item in your_givingList) == True:
                your_givingList.remove(item)
                your_giving.config(state=NORMAL)
                for key, value in propData.items():
                    if propData[key]['name'] == item:
                        trade_money_manage(False, player, "sub", propData[key]['cost']) # removes money to the total value
                your_giving.delete(1.0, END) # The index in the string of the item
                newList = ""
                for word in your_givingList: # Recreates the list of properties
                    newList += word+", "
                your_giving.insert(END, newList) # Inserts the new list
                your_giving.config(state=DISABLED)
        else: # If the player is editing the other player
            if (item in your_givingList) == True:
                your_givingList.remove(item)
                your_giving.config(state=NORMAL)
                for key, value in propData.items():
                    if propData[key]['name'] == item:
                        trade_money_manage(False, player, "sub", propData[key]['cost']) # removes money to the total value
                your_giving.delete(1.0, END) # The index in the string of the item
                newList = ""
                for word in your_givingList: # Recreates the list of properties
                    newList += word+", "
                your_giving.insert(END, newList) # Inserts the new list
                your_giving.config(state=DISABLED)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Shows the Add/Remove buttons for trading
def update_button(player, item):
    from games.monopoly import action_buttons, players, turn
    try:
        if 'do not have' in str(item):
            return
        if player == turn:
            you_give_button = Button(moreBx, text='Add Property', command=lambda : add_property_list(item, player));you_give_button.place(x=0, y=180, relx=0.35, rely=0.0, anchor=CENTER)
            you_remove_button = Button(moreBx, text='Remove Property', command=lambda : remove_property_list(item, player));you_remove_button.place(x=0, y=210, relx=0.35, rely=0.0, anchor=CENTER)
        else:
            their_give_button = Button(moreBx, text='Add Property', command=lambda : add_property_list(item, player));their_give_button.place(x=0, y=180, relx=0.70, rely=0.0, anchor=CENTER)
            their_remove_button = Button(moreBx, text='Remove Property', command=lambda : remove_property_list(item, player));their_remove_button.place(x=0, y=210, relx=0.70, rely=0.0, anchor=CENTER)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Shows the Dropdowns Menu for trading
def user_change(propData, trade_with):
    from games.monopoly import action_buttons, players, turn
    try:
        global your_giving, their_giving, your_moneyEntry, their_moneyEntry
        global your_totalLabel, their_totalLabel, your_givingLabel, their_givingLabel
        global your_complete, their_complete, their_propList_raw, your_propList_raw

        # Makes the trade_with from ID into a name
        for key, value in players.items():
            print(f'players: '+players[key].get_player_name()+f' | trade_with: {trade_with}')
            if turn != key:
                if players[key].get_player_name() == trade_with:
                    trade_with = key
                    break
        try:
            your_moneyEntry != None
            # Your Objects
            your_nameLabel.destroy()
            your_moneyLabel.destroy()
            your_moneyEntry.destroy()
            your_addMoney.destroy()
            your_removeMoney.destroy()
            your_givingMoney.destroy()
            your_totalLabel.destroy()
            your_complete.destroy()
            your_giving.destroy()
            turnList.destroy()
            # Their Objects
            their_nameLabel.destroy()
            their_moneyLabel.destroy()
            their_moneyEntry.destroy()
            their_addMoney.destroy()
            their_removeMoney.destroy()
            their_givingMoney.destroy()
            their_totalLabel.destroy()
            their_complete.destroy()
            their_giving.destroy()
            otherList.destroy()
        except NameError:
            placeholder = 0 # Put in place for the try and except
            
        # If the player has no tradable items
        your_propList = [players[turn].get_player_name()+f' has no tradable items'] # Frontend
        your_propList_raw = [] # Backend 
        their_propList = [players[trade_with].get_player_name()+f' has no tradable items'] # Frontend
        their_propList_raw = [] # Backend 

        # Adds all the properties to the current turn owns to a list
        for key, value in players[turn].get_player_properties().items():
            if players[turn].get_player_properties()[key]['house'] == 0:
                your_propList_raw.append(key) # This will have the key for the property
                your_propList.append(propData[key]['name']) # This will show on the user side for names

        # Adds all the properties to trade_with owns to a list
        for key, value in players[trade_with].get_player_properties().items():
            if players[trade_with].get_player_properties()[key]['house'] == 0:
                # Instead of adding the name it will add the key so it will be more simple and faster later on
                their_propList_raw.append(key) # This will have the key for the property
                their_propList.append(propData[key]['name'])# This will show on the user side for names
                

        # Checks to see if the list of properties is greater than 2 
        # if it is then it will remove the "no tradable items"
        if len(your_propList) >= 2:
            your_propList.remove(players[turn].get_player_name()+f' has no tradable items')
        
        if len(their_propList) >= 2:
            their_propList.remove(players[trade_with].get_player_name()+f' has no tradable items')

        # The traders nametags
        your_nameLabel = Label(moreBx, text=players[turn].get_player_name()+f' Items', font=('Helvetica 10 underline'));your_nameLabel.place(x=0, y=20, relx=0.35, rely=0.0, anchor=CENTER)
        their_nameLabel = Label(moreBx, text=players[trade_with].get_player_name()+f' Items', font=('Helvetica 10 underline'));their_nameLabel.place(x=0, y=20, relx=0.70, rely=0.0, anchor=CENTER)

        # The traders money management
        your_moneyLabel = Label(moreBx, text='Add/Remove Money');your_moneyLabel.place(x=0, y=40, relx=0.35, rely=0.0, anchor=CENTER)
        your_moneyEntry = Entry(moreBx);your_moneyEntry.place(x=0, y=60, relx=0.35, rely=0.0, anchor=CENTER)
        your_addMoney = Button(moreBx, text='Add Money');your_addMoney.place(x=0, y=90, relx=0.35, rely=0.0, anchor=CENTER);your_addMoney.bind("<Button-1>", lambda e: trade_money_manage(True, turn, 'add', your_moneyEntry.get()))
        your_removeMoney = Button(moreBx, text='Remove Money');your_removeMoney.place(x=0, y=120, relx=0.35, rely=0.0, anchor=CENTER);your_removeMoney.bind("<Button-1>", lambda e: trade_money_manage(True, turn, 'sub', your_moneyEntry.get()))

        # The trade_with mony management
        their_moneyLabel = Label(moreBx, text='Add/Remove Money');their_moneyLabel.place(x=0, y=40, relx=0.70, rely=0.0, anchor=CENTER)
        their_moneyEntry = Entry(moreBx);their_moneyEntry.place(x=0, y=60, relx=0.70, rely=0.0, anchor=CENTER)
        their_addMoney = Button(moreBx, text='Add Money');their_addMoney.place(x=0, y=90, relx=0.7, rely=0.0, anchor=CENTER);their_addMoney.bind("<Button-1>", lambda e: trade_money_manage(True, trade_with, 'add', their_moneyEntry.get()))
        their_removeMoney = Button(moreBx, text='Remove Money');their_removeMoney.place(x=0, y=120, relx=0.7, rely=0.0, anchor=CENTER); their_removeMoney.bind("<Button-1>", lambda e: trade_money_manage(True, trade_with, 'sub', their_moneyEntry.get()))

        # The trader select property dropdown menu
        your_selectProp = StringVar()
        your_selectProp.set('Pick a Property')
        turnList = OptionMenu(moreBx, your_selectProp, *your_propList, command=lambda e: update_button(turn, your_selectProp.get()));turnList.place(x=0, y=150, relx=0.35, rely=0.0, anchor=CENTER)

        # The trade_with select property dropdown menu
        their_selectProp = StringVar()
        their_selectProp.set('Pick a Property')
        otherList = OptionMenu(moreBx, their_selectProp, *their_propList, command=lambda e: update_button(trade_with, their_selectProp.get()));otherList.place(x=0, y=150, relx=0.70, rely=0.0, anchor=CENTER)

        # The trader's givingMoney, confirm button, and totalValue widgets
        your_givingLabel = Label(moreBx, text=players[turn].get_player_name()+f' Giving: ${your_givingMoney}');your_givingLabel.place(x=0, y=-30, relx=0.25, rely=0.6, anchor=CENTER)
        your_totalLabel = Label(moreBx, text=players[turn].get_player_name()+f' Total Value: ${your_totalValue}');your_totalLabel.place(x=0, y=0, relx=0.25, rely=0.6, anchor=CENTER)
        your_complete = Button(moreBx, text=players[turn].get_player_name()+f' Confirm');your_complete.place(x=0, y=30, relx=0.25, rely=0.6, anchor=CENTER)
        your_complete.bind('<Button-1>', lambda e: confirm_trade(turn)); your_complete.config(state=DISABLED)
        your_giving = Text(moreBx, width=250, height=10);your_giving.place(x=0, y=350)
        your_giving.config(state=DISABLED)

        # The trade_with givingMoney, confirm button, and totalValue Widgets
        their_givingLabel = Label(moreBx, text=players[trade_with].get_player_name()+f' Giving: ${their_givingMoney}');their_givingLabel.place(x=0, y=-30, relx=0.75, rely=0.6, anchor=CENTER)
        their_totalLabel = Label(moreBx, text=players[trade_with].get_player_name()+f' Total Value: ${your_totalValue}');their_totalLabel.place(x=0, y=0, relx=0.75, rely=0.6, anchor=CENTER)
        their_complete = Button(moreBx, text=players[trade_with].get_player_name()+f' Confirm');their_complete.place(x=0, y=30, relx=0.75, rely=0.6, anchor=CENTER)
        their_complete.bind('<Button-1>', lambda e: confirm_trade(trade_with));their_complete.config(state=DISABLED)
        their_giving = Text(moreBx, width=250, height=10);their_giving.place(x=250, y=350)
        their_giving.config(state=DISABLED)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Makes the trade window
def trade_items():
    from games.monopoly import action_buttons, players, turn
    try:
        global your_givingList; global their_givingList; global select_player
        global your_givingMoney; global their_givingMoney; global your_confirm; global they_confirm
        global your_totalValue; global their_totalValue
        moreBx.geometry('500x500')
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd) 

        playList = []
        playList_raw = []

        for key, value in players.items():
            if key != turn:
                playList.append(players[key].get_player_name())
                playList_raw.append(key)

        # variables for Trading
        your_givingList = [];your_givingMoney = 0;your_totalValue = 0;your_confirm = False
        their_givingList = [];their_givingMoney = 0;their_totalValue = 0;they_confirm = False

        # Allows the user to select a player to trade with
        select_player = StringVar()
        select_player.set('Select Player')
        pList = OptionMenu(moreBx, select_player, *playList, command=lambda e: user_change(propData, select_player.get()));pList.place(x=0, y=20, relx=0.10, rely=0.0, anchor=CENTER)
        c_trade = Button(moreBx, text='Cancel', command=destroy_moreBx);c_trade.place(x=0, y=50, relx=0.10, rely=0.0, anchor=CENTER)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Trading | END

# Gets Property Details
def property_get_details():
    from games.monopoly import action_buttons, players, turn, board, grid
    try:
        global prop_land_cost_list
        moreBx.geometry("500x500")
        # Property Data
        with open('gameData/propertyDetails.json', 'r') as pd:
            propData = json.load(pd)

        # Gets the clicked item
        propId = board.gettags("current")[0]
        # Dictionary of the labels for prop_land_cost
        prop_land_cost_list = {}

        # Allows the house placement to be clicked
        for key, value in grid.items():
            if grid[key]['place'] in propId:
                propId = grid[key]['place']
                break
        prop = propData[propId]

        # Gets the properties Color
        for key, value in grid.items():
            if grid[key]['place'] == propId:
                color = grid[key]['color']

        border = Canvas(moreBx, width=500, height=100);border.place(x=0, y=20, relx=0.5, rely=0.0, anchor=CENTER)
        border.create_rectangle(0, 0, 500, 100, fill=color, tag='PropBorder')

        # The properties name/price Label
        prop_name = Label(moreBx, text=f'Property Name: '+str(prop['name']), font=('Helvetica 10 underline'));prop_name.place(x=0, y=20, relx=0.5, rely=0.3, anchor=CENTER)
        prop_price = Label(moreBx, text=f'Property Price: $'+str(prop['cost']), font=('Helvetica 10 underline'));prop_price.place(x=0, y=50, relx=0.5, rely=0.3, anchor=CENTER)

        # Checks to see if the property can by houses
        if prop.get('price') != None:
            prop_house_cost = Label(moreBx, text=f'Property Price per House: $'+str(prop['price']), font=('Helvetica 10 underline'));prop_house_cost.place(x=0, y=80, relx=0.5, rely=0.3, anchor=CENTER)

        # Checks to see if the property has rent
        if prop.get('rent') != None:
            for i in range(5):
                prop_land_cost = Label(moreBx, text=f'Rent With {i} House(s): $'+str(prop['rent'][i]), font=('Helvetica 10 underline'))
                prop_land_cost.place(x=0, y=110+(i*30), relx=0.5, rely=0.3, anchor=CENTER)
                prop_land_cost_list[f'house{i}'] = prop_land_cost
            prop_land_cost = Label(moreBx, text=f'Rent With a Hotel: $'+str(prop['rent'][5]), font=('Helvetica 10 underline'))
            prop_land_cost.place(x=0, y=260, relx=0.5, rely=0.3, anchor=CENTER)
            prop_land_cost_list[f'hotel'] = prop_land_cost

        go_back = Button(moreBx, text='Go Back');go_back.place(x=0, y=0, relx=0.5, rely=0.9, anchor=CENTER);go_back.bind('<Button-1>', lambda e: destroy_moreBx())
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)

# Used to make the new window for other options
def new_frame(type, item = None, props = None, bankrupt_boolean = False):
    from games.monopoly import action_buttons, players, turn, reset_action_buttons
    try:
        global moreBx; global edit_prop; global player_prop_list; global br_boolean
        moreBx = tk.Toplevel()
        moreBx.title(type)
        moreBx.resizable(False, False)
        player_prop_list = props
        br_boolean = bankrupt_boolean
        reset_action_buttons('disable')
        if type == 'edit':
            edit_property()
            edit_prop = True
        elif type == 'trade':
            trade_items()
        elif type == 'propDetails':
            property_get_details()
        elif type == 'auction':
            auction_item(item)
        elif type == 'shop':
            make_player_shop()
        elif type == 'mafia':
            maifa_bank_menu(moreBx)
        elif type == 'casino':
            open_casino()
        else:
            print('THIS ISNT POSSIBLE TO SEE')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        send_monopoly_error(exc_type, fname, exc_tb.tb_lineno, e)
