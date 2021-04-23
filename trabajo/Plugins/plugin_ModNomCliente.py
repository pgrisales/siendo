#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cambia el formato de fecha dd/mm/aaaa por aaaa-mm-dd
ejemplo:
entrada = 20/04/2021
salida = 2021-20-04
"""

def plugin_main(*args, **kwargs):
    #print ('args  : ',kwargs)
    salida  = kwargs['entregadoa'][0]
    salida  = salida [salida.find('-')+1: ].strip()
    #print ('aqui',salida)
    return 'entregadoa', salida
