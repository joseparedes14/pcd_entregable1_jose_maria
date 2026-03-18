# Inicializando línea de desarrollo

# MIIMPERIO

from enum import Enum
from abc import ABCMeta, abstractmethod



# -----------------------
# EXCEPCIONES

class ErrorImperio(Exception):
    pass

class ErrorInexistenciaUd(ErrorImperio):
    # cuando una entidad: unidad de combate o almacén, no existe
    pass

class ErrorInexistenciaAlmacen(ErrorInexistenciaUd):
    # cuando un almacén no existe
    pass

class ErrorInexistenciaNave(ErrorInexistenciaUd):
    pass

class ErrorRepuesto(ErrorImperio):
    pass

class ErrorRepuestoNoCatalogo(ErrorRepuesto):
    # consultar o actualizar un repuesto que no tenemos en el catalogo
    pass

class ErrorStockInsuficiente(ErrorImperio):
    pass

# ------------------------------ 

# Enumeraciones presentes en el diagrama UML con el módulo enum
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
    '''
    TAD Repuesto (DESCRIPCIÓN: Clase que representa una pieza con los atributos nombre, proveedor, cantidad y precio, VALORES:
    dos cadenas (nombre y proveedor) y dos enteros (numero y precio); OPERACIONES: __init__, mostrar_información, _get_numero, _set_numero)
    '''
    
    def __init__(self, nombre: str, proveedor: str, numero: int, precio : int):
        '''
        CrearRepuesto(str, str, int, int) --> Repuesto
        Efecto: crea un objeto Repuesto con nombre, proveedor, cantidad inicial y precio.
        Excepciones: el atributo numero (cantidad) se define como privado
        '''
        self.nombre = nombre
        self.proveedor = proveedor
        self._numero = numero  # Nos pide explícitamente el enunciado que pongamos este atributo como privado
        self.precio = precio
    
    def __str__(self):
        '''
        Efecto: devuelve una cadena con toda la información del repuesto para imprimir
        '''
        return f"Nombre: {self.nombre}; Proveedor: {self.proveedor}, Numero: {self._numero}, Precio: {self.precio}"


    def mostrar_informacion(self):   
        '''
        Efecto: Imprime en la consola el repuesto. Invoca el método mágico __str__ definido en la clase
        '''
        print(self)


    def _get_numero(self):
        '''
        Efecto: Devuelve la cantidad de un repuesto disponible. Es un método privado para controlar la recuperación del atributo privado _numero.
        '''
        return self._numero
    
    def _set_numero(self,nuevo):
        '''
        Efecto: Modifica la cantidad de un repuesto disponible. 
        Excepciones: Si el nuevo valor de numero es negativo, lanzamos una excepción ValueError porque no puede haber cantidad negativa de un repuesto
        '''
        if nuevo <0:
            raise ValueError('El stock no puede ser negativo')
        self._numero = nuevo
# ------------------------------ 
    

class TripuPasaje():
    '''
    TAD TripuPasaje (DESCRIPCIÓN: Clase que agrupa los atributos de tripulacion y pasaje; VALORES: dos enteros; OPERACIONES: __init__)
    '''
    def __init__(self, tripulacion: int, pasaje:int):
        '''
        CrearTripuPasaje(int, int) --> TripuPasaje
        Efecto: Inicializa los valores de tripulación (personas responsables de la unidad) y pasaje (numero de personas que caben en la unidad que no participan en su operación)
        '''
        self.tripulacion = tripulacion
        self.pasaje = pasaje

# ------------------------------ 


