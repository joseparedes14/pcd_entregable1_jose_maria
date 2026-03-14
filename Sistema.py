# Inicializando línea de desarrollo

# MIIMPERIO

from enum import Enum
from abc import ABCMeta, abstractmethod

# Creamos Primero las Enumeraciones presentes en el diagrama UML con el módulo enum

class EClase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2



class EUbicacion(Enum):
    ENDOR = 0
    CUMULO_RAIMOS = 1
    NEBULOSA_KALIIDA = 2


# Creamos la clase abstracta UnidadCombate con el módulo abc


class UnidadCombate(metaclass=ABCMeta):

    def __init__(self, id_combate : str, num_cod : int):
        self.id_combate = id_combate
        self._num_cod = num_cod # Importante calificar este atributo como privado al ser una identifiación de odificación

    @abstractmethod

    def mostrar_informacion(self):
        pass

    @abstractmethod

    def get_repuestos(self):
        pass




# Creammos las distintas clases del esquema

class Repuesto():
    def __init__(self, nombre: str, proveedor: str, numero: int, precio : int):
        self.nombre = nombre
        self.proveedor = proveedor
        self._numero = numero  # Nos pide explícitamente el enunciado que pongamos este atributo como privado
        self.precio = precio

    
    def __str__(self):
        return f"Nombre: {self.nombre}; Proveedor: {self.proveedor}, Numero: {self._numero}, Precio: {self.precio}"


    def mostrar_informacion(self):
        print(self)


    

'''

¿Implementación?

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

'''


class TripuPasaje():
    def __init__(self, tripulacion: int, pasaje:int):
        self.tripulacion = tripulacion
        self.pasaje = pasaje


    



class Nave(UnidadCombate):
    def __init__(self, id_combate: str, num_cod: int, nombre: str):
        super().__init__(id_combate, num_cod)
        self.nombre = nombre
        self.piezas_repuesto = []
    

    def consultar_repuesto(self, nombre:str):
        for repuesto in self.piezas_repuesto:
            if repuesto.nombre == nombre:
                return True
        return False
    

    def mostrar_informacion(self):
        print(f"Id_combate: {self.id_combate}; Num_cod: {self.num_cod}; Nombre: {self.nombre}")
    
    def get_repuestos(self):
        for i in self.piezas_repuesto:
            print(i + '\n')

    # Añadir aquí anyadir_repuestos() ?




class EstacionEspacial(TripuPasaje, Nave):

    def __init__(self, id_combate: str, num_cod: int, nombre: str, tripulacion: int, pasaje : int, ubicacion: EUbicacion):
        TripuPasaje.__init__(tripulacion, pasaje)
        Nave.__init__(id_combate, num_cod, nombre)
        self.ubicacion = ubicacion

    def mostrar_informacion(self):
        print(f"Id_combate: {self.id_combate}; Num_cod: {self.num_cod}; Nombre: {self.nombre}")




hola = EClase.ECLIPSE

print(hola)