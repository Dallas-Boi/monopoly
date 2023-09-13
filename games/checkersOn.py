import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import json
import time
import requests
from io import BytesIO
from PIL import Image, ImageTk
import asyncio
import math

# Sets movement vars to blank
def set_b():
    global toGrid; global fromGrid
    toGrid = ''; fromGrid = ''

# Kings the piece if called
def king_piece(fm):
    print(f'Kinged {fm}')
    pieceCoords[fm]['kinged'] = True
    board.itemconfig(fm, outline='white')

# Checks to see if the jump is valid
def check_jump(fm, to, moveX, moveY):
    for key, value in pieceCoords.items():
        if (pieceCoords[key]['x'] == gridCoords[to]['x']-((moveX)/2)) and (pieceCoords[key]['y'] == gridCoords[to]['y']-((moveY)/2)):
            print('Jumping')
            board.delete(key)
            del pieceCoords[key]
            return;
    print('Can not jump nothing')
    return 'no';

# Movement process
def move_piece(fm, to, moveX, moveY):
    global turn
    # Checks to see if the piece can move their
    for key, value in pieceCoords.items():
        if pieceCoords[key]['y'] == gridCoords[to]['y'] and pieceCoords[key]['x'] == gridCoords[to]['x']:
            print(f'Spot Taken by {key}')
            return;
    
    # Checks for jump
    if (moveX == 100 or moveX == -100) and (moveY == 100 or moveY == -100):
        if check_jump(fm, to, moveX, moveY) == 'no':
            return
        jumped = True
    
    pieceCoords[fromGrid]['x'] = pieceCoords[fromGrid]['x'] + moveX; pieceCoords[fromGrid]['y'] = pieceCoords[fromGrid]['y']+moveY
    board.move(fromGrid, moveX, moveY)
    
    # Checks to see if piece can be kinged
    if 'b' in fromGrid:
            if pieceCoords[fromGrid]['y'] == 400:
                king_piece(fromGrid)
    else:
            if pieceCoords[fromGrid]['y'] == 50:
                king_piece(fromGrid)
    # Changes the Turn
    if turn == 'Black':
        turnLabel['text'] = 'It is Red\'s Turn'
        turn = 'Red'
    else:
        turnLabel['text'] = 'It is Black\'s Turn'
        turn = 'Black'

# When the user clicks a piece (After a click of a piece and grid 
#then moves piece)
# NEW SYSTEM | Old System was 200 lines
def click(event):
    global fromGrid; global toGrid; global turn
    # Checks to see if the player has already pick a piece to move or a grid to
    # move to
    print(board.gettags('current'))
    if 'g' in board.gettags('current')[0]:
        toGrid = board.gettags('current')[0]
    else:
        fromGrid = board.gettags('current')[0]
    # Movement Process
    # Checks to see if the user has selected a piece to move to the selected grid
    if toGrid != "" and fromGrid != "":
        moveX = gridCoords[toGrid]['x'] - pieceCoords[fromGrid]['x']
        moveY = gridCoords[toGrid]['y'] - pieceCoords[fromGrid]['y']
        print(f'grid x: '+str(gridCoords[toGrid]['x']))
        print(f'grid y: '+str(gridCoords[toGrid]['y']))
        print(f'y: {moveY}')
        print(f'x: {moveX}')
        
        # Checks to see if piece is king
        if 'b' in fromGrid:
            if turn == 'Black':
                if moveY == -50 or moveY == -100:
                    if pieceCoords[fromGrid]['kinged'] != True:
                        print('That Piece is not Kinged')
                        set_b()
                        return;
            else:
                print('It is not your Turn')
                set_b()
                return
        else:
            if turn == 'Red':
                if moveY == 50 or moveY == 100:
                    if pieceCoords[fromGrid]['kinged'] != True:
                        print('That Piece is not Kinged')
                        set_b()
                        return;
            else:
                print('It is not your Turn')
                set_b()
                return;
        
        # Checks if the move is valid    
        if (pow(moveX,2) == pow(moveY,2)) and (moveY <= 100 or moveY >= -100 and moveY != 0) & (moveX <= 100 and moveX >= -100 and moveX != 0):
            move_piece(fromGrid, toGrid, moveX, moveY)
        else:
            print(f'Can not move to {toGrid}')
        
        set_b()
    
