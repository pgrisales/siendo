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
    #print ('kwargs: ',kwargs)
    salida  = kwargs['valor_total'][0]
    salida  = salida.replace('$','')
    salida  = salida.replace('.','')
    salida  = salida.replace(',','.')
    if salida.find('-')>-1:
        salida = salida.replace('-','')
        salida ='-'+salida

    salida  = float( salida.strip())
    return 'valor_total', salida
