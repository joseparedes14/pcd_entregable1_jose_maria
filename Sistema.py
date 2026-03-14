# Inicializando línea de desarrollo

# MIIMPERIO

from enum import Enum
from abc import ABCMeta, abstractmethod

# ------------------------------ 

# Creamos Primero las Enumeraciones presentes en el diagrama UML con el módulo enum
class EClase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2


class EUbicacion(Enum):
    ENDOR = 0
    CUMULO_RAIMOS = 1
    NEBULOSA_KALIIDA = 2


# ------------------------------ 


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

# ------------------------------ 

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

# ------------------------------ 
    
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

# ------------------------------ 


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
        print(f"Id_combate: {self.id_combate}; Num_cod: {self._num_cod}; Nombre: {self.nombre}")
    
    def get_repuestos(self):
        # Muestra los nombres de piezas que este tipo de nave puede usar
        for i in self.piezas_repuesto:
            print(i + '\n')

    # Añadir aquí anyadir_repuestos() ?

'''
class Nave(UnidadCombate):
    def __init__(self, id_combate: str, num_cod: int, nombre: str):
        super().__init__(id_combate, num_cod)
        self.nombre = nombre
        self.piezas_repuesto = []
    
    def consultar_repuesto(self, nombre:str):
        busqueda = nombre.lower().strip()
        for repuesto in self.piezas_repuesto:
            if repuesto.nombre.lower().strip() == busqueda:
                return True
        return False
    
    def mostrar_informacion(self):
        print(f"Id_combate: {self.id_combate}; Num_cod: {self._num_cod}; Nombre: {self.nombre}")
    
    def get_repuestos(self):
        for i in self.piezas_repuesto:
            print(i + '\n')
'''


# ------------------------------ 

class EstacionEspacial(TripuPasaje, Nave):

    def __init__(self, id_combate: str, num_cod: int, nombre: str, tripulacion: int, pasaje : int, ubicacion: EUbicacion):
        TripuPasaje.__init__(self,tripulacion, pasaje)
        Nave.__init__(self,id_combate, num_cod, nombre)
        self.ubicacion = ubicacion

    def mostrar_informacion(self):
        print(f"Id_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}")

# ------------------------------ 

class NaveEstelar(TripuPasaje, Nave):
    
    def __init__(self, id_combate: str, num_cod: int, nombre: str, tripulacion: int, pasaje : int, clase: EClase):
        TripuPasaje.__init__(self,tripulacion, pasaje)
        Nave.__init__(self,id_combate, num_cod, nombre)
        self.clase = clase
    
    def mostrar_informacion(self):
        print(f'd_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}')
        

# ------------------------------ 

class CazaEstelar(Nave):
   
    def __init__(self, id_combate: str, num_cod: int, nombre: str, dotacion: int):
        super().__init__(id_combate, num_cod, nombre)
        self.dotacion = dotacion
    
    def mostrar_informacion(self):
        print(f'd_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}')
        

# ------------------------------ 

class Almacen():
    
    def __init__(self, nombre: str, localizacion: str, catalogo: list):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = []
    
    def comprobar_stock(self, nombre_repuesto): #devuelve si hay stock de ese repuesto que consulta
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre_repuesto and repuesto._numero > 0:
                return True
        return False
    
    def contar_existencias(self): #contar las existencias del almacen de todos los repuestos
        total = 0
        for repuesto in self.catalogo:
            total += repuesto._numero
        return total
    
    def actualizar(self, nombre_repuesto: str, cantidad: int):
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre_repuesto:
                repuesto._numero += cantidad


# ------------------------------         

class FlotaEspacial():
    
    def __init__(self, ud_combate_imperial:list, almacenes: list):
        self.ud_combate_imperial = []
        self.almacenes = []
    
    def adquirir_repuesto(self, nave:str, nombre_repuesto:str, cantidad:int, almacenes: list):
        # vemos si esa nave tiene ese repuesto
        if not nave.consultar_repuesto(nombre_repuesto):
            print(f'La nave {nave} no usa el repuesto: {nombre_repuesto}')
            return []
        
        repuestos_adquiridos = []
        cantidad_solicitada = cantidad
        
        # si lo tiene, comprobamos en los almacenes los stocks
        for almacen in almacenes:
            stock_disp = almacen.comprobar_stock(nombre_repuesto)
            if True: #esto se complica. Posible cambio a que comprobar_stock() devuelva la cantidad?
                
             
             
 
# ------------------------------        
if __name__ == "__main__": 
    hola = EClase.ECLIPSE
    print(hola)
    almacen_maria = Almacen('Almacen Maria', 'Marte', [])
    rep1 = Repuesto('Tornillo oro','Marias', 100, 200000)
    almacen_maria.catalogo.append(rep1)
    print(f'Almacen: {almacen_maria.nombre} -> Existencias: {almacen_maria.contar_existencias()}')
    
    nav1 = NaveEstelar("MCN-2005", 123, 'MCN', 10, 5, 'ECLIPSE' )
    nav1.mostrar_informacion()
    
    nav1.piezas_repuesto.append(rep1)
    print(f'¿Quedan tornillos de oro?: {nav1.consultar_repuesto('Tornillo oro')}')
    print(f'¿Quedan tornillos de cristal?: {nav1.consultar_repuesto('Tornillo cristal')}')