# g: column
# r: row
# This makes the game board
def make_board():
    global board; global gridCoords; global turnLabel
    
    gridCoords = {}
    board = Canvas(game, width=400, height=400);board.place(x=300, y=50)
    color = 'tan'
    turnLabel = ttk.Label(game, text='It is Black\'s Turn');turnLabel.place(x=50, y=20, relx=0.5, rely=0.0, anchor=CENTER)
    for r in range(0, 8):
        if color == 'tan':
            color = 'grey'
        elif color == 'grey':
            color = 'tan'
        for c in range(0, 8):
            #print(f'x: {(c+1)*50-50}, {(r+1)*50-50}, {(c+1)*50}, {(r+1)*50}')
            board.create_rectangle((c+1)*50-50, (r+1)*50-50, (c+1)*50, (r+1)*50, fill=color, tag=f'g{c}r{r}')
            gridCoords[f'g{c}r{r}'] = {'x':(c+1)*50, 'y':(r+1)*50}
            
            if color == 'tan':
                color = 'grey'
            elif color == 'grey':
                color = 'tan'
    board.bind("<Button-1>", click)
    
def debug_remove(event):
    print(f'Removed \'{pID.get()}\'')
    del pieceCoords[pID.get()]
    board.delete(pID.get())

# Makes the Piece
def checkers_piece():
    global pieceCoords; global debug
    pieceCoords = {}
    if debug == True:
        global pID; global pick
        pID = ttk.Entry(game);pID.grid(column=0, row=0);
        pick = ttk.Button(game, text="Print");pick.grid(column=0, row=1)
        kingP = ttk.Button(game, text='King');kingP.grid(column=0, row=2)
        remove = ttk.Button(game, text='Remove');remove.grid(column=0, row=3)
        
        pick.bind("<Button-1>", lambda e: print(pieceCoords.get(pID.get())))
        kingP.bind("<Button-1>", lambda e: king_piece(pID.get()))
        remove.bind("<Button-1>", debug_remove)
        
    # Blacks
    for c in range(0, 4):
        board.create_rectangle((c)*100+12.5, 12.5, (c)*100+37.5, 37.5, fill='black', tag=f'b{c}r1')
        pieceCoords[f'b{c}r1'] = {'x':(c)*100+50, 'y':50, 'grid': f'g{c}r1', 'kinged': False}
        
        board.create_rectangle((c)*100+62.5, 62.5, (c)*100+87.5, 87.5, fill='black', tag=f'b{c}r2')
        pieceCoords[f'b{c}r2'] = {'x':(c)*100+100, 'y':100, 'grid': f'g{c}r2', 'kinged': False}
        
        board.create_rectangle((c)*100+12.5, 112.5, (c)*100+37.5, 137.5, fill='black', tag=f'b{c}r3')
        pieceCoords[f'b{c}r3'] = {'x':(c)*100+50, 'y':150, 'grid': f'g{c}r3', 'kinged': False}
            
    # Reds
    for c in range(0, 4):
        board.create_rectangle((c)*100+62.5, 262.5, (c)*100+87.5, 287.5, fill='red', tag=f're{c}r1')
        pieceCoords[f're{c}r1'] = {'x':(c)*100+100, 'y':300, 'grid': f'g{c}r1', 'kinged': False}
        
        board.create_rectangle((c)*100+12.5, 312.5, (c)*100+37.5, 337.5, fill='red', tag=f're{c}r2')
        pieceCoords[f're{c}r2'] = {'x':(c)*100+50, 'y':350, 'grid': f'g{c}r2', 'kinged': False}
        
        board.create_rectangle((c)*100+62.5, 362.5, (c)*100+87.5, 387.5, fill='red', tag=f're{c}r3')
        pieceCoords[f're{c}r3'] = {'x':(c)*100+100, 'y':400, 'grid': f'g{c}r3', 'kinged': False}

#Gets all the items step up
def checkers():
    global fromGrid; global toGrid
    fromGrid=''; toGrid=''
    print('Playing Checkers')
    checkers_piece()

#Starts the gmae
def start(gameName):
    global game; global debug; global turn
    debug = True
    game = tk.Toplevel()
    game.geometry('1000x500')
    game.title(f'{gameName}')
    game.resizable(False, False)
    
    turn = 'Black'
    
    make_board()
    checkers()
    
    game.mainloop()