class Nave(UnidadCombate):
    '''
    TAD Nave (DESCRIPCIÓN: Subclase de UnidadCombate que representa todas las naves. Tienen como atributos id_combate y num_cod (heredado de UnidadCombate) y un nombre y una lista de objetos de la clase Repuesto;
    VALORES: dos str(id_combate y nombre), un int (num_cod) y una list (piezas_repuesto); OPERACIONES: __init__, consultar_repuesto, mostrar_información,get_repuestos, get_catalogo y anyadir_catalogo)
    '''

    def __init__(self, id_combate: str, num_cod: int, nombre: str):
        '''
        CrearNave(str,int,str)--> Nave
        Efecto: Inicializa la nave llamando al constructor de la superclase UnidadCombate con super() para 
        recibir los datos id_combate y num_cod, e inicializa su nombre.
        '''
        super().__init__(id_combate, num_cod)
        self.nombre = nombre
        self.piezas_repuesto = []
        

    def consultar_repuesto(self, nombre:str):
        '''
        Efecto: Busca si un repuesto con un nombre específico (nombre) forma parte del catalogo de la nave.
        Gestiona mayusculas/minúsculas y espacios para evitar errores de usuario para comparar ocn piezas_repuesto.
        Si está dentro de su catalogo de repuestos (piezas_repuesto) devuelve True.
        '''
        busqueda = nombre.lower().strip()
        for repuesto in self.piezas_repuesto: 
            if repuesto.nombre.lower().strip() == busqueda:
                return True
        return False
        # o podemos lanzar un error
        # raise ErrorRepuestoNoCatalogo(f"La nave '{self.nombre}' no tiene el repuesto '{nombre}')

    
    def mostrar_informacion(self):
        '''
        Efecto: implementa el método abstracto heredado para imprimir por pantalla el id_combate, el num_cod y el nombre
        '''
        print(f"Id_combate: {self.id_combate}; Num_cod: {self._num_cod}; Nombre: {self.nombre}")
    
    def get_repuestos(self):
        '''
        Efecto: Recorre e imprime la lista de objetos Repuesto asociados a la nave dentro de su catalogo lista de repuestos.
        Muestra los nombres de piezas que este tipo de nave puede usar.
        '''
        for i in self.piezas_repuesto:
            print(str(i) + '\n')

    def get_catalogo(self):
        '''
        Efecto: devuelve la lista de objetos Repuesto asociados a la nave.
        '''
        return self.piezas_repuesto


    def anyadir_catalogo(self, nombre: str, proveedor: str, cantidad:int, precio:int):
        '''
        Efecto: Instancia un nuevo objeto Repuesto y lo añade a la lista piezas_repuesto de la nave. Sirve para que una nave sepa
        qué repuestos puede solicitar al almacén.
        '''
        repuesto = Repuesto(nombre, proveedor, cantidad, precio)
        self.piezas_repuesto.append(repuesto)


# ------------------------------ 

class EstacionEspacial(TripuPasaje, Nave):
    '''
    TAD EstacionEspacial (DESCRIPCIÓN: Clase que representa un tipo de nave,los atributos que tiene son id_combate, num_cod y nombre (hereadados de Nave),
    tripulacion y pasaje (heredados de UnidadCombte) y una ubicacion basada en la enumeración EUbicacion; VALORES: str, int y EUbicacion;
    OPERACIONES: __init__, mostrar_información
    '''

    def __init__(self, id_combate: str, num_cod: int, nombre: str, tripulacion: int, pasaje : int, ubicacion: EUbicacion):
        '''
        CrearEstacionEspacial (str, int, str, int, int, EUbicacion) --> EstacionEspacial
        Efecto: Construye el objeto inciializando los atributos correspondientes de su herencia múltiple y la ubicacion. En lugar de usar super(),
        realizamos llamadas individuales a los constructores de las clases padre para evitar ambigüedades.
        '''
        TripuPasaje.__init__(self,tripulacion, pasaje)
        Nave.__init__(self,id_combate, num_cod, nombre)
        self.ubicacion = ubicacion

    def mostrar_informacion(self):
        '''
        Efecto: sobreescribe el método de la superclase Nave para mostrar la información relativa de este tipo de Nave
        '''
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
            if repuesto.nombre.lower().strip() == nombre_repuesto.lower().strip():
                cantidad = repuesto._get_numero()
                if cantidad >0:
                    return True, cantidad
                else:
                    return False, 0
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no existe en el catálogo.")
    
    def contar_existencias(self): #contar las existencias del almacen de todos los repuestos
        total = 0
        for repuesto in self.catalogo:
            total += repuesto._get_numero()
        return total
    
    def actualizar(self, nombre_repuesto: str, cantidad: int):
        # funcion para mantener el stock. Cantidad positiva añadir, cantidad negativa eliminar.
        for repuesto in self.catalogo: 
            if repuesto.nombre.lower() == nombre_repuesto.lower():
                nuevo_stock = repuesto._get_numero() + cantidad
                if nuevo_stock < 0: #no puede haber stock negativo
                    raise ErrorStockInsuficiente(f'Stock insuficiente')
                repuesto._set_numero(nuevo_stock)    # no haria falta un set_numero????? 
                print(f'Stock actualizado')
                return
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no existe en el catálogo. Hay que darlo de alta en el sistema.")  # decimos esto para que cada vez que un operario quiera actualizar no tenga que meter toda la información del repuesto

    def obtener_catalogo(self):
        # para la funcionalidad de listar_catalgo del operario
        return self.catalogo
    

    def obtener_repuesto(self, nombre_repuesto:str):
        for repuesto in self.catalogo:
            if repuesto.nombre.lower() == nombre_repuesto.lower():
                return repuesto
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no está en el catálogo de este almacén.")
        

