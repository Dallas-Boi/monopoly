import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import json
import time
import requests
from io import BytesIO
from PIL import Image, ImageTk
import random

# Changes the turn
def change_turn():
    global turn
    if turn == 'Blue':
        turn = 'Red'
    else:
        turn = 'Blue'
    board.itemconfig('piece', fill=turn)
    turnLabel['text'] = f'It is {turn}\'s Turn'

# Animates the moving piece at the top of the board
def move_piece(event):
    if (event.x >= 16 and event.x <= 334) and (event.y >= 0 and event.y <= 400):
        board.moveto('piece', event.x-16, 50)

# Checks if the player has won the game
def check_win(place):
    global equalX
    equalX = 50
    pMents = 1
    winningP = [place]
    print(f'Place: {place}')
    for i in range(len(grid[turn])):
        if grid[turn][i] != place:
            if (grid[turn][i][3:4] == place[3:4]) or (grid[turn][i][1:2] == place[1:2]):
                pMents += 1
                winningP.append(grid[turn][i])
    
        if pMents == 4:
            print(f'WinningP: {winningP}')
            winLabel = Label(game, text=f'{turn} has won!');winLabel.place(x=0, y=0, relx=0.5, rely=0.5, anchor=CENTER)
            #board.unbind('<Button-1>')
            #board.unbind('<Motion>')
            return;

# Checks if a piece can be placed
def check_placement(place):
    global below
    i = 6
    while i >= 0:
        below = place[0:3]+str(i)
        print(f'Below: {below}')
        if gridCoords.get(below, {}).get('color') == '':
            print(f'Placed {below}')
            grid[turn].append(below)
            grid[turn].sort()
            board.itemconfig(below, fill = turn)
            print(board.gettags('piece'))
            gridCoords[below]['color'] = turn;
            print(grid)
            return 'place'
        i -= 1

# When the player clicks the space
def click(event):
    try:
        place = board.gettags('current')[0]
        if gridCoords.get(place, {}).get('color') == '':
            if check_placement(place) == 'place':
                check_win(place)
                change_turn()
        elif gridCoords.get(place, {}).get('x') and gridCoords.get(place, {}).get('color') != '':
            print('Take and/or Column Full')
            return;
    except:
        return

# DEBUG (REMOVE IN RELEASE) : Removes the given piece
def debug_remove(event):
    print(f'Removed {pID.get()}')
    board.itemconfig(pID.get(), fill = 'light blue')
    gridCoords[pID.get()]['color'] = ''
    grid[turn][pID.get].remove()

# Makes the board
def make_board():
    global board; global gridCoords; global turnLabel; global pID; global pick
    global remove; global movingPiece
    
    gridCoords = {}
    
    #DEBUG 
    pID = ttk.Entry(game);pID.grid(column=0, row=0);
    pick = ttk.Button(game, text="Print");pick.grid(column=0, row=1);pick.bind("<Button-1>", lambda e: print(gridCoords.get(pID.get())))
    remove = ttk.Button(game, text='Remove');remove.grid(column=0, row=2); remove.bind("<Button-1>", debug_remove)
    
    # Board Making
    board = Canvas(game, width=350, height=400);board.place(x=350, y=0)
    for r in range(0, 6):
        for c in range(0, 7):
            board.create_rectangle((c)*50, (r)*50+100, (c+1)*50, (r+1)*50+100, fill='Blue', tag='Board')
            board.create_oval((c)*50+10, (r)*50+110, (c)*50+40, (r)*50+140, fill='Light Blue', tag=f'c{c+1}r{r+1}')
            gridCoords[f'c{c+1}r{r+1}'] = {'x':(c+1)*50, 'y':(r+1)*50, 'color': ''}
    
    # Moving Piece
    board.create_oval(200, 50, 230, 80, fill=turn, tag='piece')

    # The Label that tells the current turn
    turnLabel = ttk.Label(game, text='It is Blue\'s Turn');turnLabel.place(x=15, y=-20, relx=0.5, rely=0.9, anchor=CENTER)
    
    board.bind("<Motion>", move_piece)
    board.bind("<Button-1>", click)
    
# Starts the gmae
def start(gameName):
    global game; global debug; global turn; global grid
    debug = True
    game = tk.Toplevel()
    game.geometry('1000x500')
    game.title(f'{gameName}')
    game.resizable(False, False)
    
    turn = 'Blue'
    grid = {}
    grid['Blue'] = []
    grid['Red'] = []
    
    
    print('Playing 4 in a line')
    
    make_board()
    
    game.mainloop()