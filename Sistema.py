# Inicializando línea de desarrollo

# MIIMPERIO

from enum import Enum
from abc import ABCMeta, abstractmethod

# Creamos Primero las Enumeraciones presentes en el diagrama UML con el módulo enum

class Clase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2



class Ubicacion(Enum):
    ENDOR = 0
    CUMULO_RAIMOS = 1
    NEBULOSA_KALIIDA = 2


# Creamos la clase abstracta UnidadCombate con el módulo abc


class UnidadCombate(metaclass=ABCMeta):

    def __init__(self, id_combate : str, num_cod : int):
        self.id_combate = id_combate
        self.num_cod = num_cod

    @abstractmethod

    def mostrar_informacion(self):
        pass

    @abstractmethod

    def mostrar_repuestos(self):
        pass




# Creammos las distintas clases del esquema

class Repuesto():
    def __init__(self, nombre: str, proveedor: str, numero: int, precio : int):
        self.nombre = nombre
        self.proveedor = proveedor
        self.numero = numero
        self.precio = precio

    
    def __str__(self):
        return f"Nombre: {self.nombre}; Proveedor: {self.proveedor}, Numero: {self.numero}, Precio: {self.precio}"


    def mostrar_informacion(self):
        print(self)


    


class Catalogo():
    def __init__(self):
        self.repuestos = []
    
    def anyadir_repuesto(self, nombre: str, proveedor: str, numero: str, precio: int):
        self.repuestos.append(Repuesto(nombre, proveedor, numero, precio))

    def __str__(self):
        cadena = ""
        for i in self.repuestos:
            cadena += str(i) + "\n"
        return cadena
    


class TripuPasaje():
    def __init__(self, tripulacion: int, pasaje:int):
        self.tripulacion = tripulacion
        self.pasaje = pasaje


    



class Nave(UnidadCombate):
    def __init__(self, id_combate: str, num_cod: int, nombre: str, piezas_repuesto):
        super().__init__(id_combate, num_cod)
        self.nombre = nombre
        self.piezas_repuesto = Catalogo()


    def mostrar_repuestos():
        pass

