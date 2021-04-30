#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'efrenfuentes'

import unittest
from plugin_MontoEscrito import numero_a_letras, numero_a_moneda

class TestNumeroLetras(unittest.TestCase):

    def test_numero_demasiado_alto(self):
        numero = 1000000000000
        self.assertRaises(OverflowError, numero_a_letras, numero)

    def test_unidades(self):
        numero = 8
        self.assertEqual(numero_a_letras(numero), 'ocho')
        numero = 2
        self.assertEqual(numero_a_letras(numero), 'dos')
        numero = 0
        self.assertEqual(numero_a_letras(numero), 'cero')

    def test_decena_diez(self):
        numero = 15
        self.assertEqual(numero_a_letras(numero), 'quince')
        numero = 17
        self.assertEqual(numero_a_letras(numero), 'diecisiete')
        numero = 19
        self.assertEqual(numero_a_letras(numero), 'diecinueve')

    def test_decena_veinte(self):
        numero = 23
        self.assertEqual(numero_a_letras(numero), 'veintitres')
        numero = 26
        self.assertEqual(numero_a_letras(numero), 'veintiseis')
        numero = 21
        self.assertEqual(numero_a_letras(numero), 'veintiuno')

    def test_menores_cien(self):
        numero = 32
        self.assertEqual(numero_a_letras(numero), 'treinta y dos')
        numero = 73
        self.assertEqual(numero_a_letras(numero), 'setenta y tres')
        numero = 89
        self.assertEqual(numero_a_letras(numero), 'ochenta y nueve')

    def test_centenas(self):
        numero = 167
        self.assertEqual(numero_a_letras(numero), 'ciento sesenta y siete')
        numero = 735
        self.assertEqual(numero_a_letras(numero), 'setecientos treinta y cinco')
        numero = 899
        self.assertEqual(numero_a_letras(numero), 'ochocientos noventa y nueve')

    def test_miles(self):
        numero = 1973
        self.assertEqual(numero_a_letras(numero), 'mil novecientos setenta y tres')
        numero = 5230
        self.assertEqual(numero_a_letras(numero), 'cinco mil doscientos treinta')
        numero = 41378
        self.assertEqual(numero_a_letras(numero), 'cuarenta y un mil trescientos setenta y ocho')
        numero = 197356
        self.assertEqual(numero_a_letras(numero), 'ciento noventa y siete mil trescientos cincuenta y seis')
        numero = 2004
        self.assertEqual(numero_a_letras(numero), 'dos mil cuatro')

    def test_millones(self):
        numero = 11852739
        self.assertEqual(numero_a_letras(numero), 'once millones ochocientos cincuenta y dos mil setecientos treinta y nueve')
        numero = 2000000
        self.assertEqual(numero_a_letras(numero), 'dos millones')

    def test_millardos(self):
        numero = 1212673201
        self.assertEqual(numero_a_letras(numero), 'mil doscientos doce millones seiscientos setenta y tres mil doscientos uno')
        numero = 56547567945
        self.assertEqual(numero_a_letras(numero), 'cincuenta y seis mil quinientos cuarenta y siete millones quinientos sesenta y siete mil novecientos cuarenta y cinco')

    def test_decimales(self):
        numero = 1.87
        self.assertEqual(numero_a_letras(numero), 'uno punto ochenta y siete')
        numero = 1.50
        self.assertEqual(numero_a_letras(numero), 'uno punto cincuenta')
        numero = 1.04
        self.assertEqual(numero_a_letras(numero), 'uno punto cero cuatro')
        numero = 1.00
        self.assertEqual(numero_a_letras(numero), 'uno')

    def test_negativos(self):
        numero = -4.5
        self.assertEqual(numero_a_letras(numero), 'menos cuatro punto cincuenta')

    def test_moneda(self):
        numero = 1212673201
        self.assertEqual(numero_a_moneda(numero), 'mil doscientos doce millones seiscientos setenta y tres mil doscientos un pesos con cero centavos')
        numero = 56547567945.5
        self.assertEqual(numero_a_moneda(numero), 'cincuenta y seis mil quinientos cuarenta y siete millones quinientos sesenta y siete mil novecientos cuarenta y cinco pesos con cincuenta centavos')
        numero = 1.01
        self.assertEqual(numero_a_moneda(numero), 'un peso con un centavo')


if __name__ == '__main__':
    unittest.main()
