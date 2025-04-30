import tkinter as tk
from tkinter import ttk, messagebox
from database.database import Database, Cliente
from helpers.helpers import Helpers

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Gestor de Clientes")
        self.db = Database()
        self.crear_widgets()
        self.cargar()

    def crear_widgets(self):
        self.tree = ttk.Treeview(self, columns=("DNI", "Nombre", "Apellido"), show="headings")
        for col in ("DNI", "Nombre", "Apellido"):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack(pady=10)
        tk.Button(btns, text="Agregar", command=self.agregar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Modificar", command=self.modificar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Borrar", command=self.borrar).grid(row=0, column=2, padx=5)

    def cargar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for c in self.db.obtener_clientes():
            self.tree.insert("", "end", values=(c.dni, c.nombre, c.apellido))

    def agregar(self):
        self.formulario("Agregar Cliente")

    def modificar(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un cliente")
            return
        datos = self.tree.item(sel)["values"]
        self.formulario("Modificar Cliente", datos)

    def borrar(self):
        sel = self.tree.focus()
        if not sel:
            return
        valores = self.tree.item(sel)["values"]
        if messagebox.askokcancel("¿Borrar?", f"¿Borrar a {valores[1]} {valores[2]}?"):
            self.db.borrar_cliente(valores[0])
            self.cargar()

    def formulario(self, titulo, datos=None):
        win = tk.Toplevel(self)
        win.title(titulo)

        etiquetas = ["DNI", "Nombre", "Apellido"]
        valores = []

        for i, texto in enumerate(etiquetas):
            tk.Label(win, text=texto).grid(row=i, column=0)
            var = tk.StringVar(value=datos[i] if datos else "")
            entry = tk.Entry(win, textvariable=var)
            entry.grid(row=i, column=1)
            if datos and i == 0:
                entry.config(state="disabled")
            valores.append(var)

        def guardar():
            dni = valores[0].get().upper()
            nombre = valores[1].get().capitalize()
            apellido = valores[2].get().capitalize()

            if not Helpers.dni_valido(dni) or not Helpers.texto_valido(nombre) or not Helpers.texto_valido(apellido):
                messagebox.showerror("Error", "Datos inválidos.")
                return

            if datos:
                self.db.modificar_cliente(dni, nombre, apellido)
            else:
                if not self.db.agregar_cliente(Cliente(dni, nombre, apellido)):
                    messagebox.showerror("Error", "DNI duplicado.")
                    return

            self.cargar()
            win.destroy()

        tk.Button(win, text="Guardar", command=guardar).grid(row=3, columnspan=2, pady=10)
