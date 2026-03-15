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
        self._num_cod = num_cod # Importante calificar este atributo como privado al ser una identifiación de codificación
        self.piezas_repuesto = []

    @abstractmethod

    def mostrar_informacion(self):
        pass

    @abstractmethod

    def get_repuestos(self):
        pass

    @abstractmethod

    def get_catalogo(self):
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


    def _get_numero(self):
        return self._numero

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
        
    
    def consultar_repuesto(self, nombre:str):
        busqueda = nombre.lower().strip()
        for repuesto in self.piezas_repuesto:
            if repuesto.nombre.lower().strip() == busqueda:
                return True
        return False
    
    def mostrar_informacion(self):
        print(f"Id_combate: {self.id_combate}; Num_cod: {self._num_cod}; Nombre: {self.nombre}")
    
    def get_repuestos(self):
        # Muestra los nombres de piezas que este tipo de nave puede usar
        for i in self.piezas_repuesto:
            print(str(i) + '\n')

    def get_catalogo(self):
        return self.piezas_repuesto


    def anyadir_catalogo(self, nombre: str, proveedor: str, cantidad:int, precio:int):
        repuesto = Repuesto(nombre, proveedor, cantidad, precio)
        self.piezas_repuesto.append(repuesto)


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
        print(f'Id_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}')
        

# ------------------------------ 

class CazaEstelar(Nave):
   
    def __init__(self, id_combate: str, num_cod: int, nombre: str, dotacion: int):
        super().__init__(id_combate, num_cod, nombre)
        self.dotacion = dotacion
    
    def mostrar_informacion(self):
        print(f'd_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}')
        

# ------------------------------ 

class Almacen():
    
    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = []

        
    def dar_de_alta(self, nombre:str, proveedor:str, cantidad:int, precio:int):
        nuevo = Repuesto(nombre, proveedor, cantidad, precio)
        self.catalogo.append(nuevo)
    
    def comprobar_stock(self, nombre_repuesto): #devuelve si hay stock de ese repuesto que consulta
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre_repuesto and repuesto._numero > 0:
                return True,repuesto._numero
        return False,0
    
    def contar_existencias(self): #contar las existencias del almacen de todos los repuestos
        total = 0
        for repuesto in self.catalogo:
            total += repuesto._get_numero()
        return total
    
    def actualizar(self, nombre_repuesto: str, cantidad: int):
        # funcion para mantener el stock. Cantidad positiva añadir, cantidad negativa eliminar. Si llega a 0, eliminamos
        # como catalogo es una lista,necesitamos el indice para borrar cuando llegue a 0
        for i, repuesto in enumerate(self.catalogo): 
            if repuesto.nombre.lower() == nombre_repuesto.lower():
                if repuesto._get_numero() + cantidad < 0: #no puede haber stock negativo
                    raise ValueError(f'Stock insuficiente')
                repuesto._numero += cantidad   
                if repuesto._numero == 0:
                    self.catalogo.pop(i)
                else:
                    print(f'Stock actualizado')
                return
        raise ValueError("Repuesto no encontrado. Hay que darlo de alta en el sistema.")  # decimos esto para que cada vez que un operario quiera actualizar no tenga que meter toda la información del repuesto

    def obtener_catalogo(self):
        # para la funcionalidad de listar_catalgo del operario
        return self.catalogo
    

    def obtener_repuesto(self, nombre_repuesto:str):
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre_repuesto:
                return repuesto
        return False
        

# ------------------------------         

