from database.database import Database, Cliente
from helpers.helpers import Helpers

class Menu:
    def __init__(self):
        self.db = Database()

    def iniciar(self):
        while True:
            print("\n=== GESTOR DE CLIENTES ===")
            print("[1] Listar")
            print("[2] Buscar")
            print("[3] Añadir")
            print("[4] Modificar")
            print("[5] Borrar")
            print("[6] Salir")
            opcion = input("> ")

            if opcion == "1": self.listar()
            elif opcion == "2": self.buscar()
            elif opcion == "3": self.agregar()
            elif opcion == "4": self.modificar()
            elif opcion == "5": self.borrar()
            elif opcion == "6": self.db.cerrar(); break
            else: print("Opción inválida.")

    def listar(self):
        for c in self.db.obtener_clientes(): print(c)

    def buscar(self):
        dni = input("DNI: ").upper()
        c = self.db.buscar_cliente(dni)
        print(c if c else "No encontrado.")

    def agregar(self):
        dni = input("DNI (2 números y 1 letra): ").upper()
        if not Helpers.dni_valido(dni): print("DNI inválido."); return
        nombre = input("Nombre: ").capitalize()
        apellido = input("Apellido: ").capitalize()
        if not Helpers.texto_valido(nombre) or not Helpers.texto_valido(apellido):
            print("Nombre o apellido inválido."); return
        cliente = Cliente(dni, nombre, apellido)
        ok = self.db.agregar_cliente(cliente)
        print("Añadido." if ok else "Ya existe.")

    def modificar(self):
        dni = input("DNI: ").upper()
        c = self.db.buscar_cliente(dni)
        if not c: print("No encontrado."); return
        nombre = input(f"Nombre nuevo [{c.nombre}]: ") or c.nombre
        apellido = input(f"Apellido nuevo [{c.apellido}]: ") or c.apellido
        self.db.modificar_cliente(dni, nombre, apellido)
        print("Modificado.")

    def borrar(self):
        dni = input("DNI: ").upper()
        ok = self.db.borrar_cliente(dni)
        print("Borrado." if ok else "No encontrado.")
