import sys
import tkinter as tk
from menu.menu import Menu
from ui.ui import MainWindow

def iniciar_aplicacion():
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu = Menu()
        menu.iniciar()
    else:
        root = tk.Tk()
        app = MainWindow(root)
        app.pack()
        root.mainloop()
