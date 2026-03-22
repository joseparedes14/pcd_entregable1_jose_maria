import pytest
import Sistema as Sis




# Test Enfocados a las operaciones de Flota Espacial



# Test asociado al comportamiento de dar de alta un almacen

def test_dar_alta():

    flota = Sis.FlotaEspacial()
    almacen = Sis.Almacen('A1', 'Marte')
    flota.anyadir_almacen(almacen) # Instanciamos una flota y le añadimos un almacen

    flota.dar_de_alta('Tornillos de Oro', 'Joses', 100, 200, 'A1')

    assert almacen.contar_existencias() == 100  # Comprobamos que efectivamente se han añadido las distintas unidades al almacen



# Test asociado al correcto manejo de la función actualizar() dentro de flota (integracion)

def test_stock_insuficiente():
    flota = Sis.FlotaEspacial()
    almacen = Sis.Almacen("A1", "Marte")
    flota.anyadir_almacen(almacen)  # Instanciamos una flota y le añadimos un almacen


    flota.dar_de_alta("Tornillo", "Prov", 5, 5, "A1")

    with pytest.raises(Sis.ErrorStockInsuficiente): # Intentamos modificar quitando más unidades de las que hay disponibles
        flota.actualizar("Tornillo", -10)



# Tests asociado a consultar repuestos en naves


# Test que comprueba que maneja que no consultemos a una nave que no existe
def test_consultar_repuesto_nave_no_existente():
    flota = Sis.FlotaEspacial()
    nave = Sis.NaveEstelar('CAE1', 32124, 'Halcón 17', 40, 21, Sis.EClase.SOBERANO)
    nave.anyadir_catalogo('Tornillos De Diamante', 'Joses', 300, 200) 
    flota.anyadir_nave(nave) # Añadimos a la flota una nave con un repuesto en el catálogo

    with pytest.raises(Sis.ErrorInexistenciaNave): #  Intentamos acceder a otra nave no registrada en nuestra Flota 
        flota.consultar_repuesto('Tornillos de Oro', 'CAE2') 


# Test que maneja que efectivamente devuelva False el programa cuando consultemos un repuesto en una nave no compatible con ese repuesto
def test_repuesto_sin_nave():
    nave = Sis.NaveEstelar('CAE1', 32124, 'Halcón 17', 40, 21, Sis.EClase.SOBERANO)
    nave.anyadir_catalogo('Tornillos De Diamante', 'Joses', 300, 200)

    assert nave.consultar_repuesto('Tornillos de Oro') == False



# Test asociado a la función adquirir_repuesto

def test_adquirir_repuesto():
    flota = Sis.FlotaEspacial()

    nave = Sis.NaveEstelar('CAE1', 32124, 'Halcón 17', 40, 21, Sis.EClase.SOBERANO)
    nave.anyadir_catalogo('Tornillos', 'Prov', 0, 200)
    nave.anyadir_catalogo('Tornillos de Oro', 'Prov', 0, 200)
    flota.anyadir_nave(nave) # Añadimos a la flota una nave con dos repuestos en su catalogo


    almacen = Sis.Almacen("A1", "Marte")
    flota.anyadir_almacen(almacen)

    flota.dar_de_alta("Tornillos", "Prov", 10, 200, "A1")

    with pytest.raises(Sis.ErrorStockInsuficiente): # Comprobamos el error de stock insuficiente
        flota.adquirir_repuesto('Tornillos', 'CAE1', 100)

    with pytest.raises(Sis.ErrorRepuestoNoCatalogo): # Compprobamos el error de repuesto incompatible con la nave
        flota.adquirir_repuesto('Tornillo de Oro', 'CAE1', 2)
    
    with pytest.raises(Sis.ErrorInexistenciaNave): # Comprobamos el error de nave que no s eencuentra registrada en la nave
        flota.adquirir_repuesto('Tornillos', 'CAE2', 5)

    
# Test asociado a la funcion contar_existencias
def test_contar_existencias_almacen():
    almacen = Sis.Almacen('A2','Venus')
    almacen.dar_de_alta('Tornillos','Prov1',10,5)
    almacen.dar_de_alta('Tornillos','Prov2',15,5)
    
    assert almacen.contar_existencias()==25
    

# Test para la clase Repuesto que comrpuebe que no puedes ponerle a un repusto stock negativo (unitario)
def test_udneg_repuesto():
    repuesto = Sis.Repuesto('Cristal Rosa','MC',10, 2)
    with pytest.raises(ValueError):
        repuesto._set_numero(-10)
        

# Test para probar la herencia multiple en EstacionEspacial
def test_herencia_estacionespacial():
    estacion = Sis.EstacionEspacial('3928M',135,'Estacion Mayor',10,18,Sis.EUbicacion.ENDOR)
    assert isinstance(estacion, Sis.Nave)
    assert isinstance(estacion, Sis.TripuPasaje)
    assert isinstance(estacion, Sis.UnidadCombate)
    

# Test para probar la herencia multiple en NaveEstelar
def test_herencia_naveestelar():
    nave = Sis.NaveEstelar('98471M',819,'Nave Mayor',5 ,10, Sis.EClase.EJECUTOR)
    assert isinstance(nave, Sis.Nave)
    assert isinstance(nave, Sis.TripuPasaje)
    assert isinstance(nave, Sis.UnidadCombate)

# Test para comprobar la herencia en CazaEstelar
def test_herencia_cazaestelar():
    caza = Sis.CazaEstelar('945721Q',1095,'Caza Mayor',100) 
    assert isinstance(caza, Sis.Nave)
    assert isinstance(caza, Sis.UnidadCombate)