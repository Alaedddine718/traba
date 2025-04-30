import re

class Helpers:
    @staticmethod
    def dni_valido(dni):
        """Ejemplo válido: 12A (2 números + 1 letra mayúscula)"""
        return bool(re.fullmatch(r'\d{2}[A-Z]', dni))

    @staticmethod
    def texto_valido(texto, minimo=2, maximo=30):
        """Valida si el texto tiene solo letras y un tamaño adecuado"""
        return texto.isalpha() and minimo <= len(texto) <= maximo
