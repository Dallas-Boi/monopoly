import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from menu import make_menu

def run_easyGO():
    placeholder = tk.Tk()
    placeholder.geometry("0x0+10+10")
    make_menu()
    placeholder.mainloop()

run_easyGO()
