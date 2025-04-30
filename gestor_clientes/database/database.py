import sqlite3

class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("clientes.db")  # Se crea si no existe
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                dni TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def agregar_cliente(self, cliente):
        try:
            self.cursor.execute("INSERT INTO clientes VALUES (?, ?, ?)",
                                (cliente.dni, cliente.nombre, cliente.apellido))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # El cliente ya existe

    def obtener_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        rows = self.cursor.fetchall()
        return [Cliente(*row) for row in rows]

    def buscar_cliente(self, dni):
        self.cursor.execute("SELECT * FROM clientes WHERE dni=?", (dni,))
        row = self.cursor.fetchone()
        return Cliente(*row) if row else None

    def modificar_cliente(self, dni, nombre, apellido):
        self.cursor.execute("""
            UPDATE clientes SET nombre=?, apellido=? WHERE dni=?
        """, (nombre, apellido, dni))
        self.conn.commit()

    def borrar_cliente(self, dni):
        self.cursor.execute("DELETE FROM clientes WHERE dni=?", (dni,))
        self.conn.commit()

    def cerrar(self):
        self.conn.close()