# ------------------------------         

class FlotaEspacial():
    
    def __init__(self):
        self.ud_combate_imperial = []
        self.almacenes = []

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
            except ErrorRepuestoNoCatalogo:
                continue
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no se ha encontrado en ningún almacén.")
        # si no se encontro en ningun almacen, es porque hay que darlo de alta


    def dar_de_alta(self, nombre_repuesto:str, proveedor: str, cantidad:int, precio:int, nombre_almacen:str):
        #Buscamos si el almacen existe
        encontrado = False
        for almacen in self.almacenes:
            if almacen.nombre == nombre_almacen:
                encontrado = almacen
                break
        if not encontrado:
            raise ErrorInexistenciaAlmacen(f"El almacén '{nombre_almacen}' no está registrado.")
        #Si existe damos de alts
        almacen.dar_de_alta(nombre_repuesto, proveedor, cantidad, precio)
    
    def consultar_repuesto(self, nombre_repuesto: str, id: str):
        for udcombate in self.ud_combate_imperial:
            if udcombate.id_combate == id:
                return udcombate.consultar_repuesto(nombre_repuesto)
        raise ErrorInexistenciaNave(f"Unidad de Combate con id '{id}' no encontrada en la Flota Espacial.")        
    
    def anyadir_repuesto_a_nave(self,id_nave:str, nombre: str, proveedor:str, cantidad:int, precio:int):
        # Como la nave tiene repuestos en su catalogo (sin stock, solo referenciados)
        # para la funcion anyadir_catalogo en Nave
        for nave in self.ud_combate_imperial:
            if nave.id_combate == id_nave:
                nave.anyadir_catalogo(nombre,proveedor,cantidad,precio)
                return
        raise ErrorInexistenciaNave(f"La nave '{id_nave}' no está registrada en la flota.")

    def adquirir_repuesto(self, nombre_repuesto:str, id: str, cantidad:int):
        # Vemos si la nave usa este repuesto
        consulta = self.consultar_repuesto(nombre_repuesto, id)
        if not consulta:
            raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto} no está en el catálogo de la Nave '{id}'.")
        #comprobamos el stock de los almacenes
        for almacen in self.almacenes:
            comprobacion, cant_alm = almacen.comprobar_stock(nombre_repuesto)
            if comprobacion: #vemos si existe el repuesto en el almacen
                if cant_alm>=cantidad:
                    almacen.actualizar(nombre_repuesto, -cantidad)
                    repuesto = almacen.obtener_repuesto(nombre_repuesto)
                    return Repuesto(nombre_repuesto, repuesto.proveedor, cantidad, repuesto.precio)
                else: #existe pero no tiene stock suficiente
                    raise ErrorStockInsuficiente(f"Stock insuficiente en el almacén '{almacen.nombre}'. Cantidad disponible: {cant_alm}")
        # entonces el repuesto no está en ningún almacen       
        raise ErrorRepuestoNoCatalogo(f"No hay repuestos del tipo '{nombre_repuesto}' en ningún almacén.")

