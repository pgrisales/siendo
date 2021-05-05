#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cambia el formato de fecha dd/mm/aaaa por aaaa-mm-dd
ejemplo:
entrada = 20/04/2021
salida = 2021-20-04
"""

def plugin_main(*args, **kwargs):
    # print ('args  : ',args)
    # print ('kwargs: ',kwargs)
    fecha = kwargs['fecha'][0]
    fecha = '{}-{}-{}'.format(fecha[-4:], fecha[3:5], fecha[:2])
    #print (fecha)
    return 'fecha',fecha