class FlotaEspacial():
    
    def __init__(self):
        self.ud_combate_imperial = []
        self.almacenes = []
    '''
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
            if True: #esto se complica. --> cambio a que comprobar_stock() devuelva (bool,cantidad)
    '''



    def anyadir_almacen(self, almacen: Almacen):
        self.almacenes.append(almacen)

    
    def anyadir_nave(self, nave: Nave):
        self.ud_combate_imperial.append(nave)



    # El operario mantiene y lista stock 
    def listar_repuestos(self):
        #listamos el stock de todos repuestos
        for almacen in self.almacenes:
            print(f'Repuestos en el Almacén : {almacen.nombre}')
            catalogo = almacen.obtener_catalogo()
            if not catalogo:
                print('El almacén está vacío')
            else:
                for repuesto in catalogo:
                    print(f"- {repuesto}")
    
    def actualizar(self,nombre_repuesto: str, cantidad:int):
        # La Flota manda la tarea a almacen.
        for almacen in self.almacenes:
            try:
                almacen.actualizar(nombre_repuesto, cantidad)
                return
            except ValueError:
                print('No está el producto. Hay que darlo de alta')
        # si no se encontro en ningun almacen, es porque hay que darlo de alta


    def dar_de_alta(self, nombre_repuesto:str, proveedor: str, cantidad:int, precio:int, nombre_almacen:str):
        for almacen in self.almacenes:
            if almacen.nombre == nombre_almacen:
                almacen.dar_de_alta(nombre_repuesto, proveedor, cantidad, precio)

        
    
    def consultar_repuesto(self, nombre_repuesto: str, id: str):
        for udcombate in self.ud_combate_imperial:
            if udcombate.id_combate == id:
                consulta = udcombate.consultar_repuesto(nombre_repuesto)
                if consulta:
                    return True
                else:
                    return False
        raise ValueError('Unidad de Combate no encontrada en la Flota Espacial')
    


    def adquirir_repuesto(self, nombre_repuesto:str, id: str, cantidad:int):
        consulta = self.consultar_repuesto(nombre_repuesto, id)
        if not consulta:
            raise ValueError('Repuesto No Disponible para la Nave Especificada')
    
        for almacen in self.almacenes:
            comprobacion, cant_alm = almacen.comprobar_stock(nombre_repuesto)
            if comprobacion and cant_alm >= cantidad:
                almacen.actualizar(nombre_repuesto, -cantidad)
                repuesto = almacen.obtener_repuesto(nombre_repuesto)
                return Repuesto(nombre_repuesto, repuesto.proveedor, cantidad, repuesto.precio)

        raise ValueError('No hay repuestos de este tipo en ningún almacen')


            
        

    
             
 
# ------------------------------        
if __name__ == "__main__":



    # -- PRUEBA MARÍA (ANOTADO JOSE) --

    # CAMBIA LO DEL SI ES = 0, SE QUITA
    # Poner en las funciones donde modificas numero, una funcion en repuesto para modificarlo? Y así evitar _numer


    print("Pruebas de OPERARIO" + '\n')
    almacen_1= Almacen('Almacen Maria', 'Marte')
    mi_flota= FlotaEspacial()
    rep1 = Repuesto('Tornillo oro','Marias', 200000, 13)
    almacen_1.catalogo.append(rep1) # Corregir desde una funcion desde miflota
    print(f'Almacen: {almacen_1.nombre} -> Existencias: {almacen_1.contar_existencias()}')

    mi_flota.anyadir_almacen(almacen_1)
    
    nav1 = NaveEstelar("MCN-2005", 123, 'MCN', 10, 5, 'ECLIPSE' ) # Eclipse? No debería ser un tipo enumeración
    nav1.mostrar_informacion()
    

    nav1.piezas_repuesto.append(rep1) # Corregir con implementacion de funcion
    print(f'¿Quedan tornillos de oro?: {nav1.consultar_repuesto('Tornillo oro')}')
    print(f'¿Quedan tornillos de cristal?: {nav1.consultar_repuesto('Tornillo cristal')}')
    
    #prueba de actualizacion de stock que existe
    mi_flota.actualizar('Tornillo oro',13)
    mi_flota.actualizar('Tornillo oro',-200013)  #vemos si se elimina porque se queda a 0
    print(f'Vacio?: {len(almacen_1.catalogo)}') #aqui me sale 1, deberia ser 0
    
    # dar de alta
    # mi_flota.actualizar("Motor de Salto", 5)





    # -- PRUEBA JOSE 
    print("PRUEBAS DE COMANDANTE" + '\n')

    nav1.anyadir_catalogo('Tornillo de Diamante', 'Locs', 0, 20) # Ponemos 0 en cantidad pues solo es referencia
    mi_flota.anyadir_nave(nav1)
    
    mi_flota.dar_de_alta('Tornillo de Diamante', 'Locs', 200, 20, 'Almacen Maria')

    mi_flota.listar_repuestos()
    

    repuesto_necesitado = mi_flota.adquirir_repuesto('Tornillo de Diamante', 'MCN-2005', 20)

    print(repuesto_necesitado) # Vemos como nos ha devuelto 20 repuestos del mismo 

    mi_flota.listar_repuestos() # Vemos como se ha reducido en 2

    