'''
Esto es similar al de teoria, pero a mi me gusta menos.
def adquirir_repuesto(self,nombre_repuesto,id,cantidad):
    adquirido = None
    try:
        consulta = self.consultar_repuesto(nombre_repuesto, id)
        if not consulta:
            raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto} no está en el catálogo de la Nave '{id}'.")
        #comprobamos el stock de los almacenes
        for almacen in self.almacenes:
            comprobacion, cant_alm = almacen.comprobar_stock(nombre_repuesto)
            if comprobacion and cant_alm >= cantidad:
                almacen.actualizar(nombre_repuesto, -cantidad)
                repuesto = almacen.obtener_repuesto(nombre_repuesto)
                break
        if not adquirido:
            raise ErrorStockInsuficiente(f"Stock insuficiente en el almacén '{almacen.nombre}'. Cantidad disponible: {cant_alm}")
    except ErrorInexistenciaNave:
        print("Error: Nave no encontrada.")
    except ErrorRepuestoNoCatalogo:
        print("Error: Repuesto no disponible en esta nave.")
    except ErrorStockInsuficiente:
        print("Error: Fallo en el inventario de los almacenes.")
    finally:
        return repuesto_adquirido
'''             
             
 
# ------------------------------        
if __name__ == "__main__":



    # -- PRUEBA MARÍA (ANOTADO JOSE) --


    # Poner en las funciones donde modificas numero, una funcion en repuesto para modificarlo? Y así evitar _numer

    # CREAMOS LA FLOTA Y UN ALMACÉN
    print("Pruebas de OPERARIO" + '\n')
    mi_flota= FlotaEspacial()
    almacen_1= Almacen('Almacen Maria', 'Marte')
    mi_flota.anyadir_almacen(almacen_1)
    
    # DAMOS DE ALTA UN REPUESTO
    mi_flota.dar_de_alta('Tornillo oro', 'Marias', 200000, 13, 'Almacen Maria')
    print(f'Almacen: {almacen_1.nombre} -> Existencias: {almacen_1.contar_existencias()}')

    # CREAMOS UNA NAVE Y LA AÑADIMOS A LA FLOTA
    nav1 = NaveEstelar("MCN-2005", 123, 'MCN', 10, 5, EClase.ECLIPSE ) 
    mi_flota.anyadir_nave(nav1)
    nav1.mostrar_informacion()
    
    # AQUI EL COMANDANTE AÑADIRÍA ESE REPUESTO A ESA NAVE
    mi_flota.anyadir_repuesto_a_nave('MCN-2005', 'Tornillo oro', 'Marias', 200000, 13)
    
    # CONSULTAMOS LOS REPUESTOS DE LAS NAVES
    print(f'Usa la nave {nav1.nombre} tornillos de oro?: {mi_flota.consultar_repuesto('Tornillo oro', "MCN-2005")}')
    print(f'Usa la nave {nav1.nombre} tornillos de cristal?: {mi_flota.consultar_repuesto('Tornillo cristal', "MCN-2005")}')
    
    # ACTUALIZAMOS STOCK
    # - Añadir
    mi_flota.actualizar('Tornillo oro',13)
    print('Stock final: \n')
    mi_flota.listar_repuestos()
    
    
    # - Eliminar
    mi_flota.actualizar('Tornillo oro',-12)
    print(f'Stock final: {mi_flota.listar_repuestos()}')
    
    # - Retirar más del disponible
    mi_flota.actualizar('Tornillo oro',-1200000)


    # -- PRUEBA JOSE 
    print("PRUEBAS DE COMANDANTE" + '\n')

    nav1.anyadir_catalogo('Tornillo de Diamante', 'Locs', 0, 20) # Ponemos 0 en cantidad pues solo es referencia
    # HE PENSADO PONER ESTO DESDE MI FLOTA??
    
    
    mi_flota.dar_de_alta('Tornillo de Diamante', 'Locs', 200, 20, 'Almacen Maria')

    mi_flota.listar_repuestos()
    

    repuesto_necesitado = mi_flota.adquirir_repuesto('Tornillo de Diamante', 'MCN-2005', 20)

    print(repuesto_necesitado) # Vemos como nos ha devuelto 20 repuestos del mismo 

    mi_flota.listar_repuestos() # Vemos como se ha reducido en 2

    