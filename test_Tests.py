import pytest
import Sistema as Sis




# Test Enfocados a las operaciones de Flota Espacial



# Test asociado al comportamiento de dar de alta un almacen

def test_dar_alta():
    flota = Sis.FlotaEspacial()
    almacen = Sis.Almacen('A1', 'Marte')
    flota.anyadir_almacen(almacen)

    flota.dar_de_alta('Tornillos de Oro', 'Joses', 100, 200, 'A1')

    assert almacen.contar_existencias() == 100  # Comprobamos que efectivamente se han añadido las distintas unidades al almacen



# Test asociado al correcto manejo de la función actualizar() dentro de flota

def test_stock_insuficiente():
    flota = Sis.FlotaEspacial()
    almacen = Sis.Almacen("A1", "Marte")
    flota.anyadir_almacen(almacen)

    flota.dar_de_alta("Tornillo", "Prov", 5, 5, "A1")

    with pytest.raises(Sis.ErrorStockInsuficiente):
        flota.actualizar("Tornillo", -10)



# Tests asociado a consultar repuestos en naves


# Test que comprueba que maneja que no consultemos a una nave que no existe
def test_consultar_repuesto_nave_no_existente():
    flota = Sis.FlotaEspacial()
    nave = Sis.NaveEstelar('CAE1', 32124, 'Halcón 17', 40, 21, Sis.EClase.SOBERANO)
    nave.anyadir_catalogo('Tornillos De Diamante', 'Joses', 300, 200)
    flota.anyadir_nave(nave)

    with pytest.raises(Sis.ErrorInexistenciaNave):
        flota.consultar_repuesto('Tornillos de Oro', 'CAE2') # No estará


# Test que maneja que no
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
    flota.anyadir_nave(nave)


    almacen = Sis.Almacen("A1", "Marte")
    flota.anyadir_almacen(almacen)

    flota.dar_de_alta("Tornillos", "Prov", 10, 200, "A1")

    with pytest.raises(Sis.ErrorStockInsuficiente):
        flota.adquirir_repuesto('Tornillos', 'CAE1', 100)

    with pytest.raises(Sis.ErrorRepuestoNoCatalogo):
        flota.adquirir_repuesto('Tornillo de Oro', 'CAE1', 2)
    
    with pytest.raises(Sis.ErrorInexistenciaNave):
        flota.adquirir_repuesto('Tornillos', 'CAE2', 5)

    

        

