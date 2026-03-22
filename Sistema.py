# Inicializando línea de desarrollo

# MIIMPERIO

from enum import Enum
from abc import ABCMeta, abstractmethod



# -----------------------
# EXCEPCIONES

class ErrorImperio(Exception): # La clase general 
    pass

class ErrorInexistenciaUd(ErrorImperio):
    # cuando una entidad: unidad de combate o almacén, no existe
    pass

class ErrorInexistenciaAlmacen(ErrorInexistenciaUd):
    # cuando un almacén no existe
    pass

class ErrorInexistenciaNave(ErrorInexistenciaUd):
    # cuando empleamos una nave que no existe
    pass

class ErrorRepuesto(ErrorImperio): # Clase general para los errores referentes a los repuestos
    pass

class ErrorRepuestoNoCatalogo(ErrorRepuesto):
    # consultar o actualizar un repuesto que no tenemos en el catalogo
    pass

class ErrorStockInsuficiente(ErrorImperio):
    # para cuando vamos a modificar un stock de un repuesto más de lo que se puede realizar
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
    '''
    TAD UnidadCombate (DESCRIPCIÓN: Clase  abstracta que define la interfaz base para cualquier entidad, naves, vehiculos terrestres
    y demás. No puede ser instanciada directamente. Sus atributos son id_combate y _num_cod; VALORES: str e int; OPERACIONES: __init__,
    mostrar_informacion(), get_repuestos(), get_catalogo())
    '''

    def __init__(self, id_combate : str, num_cod : int):
        '''
        CrearUnidadCombate(str,int)--> UnidadCombate
        Efecto: crea un objeto UnidadCombate con id_combate, y _num_cod
        '''
        self.id_combate = id_combate
        self._num_cod = num_cod # Importante calificar este atributo como privado al ser una identifiación de codificación

    
    # Todos sus métodos son métodos abstractos
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
    TAD Nave (DESCRIPCIÓN: Subclase de UnidadCombate que representa todas las naves. Tienen como atributos id_combate y num_cod (heredado de UnidadCombate) y un nombre;
    VALORES: dos str(id_combate y nombre), un int (num_cod); OPERACIONES: __init__, consultar_repuesto, mostrar_información,get_repuestos, get_catalogo y anyadir_catalogo)
    '''

    def __init__(self, id_combate: str, num_cod: int, nombre: str):
        '''
        CrearNave(str,int,str)--> Nave
        Efecto: Inicializa la nave llamando al constructor de la superclase UnidadCombate con super() para 
        recibir los datos id_combate y num_cod, e inicializa su nombre. Además, crea una lista vacía piezas_repuesto que 
        actuará como el catálogo de componentes técnicos que la nave puede utilizar. No la pasamos como atirbuto porque debe ir añadiendo
        sólo los repuestos disponibles en nuestra flota, que inicialmente puede no haber a la hora de recibir la nave.
        '''
        super().__init__(id_combate, num_cod)
        self.nombre = nombre
        self.piezas_repuesto = []
        

    def consultar_repuesto(self, nombre:str):
        '''
        Efecto: Busca si un repuesto con un nombre específico (nombre) forma parte del catalogo de la nave.
        Gestiona mayusculas/minúsculas y espacios para evitar errores de usuario para comparar ocn piezas_repuesto.
        Si está dentro de su catalogo de repuestos (piezas_repuesto) devuelve True.
        Empleamos T/F en vez de la excepción ErrorRepuestoNoCatalogo porque no queremos que se termine el programa.
        '''
        busqueda = nombre.lower().strip()
        for repuesto in self.piezas_repuesto: 
            if repuesto.nombre.lower().strip() == busqueda:
                return True
        return False 

    
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
    '''
    TAD NaveEstelar (DESCRIPCIÓN: Clase que representa un tipo de nave,los atributos que tiene son id_combate, num_cod y nombre (hereadados de Nave),
    tripulacion y pasaje (heredados de UnidadCombte) y una clase basada en la enumeración EClase; VALORES: str, int y EClase;
    OPERACIONES: __init__, mostrar_información
    '''
    def __init__(self, id_combate: str, num_cod: int, nombre: str, tripulacion: int, pasaje : int, clase: EClase):
        '''
        CrearNaveEstelar (str, int, str, int, int, EClase) --> NaveEstelar
        Efecto: Construye el objeto inciializando los atributos correspondientes de su herencia múltiple y la clase. En lugar de usar super(),
        realizamos llamadas individuales a los constructores de las clases padre para evitar ambigüedades.
        '''
        TripuPasaje.__init__(self,tripulacion, pasaje)
        Nave.__init__(self,id_combate, num_cod, nombre)
        self.clase = clase
    
    def mostrar_informacion(self):
        '''
        Efecto: sobreescribe el método de la superclase Nave para mostrar la información relativa de este tipo de Nave
        '''
        print(f'Id_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}')
        

# ------------------------------ 

class CazaEstelar(Nave):
    '''
    TAD CazaEstelar (DESCRIPCIÓN: Clase que representa un tipo de nave,los atributos que tiene son id_combate, num_cod y nombre (hereadados de Nave),
    y dotacion; VALORES: str e int;
    OPERACIONES: __init__, mostrar_información
    '''
    def __init__(self, id_combate: str, num_cod: int, nombre: str, dotacion: int):
        '''
        CrearCazaEstelar (str, int, str, int) --> CazaEstelar
        Efecto: Construye el objeto inciializando los atributos correspondientes de su herencia y la dotación. Aquí utilizamos el método
        super() porque no hay ambigüedades.
        '''
        super().__init__(id_combate, num_cod, nombre)
        self.dotacion = dotacion
    
    def mostrar_informacion(self):
        '''
        Efecto: sobreescribe el método de la superclase Nave para mostrar la información relativa de este tipo de Nave
        '''
        print(f'd_combate: {self.id_combate} -- Num_cod: {self._num_cod} -- Nombre: {self.nombre}')
        

# ------------------------------ 

class Almacen():
    '''
    TAD Almacen (DESCRIPCIÓN: Clase que representa un almacén,los atributos que tiene son nombre y localización; VALORES: str ;
    OPERACIONES: __init__,dar_de_alta, comprobar_stock, contar_existencias, actualizar,obtener_catalogo, obtener_repuesto.
    '''
    
    def __init__(self, nombre: str, localizacion: str):
        '''
        CrearAlmacen (str, str) --> Almacén
        Efecto: Construye el objeto incializando los atributos correspondientes. Además creamos una lista para el catálogo,
        que no añadimos a los parámetros del constructor para posibilitar que una vez construido el almacén desde cero no se le obligue
        a tener ya una lista de repuestos (que pueda inicializarse vacío).
        '''
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = []
 
    
    def dar_de_alta(self, nombre:str, proveedor:str, cantidad:int, precio:int):
        '''
        Efecto: Crear una instancia de la clase Repuesto y añadirla al catálogo por primera vez.
        '''
        nuevo = Repuesto(nombre, proveedor, cantidad, precio)
        self.catalogo.append(nuevo)
    
    
    
    def comprobar_stock(self, nombre_repuesto):
        '''
        Efecto: Devolver un booleano que indique si hay stock de un repuesto que queremos consultar a partir de su nombre.
        Para ello recorremos todos los elementos disponibles en el catalogo de esta instancia de Almacén y depuramos
        minúsculas/mayúsculas y espacios para ver si el nombre del repuesto consultado coincide con el nombre de algún repuesto del catálogo.
        Una vez localizado el repuesto comprobamos la cantidad del mismo en el almacen (su stock) con el método _get_numero() que accede al atrbibuto
        privado. Si esa cantidad es >0, entonces devolvemos que ese repuesto está en el Almacén y su stock. En caso contrario,
        retornamos False y cantidad 0. 
        Excepcion: Si al recorrer la lista de todos los repuestos del catalogo del almacén no lo encontramos, lanzamos una excepción de que 
        el repuesto buscado no está en el catalogo de esta instancia de almacén.
        '''
        for repuesto in self.catalogo:
            if repuesto.nombre.lower().strip() == nombre_repuesto.lower().strip():
                cantidad = repuesto._get_numero()
                if cantidad >0:
                    return True, cantidad
                else:
                    return False, 0
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no existe en el catálogo.") 
    
    
    
    def contar_existencias(self): 
        '''
        Efecto: Contamos cuantas existencias, de todos los tipos de repuesto, tiene un almacén. Para ello
        recorremos todos los repuestos del catalogo y sacamos el stock de cada uno. Esa cantidad se va sumando a un contador
        llamado total, que será el entero que devolvamos.
        '''
        total = 0
        for repuesto in self.catalogo:
            total += repuesto._get_numero()
        return total
    
    
    
    def actualizar(self, nombre_repuesto: str, cantidad: int):
        '''
        Efecto: Mantiene el stock de los repuestos en el catálogo del almacén. Recibe el nombre del repuesto cuya cantidad(stock) se quiera modificar
        y el importe de la misma (en el atributo cantidad). Si la cantidad es positiva, es que queremos aumentar el stock de ese repuesto,
        si es negativa, es que queremos disminuirlo. Para ello recorremos la lista de repuestos en nuestro catálogo del almacén y comprobamos, como en el método anterior,
        si ese repuesto que queremos actualizar se encuentra en el catálogo. Si no, devolveremos la misma excepción que antes, ErrorRepuestoNoCatalogo.
        Una vez confirmado que ese repuesto está en el catálogo, calculamos el nuevo stock deseado, sumandole la cantidad deseada al stock existente.
        Si es menor que cero, como no queremos mantener stock negativo de un repuesto, lanzamos la excepción ErrorStockInsuficiente.
        En el caso contrario, actualizamos el stock con el método _set_numero().
        '''
        for repuesto in self.catalogo: 
            if repuesto.nombre.lower() == nombre_repuesto.lower():
                nuevo_stock = repuesto._get_numero() + cantidad
                if nuevo_stock < 0: 
                    raise ErrorStockInsuficiente(f'Stock insuficiente')
                repuesto._set_numero(nuevo_stock) 
                print(f'Stock actualizado')
                return
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no existe en el catálogo. Hay que darlo de alta en el sistema.")  
    
    # Lanzamos ese error para que el usuario deba invocar a la funcion dar_de_alta(). Podríamos haberlo implementado todo aquí, que si no exista, se dé de alta
    # automaticamente, pero hemos evitado esto para que cada vez que un operario quiera actualizar no tenga que meter toda la información del repuesto

    
    
    def obtener_catalogo(self):
        '''
        Efecto: Función para devolver el catálogo de repuestos un almacén. Para la funcionalidad de listar_catalogo() del Operario.
        '''
        return self.catalogo
    

   
    def obtener_repuesto(self, nombre_repuesto:str):
        '''
        Efecto: Devolver la instancia de la clase Repuesto almacenada dentro de la lista catálogo de un Almacén. Si el nombre de repuesto buscado no coincide,
        lanza una excepción ErrorRepuestoNoCatalogo.
        '''
        for repuesto in self.catalogo:
            if repuesto.nombre.lower() == nombre_repuesto.lower():
                return repuesto
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no está en el catálogo de este almacén.")
        

# ------------------------------         

class FlotaEspacial():
    '''
    TAD FlotaEspacial (DESCRIPCIÓN: Clase que representa la Flota Espacial, la organización; OPERACIONES: __init__,anyadir_almacen, 
    anyadir_nave, listar_repuestos, actualizar,dar_de_alta, consultar_repuesto,anyadir_repuesto_a_nave,adquirir_repuesto.
    '''
    
    def __init__(self):
        '''
        CrearFlotaEpacial()-->FlotaEspacial
        Efecto: Creamos la clase contenedora, la organización. Inicialmente la flota cuando se crea está vacía, por lo que no le pasamos ningún atributo, simplemente
        vamos a ir añadiendo unidades de combate y almacenes cuando lo haga el Operario o el Comandante. Para ello creamos dos listas vacias, una para las Unidades de Combate y
        otra para los almacenes.
        '''
        self.ud_combate_imperial = []
        self.almacenes = []


    def anyadir_almacen(self, almacen: Almacen):
        '''
        Efecto: Función para añadir un almacén a la lista de almacenes de la flota.
        '''
        self.almacenes.append(almacen)



    def anyadir_nave(self, nave: Nave):
        '''
        Efecto: Función para añadir una nave a la lista de unidades de combate imperial de la flota.
        '''
        self.ud_combate_imperial.append(nave)

    
    def listar_repuestos(self):
        '''
        Efecto: Listamos los repuestos de todos los almacenes en la flota. Imprimos por pantalla
        , para cada almacén de la lista de almacenes, todo su catalogo de repuestos con el método de la clase
        Almacén obtener_catalogo(), que devolvía una lista de todos sus repuestos. Si esta lista existe, pues iteramos
        por cada uno de sus instancias de Repuesto para imprimirlas. En el caso de no existir esa lista de repuestos en Almacén, devolvemos
        que el almacén está vacío.
        '''
        for almacen in self.almacenes:
            print(f'Repuestos en el Almacén : {almacen.nombre}')
            catalogo = almacen.obtener_catalogo()
            if not catalogo:
                print('El almacén está vacío')
            else:
                for repuesto in catalogo:
                    print(f"- {repuesto}")
    
    
    
    def actualizar(self,nombre_repuesto: str, cantidad:int):
        '''
        Efecto: Actualizar el stock de un repuesto pero mandando la tarea a Almacén. Implementamos este método en esta clase
        pues los clientes solo interactúan con esta clase. Este es un principio básico del encapsulamiento.
        La flota recorre sus almacenes e invoca el método actualizar() de la clase Almacén. Si el repuesto se encuentra y 
        se actualiza con éxito, el proceso termina. 
        Excepciones: Si el repuesto no existe en ningún almacén tras recorrer la lista completa,  se lanza una excepción ErrorRepuestoNoCatalogo 
        indicando que debe darse de alta.
        '''
        for almacen in self.almacenes:
            try:
                almacen.actualizar(nombre_repuesto, cantidad)
                return
            except ErrorRepuestoNoCatalogo:
                continue
        raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto}' no se ha encontrado en ningún almacén.")



    def dar_de_alta(self, nombre_repuesto:str, proveedor: str, cantidad:int, precio:int, nombre_almacen:str):
        '''
        Efecto: Registra un nuevo repuesto en un almacén específico de la flota. El método primero valida la existencia del almacén mediante una 
        búsqueda por nombre en la lista de almacenes. Si se localiza, delega la creación del objeto Repuesto al método dar_de_alta() del almacén correspondiente.
        Excepciones: Si el almacén no existe, lanza una excepción ErrorInexistenciaAlmacen,
        '''
        encontrado = False
        for almacen in self.almacenes:
            if almacen.nombre == nombre_almacen:
                encontrado = almacen
                break
        if not encontrado:
            raise ErrorInexistenciaAlmacen(f"El almacén '{nombre_almacen}' no está registrado.")
        almacen.dar_de_alta(nombre_repuesto, proveedor, cantidad, precio)
    
    
    
    def consultar_repuesto(self, nombre_repuesto: str, id: str):
        '''
        Efecto: Verifica si una unidad de combate específica tiene un repuesto determinado en su catálogo. Busca la unidad en 
        la lista de la flota mediante su id_combate. Si la encuentra, delega la búsqueda del repuesto al método consultar_repuesto() 
        de la propia unidad. 
        Excepciones: Si la unidad no existe en el registro de la flota, lanza una excepción ErrorInexistenciaNave.
        '''
        for udcombate in self.ud_combate_imperial:
            if udcombate.id_combate == id:
                return udcombate.consultar_repuesto(nombre_repuesto)
        raise ErrorInexistenciaNave(f"Unidad de Combate con id '{id}' no encontrada en la Flota Espacial.")        
    
    
    def anyadir_repuesto_a_nave(self,id_nave:str, nombre: str, proveedor:str, cantidad:int, precio:int):
        '''
        Efecto: Registra un repuesto en el catálogo de una nave específica. Busca la unidad de combate en la flota por su id_nave. 
        Si la localiza, invoca el método anyadir_catalogo() de la nave para que esta reconozca el repuesto como parte de 
        su equipamiento. 
        Excepciones: Si el id_nave no corresponde a ninguna nave registrada, lanza una excepción ErrorInexistenciaNave.
        '''
        for nave in self.ud_combate_imperial:
            if nave.id_combate == id_nave:
                nave.anyadir_catalogo(nombre,proveedor,cantidad,precio)
                return
        raise ErrorInexistenciaNave(f"La nave '{id_nave}' no está registrada en la flota.")



    def adquirir_repuesto(self, nombre_repuesto:str, id: str, cantidad:int):
        '''
        Efecto: Gestiona el proceso completo de transferencia de un repuesto desde la logística de la flota hacia una unidad de combate.
        Primero comprueba si la nave tiene el repuesto en su catálogo técnico, es decir, si lo necesita para su funcionamiento. luego ecorre 
        los almacenes buscando stock disponible del repuesto solicitado. Si hay stock suficiente, actualiza el inventario del almacén (restando/sumando la cantidad) 
        y devuelve un nuevo objeto Repuesto con la cantidad adquirida.
  
        Excepciones: Lanza ErrorRepuestoNoCatalogo si la nave no usa la pieza o si no existe en los almacenes, y ErrorStockInsuficiente si la cantidad en el 
        almacén es menor a la solicitada.
        '''
        consulta = self.consultar_repuesto(nombre_repuesto, id)
        if not consulta:
            raise ErrorRepuestoNoCatalogo(f"El repuesto '{nombre_repuesto} no está en el catálogo de la Nave '{id}'.")

        for almacen in self.almacenes:
            try:
                comprobacion, cant_alm = almacen.comprobar_stock(nombre_repuesto)
                if comprobacion and cant_alm>=cantidad:
                    almacen.actualizar(nombre_repuesto, -cantidad)
                    repuesto = almacen.obtener_repuesto(nombre_repuesto)
                    return Repuesto(nombre_repuesto, repuesto.proveedor, cantidad, repuesto.precio)
                continue # si no hay suficiente, pasamos al siguiente almacén
            except ErrorRepuestoNoCatalogo: #si el repuesto no existe en este almacén, ignoramos el error y pasamos al siguiente
                continue
        raise ErrorStockInsuficiente(f"No hay stock suficiente de '{nombre_repuesto}' en toda la flota.")
            
         
 
# ------------------------------        
if __name__ == "__main__":

    # CREAMOS LA FLOTA Y UN ALMACÉN
    print("Pruebas de OPERARIO" + '\n')
    mi_flota= FlotaEspacial()
    almacen_1= Almacen('Almacen Maria', 'Marte')
    mi_flota.anyadir_almacen(almacen_1)
    
    # DAMOS DE ALTA UN REPUESTO
    mi_flota.dar_de_alta('Tornillo oro', 'Marias', 200000, 13, 'Almacen Maria')
    print(f'Almacen: {almacen_1.nombre} -> Existencias: {almacen_1.contar_existencias()}')

    # CREAMOS UNA NAVE Y LA AÑADIMOS A LA FLOTA
    nav1 = NaveEstelar("MCN-2005", 123, 'MCN', 10, 5, EClase.EJECUTOR) 
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
    
    print("PRUEBAS DE COMANDANTE" + '\n')

    mi_flota.anyadir_repuesto_a_nave('MCN-2005', 'Tornillo de Diamante', 'Marias', 0, 20)
    
    
    mi_flota.dar_de_alta('Tornillo de Diamante', 'Locs', 200, 20, 'Almacen Maria')

    mi_flota.listar_repuestos()
    

    repuesto_necesitado = mi_flota.adquirir_repuesto('Tornillo de Diamante', 'MCN-2005', 20)

    print("Los productos adquiridos son:", repuesto_necesitado) # Vemos como nos ha devuelto 20 repuestos del mismo 

    mi_flota.listar_repuestos() # Vemos como se ha reducido en 20 los tornillos de Diamante

    